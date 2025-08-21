# utils/module_loader.py
import os
import yaml

# Root-relative folder holding Module1.yaml ... Module6.yaml
MODULE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "modules")

def _module_path(module_id: int) -> str:
    # Accept 1..6 or any int that maps to Module{n}.yaml
    fname = f"Module{int(module_id)}.yaml"
    return os.path.join(MODULE_DIR, fname)

def load_module(module_id: int) -> dict:
    """
    Load a module YAML and return a dict with expected fields used by the UI:
      title, objective, audit_context, sample_note, preferred_height, checks, guidance
    """
    path = _module_path(module_id)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Module file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    # Normalize with defaults so your UI never crashes
    return {
        "id": module_id,
        "title": data.get("title", f"Module {module_id}"),
        "objective": data.get("objective", "Clarify and strengthen the audit note."),
        "audit_context": data.get("audit_context", "General nonprofit audit context."),
        "sample_note": data.get("sample_note", ""),
        "preferred_height": data.get("preferred_height", 175),
        # Optional, used to enrich the prompt
        "checks": data.get("checks", []),            # list[str]
        "guidance": data.get("guidance", ""),        # str (freeform)
        "gaap_refs": data.get("gaap_refs", []),      # list[str] optional references
    }
