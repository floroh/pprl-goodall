import pathlib

import streamlit as st
from streamlit import session_state as sts


# Workaround for errors with layout in multi-page app
def set_streamlit_page_config_once(page_title: str | None = None):
    try:
        if page_title is None:
            st.set_page_config(layout="wide")
        else:
            st.set_page_config(layout="wide", page_title=page_title)
    except st.errors.StreamlitAPIException as e:
        if "can only be called once per app" in e.__str__():
            return  # ignore this error
        raise e


# Via https://github.com/Sven-Bo/streamit-css-styling-demo
def load_css(file_path, is_relative_to_ui_base: bool = True):
    if is_relative_to_ui_base:
        base_path = pathlib.Path(__file__).parent.resolve()
        file_path = base_path / file_path
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def del_state_if_exists(state_name):
    if state_name in sts:
        del sts[state_name]


def state_exists_and_is_in(state_name, others: list):
    for other in others:
        ret = state_exists_and_equals(state_name, other)
        if ret:
            return True
    return False


def state_exists_and_equals(state_name, other):
    if state_name in sts:
        if sts[state_name] == other:
            return True
    return False


def get_state_or_default(state_name, default):
    if state_name in sts:
        return sts[state_name]
    else:
        return default


def god(value, default, to_replace=None):
    if to_replace is None:
        if value is None:
            return default
    elif value == to_replace:
        return default
    return value

# Dictionary to hold dynamically cached versions of functions
_cached_funcs = {}

def st_cache_wrapper(func, *args, **kwargs):
    """Caches any function call via Streamlit's st.cache_data."""
    # If we haven’t seen this function before, wrap and cache it
    if func not in _cached_funcs:
        # Dynamically create a cached version of the function
        @st.cache_data
        def cached_func(*a, **kw):
            return func(*a, **kw)
        _cached_funcs[func] = cached_func

    # Call the cached version
    return _cached_funcs[func](*args, **kwargs)

def clear_cache_for(func):
    """Clears Streamlit cache for a specific wrapped function."""
    cached_func = _cached_funcs.get(func)
    if cached_func:
        cached_func.clear()