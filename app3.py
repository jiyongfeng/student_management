#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-26 11:28:47
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-26 11:28:56
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import streamlit as st
import utils.auth as auth

# 注册功能


def register():
    st.header("注册")
    username = st.text_input("用户名")
    email = st.text_input("邮箱")
    password = st.text_input("密码", type="password")
    if st.button("注册"):
        auth.add_user(username, email, password)
        st.success("注册成功！")

# 登录功能


def login():
    st.header("登录")
    username_or_email = st.text_input("用户名或邮箱")
    password = st.text_input("密码", type="password")
    if st.button("登录"):
        if auth.authenticate_user(username_or_email, password):
            st.success("登录成功！")
        else:
            st.error("用户名或密码错误")

# 修改密码功能


def change_password():
    st.header("修改密码")
    username_or_email = st.text_input("用户名或邮箱")
    new_password = st.text_input("新密码", type="password")
    if st.button("修改密码"):
        auth.change_password(username_or_email, new_password)
        st.success("密码修改成功！")

# 主函数


def main():
    st.sidebar.title("导航")
    choice = st.sidebar.radio("选择功能", ["注册", "登录", "修改密码"])

    if choice == "注册":
        register()
    elif choice == "登录":
        login()
    elif choice == "修改密码":
        change_password()


if __name__ == "__main__":
    main()
