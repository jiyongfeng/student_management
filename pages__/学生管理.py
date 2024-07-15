#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-12 09:50:27
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-12 10:01:15
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import logging

import matplotlib.pyplot as plt
import pandas as pd
import pymysql
import seaborn as sns
import streamlit as st

from utils.database import get_connection

# 设置Seaborn样式
sns.set_theme(style="whitegrid")

# 配置日志记录
logging.basicConfig(level=logging.DEBUG)


# 学生管理


def add_student():
    st.subheader("增加学生")
    student_name = st.text_input("学生姓名")
    create_by = st.text_input("创建者")
    if st.button("提交"):
        connection = get_connection(CONFIG_FILE)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO tb_student (student_name, create_by) VALUES (%s, %s)"
                cursor.execute(sql, (student_name, create_by))
            connection.commit()
            st.success("学生添加成功")
        finally:
            connection.close()


def view_students():
    st.subheader("显示学生")
    connection = get_connection(CONFIG_FILE)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_student"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                st.dataframe(result)
            else:
                st.warning("没有学生")
    finally:
        connection.close()


def edit_student():
    st.subheader("编辑学生")
    connection = get_connection(CONFIG_FILE)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_student"
            cursor.execute(sql)
            students = cursor.fetchall()
        student_dict = {student['student_name']
            : student['stu_id'] for student in students}
        selected_student = st.selectbox("选择学生", list(student_dict.keys()))
        new_name = st.text_input("新姓名")
        updated_by = st.text_input("更新者")
        if st.button("提交"):
            with connection.cursor() as cursor:
                sql = "UPDATE tb_student SET student_name=%s, updated_by=%s WHERE stu_id=%s"
                cursor.execute(sql, (new_name, updated_by,
                               student_dict[selected_student]))
            connection.commit()
            st.success("学生更新成功")
    finally:
        connection.close()


def main():
    st.title("学生管理")

    sub_menu_option = st.sidebar.radio(
        "请选择操作",
        ["增加学生", "显示学生", "编辑学生"]
    )
    if sub_menu_option == "增加学生":
        add_student()
    elif sub_menu_option == "显示学生":
        view_students()
    elif sub_menu_option == "编辑学生":
        edit_student()


if __name__ == "__main__":
    CONFIG_FILE = "config.ini"
    main()
