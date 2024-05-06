import datetime as dt

import streamlit as st

from Repository.FirebaseRepository import FirebaseRepository
from model.ResearchModel import TagModel
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
create_or_update_session(
    States.CREATE_RESEARCH,
    init_value=False
)
mainContainer = st.container()
sidebar = st.sidebar


def log_in_screen():
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


def side_bar():
    with sidebar:
        with st.expander(label='User', expanded=True):
            st.image(userModel.photoUrl, width=150)
            st.title('Research Hub')
            st.write(f'Welcome {userModel.name}')
            st.write(f'Email: {userModel.email}')
            if st.button('Logout', use_container_width=True, type='primary'):
                reset_to_none(States.User.value)
                st.rerun()


if create_or_update_session(States.User.value) is None:
    log_in_screen()
else:
    with mainContainer:
        userModel: UserModel = create_or_update_session(States.User.value)
        # st.balloons()
        st.title('Research Hub')
        st.write(f'Welcome {userModel.name}')
        side_bar()
        if not create_or_update_session(States.CREATE_RESEARCH):
            if st.button('Create New Research Application Form', type='primary'):
                create_or_update_session(States.CREATE_RESEARCH, updated_value=True)
                st.rerun()
        else:
            with st.container(border=True):
                st.header('Create New Research Application Form')
                title = st.text_input('Title')
                description = st.text_area('Description')
                if st.checkbox('Add Deadline'):
                    dead_line = st.date_input('Deadline')
                    dead_line_time_stamp = int(
                        dt.datetime.combine(dead_line, dt.datetime.min.time()).timestamp() * 1000)
                st.write('Note: Leave the deadline empty if there is no deadline')
                tags = database.get_tags()
                if len(tags) != 0:
                    st.write('Tags')
                    checkbox_states = {tag.name: st.checkbox(tag.name, key=tag.name) for tag in tags}
                    getSelectedTags = [tag for tag in tags if checkbox_states[tag.name]]
                st.write('Create New Tag')
                new_tag = st.text_input('Tag Name')
                if st.button('Done', type='primary', key='done'):
                    try:
                        database.add_tag(
                            TagModel(
                                name=new_tag,
                            )
                        )
                        st.success('Tag created successfully')
                        st.rerun()
                    except Exception as e:
                        st.error(f'An unexpected error occurred: {str(e)}')

            col1, col2 = st.columns(2)
            with col1:
                if st.button('Submit', type='primary', use_container_width=True):
                    if title == '' or description == '' or len(getSelectedTags) == 0:
                        st.error('Title, Description, and Tags cannot be empty')
                        st.stop()
                    try:
                        st.write(getSelectedTags)
                        st.success('Research Application Form created successfully')
                        # create_or_update_session(States.CREATE_RESEARCH, updated_value=False)
                        # st.rerun()
                    except Exception as e:
                        st.error(f'An unexpected error occurred: {str(e)}')
            with col2:
                if st.button('Back', type='primary', use_container_width=True):
                    create_or_update_session(States.CREATE_RESEARCH, updated_value=False)
                    st.rerun()
