from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "distributions" / "ai-platform" / "powerpoint-skill" / "scripts" / "validate_pptx.py"
SPEC = importlib.util.spec_from_file_location("validate_pptx", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)

P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PR_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"


def base_parts() -> dict[str, bytes]:
    content_types = f"""<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="{CT_NS}">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
</Types>"""
    package_rels = f"""<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="{PR_NS}">
  <Relationship Id="rId1" Type="{R_NS}/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>"""
    presentation = f"""<?xml version="1.0" encoding="UTF-8"?>
<p:presentation xmlns:p="{P_NS}" xmlns:r="{R_NS}">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst><p:sldId id="256" r:id="rId2"/></p:sldIdLst>
  <p:sldSz cx="12192000" cy="6858000"/>
</p:presentation>"""
    presentation_rels = f"""<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="{PR_NS}">
  <Relationship Id="rId1" Type="{R_NS}/slideMaster" Target="slideMasters/slideMaster1.xml"/>
  <Relationship Id="rId2" Type="{R_NS}/slide" Target="slides/slide1.xml"/>
</Relationships>"""
    slide = f"""<?xml version="1.0" encoding="UTF-8"?>
<p:sld xmlns:p="{P_NS}" xmlns:a="{A_NS}" xmlns:r="{R_NS}">
  <p:cSld><p:spTree><p:sp><p:nvSpPr><p:cNvPr id="2" name="Title"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:txBody><a:p><a:r><a:t>Decision title</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld>
</p:sld>"""
    slide_rels = f"""<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="{PR_NS}">
  <Relationship Id="rId1" Type="{R_NS}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>"""
    layout = f"""<?xml version="1.0" encoding="UTF-8"?>
<p:sldLayout xmlns:p="{P_NS}" xmlns:a="{A_NS}" xmlns:r="{R_NS}"><p:cSld name="Title and Content"><p:spTree/></p:cSld></p:sldLayout>"""
    layout_rels = f"""<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="{PR_NS}"><Relationship Id="rId1" Type="{R_NS}/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>"""
    master = f"""<?xml version="1.0" encoding="UTF-8"?>
<p:sldMaster xmlns:p="{P_NS}" xmlns:a="{A_NS}" xmlns:r="{R_NS}"><p:cSld><p:spTree/></p:cSld></p:sldMaster>"""
    master_rels = f"""<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="{PR_NS}">
  <Relationship Id="rId1" Type="{R_NS}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="{R_NS}/theme" Target="../theme/theme1.xml"/>
</Relationships>"""
    theme = f"""<?xml version="1.0" encoding="UTF-8"?>
<a:theme xmlns:a="{A_NS}" name="Test"><a:themeElements><a:clrScheme name="Test"><a:dk1><a:srgbClr val="000F47"/></a:dk1></a:clrScheme><a:fontScheme name="Test"><a:majorFont><a:latin typeface="Marsh Serif"/></a:majorFont><a:minorFont><a:latin typeface="Noto Sans"/></a:minorFont></a:fontScheme></a:themeElements></a:theme>"""
    return {
        "[Content_Types].xml": content_types.encode(),
        "_rels/.rels": package_rels.encode(),
        "ppt/presentation.xml": presentation.encode(),
        "ppt/_rels/presentation.xml.rels": presentation_rels.encode(),
        "ppt/slides/slide1.xml": slide.encode(),
        "ppt/slides/_rels/slide1.xml.rels": slide_rels.encode(),
        "ppt/slideLayouts/slideLayout1.xml": layout.encode(),
        "ppt/slideLayouts/_rels/slideLayout1.xml.rels": layout_rels.encode(),
        "ppt/slideMasters/slideMaster1.xml": master.encode(),
        "ppt/slideMasters/_rels/slideMaster1.xml.rels": master_rels.encode(),
        "ppt/theme/theme1.xml": theme.encode(),
    }


