# pages/20_Financial_Clarity_Assistant.py

import os
import json
import streamlit as st
from openai import AzureOpenAI
from utils.module_loader import load_module  # loads .md files by dotted path (e.g., "prompts.finance.clarifier.system")

# Hide Streamlit's default multipage sidebar links on this page
st.markdown(
    """
    <style>
      /* Cover multiple Streamlit versions */
      [data-testid="stSidebarNav"],
      section[data-testid="stSidebarNav"],
      div[data-testid="stSidebarNav"],
      ul[data-testid="stSidebarNavItems"],
      a[data-testid="stSidebarNavLink"] { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
# Global sidebar nav (shows both tools on every page)
# ─────────────────────────────────────────────────────────────
def render_global_nav(active: str):
    with st.sidebar:
        st.markdown("### 🧭 Clarity Assistant")
        # subtle separator under the section header
        st.markdown(
            "<hr style='margin:4px 0 8px 0; border: none; border-top: 1px solid #e6e6e6;'>",
            unsafe_allow_html=True,
        )

        if active == "audit":
            st.markdown("- **🧠 Nonprofit Audit Clarity Assistant**")
        else:
            st.page_link(
                "pages/10_Audit_Clarity_Assistant.py",
                label="🧠 Nonprofit Audit Clarity Assistant",
            )

        if active == "finance":
            st.markdown("- **💰 Financial Clarity Assistant**")
        else:
            st.page_link(
                "pages/20_Financial_Clarity_Assistant.py",
                label="💰 Financial Clarity Assistant",
            )
            
# ---- Session state for finance page ----
if "finance_plan" not in st.session_state:
    st.session_state.finance_plan = None
if "finance_user_text" not in st.session_state:
    st.session_state.finance_user_text = ""
# optional: will hold values the user enters in the refinement expander (applied on next run)
if "finance_pending" not in st.session_state:
    st.session_state.finance_pending = None

# If we have pending refined values, apply them BEFORE widgets are created
if st.session_state.finance_pending:
    p = st.session_state.finance_pending
    # Only set keys that have a non-empty value
    if p.get("income"):
        st.session_state["finance_income"] = p["income"]
    if p.get("expenses") is not None:
        st.session_state["finance_expenses"] = p["expenses"]
    if p.get("goals"):
        st.session_state["finance_goals"] = p["goals"]
    if p.get("constraints"):
        st.session_state["finance_constraints"] = p["constraints"]
    st.session_state.finance_pending = None  # clear handoff

# ---------- Small UI helpers ----------
def render_action_card(a: dict):
    step = a.get("step", "")
    title = (a.get("title") or "").strip()
    details = (a.get("details") or "").strip()
    topic = (a.get("topic") or "").strip()          # optional
    priority = (a.get("priority") or "").strip()    # optional
    due = (a.get("due_date") or "").strip()         # optional

    with st.container(border=True):
        cols = st.columns([0.12, 0.68, 0.20])
        with cols[0]:
            st.markdown(
                "<div style='width:32px;height:32px;border-radius:50%;background:#111;"
                "color:#fff;display:flex;align-items:center;justify-content:center;"
                "font-weight:700'>"
                f"{step}</div>",
                unsafe_allow_html=True
            )
        with cols[1]:
            st.markdown(f"**{title}**")
            if topic or priority or due:
                row = ""
                if topic:
                    row += "<span style='padding:2px 8px;border-radius:9999px;background:#eef2ff;color:#1e3a8a;font-size:12px;margin-right:6px'>#" + topic + "</span>"
                if priority:
                    row += "<span style='padding:2px 8px;border-radius:9999px;background:#fef3c7;color:#92400e;font-size:12px;margin-right:6px'>Priority: " + priority + "</span>"
                if due:
                    row += "<span style='padding:2px 8px;border-radius:9999px;background:#dcfce7;color:#166534;font-size:12px;margin-right:6px'>Due: " + due + "</span>"
                st.markdown(row, unsafe_allow_html=True)
        with cols[2]:
            st.checkbox("Done", key=f"done_{step}_{title}")

        if details:
            st.markdown(
                f"<div style='color:#4b5563;font-size:14px;margin-top:6px'>{details}</div>",
                unsafe_allow_html=True
            )

# Page title (config is set in app.py)
st.title("Financial Clarity Assistant")
st.caption("Turn vague money notes into a clear, actionable plan.")

# 👉 Add the global nav right after title/caption (so it's always visible)
render_global_nav(active="finance")

# 🔐 Azure OpenAI client
client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
)

# 🧠 Optional context in sidebar (helps produce more specific plans)
with st.sidebar:
    # subtle divider between the global nav and this section
    st.markdown(
        "<hr style='margin:4px 0 8px 0; border: none; border-top: 1px solid #e6e6e6;'>",
        unsafe_allow_html=True,
    )

    st.markdown("## 💡 Financial Context (Optional)")
    income = st.text_input("Monthly income", placeholder="e.g., 5200", key="finance_income")
    goals = st.text_input("Savings goals", placeholder="e.g., $5k emergency fund by Dec", key="finance_goals")
    debts = st.text_area("Debt summary", placeholder="e.g., Card A $3.2k @ 23%, Card B $1.1k @ 18%", key="finance_debts")
    horizon = st.text_input("Time horizon", placeholder="e.g., Next 3 months", key="finance_horizon")
    constraints = st.text_area("Constraints", placeholder="e.g., Travel in Oct; fixed rent", key="finance_constraints")
    st.markdown("---")
    st.markdown("<small>Built for clarity, simplicity, and action.</small>", unsafe_allow_html=True)


# ── Controls (place BEFORE the textarea so we can safely set session state) ──
col1, col2, col3, col4 = st.columns([1,1,1,1])
with col1:
    run = st.button("Clarify Plan", type="primary", use_container_width=True, key="finance_run")
with col2:
    show_raw = st.toggle("Show raw JSON", value=False, key="finance_raw")
with col3:
    if st.button("Try Demo", use_container_width=True, key="finance_demo"):
        st.session_state.finance_user_text = (
            "I want to save more but my credit card balance keeps growing. "
            "Maybe cut dining? Not sure."
        )
        st.rerun()
with col4:
    if st.button("Reset", use_container_width=True, key="finance_reset"):
        st.session_state.finance_plan = None
        st.session_state.finance_user_text = ""
        # also clear any refined values
        for k in ("finance_income", "finance_expenses", "finance_goals", "finance_constraints"):
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

# 📝 Main input (binds to session state AFTER any Try Demo/Reset changes)
user_text = st.text_area(
    "Paste a note (messy is fine):",
    height=175,
    placeholder="Need to cover a $600 car repair this month but still save something…",
    key="finance_user_text"
)

# 🚀 Invoke model (updates session state only)
if run and user_text.strip():
    try:
        system = load_module("prompts.finance.clarifier.system")
        developer = load_module("prompts.finance.clarifier.developer")
        user_tmpl = load_module("prompts.finance.clarifier.user.tmpl")

        user_msg = user_tmpl.format(
            user_text=user_text.strip(),
            income=income or "TBD",
            goals=goals or "TBD",
            debts=debts or "TBD",
            time_horizon=horizon or "TBD",
            constraints=constraints or "None"
        )

        with st.spinner("Thinking…"):
            resp = client.chat.completions.create(
                model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
                temperature=0.2,
                max_tokens=900,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "system", "content": developer},
                    {"role": "user", "content": user_msg}
                ]
            )

        raw = resp.choices[0].message.content

        try:
            plan = json.loads(raw)
        except Exception:
            plan = {"summary": "Parse issue", "raw": raw}

        # Save to session state so it persists across reruns
        st.session_state.finance_plan = plan

    except Exception as e:
        st.error(f"❌ Error calling Azure OpenAI: {e}")

# --- Render stored plan (persists across reruns) ---
plan = st.session_state.get("finance_plan")
if plan:
    # Optional raw JSON
    if show_raw:
        st.code(json.dumps(plan, indent=2), language="json")

    # Summary / Risks / Questions
    with st.container(border=True):
        st.subheader("Summary")
        st.write(plan.get("summary", ""))

        risks = plan.get("risks_or_considerations") or []
        if risks:
            st.markdown("**Risks / Considerations**")
            for r in risks:
                st.write(f"- {r}")

        qs = plan.get("clarifying_questions") or []
        if qs:
            st.markdown("**Clarifying Questions**")
            for q in qs:
                st.write(f"- {q}")

    # Actions & Budget Adjustments
    with st.container(border=True):
        st.subheader("Actions")

        actions = plan.get("actions") or []
        if not actions:
            st.info("No actions returned. Try adding more context or click **Try Demo**.")
        else:
            for a in actions:
                render_action_card(a)

        # Guardrail: if we don't have a savings baseline, skip savings adjustments
        adj = plan.get("budget_adjustments") or []
        clean_adj = []
        for b in adj:
            cat = (b.get("category") or "").strip().lower()
            if cat == "savings" and not (st.session_state.get("finance_goals") or st.session_state.get("finance_income")):
                continue
            clean_adj.append(b)

        if clean_adj:
            st.subheader("Budget Adjustments")
            for b in clean_adj:
                st.markdown(
                    f"- **{b.get('category')}**: {b.get('change')} "
                    f"({b.get('period')}) — {b.get('rationale')}"
                )

    # --- Refinement prompt: collect missing numbers and refine the plan ---
    needs_income = not (st.session_state.get("finance_income") and str(st.session_state["finance_income"]).strip())
    has_savings_baseline = bool(st.session_state.get("finance_goals") and str(st.session_state["finance_goals"]).strip())
    needs_expenses = st.session_state.get("finance_expenses") is None

    missing_bits = []
    if needs_income: missing_bits.append("monthly income")
    if needs_expenses: missing_bits.append("monthly expenses (estimate)")
    if not has_savings_baseline: missing_bits.append("savings baseline/target")

    if missing_bits:
        st.info(
            "To get more concrete actions (and realistic budget adjustments), add: "
            + ", ".join(missing_bits) + ". Then click **Clarify Plan** to re-run."
        )

    with st.expander("Add or update numbers to refine the plan"):
        colA, colB, colC = st.columns(3)
        with colA:
            income_refine = st.text_input(
                "Monthly income",
                value=str(st.session_state.get("finance_income") or ""),
                key="finance_income_refine"
            )
        with colB:
            expenses_default = float(st.session_state.get("finance_expenses") or 0)
            expenses_refine = st.number_input(
                "Monthly expenses (estimate, $)",
                min_value=0.0,
                step=50.0,
                value=expenses_default,
                key="finance_expenses_refine"
            )
        with colC:
            savings_refine = st.text_input(
                "Savings target / baseline (e.g., $300/mo or $5k EF by Dec)",
                value=str(st.session_state.get("finance_goals") or ""),
                key="finance_goals_refine"
            )

        extra_notes = st.text_area(
            "Optional notes (new debts, constraints, timing)",
            value=str(st.session_state.get("finance_constraints") or ""),
            key="finance_constraints_refine"
        )

        # Show quick net-available estimate if possible
        try:
            if income_refine.strip():
                inc_val = float(str(income_refine).replace(",", "").replace("$", ""))
                net_available = inc_val - float(expenses_refine or 0)
                st.caption(f"Estimated net available: **${net_available:,.0f}/mo** (before debt paydown/savings)")
        except Exception:
            pass

        if st.button("Save numbers (then click Clarify Plan)", type="primary", key="finance_refine_save"):
            # hand off refined values to next run (so we apply them BEFORE widgets)
            st.session_state.finance_pending = {
                "income": income_refine.strip() or None,
                "expenses": float(expenses_refine or 0),
                "goals": savings_refine.strip() or None,
                "constraints": extra_notes.strip() or None,
            }
            st.toast("Numbers saved. Now click **Clarify Plan** to re-run with updated context.")
            st.rerun()

# 🔻 Footer
st.markdown("---")
st.markdown("<small>Built for clarity, compliance, and impact.</small>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='font-size: 14px; color: #888; text-align: center; margin-top: 20px;'>
        © 2025 <a href="https://github.com/aprillnorthcutt" target="_blank" style="color: #888; text-decoration: none;'>April Northcutt</a>
    </div>
    """,
    unsafe_allow_html=True,
)
