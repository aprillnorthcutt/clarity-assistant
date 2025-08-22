# utils/module_loader.py
from __future__ import annotations
import os
from pathlib import Path
from typing import Optional, Sequence, Union
import yaml

# ✅ Base folders (adjust if your layout differs)
REPO_ROOT   = Path(os.getcwd())
MODULE_DIR  = REPO_ROOT / "modules"         # numeric modules live here (unchanged)
PROMPTS_DIR = REPO_ROOT / "prompts"         # dotted-path prompts live here

# ---------- helpers ----------
def _read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")

def _try_with_extensions(base: Path, exts: Sequence[str]) -> Optional[str]:
    for ext in exts:
        candidate = base.with_suffix(ext)
        if candidate.exists():
            return _read_text(candidate)
    return None

def _module_path_numeric(module_id: int) -> Path:
    # Keep your existing numeric behavior: modules/module{ID}.yaml
    fname = f"module{int(module_id)}.yaml"
    return MODULE_DIR / fname

def _load_numeric_module(module_id: int) -> dict:
    path = _module_path_numeric(module_id)
    if not path.exists():
        raise FileNotFoundError(f"Module file not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
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

def _load_dotted_prompt(dotted: str) -> str:
    """
    Map e.g. 'prompts.finance.clarifier.system' to:
      <repo>/prompts/finance/clarifier/system.(md|txt|yaml|yml|json)

    Also supports names like 'user.tmpl' -> user.tmpl.(md|txt|yaml|yml|json)
    """
    dotted = (dotted or "").strip()
    if not dotted:
        raise ValueError("module_id is empty.")

    parts = dotted.split(".")
    # allow with or without leading 'prompts'
    if parts[0] == "prompts":
        parts = parts[1:]

    base = PROMPTS_DIR.joinpath(*parts)  # e.g., prompts/finance/clarifier/system
    # Try common extensions
    content = _try_with_extensions(base, [".md", ".txt", ".yaml", ".yml", ".json"])
    if content is not None:
        return content

    # Special-case stems with a dot (e.g., user.tmpl.md)
    if "." in base.name:
        base_parent = base.parent / base.name
        content = _try_with_extensions(base_parent, [".md", ".txt", ".yaml", ".yml", ".json"])
        if content is not None:
            return content

    raise FileNotFoundError(
        f"Prompt not found for '{dotted}'. Tried: {base}(.md|.txt|.yaml|.yml|.json)"
    )

# ---------- public API ----------
def load_module(module_id: Union[int, str]) -> Union[dict, str]:
    """
    Backward-compatible loader:

    - If module_id is an int OR a string of digits:
        returns dict from modules/module{ID}.yaml  (same structure as before)
    - Otherwise (string with dots):
        returns text contents of the prompt file resolved under /prompts
    """
    if isinstance(module_id, int) or (isinstance(module_id, str) and module_id.isdigit()):
        return _load_numeric_module(int(module_id))
    return _load_dotted_prompt(str(module_id))
