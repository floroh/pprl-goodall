import pathlib

import streamlit as st


# Via https://github.com/Sven-Bo/streamit-css-styling-demo
def load_css(file_path, is_relative_to_ui_base: bool = True):
    if is_relative_to_ui_base:
        base_path = pathlib.Path(__file__).parent.resolve()
        file_path = base_path / file_path
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def del_state_if_exists(state_name):
    if state_name in st.session_state:
        del st.session_state[state_name]


def state_exists_and_is_in(state_name, others: list):
    for other in others:
        ret = state_exists_and_equals(state_name, other)
        if ret:
            return True
    return False

def state_exists_and_equals(state_name, other):
    if state_name in st.session_state:
        if st.session_state[state_name] == other:
            return True
    return False


def get_state_or_default(state_name, default):
    if state_name in st.session_state:
        return st.session_state[state_name]
    else:
        return default

def god(value, default, to_replace = None):
    if to_replace is None:
        if value is None:
            return default
    elif value == to_replace:
            return default
    return value