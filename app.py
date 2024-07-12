#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-11 11:59:32
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-12 10:40:33
 * @Description  : 成绩分析器
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import streamlit as st
# Streamlit 应用的主函数


def main():
    st.title("学生管理系统")

    if st.button("Home"):
        st.switch_page("app.py")
    if st.button("成绩管理"):
        st.switch_page("pages/成绩管理.py")
    if st.button("考试管理"):
        st.switch_page("pages/考试管理.py")
    if st.button("课程管理"):
        st.switch_page("pages/课程管理.py")
    if st.button("学生管理"):
        st.switch_page("pages/学生管理.py")


if __name__ == "__main__":
    main()
