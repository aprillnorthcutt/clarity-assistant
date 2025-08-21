# utils/module_loader.py
import os
import yaml

# ✅ Use absolute path so it works in Azure
MODULE_DIR = os.path.join(os.getcwd(), "modules")

def _module_path(module_id: int) -> str:
    fname = f"Module{int(module_id)}.yaml"
    return os.path.join(MODULE_DIR, fname)

def load_module(module_id: int) -> dict:
    path = _module_path(module_id)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Module file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    return {
        "id": module_id,
        "title": data.get("title", f"Module {module_id}"),
        "objective": data.get("objective", "Clarify and strengthen the audit note."),
        "audit_context": data.get("audit_context", "General nonprofit audit context."),
        "sample_note": data.get("sample_note", ""),
        "preferred_height": data.get("preferred_height", 175),
        "checks": data.get("checks", []),
        "guidance": data.get("guidance", ""),
        "gaap_refs": data.get("gaap_refs", []),
    }
