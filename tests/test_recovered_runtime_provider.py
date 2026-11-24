from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "evaluation" / "recovered_runtime_provider.py"
SPEC = importlib.util.spec_from_file_location("recovered_runtime_provider", MODULE_PATH)
assert SPEC and SPEC.loader
provider = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(provider)


class RecoveredRuntimeProviderTests(unittest.TestCase):
    def test_descriptor_is_evaluation_only_and_disables_grouped_layouts(self) -> None:
        descriptor = provider.descriptor()
        self.assertEqual(descriptor["classification"], "evaluation_only")
        self.assertEqual(descriptor["supported_mode"], "create")
        self.assertTrue(provider.DISABLED_GROUPED_LAYOUTS <= set(descriptor["disabled_layouts"]))
        self.assertFalse(set(descriptor["automatic_layouts"]) & set(descriptor["disabled_layouts"]))

    def test_job_directory_must_be_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary)
            (path / "stale.txt").write_text("stale", encoding="utf-8")
            with self.assertRaises(provider.ProviderError):
                provider.ensure_clean_job_dir(path)

    def test_hard_gate_failure_is_blocking(self) -> None:
        result = {
            "passed": True,
            "checks": {
                "overflow": {
                    "severity": "hard",
                    "passed": False,
                    "detail": "detected",
                }
            },
        }
        blockers = provider.runtime_gate_blockers(result)
        self.assertTrue(any("overflow" in item for item in blockers))

    def test_render_plan_cannot_reference_unknown_required_element(self) -> None:
        deck_spec = {
            "deck_id": "deck",
            "task_instance_id": "task",
            "slides": [{
                "slide_id": "S01",
                "position": 1,
                "layout": {"template_name": "Title and Content"},
                "elements": [{"element_id": "E01"}],
            }],
        }
        render_plan = {
            "deck_id": "deck",
            "task_instance_id": "task",
            "slides": [{
                "slide_id": "S01",
                "source_position": 1,
                "layout": {"template_name": "Title and Content"},
                "required_element_ids": ["MISSING"],
                "blocks": [{"element_id": "MISSING"}],
            }],
        }
        with self.assertRaises(provider.ProviderError):
            provider.validate_plan_parity(deck_spec, render_plan)

    def test_render_plan_cannot_drop_decision_critical_requirement(self) -> None:
        deck_spec = {
            "deck_id": "deck",
            "task_instance_id": "task",
            "decision_critical_requirements": [{
                "requirement_id": "CR-001",
                "required_in_deck": True,
                "target_slide_ids": ["S01"],
                "target_element_ids": ["E01"],
            }],
            "slides": [{
                "slide_id": "S01",
                "position": 1,
                "layout": {"template_name": "Title and Content"},
                "elements": [{"element_id": "E01"}],
            }],
        }
        render_plan = {
            "deck_id": "deck",
            "task_instance_id": "task",
            "requirement_bindings": [],
            "slides": [{
                "slide_id": "S01",
                "source_position": 1,
                "layout": {"template_name": "Title and Content"},
                "required_element_ids": ["E01"],
                "blocks": [{"element_id": "E01"}],
            }],
        }
        with self.assertRaises(provider.ProviderError):
            provider.validate_plan_parity(deck_spec, render_plan)


if __name__ == "__main__":
    unittest.main()
