from enum import Enum

import streamlit as st
import json


class States(Enum):
    Screen = 'Screen'
    Database = 'Database'
    User = 'User'
    CREATE_RESEARCH = 'Create Research'
    UPDATE_RESEARCH = 'Update Research'
    QUESTION_LIST = 'Question List'
    VIEW_APPLICATION_ITEM_PATH = 'View Application Item Path'


def create_or_update_session(key, init_value=None, updated_value=None):
    """Function to create or update a session state.

    Args:
        key (any): _description_
        init_value (any, optional): Initial value. Defaults to None.
        updated_value (any, optional): Updated value. Defaults to None.

    Returns:
        any: Value of the session state
    """
    if key not in st.session_state and init_value is not None:
        st.session_state[key] = init_value
    elif key in st.session_state and updated_value is not None:
        st.session_state[key] = updated_value

    return st.session_state[key] if key in st.session_state else None


def remove_key_from_session_state(key):
    """Function to remove a key from session state.
    """
    if key in st.session_state:
        del st.session_state[key]


def reset_to_none(key):
    """Function to reset a session state to None.

    Args:
        key (any): _description_
    """
    if key in st.session_state:
        st.session_state[key] = None


def list_to_json(lst):
    try:
        return json.dumps(lst)
    except json.JSONDecodeError:
        return ''


def json_to_list(json_str) -> list[str]:
    if json_str == '':
        return []
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return []


def check_item_is_present(lst: list[str], item: str):
    item = item.lower()
    for i in lst:
        if i.lower() == item:
            return True
    return False
