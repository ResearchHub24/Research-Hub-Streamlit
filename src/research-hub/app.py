import streamlit as st

from Repository.FirebaseRepository import FirebaseRepository
from model.UserModel import UserModel
from utils.Utils import create_or_update_session, States, reset_to_none

if create_or_update_session(States.User.value) is None:
    st.set_page_config(page_title='Research Hub', page_icon='📚', layout='centered')
else:
    st.set_page_config(page_title='Research Hub', page_icon='🔒', layout='wide')

database: FirebaseRepository = create_or_update_session(
    States.Database.value,
    init_value=FirebaseRepository()
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
                user = database.log_in(email, password)
                st.session_state[States.User.value] = user
                st.rerun()
            except Exception as e:
                mainContainer.warning(f'An unexpected error occurred: {str(e)}')
else:
    with mainContainer:
        userModel: UserModel = create_or_update_session(States.User.value)
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
