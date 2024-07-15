#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-14 15:52:17
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-14 17:00:05
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import streamlit as st

# 定义会话状态以存储用户名和页面状态
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'page' not in st.session_state:
    st.session_state['page'] = 'main_page'
if 'logout_confirm' not in st.session_state:
    st.session_state['logout_confirm'] = False

st.write(st.secrets['database']['user'])
st.write(st.secrets["OpenAI_key"])
# 定义主页


placeholder = st.empty()

# Replace the placeholder with some text:
placeholder.text("Hello")

# Replace the text with a chart:
placeholder.line_chart({"data": [1, 5, 2, 6]})

with st.popover("Open popover"):
    st.markdown("Hello World 👋")
    name = st.text_input("What's your name?")

st.write("Your name:", name)


@st.experimental_dialog("Cast your vote")
def vote(item):
    st.write(f"Why is {item} your favorite?")
    reason = st.text_input("Because...")
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()


if "vote" not in st.session_state:
    st.write("Vote for your favorite")
    if st.button("A"):
        vote("A")
    if st.button("B"):
        vote("B")
else:
    f"You voted for {st.session_state.vote['item']} because {
        st.session_state.vote['reason']}"


def main_page():
    st.title("Main Page")

    st.write("Please enter your username to continue:")
    username = st.text_input("Username", value=st.session_state['username'])

    if username:
        st.session_state['username'] = username
        st.write(f"Hello, {username}!")
        st.rerun()

    if st.button("Go to Other Page"):
        st.session_state['page'] = 'other_page'
        st.query_params["page"] = 'other_page'
        st.rerun()

    if st.button("Logout"):
        st.session_state['logout_confirm'] = True

# 定义其他页面


def other_page():
    st.title("Other Page")

    if 'username' in st.session_state and st.session_state['username']:
        st.write(f"This page was updated by: {st.session_state['username']}")
    else:
        st.write("No username provided.")
    if st.button("Go Back to Main Page"):
        st.session_state['page'] = 'main_page'
        st.query_params["page"] = 'main_page'
        st.rerun()

    if st.button("Logout"):
        st.session_state['logout_confirm'] = True

# 定义注销确认对话框


def logout_confirm():
    st.write("Are you sure you want to logout?")
    if st.button("Yes, logout"):
        st.session_state['username'] = ''
        st.session_state['page'] = 'main_page'
        st.session_state['logout_confirm'] = False
        st.query_params["page"] = 'main_page'
        st.rerun()
    if st.button("No, go back"):
        st.session_state['logout_confirm'] = False


# 页面导航
if st.session_state['logout_confirm']:
    logout_confirm()
elif st.session_state['page'] == 'main_page':
    main_page()
else:
    other_page()
