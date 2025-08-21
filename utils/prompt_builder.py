# utils/prompt_builder.py

from typing import List, Dict

def _bulletize(items):
    if not items:
        return ""
    return "\n".join([f"- {x}" for x in items])

def build_prompt(module_data: Dict, audit_note: str) -> List[Dict[str, str]]:
    """
    Construct Azure OpenAI chat messages from a module YAML and the user note.
    Expects module_data from utils.module_loader.load_module(...)
    """
    title = module_data.get("title", "")
    objective = module_data.get("objective", "")
    context = module_data.get("audit_context", "")
    checks = module_data.get("checks", [])
    guidance = module_data.get("guidance", "")
    gaap_refs = module_data.get("gaap_refs", [])

    checks_block = _bulletize(checks)
    refs_block = _bulletize(gaap_refs)

    system_prompt = f"""
You are an expert nonprofit audit reviewer and technical writer.
Your goal is to improve clarity, specificity, and GAAP-aligned disclosure quality.

Module: {title}
Objective: {objective}
Audit Context: {context}

Primary review checks:
{checks_block if checks_block else "- Identify vague or ambiguous language\n- Provide precise, supportable alternatives\n- Flag missing or risky disclosures"}

Additional guidance:
{guidance if guidance else "Use plain, specific language; avoid boilerplate; include concrete amounts, dates, policies, restrictions, and constraints when known."}

If GAAP references are relevant, consider:
{refs_block if refs_block else "- Use relevant GAAP guidance when applicable."}

Output format:
- Start with a concise summary of issues.
- Provide improved wording (redlines or “before → after”).
- Include clarifying questions to fill gaps.
- Note risks or compliance considerations.
- Keep recommendations specific and actionable.
    """.strip()

    user_prompt = f"""Audit note to review:
---
{audit_note.strip()}
---
Please apply the checks and return a reviewer-friendly output as described.
"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
