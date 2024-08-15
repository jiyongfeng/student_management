#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-13 10:14:11
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-08-15 11:06:18
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import streamlit as st

from utils.logger import logger
from utils import auth

# 定义会话状态、用户名、页面等全局变量
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = None
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = None
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = 'login_page'
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None


ROLES = [None, "Requester", "Responder", "Admin"]


@st.dialog("请确认是否退出系统?")
def logout_confim():
    """ 退出系统
    """
    st.write("请确认是否退出系统?")
    col2, col3 = st.columns([1, 1], gap="small")
    with col2:
        if st.button("退出"):
            logger.info("%s 退出系统", st.session_state.user_name)
            st.session_state.clear()
            st.rerun()
    with col3:
        if st.button("取消"):

            st.rerun()


def login():
    """用户登录
    """
    user_name = st.text_input("用户名", help="请输入用户名或邮箱", placeholder="请输入用户名或邮箱")
    password = st.text_input("密码", type="password",
                             help="请输入密码", placeholder="请输入密码")
    # role = st.selectbox("Choose your role", ROLES)

    if st.button("登录"):
        user_name = auth.authenticate_user(user_name, password)
        if user_name:
            st.session_state.logged_in = True
            st.session_state.user_name = user_name
            st.session_state.user_info = auth.get_user_info(user_name)
            st.session_state.user_email = auth.get_user_info(user_name)[
                'email']
            st.success("登录成功！")
            # 记录日志
            logger.info("%s 登录系统成功", f'{st.session_state.user_name}')
            st.rerun()
        else:
            st.error("用户名或密码错误！")
            logger.error("%s 登录系统失败", st.session_state.user_name)


def loginfo():
    """登录信息
    """
    st.header("欢迎来到学生成绩管理系统", divider="rainbow")
    col1, col2, col3 = st.columns(
        [22, 2, 2], vertical_alignment="center")
    with col1:
        st.write("")
    with col2:
        if st.button(f"{st.session_state.user_name}"):
            # 切换到用户设置页面
            pass

    with col3:
        if st.button("注销"):
            logout_confim()


# define pages
student_management = st.Page(
    'page/student_management.py', title='学生管理', icon=":material/person:")
course_management = st.Page(
    'page/course_management.py', title='课程管理', icon=":material/book:")
exam_management = st.Page(
    'page/exam_management.py', title='考试管理', icon=":material/dvr:")
score_management = st.Page(
    'page/score_management.py', title='成绩管理', icon=":material/dataset:")
user_settings = st.Page('page/user_settings.py',
                        title="用户设置", icon=":material/settings:", default=True)
login_page = st.Page(login, title="Log in", icon=":material/login:")

# define page groups
account_pages = [user_settings]
setting_pages = [student_management, course_management, exam_management]
respond_pages = [score_management]


st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

if st.session_state.logged_in:
    loginfo()
    pg = st.navigation(
        {
            "Account": account_pages,
            "配置": setting_pages,
            "成绩管理": respond_pages})
else:
    pg = st.navigation([login_page])
    st.session_state.page = "login_page"

pg.run()
