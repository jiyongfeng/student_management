#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-14 15:18:45
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-08-13 16:03:51
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""

import streamlit as st
import utils.auth as auth
from utils.logger import logger

st.subheader("用户设置")

st.write(f"You are logged in as {st.session_state.user_name}.")

st.subheader("修改密码")

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
