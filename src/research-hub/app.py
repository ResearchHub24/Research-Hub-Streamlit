import datetime as dt
from typing import List

import streamlit as st

from Repository.FirebaseRepository import FirebaseRepository
from model.ResearchModel import TagModel, ResearchModel, ApplicationModel
from model.UserModel import UserModel
from utils.Utils import create_or_update_session, States, reset_to_none, json_to_list, check_item_is_present, \
    list_to_json, remove_key_from_session_state

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
create_or_update_session(
    States.UPDATE_RESEARCH,
    init_value=False
)
create_or_update_session(
    States.VIEW_APPLICATION_ITEM_PATH,
    init_value=''
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


def research_model(model_class: ResearchModel):
    with st.container(border=True):
        st.header(model_class.title)
        if len(model_class.description) > 500:
            st.write(model_class.description[:500] + '...')
        else:
            st.write(model_class.description)
        if len(model_class.tagsToList) != 0:
            all_tags = 'Tag : '
            for tag in model_class.tagsToList:
                all_tags += f'{tag.name}, '
            st.write(all_tags[:-2])
        with st.expander('More Info'):
            date, deadline = st.columns(2)
            with date:
                st.write(f'Created on: {model_class.formattedTime}')
            with deadline:
                st.write(f'Deadline: {model_class.formattedDeadline}')
        if st.button('View Applications', type='primary', use_container_width=True,
                     key=str(model_class.created) + model_class.title + 'applications'):
            create_or_update_session(States.VIEW_APPLICATION_ITEM_PATH, updated_value=model_class.key)
            st.rerun()
        edit_tag, delete_tab = st.columns(2)
        with edit_tag:
            if st.button('Edit', type='primary', use_container_width=True,
                         key=str(model_class.created) + model_class.title + 'edit'):
                create_or_update_session(States.CREATE_RESEARCH, updated_value=True)
                create_or_update_session(States.UPDATE_RESEARCH, updated_value=model_class)
                st.rerun()
        with delete_tab:
            with st.popover('Delete', use_container_width=True):
                if st.button('Are you sure you want to delete this research',
                             key=str(model_class.created) + model_class.title + 'delete-confirm'):
                    database.delete_research(model_class.key)
                    st.rerun()


def home_screen():
    if st.button('Create New Research Application Form', type='primary'):
        create_or_update_session(States.CREATE_RESEARCH, updated_value=True)
        st.rerun()
    all_research = database.get_research()
    if len(all_research) != 0:
        st.header('My Research')
        for research in all_research:
            research_model(research)


title = None
description = None
model = None


def create_application_screen():
    global title, description, model
    with st.container(border=True):
        is_edit = create_or_update_session(States.UPDATE_RESEARCH) and \
                  create_or_update_session(States.UPDATE_RESEARCH) is not None
        dead_line_time_stamp = None
        st.header('Create New Research Application Form')
        title = st.text_input('Title',
                              value=create_or_update_session(States.UPDATE_RESEARCH).title if is_edit else None)
        description = st.text_area('Description',
                                   value=create_or_update_session(
                                       States.UPDATE_RESEARCH).description if is_edit else None)
        if st.checkbox('Add Deadline', key='add_deadline'):
            dead_line = st.date_input('Deadline')
            dead_line_time_stamp = int(
                dt.datetime.combine(dead_line, dt.datetime.min.time()).timestamp() * 1000)
        st.write('Note: Leave the deadline empty if there is no deadline')
        if is_edit:
            selected_tag: List[TagModel] = create_or_update_session(States.UPDATE_RESEARCH).tagsToList
    with st.expander('Tags', expanded=create_or_update_session(States.UPDATE_RESEARCH) is not None):
        tags = database.get_tags()
        if len(tags) != 0:
            checkbox_states = {tag.name: st.checkbox(tag.name, key=tag.name,
                                                     value=tag in selected_tag if is_edit else False) for tag
                               in tags}
        get_selected_tags = [tag for tag in tags if checkbox_states[tag.name]]
        with st.popover('Create New Tag', use_container_width=True):
            name = st.text_input("Tag name", key='tag_name')
        if st.button('Done', type='primary', key='done'):
            try:
                database.add_tag(
                    TagModel(
                        name=name,
                    )
                )
                st.success('Tag created successfully')
                st.rerun()
            except Exception as e:
                st.error(f'An unexpected error occurred: {str(e)}')
    with st.expander('Questions', expanded=create_or_update_session(States.UPDATE_RESEARCH) is not None):
        question_list: list[str] = create_or_update_session(States.QUESTION_LIST, init_value=json_to_list(
            create_or_update_session(States.UPDATE_RESEARCH).questions) if is_edit else []
                                                            )
        # if is_edit:
        #     create_or_update_session(
        #         States.QUESTION_LIST,
        #         updated_value=json_to_list(create_or_update_session(States.UPDATE_RESEARCH).questions)
        #     )
        #     question_list = create_or_update_session(States.QUESTION_LIST)

        question = st.text_area('Question')
        for q in question_list:
            write, delete = st.columns([4, 1])
            with write:
                st.write(q)
            with delete:
                if st.button('Delete', key=q):
                    question_list.remove(q)
                    if is_edit:
                        create_or_update_session(
                            States.QUESTION_LIST,
                            updated_value=question_list
                        )
                    st.rerun()
        if st.button('Add Question', type='primary'):
            if question == '':
                st.error('Question cannot be empty')
                st.stop()
            if check_item_is_present(question_list, question):
                st.error('Question already exists')
                st.stop()
            question_list.append(question)
            create_or_update_session(States.QUESTION_LIST, updated_value=question_list)
            st.rerun()
    col1, col2 = st.columns(2)
    with col2:
        if st.button('Back', type='primary', use_container_width=True):
            create_or_update_session(States.CREATE_RESEARCH, updated_value=False)
            create_or_update_session(States.QUESTION_LIST, updated_value=[])
            reset_to_none(States.UPDATE_RESEARCH)
            remove_key_from_session_state(States.QUESTION_LIST)
            st.rerun()
    with col1:
        if st.button('Submit', type='primary', use_container_width=True):
            if title == '':
                st.error('Title cannot be empty')
                st.stop()
            if description == '':
                st.error('Description cannot be empty')
                st.stop()
            if len(get_selected_tags) == 0:
                st.error('Please select at least one tag')
                st.stop()
            if len(question_list) == 0:
                st.error('Please add at least one question')
                st.stop()
            try:
                model = ResearchModel(
                    title=title,
                    description=description,
                    created_by=userModel.name,
                    created_by_UID=userModel.uid,
                    tags=str([tag.__dict__ for tag in get_selected_tags]),
                    dead_line=dead_line_time_stamp if dead_line_time_stamp else None,
                    key=create_or_update_session(States.UPDATE_RESEARCH).key if is_edit else None,
                    questions=list_to_json(question_list)
                )
                if is_edit:
                    database.update_research(model)
                else:
                    database.add_new_research(
                        research=model
                    )
                create_or_update_session(States.CREATE_RESEARCH, updated_value=False)
                reset_to_none(States.UPDATE_RESEARCH)
                create_or_update_session(States.QUESTION_LIST, updated_value=[])
                remove_key_from_session_state(States.QUESTION_LIST)
                st.rerun()
            except Exception as e:
                st.error(f'An unexpected error occurred: {str(e)}')


def application_item(item: ApplicationModel):
    with st.container(border=True):
        st.header(f'Application by {item.studentName}')
        st.write(f'Email: {item.studentEmail}')
        st.write(f'Phone Number: {item.studentPhoneNumber}')
        st.write(f'Filled on: {dt.datetime.fromtimestamp(item.filledDate / 1000).strftime("%d %b %Y")}')
        answers = item.convert_answer_json_to_question_model
        with st.expander('Answers', expanded=True):
            for answer in answers:
                with st.container(border=True):
                    st.write(f'Q: {answer.question}')
                    st.write(f'A: {answer.answer}')


if create_or_update_session(States.User.value) is None:
    log_in_screen()
else:
    with (mainContainer):
        userModel: UserModel = create_or_update_session(States.User.value)
        # st.balloons()
        st.title('Research Hub')
        st.write(f'Welcome {userModel.name}')
        side_bar()
        if not create_or_update_session(States.CREATE_RESEARCH) and create_or_update_session(
                States.VIEW_APPLICATION_ITEM_PATH) == '':
            home_screen()
        elif create_or_update_session(States.VIEW_APPLICATION_ITEM_PATH) != '':
            st.header('Filled Applications')
            all_application = database.get_application(create_or_update_session(States.VIEW_APPLICATION_ITEM_PATH))
            if len(all_application) == 0:
                st.write('No applications found')
            else:
                for app in all_application:
                    application_item(app)
            if st.button('Back', use_container_width=False):
                create_or_update_session(States.VIEW_APPLICATION_ITEM_PATH, updated_value='')
                st.rerun()
        else:
            create_application_screen()
