#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-12 09:50:27
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-12 10:12:16
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


# 考试项目管理


def add_exam():
    st.subheader("增加考试项目")
    exam_name = st.text_input("考试项目名称")
    create_by = st.text_input("创建者")
    if st.button("提交"):
        connection = get_connection(CONFIG_FILE)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO tb_exam (exam_name, create_by) VALUES (%s, %s)"
                cursor.execute(sql, (exam_name, create_by))
            connection.commit()
            st.success("考试项目添加成功")
        finally:
            connection.close()


def view_exams():
    st.subheader("显示考试项目")
    connection = get_connection(CONFIG_FILE)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_exam"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                st.dataframe(result)
            else:
                st.warning("考试项目为空")
    finally:
        connection.close()


def edit_exam():
    st.subheader("编辑考试项目")
    connection = get_connection(CONFIG_FILE)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_exam"
            cursor.execute(sql)
            exams = cursor.fetchall()
        exam_dict = {exam['exam_name']: exam['exam_id'] for exam in exams}
        selected_exam = st.selectbox("选择考试项目", list(exam_dict.keys()))
        new_name = st.text_input("新名称")
        updated_by = st.text_input("更新者")
        if st.button("提交"):
            with connection.cursor() as cursor:
                sql = "UPDATE tb_exam SET exam_name=%s, updated_by=%s WHERE exam_id=%s"
                cursor.execute(sql, (new_name, updated_by,
                               exam_dict[selected_exam]))
            connection.commit()
            st.success("考试项目更新成功")
    finally:
        connection.close()


def main():
    st.title("考试管理")

    sub_menu_option = st.sidebar.radio(
        "请选择操作",
        ["增加考试", "显示考试", "编辑考试"]
    )
    if sub_menu_option == "增加考试":
        add_exam()
    elif sub_menu_option == "显示考试":
        view_exams()
    elif sub_menu_option == "编辑考试":
        edit_exam()


if __name__ == "__main__":
    CONFIG_FILE = "config.ini"
    main()
