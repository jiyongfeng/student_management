#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-14 15:18:45
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-08-15 11:43:19
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""

import streamlit as st
import utils.auth as auth
from utils.logger import logger

st.subheader("用户设置")


# 两列列出用户名、用户姓名、邮箱
col1, col2 = st.columns([1, 10], gap="small")
with col1:
    st.write("用户名:")
    st.write("学生姓名:")
    st.write("邮箱:")
with col2:
    st.write(st.session_state.user_name)
    st.write(st.session_state.user_info['student_name'])
    st.write(st.session_state.user_info['email'])


st.subheader("修改邮箱", divider='gray')

new_email = st.text_input("请输入新邮箱")

if st.button("修改邮箱"):
    if auth.is_valid_email(new_email) is False:
        st.error("邮箱格式不正确，请重新输入。")
    elif new_email and new_email == st.session_state.user_email:
        st.error("新邮箱不能与原邮箱相同，请重新输入。")

    else:
        auth.update_user_info(st.session_state.user_name, email=new_email)
        st.session_state.user_email = new_email
        st.success("邮箱修改成功！")
        # 记录日志
        logger.info("%s 修改邮箱成功", st.session_state.user_name)


st.subheader("修改密码", divider='gray')

old_password = st.text_input("请输入原密码", type="password")
new_password = st.text_input("请输入新密码", type="password")
new_password_confirm = st.text_input("请再次输入新密码", type="password")

if st.button("修改密码"):
    if new_password != new_password_confirm:
        st.error("两次密码输入不一致,请重新输入。")

    elif not auth.authenticate_user(st.session_state.user_name, old_password):
        st.error("原密码不正确,请重新输入。")

    elif new_password == old_password:
        st.error("新密码不能与原密码相同，请重新输入。")
    else:
        auth.change_password(st.session_state.user_name, new_password)
        st.success("密码修改成功！")
        # 记录日志
        logger.info("%s 修改密码成功", st.session_state.user_name)
