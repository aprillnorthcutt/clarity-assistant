# pages/10_Audit_Clarity_Assistant.py

import os
import streamlit as st
from openai import AzureOpenAI
from utils.module_loader import load_module
from utils.prompt_builder import build_prompt

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
        st.markdown("## 🧭 Clarity Assistant")
        st.markdown("<hr style='margin:4px 0 8px 0; border: none; border-top: 1px solid #e6e6e6;'>", unsafe_allow_html=True )
        #st.markdown("---")
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

        # visual break under the global nav
      #  st.markdown("---")

# ─────────────────────────────────────────────────────────────
# Page title (config is set in app.py)
# ─────────────────────────────────────────────────────────────
st.title("Nonprofit Audit Clarity Assistant")
render_global_nav(active="audit")  # show cross-links at the top of the sidebar

# 🔐 Azure OpenAI client
client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
)

# ─────────────────────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────────────────────
if "audit_user_text" not in st.session_state:
    st.session_state.audit_user_text = ""
if "audit_result" not in st.session_state:
    st.session_state.audit_result = None
if "selected_module_id" not in st.session_state:
    st.session_state.selected_module_id = 6
if "selected_module_label" not in st.session_state:
    st.session_state.selected_module_label = "General Note Review"
if "last_module_id" not in st.session_state:
    st.session_state.last_module_id = None

# ─────────────────────────────────────────────────────────────
# Module options
# ─────────────────────────────────────────────────────────────
module_options = {
    "General Note Review": 6,
    "Donated Services": 1,
    "Multi-Year Pledges": 2,
    "Expense Allocations": 3,
    "Net Asset Restrictions": 4,
    "Grant Disclosures": 5,
}
module_icons = {
    "General Note Review": "✏️",
    "Donated Services": "🎁",
    "Multi-Year Pledges": "📅",
    "Expense Allocations": "📊",
    "Net Asset Restrictions": "🔒",
    "Grant Disclosures": "📄",
}

# ─────────────────────────────────────────────────────────────
# Page-specific sidebar: Module selector
# ─────────────────────────────────────────────────────────────
def render_sidebar_modules():
    with st.sidebar:
        # ⬇️ spacer to separate the global nav ("Clarity Assistant") from the audit section
        st.markdown(
            "<div style='margin:14px 0; border-top:1px solid #e5e7eb;'></div>",
            unsafe_allow_html=True,
        )
        st.markdown("## 🧠 Nonprofit Audit Clarity Assistant")
        st.markdown("#### Select a Module")

        for label, icon in module_icons.items():
            is_active = (st.session_state.selected_module_label == label)

            active_style = """
                background-color: #e6f0ff;
                color: #003366;
                font-weight: 600;
                border-radius: 6px;
                padding: 8px 12px;
                margin-bottom: 6px;
                width: 100%;
            """

            if is_active:
                st.markdown(
                    f"<div style='{active_style}'>{icon} {label}</div>",
                    unsafe_allow_html=True
                )
            else:
                if st.button(f"{icon} {label}", key=f"module_{label}"):
                    st.session_state.selected_module_label = label
                    st.session_state.selected_module_id = module_options[label]
                    # Clear inputs/outputs on module switch
                    st.session_state.audit_user_text = ""
                    st.session_state.audit_result = None
                    st.rerun()

        st.markdown("---")
        st.markdown("<small><center>Built for clarity, simplicity, and action.</center></small>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style='font-size: 14px; color: #888; text-align: center; margin-top: 0px;'>
                © 2025 <a href="https://github.com/aprillnorthcutt" target="_blank" style="color: #888; text-decoration: none;">April Northcutt</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

render_sidebar_modules()

# ─────────────────────────────────────────────────────────────
# Load selected module (YAML)
# ─────────────────────────────────────────────────────────────
selected_id = st.session_state.selected_module_id
selected_label = st.session_state.selected_module_label
module_data = load_module(selected_id)

sample_note = module_data.get("sample_note", "").strip()
note_height = int(module_data.get("preferred_height", 175))

# Track module change (do NOT auto-inject sample text)
if st.session_state.last_module_id != selected_id:
    st.session_state.audit_result = None
    st.session_state.last_module_id = selected_id

# ─────────────────────────────────────────────────────────────
# Module header / context
# ─────────────────────────────────────────────────────────────
st.subheader(module_data.get("title", ""))
st.markdown(f"**🎯 Objective:** {module_data.get('objective','')}")
st.markdown(f"**📚 Audit Context:** {module_data.get('audit_context','')}")

# ─────────────────────────────────────────────────────────────
# Controls (before textarea so state changes are safe)
# ─────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    run = st.button("Review with GPT-4o", type="primary", use_container_width=True, key="audit_run")
with col2:
    if st.button("Try Demo", use_container_width=True, key="audit_demo"):
        st.session_state.audit_user_text = sample_note or (
            "The Organization received various donated services during the year, "
            "which may or may not be recognized in the financial statements."
        )
        st.session_state.audit_result = None
        st.rerun()
with col3:
    if st.button("Reset", use_container_width=True, key="audit_reset"):
        st.session_state.audit_user_text = ""
        st.session_state.audit_result = None
        st.rerun()

# ─────────────────────────────────────────────────────────────
# Main input (bind only by key; no value= to avoid conflicts)
# ─────────────────────────────────────────────────────────────
user_text = st.text_area(
    "Paste audit note here",
    height=note_height,
    key="audit_user_text"
)

# ─────────────────────────────────────────────────────────────
# Call model (stores output in session_state.audit_result)
# ─────────────────────────────────────────────────────────────
if run and user_text.strip():
    messages = build_prompt(module_data, user_text)
    try:
        with st.spinner("Reviewing…"):
            response = client.chat.completions.create(
                model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
                messages=messages
            )
        st.session_state.audit_result = response.choices[0].message.content
        st.toast("Review complete.")
    except Exception as e:
        st.error(f"❌ Error calling Azure OpenAI: {e}")

# ─────────────────────────────────────────────────────────────
# Render persisted output (doesn't vanish on reruns)
# ─────────────────────────────────────────────────────────────
if st.session_state.audit_result:
    with st.container():
        st.markdown("### 🤖 GPT-4o Output")
        st.write(st.session_state.audit_result)
