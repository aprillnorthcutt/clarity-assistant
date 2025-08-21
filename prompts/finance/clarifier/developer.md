Return one JSON object:

{
  "summary": "one-sentence reformulation of the user note",
  "actions": [
    {"step": 1, "title": "Concise action", "details": "Specific next step"}
  ],
  "budget_adjustments": [
    {"category": "string", "change": "+/-number", "period": "monthly|one-time", "rationale": "string"}
  ],
  "risks_or_considerations": ["bullets about tradeoffs or constraints"],
  "clarifying_questions": ["short questions to unblock decisions"],
  "tone": "supportive|neutral|urgent"
}

Rules:
- 3–6 actions.
- Use provided amounts/dates; else use "TBD".
- If multiple topics (debt/savings/bills), group by topic in action titles.
- If input isn’t financial, return an empty plan and one clarifying question.
