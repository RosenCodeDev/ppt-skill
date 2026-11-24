#!/usr/bin/env python3
"""Fail-closed, evaluation-only bridge to the external recovered runtime."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib
import json
import logging
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid
import zipfile

INTERFACE_VERSION = "1.0.0"
PROVIDER_VERSION = "1.0.0"
RUNTIME_VERSION = "2.6.18"
RUNTIME_SHA256 = "c595e17c097d16aa33880193fceec3928e7a08cfcca603ffa82f0a03a2f7663d"

SAFE_LAYOUTS = {
    "Title Slide", "Title and Content", "Title Only", "2 Columns",
    "3 Columns", "4 Columns", "2 Columns 2/3 Split",
    "2 Columns 1/3 Split", "Big Photo Right", "CV - Bio with Photo",
    "One Pager Credential", "Section", "Title Slide with Picture",
    "Contents", "Confidentiality", "Qualification", "Backcover", "Blank",
}
DISABLED_GROUPED_LAYOUTS = {
    "Title and Content with Heading", "2 Columns with Heading",
    "3 Columns with Heading", "4 Columns with Heading",
}
CAPABILITY_ALIASES = {
    "2 Columns": "2 columns", "3 Columns": "3 columns",
    "4 Columns": "4 columns",
    "2 Columns 1/3 Split": "2 columns 1/3 split",
    "2 Columns 2/3 Split": "2 columns 2/3 split",
    "Big Photo Right": "Big portrait photo on right",
    "CV - Bio with Photo": "CV - bio with photo",
}
FAIL_LOG_PHRASES = (
    "failed to compile", "strategy failed", "skipping",
    "could not resolve target", "unknown strategy", "falling back",
    "ignored unknown content keys", "exposes 0 content slots",
)


class ProviderError(RuntimeError):
    pass


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProviderError(f"Cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ProviderError(f"Expected a JSON object: {path}")
    return value


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate_schema(instance: dict, schema_path: Path) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        shell = shutil.which("pwsh") or shutil.which("powershell")
        if shell is None:
            raise ProviderError(
                "Schema validation requires jsonschema or PowerShell Test-Json"
            )
        script = (
            "$text = [Console]::In.ReadToEnd(); "
            "try { $ok = $text | Test-Json -SchemaFile $env:OW_SCHEMA_PATH "
            "-ErrorAction Stop; if ($ok) { exit 0 } else { exit 1 } } "
            "catch { [Console]::Error.WriteLine($_.Exception.Message); exit 2 }"
        )
        env = os.environ.copy()
        env["OW_SCHEMA_PATH"] = str(schema_path)
        completed = subprocess.run(
            [shell, "-NoProfile", "-NonInteractive", "-Command", script],
            input=json.dumps(instance, ensure_ascii=False),
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        if completed.returncode:
            raise ProviderError(
                "Schema validation failed: "
                + (completed.stderr.strip() or "instance rejected")
            )
        return
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e: list(e.path))
    if errors:
        first = errors[0]
        location = "/".join(str(part) for part in first.path) or "<root>"
        raise ProviderError(f"Schema validation failed at {location}: {first.message}")


def safe_extract(archive: Path, destination: Path) -> None:
    root = os.path.abspath(destination)
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            target = os.path.abspath(os.path.join(root, member.filename))
            if os.path.commonpath((root, target)) != root:
                raise ProviderError(f"Unsafe runtime archive member: {member.filename}")
        bundle.extractall(destination)


class LogCapture(logging.Handler):
    def __init__(self) -> None:
        super().__init__(logging.WARNING)
        self.messages: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.messages.append(record.getMessage())


def descriptor() -> dict:
    return {
        "interface_version": INTERFACE_VERSION,
        "id": "recovered-runtime-evaluation",
        "version": PROVIDER_VERSION,
        "classification": "evaluation_only",
        "engine": "deck-builder-runtime",
        "engine_version": RUNTIME_VERSION,
        "runtime_sha256": RUNTIME_SHA256,
        "supported_mode": "create",
        "automatic_layouts": sorted(SAFE_LAYOUTS),
        "disabled_layouts": sorted(DISABLED_GROUPED_LAYOUTS),
    }


def ensure_clean_job_dir(path: Path) -> None:
    if path.exists() and any(path.iterdir()):
        raise ProviderError(f"Job directory must be new and empty: {path}")
    path.mkdir(parents=True, exist_ok=True)


def configure_runtime(runtime_root: Path):
    source = runtime_root / "src"
    if not (source / "compiler.py").is_file():
        raise ProviderError("Recovered runtime archive is incomplete")
    sys.path.insert(0, str(source))
    runtime = importlib.import_module("runtime")
    compiler = importlib.import_module("compiler")
    gate = importlib.import_module("gate")
    for actual, canonical in CAPABILITY_ALIASES.items():
        if canonical in compiler.LAYOUT_CAPABILITIES:
            compiler.LAYOUT_CAPABILITIES[actual] = compiler.LAYOUT_CAPABILITIES[canonical]
    return runtime, compiler, gate


def validate_plan_parity(deck_spec: dict, render_plan: dict) -> None:
    if deck_spec.get("deck_id") != render_plan.get("deck_id"):
        raise ProviderError("DeckSpec and RenderPlan deck_id differ")
    if deck_spec.get("task_instance_id") != render_plan.get("task_instance_id"):
        raise ProviderError("DeckSpec and RenderPlan task_instance_id differ")
    deck_slides = {slide["slide_id"]: slide for slide in deck_spec.get("slides", [])}
    plan_ids = [slide["slide_id"] for slide in render_plan.get("slides", [])]
    if len(plan_ids) != len(set(plan_ids)):
        raise ProviderError("RenderPlan contains duplicate slide IDs")
    if set(plan_ids) != set(deck_slides):
        raise ProviderError("RenderPlan must cover every DeckSpec slide exactly once")
    for planned in render_plan["slides"]:
        deck_slide = deck_slides[planned["slide_id"]]
        if planned["source_position"] != deck_slide["position"]:
            raise ProviderError(f"Position mismatch for {planned['slide_id']}")
        if planned["layout"]["template_name"] != deck_slide["layout"]["template_name"]:
            raise ProviderError(f"Layout mismatch for {planned['slide_id']}")
        deck_elements = {item["element_id"] for item in deck_slide.get("elements", [])}
        if not set(planned["required_element_ids"]).issubset(deck_elements):
            raise ProviderError(f"RenderPlan references unknown required element on {planned['slide_id']}")
        block_ids = {item["element_id"] for item in planned["blocks"]}
        if not set(planned["required_element_ids"]).issubset(block_ids):
            raise ProviderError(f"Required element has no render block on {planned['slide_id']}")

    requirements = {
        item["requirement_id"]: item
        for item in deck_spec.get("decision_critical_requirements", [])
        if item.get("required_in_deck") is True
    }
    if not requirements:
        raise ProviderError("DeckSpec has no decision-critical requirements for Create")
    bindings = render_plan.get("requirement_bindings", [])
    binding_ids = [item["requirement_id"] for item in bindings]
    if len(binding_ids) != len(set(binding_ids)):
        raise ProviderError("RenderPlan contains duplicate decision-critical requirement bindings")
    if set(binding_ids) != set(requirements):
        raise ProviderError("RenderPlan must bind every required decision-critical requirement exactly once")
    planned_slides = {slide["slide_id"]: slide for slide in render_plan["slides"]}
    for binding in bindings:
        requirement = requirements[binding["requirement_id"]]
        slide_id = binding["slide_id"]
        if slide_id not in requirement["target_slide_ids"] or slide_id not in planned_slides:
            raise ProviderError(f"Invalid target slide for {binding['requirement_id']}")
        element_ids = set(binding["element_ids"])
        if not element_ids <= set(requirement["target_element_ids"]):
            raise ProviderError(f"Invalid target element for {binding['requirement_id']}")
        if not element_ids <= set(planned_slides[slide_id]["required_element_ids"]):
            raise ProviderError(f"Decision-critical element is not required on {slide_id}")


def runtime_gate_blockers(result: dict) -> list[str]:
    blockers: list[str] = []
    if result.get("passed") is not True:
        blockers.append("Recovered runtime gate did not pass")
    for name, check in (result.get("checks") or {}).items():
        if not isinstance(check, dict):
            blockers.append(f"Malformed runtime gate check: {name}")
            continue
        note = " ".join(str(check.get(key, "")) for key in ("note", "detail")).lower()
        if check.get("severity") == "hard" and "skipped" in note:
            blockers.append(f"Hard runtime gate check was skipped: {name}")
        if check.get("severity") == "hard" and check.get("passed") is not True:
            blockers.append(f"Hard runtime gate check failed: {name}")
    return blockers


def render(args: argparse.Namespace) -> int:
    started_at = utc_now()
    started_epoch = dt.datetime.now(dt.timezone.utc).timestamp()
    job_dir = args.job_dir.resolve()
    ensure_clean_job_dir(job_dir)
    deck_path = args.deck_spec.resolve()
    plan_path = args.render_plan.resolve()
    template_path = args.template.resolve()
    template_manifest_path = args.template_manifest.resolve()
    output_path = args.output.resolve()
    recovered_root = args.recovered_skill_root.resolve()
    repo_root = Path(__file__).resolve().parents[1]
    schema_root = repo_root / "distributions" / "ai-platform" / "powerpoint-skill" / "schemas"

    if output_path.parent != job_dir or output_path.exists():
        raise ProviderError("Candidate must be a new file directly inside the clean job directory")
    for required in (deck_path, plan_path, template_path, template_manifest_path):
        if not required.is_file():
            raise ProviderError(f"Required input does not exist: {required}")

    deck_spec = load_json(deck_path)
    render_plan = load_json(plan_path)
    validate_schema(deck_spec, schema_root / "deck_spec.schema.json")
    validate_schema(render_plan, schema_root / "render_plan.schema.json")
    if render_plan["publication_intent"] != "evaluate" or render_plan["provider"]["classification"] != "evaluation_only":
        raise ProviderError("Recovered provider accepts only evaluation-only plans")
    if sha256(deck_path).lower() != render_plan["source_deck_spec_sha256"].lower():
        raise ProviderError("RenderPlan DeckSpec hash mismatch")
    if sha256(template_path).lower() != render_plan["template"]["sha256"].lower():
        raise ProviderError("RenderPlan template hash mismatch")
    if sha256(template_manifest_path).lower() != render_plan["template"]["manifest_sha256"].lower():
        raise ProviderError("RenderPlan template-manifest hash mismatch")
    validate_plan_parity(deck_spec, render_plan)

    template_manifest = load_json(template_manifest_path)
    provider_rules = (template_manifest.get("semantic_model") or {}).get("recovered_evaluation_provider") or {}
    eligible = set(provider_rules.get("automatic_layouts") or [])
    if not eligible:
        raise ProviderError("Template manifest has no provider eligibility list")
    for slide in render_plan["slides"]:
        layout = slide["layout"]["template_name"]
        if layout in DISABLED_GROUPED_LAYOUTS or layout not in eligible or not slide["layout"]["provider_eligible"]:
            raise ProviderError(f"Layout is not verified for recovered provider: {layout}")

    archive = recovered_root / "assets" / "deck_system_runtime_clean.zip"
    if not archive.is_file() or sha256(archive).lower() != RUNTIME_SHA256:
        raise ProviderError("Recovered runtime archive is missing or has the wrong hash")
    runtime_root = job_dir / "runtime"
    runtime_root.mkdir()
    safe_extract(archive, runtime_root)
    runtime, compiler, gate = configure_runtime(runtime_root)
    capture = LogCapture()
    compiler.logger.addHandler(capture)
    runtime.logger.addHandler(capture)
    rt = runtime.TemplateRuntime(str(template_path))
    semantic_compiler = compiler.SemanticCompiler(rt)

    deck_payload = {"slides": []}
    slide_lineage: list[dict] = []
    dispositions: list[dict] = []
    physical_by_slide_id: dict[str, list[int]] = {}
    physical_number = 0
    for planned in sorted(render_plan["slides"], key=lambda item: item["source_position"]):
        desired = planned["layout"]["template_name"]
        if desired not in semantic_compiler.layouts:
            raise ProviderError(f"Template is missing planned layout: {desired}")
        payload = planned["provider_payload"]
        if not isinstance(payload.get("intent"), str) or not isinstance(payload.get("content"), dict):
            raise ProviderError(f"Provider payload requires intent and content: {planned['slide_id']}")
        intent = compiler.INTENTS.get(payload["intent"])
        if intent is None:
            raise ProviderError(f"Unsupported recovered intent: {payload['intent']}")
        known = {slot.name for slot in intent.slots} | {"conclusion", "footnote", "source", "why", "insight", "design_choices", "photo"}
        unknown = sorted(set(payload["content"]) - known)
        if unknown:
            raise ProviderError(f"Unknown content keys on {planned['slide_id']}: {unknown}")

        original_select = compiler.select_layout
        compiler.select_layout = lambda _intent, layouts, _items=None, name=desired: (layouts[name], "forced by RenderPlan")
        try:
            plans = semantic_compiler.compile(payload, (deck_spec.get("brief") or {}).get("audience", "default"))
        finally:
            compiler.select_layout = original_select
        if not plans or any(plan.layout_name != desired for plan in plans):
            raise ProviderError(f"Provider did not honor planned layout for {planned['slide_id']}")
        before = len(rt.prs.slides)
        for compiled in plans:
            semantic_compiler.execute(compiled)
        if len(rt.prs.slides) - before != len(plans):
            raise ProviderError(f"Physical slide count mismatch for {planned['slide_id']}")
        numbers = list(range(physical_number + 1, physical_number + len(plans) + 1))
        physical_number += len(plans)
        slide_lineage.append({"source_slide_id": planned["slide_id"], "physical_slide_numbers": numbers, "actual_layouts": [desired] * len(plans)})
        physical_by_slide_id[planned["slide_id"]] = numbers
        shape_ids = sorted({int(shape.shape_id) for n in numbers for shape in rt.prs.slides[n - 1].shapes})
        required_ids = set(planned["required_element_ids"])
        for block in planned["blocks"]:
            dispositions.append({
                "slide_id": planned["slide_id"], "element_id": block["element_id"],
                "required": block["element_id"] in required_ids or bool(block["required"]),
                "status": "emitted", "physical_slide_numbers": numbers,
                "shape_ids": shape_ids, "details": f"Rendered through {block['content_key']}",
            })
        deck_payload["slides"].append(payload)

    bad_logs = [m for m in capture.messages if any(p in m.lower() for p in FAIL_LOG_PHRASES)]
    if bad_logs:
        raise ProviderError("Recovered runtime emitted fail-open warning(s): " + " | ".join(bad_logs))
    rt.save(str(output_path))
    if not output_path.is_file() or output_path.stat().st_mtime < started_epoch:
        raise ProviderError("Provider did not create a fresh candidate")

    gate_path = job_dir / "gate_result.json"
    if gate_path.exists():
        raise ProviderError("Unexpected pre-existing gate result")
    gate_result = gate.run_gate(deck_payload, str(output_path), str(template_path), str(gate_path))
    if not gate_path.is_file() or gate_path.stat().st_mtime < started_epoch:
        raise ProviderError("Runtime did not create a fresh gate result")
    blockers = runtime_gate_blockers(gate_result)
    if blockers:
        raise ProviderError("; ".join(blockers))

    structural_path = job_dir / "structural_report.json"
    completed = subprocess.run(
        [sys.executable, str(args.structural_validator.resolve()), str(output_path),
         "--format", "json"],
        capture_output=True, text=True, check=False,
    )
    structural_path.write_text(completed.stdout, encoding="utf-8")
    if completed.returncode != 0:
        raise ProviderError("Structural validator failed: " + completed.stderr.strip())
    structural = load_json(structural_path)
    if structural.get("summary", {}).get("failed", 0):
        raise ProviderError("Structural validator reported blocking failures")

    requirement_dispositions: list[dict] = []
    for binding in render_plan["requirement_bindings"]:
        numbers = physical_by_slide_id[binding["slide_id"]]
        emitted_text = " ".join(
            str(getattr(shape, "text", ""))
            for number in numbers
            for shape in rt.prs.slides[number - 1].shapes
        ).casefold()
        missing_tokens = [
            token for token in binding["verification_tokens"]
            if token.casefold() not in emitted_text
        ]
        if missing_tokens:
            raise ProviderError(
                f"Decision-critical requirement {binding['requirement_id']} is not visibly emitted; "
                f"missing tokens: {missing_tokens}"
            )
        requirement_dispositions.append({
            "requirement_id": binding["requirement_id"],
            "required": True,
            "status": "verified_emitted",
            "slide_ids": [binding["slide_id"]],
            "element_ids": binding["element_ids"],
            "verification_evidence": [
                f"Found required tokens on physical slides {numbers}: {binding['verification_tokens']}"
            ],
        })

    build_id = str(uuid.uuid4())
    provider_result_path = job_dir / "provider_result.json"
    provider_result = {
        "interface_version": INTERFACE_VERSION, "build_id": build_id,
        "status": "succeeded", "descriptor": descriptor(),
        "inputs": {"deck_spec_sha256": sha256(deck_path), "render_plan_sha256": sha256(plan_path), "template_sha256": sha256(template_path), "template_manifest_sha256": sha256(template_manifest_path)},
        "candidate": {"path": str(output_path), "sha256": sha256(output_path), "slide_count": len(rt.prs.slides)},
        "slide_lineage": slide_lineage, "element_dispositions": dispositions,
        "requirement_dispositions": requirement_dispositions,
        "diagnostics": {"runtime_gate": str(gate_path), "captured_warnings": capture.messages},
    }
    write_json(provider_result_path, provider_result)

    def artifact(path: Path) -> dict:
        return {"path": str(path), "sha256": sha256(path)}

    findings = [{"finding_id": f"runtime-warning-{i}", "source": "recovered-runtime-gate", "severity": "advisory", "blocking": False, "status": "open", "message": str(w)} for i, w in enumerate(gate_result.get("warn_items", []), 1)]
    build_manifest = {
        "schema_version": "1.0.0", "build_id": build_id,
        "plan_id": render_plan["plan_id"], "deck_id": render_plan["deck_id"],
        "task_instance_id": render_plan["task_instance_id"],
        "publication_intent": "evaluate", "started_at": started_at,
        "completed_at": utc_now(),
        "provider": {"id": "recovered-runtime-evaluation", "interface_version": INTERFACE_VERSION, "classification": "evaluation_only", "version": PROVIDER_VERSION, "engine": "deck-builder-runtime", "engine_version": RUNTIME_VERSION},
        "inputs": {"deck_spec": artifact(deck_path), "render_plan": artifact(plan_path), "template": artifact(template_path), "template_manifest": artifact(template_manifest_path)},
        "candidate": {"path": str(output_path), "sha256": sha256(output_path), "slide_count": len(rt.prs.slides)},
        "slide_lineage": slide_lineage, "element_dispositions": dispositions,
        "requirement_dispositions": requirement_dispositions,
        "findings": findings,
        "qa": {
            "contract_validation": {"status": "passed", "evidence": ["DeckSpec, RenderPlan, parity, and hashes passed"]},
            "decision_critical_coverage": {"status": "passed", "evidence": ["Every required brief item was found in emitted slide text"]},
            "provider_result": {"status": "passed", "evidence": [str(provider_result_path), str(gate_path)]},
            "package_integrity": {"status": "passed", "evidence": [str(structural_path)]},
            "layout_geometry": {"status": "warning", "evidence": ["Overflow gate passed; rendered review remains required"]},
            "template_fidelity": {"status": "warning", "evidence": ["Evaluation provider is not a publication fidelity authority"]},
            "render_completeness": {"status": "skipped", "evidence": ["PowerPoint rendering follows provider generation"]},
            "visual_review": {"status": "skipped", "evidence": ["Blind/manual review not yet performed"]},
            "report_parity": {"status": "skipped", "evidence": ["Report is generated after visual validation"]},
        },
        "artifacts": {"provider_result": artifact(provider_result_path), "structural_report": artifact(structural_path)},
        "status": "awaiting_visual_review",
        "delivery": {"status": "ineligible", "reasons": ["Recovered runtime is external and evaluation-only", "Visual review and report parity are incomplete"]},
    }
    validate_schema(build_manifest, schema_root / "build_manifest.schema.json")
    output_manifest = job_dir / "build_manifest.json"
    write_json(output_manifest, build_manifest)
    print(json.dumps({"candidate": str(output_path), "build_manifest": str(output_manifest)}, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    sub.add_parser("describe")
    run = sub.add_parser("render")
    run.add_argument("--deck-spec", type=Path, required=True)
    run.add_argument("--render-plan", type=Path, required=True)
    run.add_argument("--template", type=Path, required=True)
    run.add_argument("--template-manifest", type=Path, required=True)
    run.add_argument("--recovered-skill-root", type=Path, required=True)
    run.add_argument("--job-dir", type=Path, required=True)
    run.add_argument("--output", type=Path, required=True)
    default_validator = Path(__file__).resolve().parents[1] / "distributions" / "ai-platform" / "powerpoint-skill" / "scripts" / "validate_pptx.py"
    run.add_argument("--structural-validator", type=Path, default=default_validator)
    return root


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "describe":
            print(json.dumps(descriptor(), indent=2))
            return 0
        return render(args)
    except ProviderError as exc:
        print(f"recovered-runtime-provider: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"recovered-runtime-provider: unexpected failure: {exc}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
