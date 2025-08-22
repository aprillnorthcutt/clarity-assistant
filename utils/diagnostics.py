# utils/diagnostics.py
import streamlit as st

def show_prompts(system: str, developer: str, user_msg: str, dep: str, ver: str):
    """Dump quick diagnostic info into the Streamlit UI."""
    st.write("🔎 Types:", type(system), type(developer), type(user_msg))
    st.write("🔎 Deployment:", repr(dep))
    st.write("🔎 API version:", repr(ver))
    st.write("🧩 system[:60]:", repr(system[:60]))
    st.write("🧩 developer[:60]:", repr(developer[:60]))

def assert_valid(system: str, developer: str, user_msg: str):
    """Ensure values are strings and not dotted paths."""
    assert isinstance(system, str), f"system is not str: {type(system)}"
    assert isinstance(developer, str), f"developer is not str: {type(developer)}"
    assert isinstance(user_msg, str), f"user_msg is not str: {type(user_msg)}"

    bad = "prompts.finance.clarifier.system"
    if bad in system or bad in developer or bad in user_msg:
        st.error(f"❌ Found dotted path literal inside prompts/messages: '{bad}'")
        st.stop()
