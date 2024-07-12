#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-12 09:50:27
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-12 23:38:09
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import logging
from datetime import datetime

import pandas as pd
import pymysql
import seaborn as sns
import streamlit as st

from utils.database import get_connection

CONFIG_FILE = "config.ini"

# 设置Seaborn样式
sns.set_theme(style="whitegrid")

# 配置日志记录
logging.basicConfig(level=logging.ERROR)

connection = get_connection(CONFIG_FILE)
c = connection.cursor()

st.title("课程管理")


def handle_database_error(error):
    # 对用户隐藏具体的错误细节，只显示一般性错误消息
    show_error_message("数据库操作失败。")
    # 在日志中记录详细的错误信息，以便于问题的追踪和定位
    log_error("数据库操作失败：", error)


def handle_general_error(error):
    # 对于非预期的异常，同样隐藏具体的错误细节
    show_error_message("发生未知错误。")
    # 在日志中记录详细的错误信息
    log_error("发生未知错误：", error)


def show_error_message(message):
    # 假设st.error是一个UI组件的方法，用于显示错误消息
    st.error(message)
    # 可以考虑将错误消息也记录到日志中，但避免敏感信息泄露
    logging.error("向用户显示错误：%s", message)


def log_error(prefix, error):
    # 记录错误日志，包括错误前缀和错误详细信息
    logging.error("%s %s", prefix, str(error))


# 上下文管理器类，用于处理数据库连接的打开和关闭
class MySQLConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.c = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


def load_courses():
    connection = get_connection(CONFIG_FILE)
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM tb_course"
                cursor.execute(sql)
                courses = pd.DataFrame(cursor.fetchall())
                return courses
        except pymysql.MySQLError as db_error:
            handle_database_error(db_error)
        except Exception as general_error:
            handle_general_error(general_error)


def insert_course(course):
    if connection:
        try:
            sql = "INSERT INTO tb_course (course_name, create_by,updated_by,create_at,updated_at) VALUES (%s, %s, %s,%s,%s)"
            c.execute(sql, (course['course_name'],
                      course['create_by'], course['updated_by'], datetime.now(), datetime.now()))
            connection.commit()
        except pymysql.MySQLError as db_error:
            handle_database_error(db_error)
        except Exception as general_error:
            handle_general_error(general_error)


def update_coures(course):
    if connection:
        try:
            sql = "UPDATE tb_course SET course_name = %s, create_by = %s, updated_by = %s, updated_at = %s WHERE cou_id = %s"
            c.execute(
                sql, (course['course_name'], course['create_by'], course['updated_by'], datetime.now(), course['cou_id']))
            connection.commit()
        except pymysql.MySQLError as db_error:
            handle_database_error(db_error)
        except Exception as general_error:
            handle_general_error(general_error)


def delete_course(delete_cou_id):
    if connection:
        try:
            sql = "DELETE FROM tb_course WHERE cou_id = %s"
            c.execute(sql, (delete_cou_id))
            connection.commit()
        except pymysql.MySQLError as db_error:
            handle_database_error(db_error)
        except Exception as general_error:
            handle_general_error(general_error)


df_courses = load_courses()

display_df = df_courses.drop(columns=['create_at', 'updated_at'])
edited_df = st.data_editor(df_courses, column_order=[
                           "course_name", "create_by", 'create_at', "updated_by", 'updated_at'], hide_index=True, num_rows="dynamic")

if st.button("提交"):

    if not display_df.equals(edited_df):
        new_rows = edited_df[~edited_df["cou_id"].isin(df_courses['cou_id'])]

        update_rows = edited_df[edited_df["cou_id"].isin(df_courses['cou_id'])]
        for index, row in update_rows.iterrows():
            original_row = df_courses[df_courses['cou_id']
                                      == row['cou_id']].iloc[0]
            if not row.equals(original_row.drop(columns=['created_at', 'updated_at'])):
                update_coures(row)
                st.success("更新成功")

        delete_rows = df_courses[~df_courses['cou_id'].isin(
            edited_df['cou_id'])]

        for index, row in new_rows.iterrows():
            insert_course(row)
            st.success("新增成功")

        for index, row in delete_rows.iterrows():
            delete_course(row['cou_id'])
            st.success("删除成功")

    else:
        st.warning("没有更改")