def write_package(path: Path, parts: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in parts.items():
            archive.writestr(name, data)


def insert_before(data: bytes, marker: bytes, addition: bytes) -> bytes:
    return data.replace(marker, addition + marker)


def finding(result: dict, check_id: str) -> dict:
    return next(check for check in result["checks"] if check["check_id"] == check_id)


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def make(self, name: str = "deck.pptx", parts: dict[str, bytes] | None = None) -> Path:
        path = self.root / name
        write_package(path, parts or base_parts())
        return path

    def validate(self, path: Path) -> dict:
        return VALIDATOR.validate_pptx(path, None)

    def test_valid_fixture_is_read_only(self) -> None:
        path = self.make()
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        result = self.validate(path)
        after = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(before, after)
        self.assertEqual(result["summary"]["failed"], 0)
        self.assertEqual(finding(result, "rendered_visual_qa")["status"], "skipped")

    def test_broken_relationship_is_blocking(self) -> None:
        parts = base_parts()
        parts["ppt/slides/_rels/slide1.xml.rels"] = parts["ppt/slides/_rels/slide1.xml.rels"].replace(b"slideLayout1.xml", b"missing.xml")
        result = self.validate(self.make(parts=parts))
        self.assertEqual(finding(result, "internal_relationship_targets")["status"], "failed")

    def test_duplicate_slide_id_is_blocking(self) -> None:
        parts = base_parts()
        duplicate = f'<p:sldId id="256" r:id="rId2"/>'.encode()
        parts["ppt/presentation.xml"] = insert_before(parts["ppt/presentation.xml"], b"</p:sldIdLst>", duplicate)
        result = self.validate(self.make(parts=parts))
        self.assertEqual(finding(result, "slide_synchronization")["status"], "failed")

    def test_missing_slide_content_type_is_blocking(self) -> None:
        parts = base_parts()
        parts["[Content_Types].xml"] = parts["[Content_Types].xml"].replace(
            b'  <Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>\n',
            b"",
        )
        result = self.validate(self.make(parts=parts))
        self.assertEqual(finding(result, "content_type_coverage")["status"], "failed")

    def test_shared_notes_are_blocking(self) -> None:
        parts = base_parts()
        parts["[Content_Types].xml"] = insert_before(
            parts["[Content_Types].xml"],
            b"</Types>",
            b'  <Override PartName="/ppt/slides/slide2.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>\n'
            b'  <Override PartName="/ppt/notesSlides/notesSlide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>\n',
        )
        parts["ppt/presentation.xml"] = insert_before(
            parts["ppt/presentation.xml"], b"</p:sldIdLst>", b'<p:sldId id="257" r:id="rId3"/>'
        )
        parts["ppt/_rels/presentation.xml.rels"] = insert_before(
            parts["ppt/_rels/presentation.xml.rels"],
            b"</Relationships>",
            f'  <Relationship Id="rId3" Type="{R_NS}/slide" Target="slides/slide2.xml"/>\n'.encode(),
        )
        parts["ppt/slides/slide2.xml"] = parts["ppt/slides/slide1.xml"]
        notes_rel = f'  <Relationship Id="rId2" Type="{R_NS}/notesSlide" Target="../notesSlides/notesSlide1.xml"/>\n'.encode()
        parts["ppt/slides/_rels/slide1.xml.rels"] = insert_before(parts["ppt/slides/_rels/slide1.xml.rels"], b"</Relationships>", notes_rel)
        parts["ppt/slides/_rels/slide2.xml.rels"] = parts["ppt/slides/_rels/slide1.xml.rels"]
        parts["ppt/notesSlides/notesSlide1.xml"] = f'<p:notes xmlns:p="{P_NS}" xmlns:r="{R_NS}"><p:cSld><p:spTree/></p:cSld></p:notes>'.encode()
        parts["ppt/notesSlides/_rels/notesSlide1.xml.rels"] = f'<Relationships xmlns="{PR_NS}"><Relationship Id="rId1" Type="{R_NS}/slide" Target="../slides/slide1.xml"/></Relationships>'.encode()
        result = self.validate(self.make(parts=parts))
        self.assertEqual(finding(result, "notes_ownership")["status"], "failed")

    def test_macro_content_is_blocking(self) -> None:
        parts = base_parts()
        parts["[Content_Types].xml"] = insert_before(
            parts["[Content_Types].xml"],
            b"</Types>",
            b'  <Override PartName="/ppt/vbaProject.bin" ContentType="application/vnd.ms-office.vbaProject"/>\n',
        )
        parts["ppt/vbaProject.bin"] = b"not executable test data"
        result = self.validate(self.make(parts=parts))
        self.assertEqual(finding(result, "macro_free")["status"], "failed")

    def test_external_workbook_is_blocking(self) -> None:
        parts = base_parts()
        relationship = f'  <Relationship Id="rId9" Type="{R_NS}/package" Target="file:///C:/linked.xlsx" TargetMode="External"/>\n'.encode()
        parts["ppt/slides/_rels/slide1.xml.rels"] = insert_before(parts["ppt/slides/_rels/slide1.xml.rels"], b"</Relationships>", relationship)
        result = self.validate(self.make(parts=parts))
        self.assertEqual(finding(result, "prohibited_external_data")["status"], "failed")

    def test_orphan_is_warning_and_not_deleted(self) -> None:
        parts = base_parts()
        parts["[Content_Types].xml"] = insert_before(
            parts["[Content_Types].xml"], b"</Types>", b'  <Default Extension="png" ContentType="image/png"/>\n'
        )
        parts["ppt/media/orphan.png"] = b"test image bytes"
        path = self.make(parts=parts)
        result = self.validate(path)
        self.assertEqual(finding(result, "orphan_candidates")["status"], "warning")
        with zipfile.ZipFile(path) as archive:
            self.assertIn("ppt/media/orphan.png", archive.namelist())

    def test_cli_json_and_exit_codes(self) -> None:
        valid = self.make("valid.pptx")
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(valid), "--format", "json"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn(json.loads(completed.stdout)["overall_status"], {"passed", "warning"})

        invalid = self.root / "invalid.pptx"
        invalid.write_bytes(b"not a zip")
        failed = subprocess.run(
            [sys.executable, str(SCRIPT), str(invalid), "--format", "json"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(failed.returncode, 1)
        self.assertEqual(json.loads(failed.stdout)["overall_status"], "failed")

        missing = subprocess.run(
            [sys.executable, str(SCRIPT), str(self.root / "missing.pptx")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(missing.returncode, 2)


if __name__ == "__main__":
    unittest.main()
