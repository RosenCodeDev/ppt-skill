#!/usr/bin/env python3
"""Read-only structural validator for macro-free the firm PPTX files."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import sys
import zipfile
from collections import Counter, defaultdict, deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET


CONTENT_TYPES_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
PACKAGE_RELS_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
PRESENTATION_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
OFFICE_RELS_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

NS = {
    "a": DRAWING_NS,
    "ct": CONTENT_TYPES_NS,
    "p": PRESENTATION_NS,
    "pr": PACKAGE_RELS_NS,
    "r": OFFICE_RELS_NS,
}

STATUS_ORDER = {"passed": 0, "skipped": 1, "warning": 2, "failed": 3}
REQUIRED_PARTS = {
    "[Content_Types].xml",
    "_rels/.rels",
    "ppt/presentation.xml",
    "ppt/_rels/presentation.xml.rels",
}

MACRO_CONTENT_MARKERS = ("macroenabled", "vbaproject", "vbadata")
MACRO_PART_MARKERS = ("vbaproject", "vbadata", "activex")
PROHIBITED_EXTERNAL_KINDS = {
    "attachedtemplate",
    "audio",
    "control",
    "externallink",
    "externallinkpath",
    "image",
    "media",
    "oleobject",
    "package",
    "video",
}

PLACEHOLDER_PATTERNS = (
    re.compile(r"\bclick\s+to\s+(?:add|edit)\b", re.IGNORECASE),
    re.compile(r"\blorem\s+ipsum\b", re.IGNORECASE),
    re.compile(r"\binsert\s+(?:text|title|subtitle|content)\b", re.IGNORECASE),
    re.compile(r"\byour\s+(?:text|title|subtitle)\s+here\b", re.IGNORECASE),
    re.compile(r"\bpresentation\s+title\b", re.IGNORECASE),
)


@dataclass(frozen=True)
class Finding:
    check_id: str
    status: str
    summary: str
    details: list[str]


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def relationship_kind(type_uri: str) -> str:
    return type_uri.rstrip("/").rsplit("/", 1)[-1].lower()


def source_part_for_rels(rels_part: str) -> str | None:
    if rels_part == "_rels/.rels":
        return ""
    directory, filename = posixpath.split(rels_part)
    if posixpath.basename(directory) != "_rels" or not filename.endswith(".rels"):
        return None
    source_directory = posixpath.dirname(directory)
    source_filename = filename[: -len(".rels")]
    return posixpath.join(source_directory, source_filename)


def resolve_target(source_part: str, target: str) -> str | None:
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path).replace("\\", "/")
    if path.startswith("/"):
        resolved = posixpath.normpath(path.lstrip("/"))
    else:
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source_part), path))
    if resolved in {"", ".", ".."} or resolved.startswith("../"):
        return None
    return resolved


class PptxValidator:
    def __init__(self, pptx_path: Path, manifest_path: Path | None = None) -> None:
        self.pptx_path = pptx_path
        self.manifest_path = manifest_path
        self.findings: list[Finding] = []
        self.names: set[str] = set()
        self.xml: dict[str, ET.Element] = {}
        self.relationships: dict[str, list[dict[str, str | None]]] = defaultdict(list)
        self.slide_order: list[str] = []
        self.defaults: dict[str, str] = {}
        self.overrides: dict[str, str] = {}

    def add(
        self,
        check_id: str,
        status: str,
        summary: str,
        details: Iterable[str] = (),
    ) -> None:
        if status not in STATUS_ORDER:
            raise ValueError(f"Unsupported status: {status}")
        self.findings.append(Finding(check_id, status, summary, list(details)))

    def root(self, part: str) -> ET.Element | None:
        return self.xml.get(part)

    def validate(self) -> dict[str, Any]:
        self._check_extension()
        try:
            with zipfile.ZipFile(self.pptx_path, "r") as archive:
                if not self._load_package(archive):
                    return self.result()
        except (zipfile.BadZipFile, OSError) as exc:
            self.add("package_integrity", "failed", "The file is not a readable PPTX ZIP package.", [str(exc)])
            self._add_unavailable_checks()
            return self.result()

        required_ok = self._check_required_parts()
        self._check_xml_well_formed()
        if not required_ok or any(
            finding.status == "failed" and finding.check_id == "xml_well_formed"
            for finding in self.findings
        ):
            self._add_unavailable_checks()
            return self.result()

        self._parse_content_types()
        self._parse_relationships()
        self._check_macros_and_controls()
        self._check_content_type_coverage()
        self._check_relationship_integrity_and_external_links()
        self._check_slide_synchronization()
        self._check_slide_layouts()
        self._check_notes_ownership()
        self._check_orphans()
        self._check_slide_content_and_placeholders()
        self._check_template_compatibility()
        self._check_native_inspection_objects()
        self._add_unavailable_checks()
        return self.result()

    def result(self) -> dict[str, Any]:
        counts = Counter(finding.status for finding in self.findings)
        if counts["failed"]:
            overall = "failed"
        elif counts["warning"]:
            overall = "warning"
        else:
            overall = "passed"
        return {
            "validator": "powerpoint-pptx-structural-validator",
            "format_version": 1,
            "input": str(self.pptx_path.resolve()),
            "input_sha256": self._sha256(),
            "overall_status": overall,
            "summary": {status: counts[status] for status in STATUS_ORDER},
            "checks": [asdict(finding) for finding in self.findings],
        }

    def _sha256(self) -> str:
        digest = hashlib.sha256()
        with self.pptx_path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _check_extension(self) -> None:
        if self.pptx_path.suffix.lower() == ".pptx":
            self.add("file_extension", "passed", "The file uses the macro-free .pptx extension.")
        else:
            self.add(
                "file_extension",
                "failed",
                "The final deliverable must use the .pptx extension.",
                [f"Found: {self.pptx_path.suffix or '(no extension)'}"],
            )

    def _load_package(self, archive: zipfile.ZipFile) -> bool:
        entries = [entry for entry in archive.infolist() if not entry.is_dir()]
        duplicate_names = sorted(name for name, count in Counter(entry.filename for entry in entries).items() if count > 1)
        if duplicate_names:
            self.add("zip_entries", "failed", "Duplicate ZIP part names make the package ambiguous.", duplicate_names)
        else:
            self.add("zip_entries", "passed", f"The package contains {len(entries)} uniquely named parts.")

        bad_part = archive.testzip()
        if bad_part:
            self.add("zip_crc", "failed", "A ZIP member failed its CRC check.", [bad_part])
            return False
        self.add("zip_crc", "passed", "All ZIP members passed CRC validation.")

        self.names = {entry.filename for entry in entries}
        for entry in entries:
            if entry.filename.endswith((".xml", ".rels")) or entry.filename == "[Content_Types].xml":
                try:
                    self.xml[entry.filename] = ET.fromstring(archive.read(entry))
                except ET.ParseError:
                    # Report all malformed XML together in _check_xml_well_formed.
                    continue
        return True

    def _check_required_parts(self) -> bool:
        missing = sorted(REQUIRED_PARTS - self.names)
        if missing:
            self.add("required_parts", "failed", "Required PPTX package parts are missing.", missing)
            return False
        self.add("required_parts", "passed", "All required PPTX package parts are present.")
        return True

    def _check_xml_well_formed(self) -> None:
        xml_parts = sorted(
            name
            for name in self.names
            if name.endswith((".xml", ".rels")) or name == "[Content_Types].xml"
        )
        malformed = [name for name in xml_parts if name not in self.xml]
        if malformed:
            self.add("xml_well_formed", "failed", "One or more XML parts are malformed.", malformed)
        else:
            self.add("xml_well_formed", "passed", f"All {len(xml_parts)} XML parts are well formed.")

    def _parse_content_types(self) -> None:
        root = self.root("[Content_Types].xml")
        if root is None:
            return
        duplicate_defaults: list[str] = []
        duplicate_overrides: list[str] = []
        for element in root:
            kind = local_name(element.tag)
            if kind == "Default":
                extension = element.get("Extension", "").lower()
                content_type = element.get("ContentType", "")
                if extension in self.defaults:
                    duplicate_defaults.append(extension)
                self.defaults[extension] = content_type
            elif kind == "Override":
                part = element.get("PartName", "").lstrip("/")
                content_type = element.get("ContentType", "")
                if part in self.overrides:
                    duplicate_overrides.append(part)
                self.overrides[part] = content_type
        duplicates = [f"default extension: {item}" for item in duplicate_defaults]
        duplicates.extend(f"override part: {item}" for item in duplicate_overrides)
        if duplicates:
            self.add("content_type_uniqueness", "failed", "Duplicate content-type declarations were found.", duplicates)
        else:
            self.add("content_type_uniqueness", "passed", "Content-type declarations are unique.")

    def _parse_relationships(self) -> None:
        duplicate_ids: list[str] = []
        missing_sources: list[str] = []
        for rels_part in sorted(name for name in self.names if name.endswith(".rels")):
            source = source_part_for_rels(rels_part)
            if source is None:
                continue
            if source and source not in self.names:
                missing_sources.append(f"{rels_part} -> missing owner {source}")
            root = self.root(rels_part)
            if root is None:
                continue
            seen_ids: set[str] = set()
            for relationship in root:
                rel_id = relationship.get("Id", "")
                if rel_id in seen_ids:
                    duplicate_ids.append(f"{rels_part}: {rel_id}")
                seen_ids.add(rel_id)
                target = relationship.get("Target", "")
                mode = relationship.get("TargetMode")
                is_external = (mode or "").lower() == "external"
                resolved = None if is_external else resolve_target(source, target)
                self.relationships[source].append(
                    {
                        "id": rel_id,
                        "type": relationship.get("Type", ""),
                        "target": target,
                        "target_mode": mode,
                        "resolved": resolved,
                        "rels_part": rels_part,
                    }
                )
        issues = duplicate_ids + missing_sources
        if issues:
            self.add("relationship_declarations", "failed", "Relationship declarations are inconsistent.", issues)
        else:
            self.add("relationship_declarations", "passed", "Relationship identifiers and owner parts are consistent.")

    def _check_macros_and_controls(self) -> None:
        suspicious_parts = sorted(
            name for name in self.names if any(marker in name.lower() for marker in MACRO_PART_MARKERS)
        )
        suspicious_types = sorted(
            {content_type for content_type in [*self.defaults.values(), *self.overrides.values()] if any(
                marker in content_type.lower() for marker in MACRO_CONTENT_MARKERS
            )}
        )
        suspicious_relationships = sorted(
            f"{source or '(package root)'}: {relationship['type']}"
            for source, relationships in self.relationships.items()
            for relationship in relationships
            if any(marker in str(relationship["type"]).lower() for marker in MACRO_PART_MARKERS)
        )
        details = suspicious_parts + suspicious_types + suspicious_relationships
        if details:
            self.add("macro_free", "failed", "Macro, VBA, or executable control content was detected.", details)
        else:
            self.add("macro_free", "passed", "No macro, VBA, or ActiveX control content was detected.")

    def _content_type_for(self, part: str) -> str | None:
        if part in self.overrides:
            return self.overrides[part]
        extension = "rels" if part.endswith(".rels") else posixpath.splitext(part)[1].lstrip(".").lower()
        return self.defaults.get(extension)

    def _check_content_type_coverage(self) -> None:
        missing_mappings = sorted(
            part
            for part in self.names
            if part != "[Content_Types].xml" and self._content_type_for(part) is None
        )
        missing_parts = sorted(part for part in self.overrides if part not in self.names)
        presentation_type = self._content_type_for("ppt/presentation.xml") or ""
        invalid_mappings: list[str] = []
        if presentation_type != "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml":
            invalid_mappings.append(f"ppt/presentation.xml: {presentation_type or '(missing)'}")
        expected_part_types = (
            (r"ppt/slides/slide\d+\.xml", "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"),
            (r"ppt/slideLayouts/slideLayout\d+\.xml", "application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"),
            (r"ppt/slideMasters/slideMaster\d+\.xml", "application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"),
            (r"ppt/notesSlides/notesSlide\d+\.xml", "application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"),
            (r"ppt/charts/chart\d+\.xml", "application/vnd.openxmlformats-officedocument.drawingml.chart+xml"),
            (r"ppt/theme/theme\d+\.xml", "application/vnd.openxmlformats-officedocument.theme+xml"),
        )
        for part in sorted(self.names):
            for pattern, expected_type in expected_part_types:
                if re.fullmatch(pattern, part):
                    actual_type = self._content_type_for(part) or ""
                    if actual_type != expected_type:
                        invalid_mappings.append(f"{part}: {actual_type or '(missing)'}; expected {expected_type}")
                    break
        details = [f"No content type: {part}" for part in missing_mappings]
        details.extend(f"Override points to missing part: {part}" for part in missing_parts)
        details.extend(f"Unexpected content type: {item}" for item in invalid_mappings)
        if details:
            self.add("content_type_coverage", "failed", "Content-type mappings are not synchronized with package parts.", details)
        else:
            self.add("content_type_coverage", "passed", "Every package part has a valid synchronized content type.")

    def _check_relationship_integrity_and_external_links(self) -> None:
        unresolved: list[str] = []
        hyperlinks: list[str] = []
        prohibited_external: list[str] = []
        other_external: list[str] = []
        for source, relationships in self.relationships.items():
            owner = source or "(package root)"
            for relationship in relationships:
                kind = relationship_kind(str(relationship["type"]))
                mode = str(relationship["target_mode"] or "").lower()
                target = str(relationship["target"])
                if mode == "external":
                    item = f"{owner} -> {target} ({kind})"
                    if kind == "hyperlink":
                        hyperlinks.append(item)
                    elif kind in PROHIBITED_EXTERNAL_KINDS or source.startswith(("ppt/charts/", "ppt/externalLinks/")):
                        prohibited_external.append(item)
                    else:
                        other_external.append(item)
                    continue
                resolved = relationship["resolved"]
                if resolved is None or resolved not in self.names:
                    unresolved.append(f"{owner} -> {target} ({kind})")

        if unresolved:
            self.add("internal_relationship_targets", "failed", "Internal relationship targets do not resolve.", sorted(unresolved))
        else:
            self.add("internal_relationship_targets", "passed", "All internal relationship targets resolve.")

        if prohibited_external:
            self.add("prohibited_external_data", "failed", "Prohibited linked media, workbook, OLE, or external data was detected.", sorted(prohibited_external))
        else:
            self.add("prohibited_external_data", "passed", "No prohibited linked media, workbook, OLE, or external data was detected.")

        if hyperlinks:
            self.add("ordinary_hyperlinks", "warning", "Ordinary external hyperlinks require content review.", sorted(hyperlinks))
        else:
            self.add("ordinary_hyperlinks", "passed", "No ordinary external hyperlinks were detected.")

        if other_external:
            self.add("unclassified_external_relationships", "warning", "Unclassified external relationships require native inspection.", sorted(other_external))
        else:
            self.add("unclassified_external_relationships", "passed", "No unclassified external relationships were detected.")

    def _relationships_of_kind(self, source: str, kind: str) -> list[dict[str, str | None]]:
        return [
            relationship
            for relationship in self.relationships.get(source, [])
            if relationship_kind(str(relationship["type"])) == kind.lower()
        ]

    def _check_slide_synchronization(self) -> None:
        presentation = self.root("ppt/presentation.xml")
        if presentation is None:
            self.add("slide_synchronization", "skipped", "Slide synchronization could not be checked because presentation.xml is unavailable.")
            return
        presentation_relationships = {str(item["id"]): item for item in self.relationships.get("ppt/presentation.xml", [])}
        declared = presentation.findall(".//p:sldIdLst/p:sldId", NS)
        ids: list[str] = []
        relationship_ids: list[str] = []
        targets: list[str] = []
        issues: list[str] = []
        for element in declared:
            slide_id = element.get("id", "")
            rel_id = element.get(f"{{{OFFICE_RELS_NS}}}id", "")
            ids.append(slide_id)
            relationship_ids.append(rel_id)
            try:
                if int(slide_id) < 256:
                    issues.append(f"Slide id must be at least 256: {slide_id}")
            except ValueError:
                issues.append(f"Slide id is not numeric: {slide_id or '(missing)'}")
            relationship = presentation_relationships.get(rel_id)
            if relationship is None or relationship_kind(str(relationship["type"])) != "slide":
                issues.append(f"Slide id {slide_id or '(missing)'} references invalid relationship {rel_id or '(missing)'}")
                continue
            target = relationship["resolved"]
            if not isinstance(target, str) or not target.startswith("ppt/slides/") or target not in self.names:
                issues.append(f"Slide relationship {rel_id} has invalid target {relationship['target']}")
                continue
            targets.append(target)

        for value, count in Counter(ids).items():
            if count > 1:
                issues.append(f"Duplicate slide id: {value}")
        for value, count in Counter(relationship_ids).items():
            if count > 1:
                issues.append(f"Duplicate slide relationship reference: {value}")
        for value, count in Counter(targets).items():
            if count > 1:
                issues.append(f"Duplicate slide target in slide order: {value}")

        slide_relationship_targets = {
            str(item["resolved"])
            for item in self._relationships_of_kind("ppt/presentation.xml", "slide")
            if item["resolved"] is not None
        }
        if slide_relationship_targets != set(targets):
            extras = sorted(slide_relationship_targets - set(targets))
            missing = sorted(set(targets) - slide_relationship_targets)
            issues.extend(f"Presentation has unlisted slide relationship: {item}" for item in extras)
            issues.extend(f"Slide order target lacks presentation relationship: {item}" for item in missing)

        self.slide_order = targets
        if issues:
            self.add("slide_synchronization", "failed", "Slide identifiers, order, and relationships are not synchronized.", issues)
        else:
            self.add("slide_synchronization", "passed", f"Slide identifiers and relationships are synchronized for {len(targets)} slides.")

    def _check_slide_layouts(self) -> None:
        issues: list[str] = []
        for slide in self.slide_order:
            layouts = self._relationships_of_kind(slide, "slidelayout")
            if len(layouts) != 1:
                issues.append(f"{slide}: expected exactly one slideLayout relationship, found {len(layouts)}")
                continue
            target = layouts[0]["resolved"]
            if not isinstance(target, str) or target not in self.names:
                issues.append(f"{slide}: layout target does not resolve")
        if issues:
            self.add("slide_layout_ownership", "failed", "One or more slides have invalid layout ownership.", issues)
        else:
            self.add("slide_layout_ownership", "passed", "Every ordered slide has exactly one valid layout relationship.")

    def _check_notes_ownership(self) -> None:
        owners: dict[str, list[str]] = defaultdict(list)
        issues: list[str] = []
        for slide in self.slide_order:
            notes_relationships = self._relationships_of_kind(slide, "notesslide")
            if len(notes_relationships) > 1:
                issues.append(f"{slide}: multiple notesSlide relationships")
            for relationship in notes_relationships:
                target = relationship["resolved"]
                if isinstance(target, str):
                    owners[target].append(slide)

        for notes_part, slides in sorted(owners.items()):
            if len(slides) != 1:
                issues.append(f"{notes_part}: shared by {', '.join(slides)}")
                continue
            back_links = self._relationships_of_kind(notes_part, "slide")
            back_targets = [item["resolved"] for item in back_links]
            if len(back_links) != 1 or back_targets[0] != slides[0]:
                issues.append(f"{notes_part}: does not uniquely reference owning slide {slides[0]}")

        if issues:
            self.add("notes_ownership", "failed", "Notes-slide ownership is not unique and reciprocal.", issues)
        else:
            self.add("notes_ownership", "passed", f"Notes ownership is valid for {len(owners)} notes slides.")

    def _reachable_parts(self) -> set[str]:
        reachable: set[str] = set()
        queue: deque[str] = deque([""])
        visited_sources: set[str] = set()
        while queue:
            source = queue.popleft()
            if source in visited_sources:
                continue
            visited_sources.add(source)
            for relationship in self.relationships.get(source, []):
                target = relationship["resolved"]
                if isinstance(target, str) and target in self.names and target not in reachable:
                    reachable.add(target)
                    queue.append(target)
        return reachable

    def _check_orphans(self) -> None:
        reachable = self._reachable_parts()
        prefixes = (
            "ppt/slides/",
            "ppt/notesSlides/",
            "ppt/media/",
            "ppt/charts/",
            "ppt/embeddings/",
        )
        candidates = sorted(
            name
            for name in self.names
            if name.startswith(prefixes) and "/_rels/" not in name and name not in reachable
        )
        if candidates:
            self.add(
                "orphan_candidates",
                "warning",
                "Potential orphaned parts were found; report them but do not delete them automatically.",
                candidates,
            )
        else:
            self.add("orphan_candidates", "passed", "No orphaned slide, notes, media, chart, or embedding candidates were detected.")

    def _check_slide_content_and_placeholders(self) -> None:
        remnants: list[str] = []
        empty_candidates: list[str] = []
        visual_names = {"pic", "graphicFrame", "cxnSp", "grpSp", "oleObj", "contentPart"}
        for slide in self.slide_order:
            root = self.root(slide)
            if root is None:
                continue
            texts = [element.text.strip() for element in root.findall(".//a:t", NS) if element.text and element.text.strip()]
            for text in texts:
                if any(pattern.search(text) for pattern in PLACEHOLDER_PATTERNS):
                    remnants.append(f"{slide}: {text[:120]}")
            has_visual = any(local_name(element.tag) in visual_names for element in root.iter())
            has_non_placeholder_shape = any(
                local_name(element.tag) == "sp" and element.find(".//p:ph", NS) is None
                for element in root.iter()
            )
            if not texts and not has_visual and not has_non_placeholder_shape:
                empty_candidates.append(slide)

        if remnants:
            self.add("placeholder_remnants", "warning", "Possible placeholder or template prompt text remains on slides.", remnants)
        else:
            self.add("placeholder_remnants", "passed", "No common placeholder prompt text was detected on ordered slides.")
        if empty_candidates:
            self.add(
                "detectable_slide_content",
                "warning",
                "Some slides have no detectable slide-level content; inspect inherited fixed-layout content visually.",
                empty_candidates,
            )
        else:
            self.add("detectable_slide_content", "passed", "Every ordered slide contains detectable slide-level content.")

    def _load_manifest(self) -> dict[str, Any] | None:
        if self.manifest_path is None or not self.manifest_path.is_file():
            return None
        try:
            value = json.loads(self.manifest_path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            return None
        return value if isinstance(value, dict) else None

    def _check_template_compatibility(self) -> None:
        manifest = self._load_manifest()
        if manifest is None:
            self.add("template_manifest_compatibility", "skipped", "The bundled template manifest was unavailable or unreadable.")
            return
        warnings: list[str] = []
        expected = manifest.get("template", {})
        presentation = self.root("ppt/presentation.xml")
        if presentation is not None:
            size = presentation.find("p:sldSz", NS)
            actual_size = (size.get("cx"), size.get("cy")) if size is not None else (None, None)
            expected_size = (str(expected.get("slide_width_emu")), str(expected.get("slide_height_emu")))
            if actual_size != expected_size:
                warnings.append(f"Slide size {actual_size} differs from expected {expected_size}")

        master_parts = sorted(
            name for name in self.names if re.fullmatch(r"ppt/slideMasters/slideMaster\d+\.xml", name)
        )
        layout_parts = sorted(
            name for name in self.names if re.fullmatch(r"ppt/slideLayouts/slideLayout\d+\.xml", name)
        )
        if len(master_parts) != expected.get("expected_master_count"):
            warnings.append(f"Master count {len(master_parts)} differs from expected {expected.get('expected_master_count')}")
        if len(layout_parts) != expected.get("expected_layout_count"):
            warnings.append(f"Layout count {len(layout_parts)} differs from expected {expected.get('expected_layout_count')}")

        expected_names = {item.get("template_name") for item in manifest.get("layouts", []) if item.get("template_name")}
        actual_names: set[str] = set()
        for part in layout_parts:
            root = self.root(part)
            if root is None:
                continue
            common_slide_data = root.find("p:cSld", NS)
            if common_slide_data is not None and common_slide_data.get("name"):
                actual_names.add(str(common_slide_data.get("name")))
        missing_names = sorted(expected_names - actual_names)
        extra_names = sorted(actual_names - expected_names)
        warnings.extend(f"Missing expected layout: {name}" for name in missing_names)
        warnings.extend(f"Unexpected layout: {name}" for name in extra_names)

        theme = self.root("ppt/theme/theme1.xml")
        expected_theme = manifest.get("theme", {})
        if theme is None:
            warnings.append("Primary theme part ppt/theme/theme1.xml is unavailable")
        else:
            major = theme.find(".//a:fontScheme/a:majorFont/a:latin", NS)
            minor = theme.find(".//a:fontScheme/a:minorFont/a:latin", NS)
            actual_fonts = (
                major.get("typeface") if major is not None else None,
                minor.get("typeface") if minor is not None else None,
            )
            expected_fonts = (expected_theme.get("heading_font"), expected_theme.get("body_font"))
            if actual_fonts != expected_fonts:
                warnings.append(f"Theme fonts {actual_fonts} differ from expected {expected_fonts}")

            color_map = {
                "dark_1": "dk1",
                "light_1": "lt1",
                "dark_2": "dk2",
                "light_2": "lt2",
                "accent_1": "accent1",
                "accent_2": "accent2",
                "accent_3": "accent3",
                "accent_4": "accent4",
                "accent_5": "accent5",
                "accent_6": "accent6",
                "hyperlink": "hlink",
                "followed_hyperlink": "folHlink",
            }
            expected_colors = expected_theme.get("colors", {})
            for manifest_key, theme_key in color_map.items():
                color_parent = theme.find(f".//a:clrScheme/a:{theme_key}", NS)
                color_value = None
                if color_parent is not None and len(color_parent):
                    color_value = color_parent[0].get("val") or color_parent[0].get("lastClr")
                expected_value = str(expected_colors.get(manifest_key, "")).lstrip("#").upper()
                if expected_value and (color_value or "").upper() != expected_value:
                    warnings.append(f"Theme color {manifest_key} is {color_value or '(missing)'}; expected {expected_value}")

        if warnings:
            self.add("template_manifest_compatibility", "warning", "The deck differs from one or more PowerPoint template-manifest expectations.", warnings)
        else:
            self.add("template_manifest_compatibility", "passed", "Slide size, masters, layouts, theme fonts, and theme colors match the manifest.")

    def _check_native_inspection_objects(self) -> None:
        candidates = sorted(
            name
            for name in self.names
            if name.startswith((
                "ppt/embeddings/",
                "ppt/diagrams/",
                "ppt/ink/",
                "ppt/model3d/",
                "ppt/3d/",
            ))
            or posixpath.splitext(name)[1].lower() in {".mp3", ".mp4", ".wav", ".avi", ".mov"}
        )
        if candidates:
            self.add(
                "native_inspection_objects",
                "warning",
                "Embedded or complex objects require PowerPoint-native inspection and were not modified.",
                candidates,
            )
        else:
            self.add("native_inspection_objects", "passed", "No embedded or complex objects requiring native inspection were detected.")

    def _add_unavailable_checks(self) -> None:
        existing = {finding.check_id for finding in self.findings}
        checks = (
            ("rendered_visual_qa", "Rendered overflow, overlap, contrast, fit, and visual hierarchy require rendering or visual inspection."),
            ("communication_qa", "Storyline, governing thought, executive communication, and exhibit quality require judgment-based review."),
            ("evidence_accessibility_report_parity", "Evidence accuracy, accessibility completeness, and companion-report parity require DeckSpec and content review."),
        )
        for check_id, summary in checks:
            if check_id not in existing:
                self.add(check_id, "skipped", summary)


def validate_pptx(pptx_path: Path, manifest_path: Path | None = None) -> dict[str, Any]:
    return PptxValidator(pptx_path, manifest_path).validate()


def render_text(result: dict[str, Any]) -> str:
    labels = {"passed": "PASS", "warning": "WARN", "failed": "FAIL", "skipped": "SKIP"}
    lines = [
        f"PPTX validation: {result['input']}",
        f"Overall status: {str(result['overall_status']).upper()}",
    ]
    for check in result["checks"]:
        lines.append(f"[{labels[check['status']]}] {check['check_id']}: {check['summary']}")
        lines.extend(f"  - {detail}" for detail in check["details"])
    summary = result["summary"]
    lines.append(
        "Summary: "
        + ", ".join(f"{status}={summary[status]}" for status in ("passed", "warning", "failed", "skipped"))
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path, help="PPTX file to inspect without modifying it")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Output format (default: text)")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.pptx.is_file():
        parser.error(f"File does not exist or is not a regular file: {args.pptx}")
    manifest = Path(__file__).resolve().parent.parent / "references" / "template_manifest.json"
    try:
        result = validate_pptx(args.pptx, manifest)
    except Exception as exc:  # pragma: no cover - last-resort CLI containment
        error_result = {
            "validator": "powerpoint-pptx-structural-validator",
            "format_version": 1,
            "input": str(args.pptx.resolve()),
            "input_sha256": None,
            "overall_status": "failed",
            "summary": {"passed": 0, "skipped": 0, "warning": 0, "failed": 1},
            "checks": [{
                "check_id": "validator_internal_error",
                "status": "failed",
                "summary": "The validator encountered an internal error.",
                "details": [f"{type(exc).__name__}: {exc}"],
            }],
        }
        print(json.dumps(error_result, indent=2) if args.format == "json" else render_text(error_result))
        return 2
    print(json.dumps(result, indent=2) if args.format == "json" else render_text(result))
    return 1 if result["overall_status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
