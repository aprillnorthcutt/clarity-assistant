# app.py
import streamlit as st

# --- Page config ---
st.set_page_config(
    page_title="Clarity Assistant",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Hide default Streamlit sidebar nav ---
st.markdown(
    """
    <style>
        /* Hide the sidebar navigation and default "app" label */
        [data-testid="stSidebarNav"], 
        [data-testid="stSidebar"] header {
            display: none !important;
        }
        /* Optional: shrink sidebar width to 0 */
        section[data-testid="stSidebar"] {
            width: 0 !important;
            min-width: 0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <style>
      section[data-testid="stSidebarNav"] { display: none; }
      .card {
        background-color: #1e1e1e;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 0 10px rgba(0,0,0,0.2);
        margin-bottom: 2rem;
        color: #ffffff;
        transition: 0.3s;
      }
      .card:hover {
        box-shadow: 0 0 15px rgba(255,255,255,0.15);
      }
      .card a {
        color: #ffffff;
        font-weight: bold;
        text-decoration: none;
        font-size: 1.2rem;
      }
      .tagline {
        font-size: 1.1rem;
        color: #aaa;
        margin-top: -0.5rem;
        margin-bottom: 2rem;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Title and intro ---
st.title("🧾 Clarity Assistant")
st.markdown('<div class="tagline">Nonprofit Audit and Financial Clarity Tools</div>', unsafe_allow_html=True)

# --- Card layout for tool links ---
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="card">
            <a href="/Audit_Clarity_Assistant">🧠 Nonprofit Audit Clarity Assistant</a>
            <p class="tagline">Review nonprofit audit notes for GAAP clarity using prompt modules.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="card">
            <a href="/Financial_Clarity_Assistant">💰 Financial Clarity Assistant</a>
            <p class="tagline">Generate clear, actionable savings or debt payoff plans.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<small>💡 Use the in-page sidebars to switch modules (audit) or enter context (finance).</small>",
    unsafe_allow_html=True,
)
