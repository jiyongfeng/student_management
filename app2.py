#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-14 15:52:17
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-16 09:36:44
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import streamlit as st
import time


def page1():
    st.write(st.session_state.foo)


def page2():
    st.write(st.session_state.bar)


# Widgets shared by all the pages
st.sidebar.selectbox("Foo", ["A", "B", "C"], key="foo")
st.sidebar.checkbox("Bar", key="bar")
st.sidebar.button("Clear", key="clear")

for i in st.session_state.keys():
    st.write(i)

with st.spinner(text="Loading..."):
    for _ in range(10):
        time.sleep(0.5)
    st.write("World")

pg = st.navigation(
    [st.Page(page1, title='hello', icon=':material/login:'), st.Page(page2)])
pg.run()
