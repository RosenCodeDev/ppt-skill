#!/usr/bin/env python3
"""Validate both skill packages, v2 examples, parity, and regression cases."""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, ValidationError
except ImportError as exc:
    raise SystemExit(
        "Missing validation dependency. Run: "
        "python -m pip install -r requirements-dev.txt"
    ) from exc


JsonObject = dict[str, Any]


def load_json(path: Path) -> JsonObject:
    with path.open("r", encoding="utf-8-sig") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"Expected a JSON object: {path}")
    return value


def assert_equal(actual: Any, expected: Any, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def option_one(element: JsonObject) -> JsonObject:
    matches = [
        option
        for option in element["options"]
        if option["option_number"] == 1 and option["used_in_pptx"] is True
    ]
    assert_equal(len(matches), 1, f"{element['element_id']} must have one used Option 1")
    if any(option["used_in_pptx"] for option in element["options"] if option is not matches[0]):
        raise AssertionError(f"{element['element_id']} marks a non-Option-1 value as used")
    return matches[0]


def selected_layout_value(layout: JsonObject) -> JsonObject:
    return {
        "template_name": layout["template_name"],
        "semantic_alias": layout["semantic_alias"],
        "custom": layout["custom"],
    }


def validate_element_parity(
    report_element: JsonObject,
    selected: JsonObject,
    alternatives: list[JsonObject],
    alternative_status: str,
    context: str,
) -> None:
    used = option_one(report_element)
    assert_equal(used["option_id"], selected["option_id"], f"{context} Option 1 id")
    assert_equal(used["value"], selected["value"], f"{context} Option 1 value")
    assert_equal(report_element["alternative_status"], alternative_status, f"{context} alternative status")

    expected_alternatives = [(item["option_id"], item["value"]) for item in alternatives]
    reported_alternatives = [
        (item["option_id"], item["value"])
        for item in report_element["options"]
        if item["option_number"] != 1
    ]
    assert_equal(reported_alternatives, expected_alternatives, f"{context} alternatives")


def validate_layout_parity(report_layout: JsonObject, deck_layout: JsonObject, context: str) -> None:
    used = option_one(report_layout)
    assert_equal(used["option_id"], deck_layout["option_id"], f"{context} layout Option 1 id")
    assert_equal(used["value"], selected_layout_value(deck_layout), f"{context} layout Option 1 value")
    assert_equal(used.get("rationale"), deck_layout["rationale"], f"{context} layout rationale")
    assert_equal(report_layout["alternative_status"], deck_layout["alternative_status"], f"{context} layout alternative status")

    expected = [
        (
            item["option_id"],
            {
                "template_name": item["template_name"],
                "semantic_alias": item["semantic_alias"],
                "custom": item["custom"],
            },
            item["rationale"],
        )
        for item in deck_layout["alternatives"]
    ]
    reported = [
        (item["option_id"], item["value"], item.get("rationale"))
        for item in report_layout["options"]
        if item["option_number"] != 1
    ]
    assert_equal(reported, expected, f"{context} layout alternatives")


def flatten_report_slides(report: JsonObject) -> dict[str, JsonObject]:
    slides: dict[str, JsonObject] = {}
    for section in report["sections"]:
        for slide in section["slides"]:
            slide_id = slide["slide_id"]
            if slide_id in slides:
                raise AssertionError(f"Duplicate report slide: {slide_id}")
            slides[slide_id] = slide
    return slides


def validate_parity(deck: JsonObject, report: JsonObject) -> None:
    assert_equal(report["deck_id"], deck["deck_id"], "Report deck id")
    assert_equal(report["task_instance_id"], deck["task_instance_id"], "Report task instance")

    output = deck["outputs"]["companion_report"]
    assert_equal(output["generated_from_deck_spec"], True, "DeckSpec report provenance")
    markdown = output["markdown_file"]
    chat = output["chat_output"]
    assert_equal(markdown["status"] in {"created", "created_with_disclosures"}, True, "Markdown status")
    assert_equal(markdown["complete"], True, "Markdown completeness")
    assert_equal(markdown["single_file"], True, "Markdown single-file requirement")
    assert_equal(chat["status"] in {"created", "created_with_disclosures"}, True, "Chat status")
    assert_equal(chat["complete"], True, "Chat completeness")
    assert_equal(chat["rendered_in_final_response"], True, "Chat rendering")
    assert_equal(chat["content_matches_markdown"], True, "Chat/Markdown parity")
    assert_equal(report["delivery"]["markdown_file"]["path"], markdown["path"], "Markdown output path")

    deck_slides = {slide["slide_id"]: slide for slide in deck["slides"]}
    expected_full = {
        slide_id
        for slide_id, slide in deck_slides.items()
        if slide["substantive"] or slide["modified_in_task"]
    }
    expected_notice = set(deck_slides) - expected_full

    for slide_id, slide in deck_slides.items():
        expected_coverage = "full" if slide_id in expected_full else "technical_notice_only"
        assert_equal(slide["companion_coverage"], expected_coverage, f"{slide_id} DeckSpec coverage")

    report_slides = flatten_report_slides(report)
    assert_equal(set(report_slides), expected_full, "Full-coverage report slide ids")

    notice_entries = report["technical_delivery_notice"]["unchanged_non_substantive_slides"]
    notice_by_id = {entry["slide_id"]: entry for entry in notice_entries}
    assert_equal(set(notice_by_id), expected_notice, "Technical-notice slide ids")
    for slide_id in expected_notice:
        assert_equal(
            notice_by_id[slide_id]["classification_reason"],
            deck_slides[slide_id]["substantive_reason"],
            f"{slide_id} technical-notice classification reason",
        )

    for slide_id in expected_full:
        deck_slide = deck_slides[slide_id]
        report_slide = report_slides[slide_id]
        context = f"Slide {slide_id}"
        for field in ("position", "substantive", "substantive_reason", "modified_in_task", "companion_coverage"):
            assert_equal(report_slide[field], deck_slide[field], f"{context} {field}")

        validate_layout_parity(report_slide["layout"], deck_slide["layout"], context)

        deck_title = deck_slide.get("title")
        report_title = report_slide["title"]
        expected_title_parts: list[str] = []
        if deck_title is None:
            assert_equal(report_title["format"], "NONE", f"{context} title format")
            assert_equal(report_title["t1"], None, f"{context} T1")
            assert_equal(report_title["t2"], None, f"{context} T2")
        else:
            assert_equal(report_title["format"], deck_title["format"], f"{context} title format")
            for field, label in (("t1", "T1"), ("t2", "T2")):
                deck_part = deck_title.get(field)
                report_part = report_title[field]
                if deck_part is None:
                    assert_equal(report_part, None, f"{context} {label}")
                else:
                    if report_part is None:
                        raise AssertionError(f"{context} is missing {label}")
                    expected_title_parts.append(label)
                    validate_element_parity(
                        report_part,
                        deck_part["selected"],
                        deck_part["alternatives"],
                        deck_part["alternative_status"],
                        f"{context} {label}",
                    )

        deck_elements = {item["element_id"]: item for item in deck_slide["elements"]}
        report_elements = {item["element_id"]: item for item in report_slide["elements"]}
        if len(report_elements) != len(report_slide["elements"]):
            raise AssertionError(f"{context} contains duplicate element ids")
        assert_equal(set(report_elements), set(deck_elements), f"{context} element coverage")
        for element_id, deck_element in deck_elements.items():
            content = deck_element["content"]
            validate_element_parity(
                report_elements[element_id],
                content["selected"],
                content["alternatives"],
                content["alternative_status"],
                f"{context} element {element_id}",
            )

        completeness = report_slide["completeness"]
        assert_equal(completeness["title_parts_reported"], expected_title_parts, f"{context} title completeness")
        assert_equal(set(completeness["expected_element_ids"]), set(deck_elements), f"{context} expected element ids")
        assert_equal(set(completeness["reported_element_ids"]), set(deck_elements), f"{context} reported element ids")


def expect_schema_failure(schema: JsonObject, instance: JsonObject, name: str) -> None:
    try:
        Draft202012Validator(schema).validate(instance)
    except ValidationError:
        return
    raise AssertionError(f"Negative schema case unexpectedly passed: {name}")


def expect_parity_failure(deck: JsonObject, report: JsonObject, name: str) -> None:
    try:
        validate_parity(deck, report)
    except AssertionError:
        return
    raise AssertionError(f"Negative parity case unexpectedly passed: {name}")


def validate_regression_cases(deck_schema: JsonObject, report_schema: JsonObject, deck: JsonObject, report: JsonObject) -> None:
    invalid = deepcopy(deck)
    next(slide for slide in invalid["slides"] if slide["slide_id"] == "S04")["companion_coverage"] = "technical_notice_only"
    expect_schema_failure(deck_schema, invalid, "substantive slide downgraded to notice only")

    invalid = deepcopy(deck)
    next(slide for slide in invalid["slides"] if slide["slide_id"] == "S03")["companion_coverage"] = "technical_notice_only"
    expect_schema_failure(deck_schema, invalid, "modified non-substantive slide downgraded")

    invalid = deepcopy(report)
    del invalid["sections"][0]["slides"][0]["layout"]
    expect_schema_failure(report_schema, invalid, "missing layout coverage")

    invalid = deepcopy(report)
    invalid["delivery"].pop("chat_output")
    expect_schema_failure(report_schema, invalid, "missing chat deliverable")

    invalid = deepcopy(report)
    s04 = next(
        slide
        for section in invalid["sections"]
        for slide in section["slides"]
        if slide["slide_id"] == "S04"
    )
    s04["elements"] = []
    s04["completeness"]["reported_element_ids"] = []
    expect_parity_failure(deck, invalid, "title-only companion entry")

    invalid = deepcopy(report)
    s04 = next(
        slide
        for section in invalid["sections"]
        for slide in section["slides"]
        if slide["slide_id"] == "S04"
    )
    s04["layout"]["options"][0]["value"]["template_name"] = "Wrong Layout"
    expect_parity_failure(deck, invalid, "layout Option 1 differs from DeckSpec")

    # Structural role does not dictate classification: these content-based exceptions remain valid.
    for role, substantive, modified, coverage in (
        ("appendix", True, False, "full"),
        ("section", True, False, "full"),
        ("contents", False, False, "technical_notice_only"),
        ("title", True, False, "full"),
    ):
        valid = deepcopy(deck)
        slide = valid["slides"][3]
        slide["structural_role"] = role
        slide["substantive"] = substantive
        slide["modified_in_task"] = modified
        slide["companion_coverage"] = coverage
        slide["substantive_reason"] = "Content-based classification regression case"
        Draft202012Validator(deck_schema).validate(valid)


def validate_package(root: Path) -> None:
    deck_schema = load_json(root / "schemas" / "deck_spec.schema.json")
    report_schema = load_json(root / "schemas" / "options_report.schema.json")
    deck = load_json(root / "examples" / "deck_spec_example.json")
    report = load_json(root / "examples" / "options_report_example.json")

    Draft202012Validator.check_schema(deck_schema)
    Draft202012Validator.check_schema(report_schema)
    Draft202012Validator(deck_schema).validate(deck)
    Draft202012Validator(report_schema).validate(report)
    validate_parity(deck, report)
    validate_regression_cases(deck_schema, report_schema, deck, report)
    print(f"JSON, parity, and regression validation passed: {root.name}")


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: validate-json.py <ai-platform-root> <addin-root>", file=sys.stderr)
        return 2

    for argument in sys.argv[1:]:
        validate_package(Path(argument).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
