import streamlit as st

from firebase.Firebase import Firebase
from model.UserModel import UserModel
from utils.Secrates import json_data
from utils.Utils import create_or_update_session, States, reset_to_none

if create_or_update_session(States.User.value) is None:
    st.set_page_config(page_title='Research Hub', page_icon='📚', layout='centered')
else:
    st.set_page_config(page_title='Research Hub', page_icon='🔒', layout='wide')

database: Firebase = create_or_update_session(
    States.Database.value,
    init_value=Firebase(json_data)
)
mainContainer = st.container()
sidebar = st.sidebar

if create_or_update_session(States.User.value) is None:
    with mainContainer:
        reset_to_none(States.User.value)
        st.header('Welcome to Research Hub')
        st.subheader('Please login to continue')
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        if st.button('Login', use_container_width=True, type='primary'):
            if email == '' or password == '':
                st.error('Email or Password cannot be empty')
                st.stop()
            try:
                create_or_update_session(States.User.value, updated_value=database.log_in(email, password))
                st.rerun()
            except Exception as e:
                mainContainer.warning(f'An unexpected error occurred: {str(e)}')
else:
    userModel: UserModel = create_or_update_session(States.User.value)
    with mainContainer:
        st.balloons()
        st.title('Research Hub')
        st.write(f'Welcome {userModel.name}')
        with sidebar:
            with st.expander(label='User', expanded=True):
                st.image(userModel.photoUrl, width=150)
                st.title('Research Hub')
                st.write(f'Welcome {userModel.name}')
                st.write(f'Email: {userModel.email}')
                if st.button('Logout', use_container_width=True, type='primary'):
                    reset_to_none(States.User.value)
                    st.rerun()
