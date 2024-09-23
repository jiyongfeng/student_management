#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-12 09:50:27
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-09-05 20:27:25
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
from datetime import datetime

import pandas as pd
import pymysql
import streamlit as st

from utils.database import (execute_sql, get_connection, handle_database_error,
                            handle_general_error)
from utils.logger import logger


def load_courses():
    """加载课程

    Returns:
        tuple: 课程信息
    """
    connection = get_connection()
    if connection:
        try:
            sql = """
                SELECT cou_id, course_name, sort, create_by,updated_by,create_at,updated_at
                FROM tb_course
                ORDER BY sort ASC
            """
            course_data = execute_sql(connection, sql)
            return course_data
        finally:
            connection.close()


def insert_course(course: dict):
    """插入课程
    Args:
        course (dict): 课程信息
    """
    connection = get_connection()
    if connection:
        try:
            sql = "INSERT INTO tb_course (course_name, sort, create_by,updated_by,create_at,updated_at) VALUES (%s, %s, %s,%s,%s, %s)"
            execute_sql(connection, sql, (
                course['course_name'],
                course['sort'],
                st.session_state.user_name,
                st.session_state.user_name,
                datetime.now(),
                datetime.now()
            ), commit=True)
            logger.info("新增课程 %s 成功", course['course_name'])
        finally:
            connection.close()


def update_course(course: dict):
    """更新课程

    Args:
        course (dict): 课程字典
    """
    connection = get_connection()
    if connection:
        try:
            sql = "UPDATE tb_course SET course_name = %s, sort=%s, create_by = %s, updated_by = %s, updated_at = %s WHERE cou_id = %s "
            execute_sql(connection, sql, (
                course['course_name'],
                course['sort'],
                course['create_by'],
                st.session_state.user_name,
                datetime.now(),
                course['cou_id']
            ), commit=True)
            logger.info("更新课程 %s 成功", course['course_name'])
        finally:
            connection.close()


def delete_course(course: dict):
    """删除课程

    Args:
        course (dict): 课程信息
    """
    connection = get_connection()
    if connection:
        try:
            sql = "DELETE FROM tb_course WHERE cou_id = %s"
            execute_sql(connection, sql, (course['cou_id'],), commit=True)
            logger.info("删除课程 [%s] 成功", course['course_name'])
        finally:
            connection.close()


def process_course_actions(df_courses, edited_df):
    """
    处理新增、更新和删除课程的逻辑，使用事务处理
    """
    connection = get_connection()
    if connection:
        try:
            # 开始事务
            connection.begin()

            new_rows = edited_df[~edited_df["cou_id"].isin(
                df_courses['cou_id'])]

            update_rows = edited_df[edited_df["cou_id"].isin(
                df_courses['cou_id'])].copy()
            # 判断更新的行
            update_rows = update_rows[update_rows.apply(
                lambda x: x['course_name'] != df_courses.loc[df_courses['cou_id'] == x['cou_id'], 'course_name'].values[0] or x['sort'] != df_courses.loc[df_courses['cou_id'] == x['cou_id'], 'sort'].values[0], axis=1)]

            delete_rows = df_courses[~df_courses['cou_id'].isin(
                edited_df['cou_id'])]

            for index, row in new_rows.iterrows():
                insert_course(row.to_dict())

            for index, row in update_rows.iterrows():
                update_course(row.to_dict())

            for index, row in delete_rows.iterrows():
                delete_course(row.to_dict())

            # 如果所有操作都成功，则提交事务
            connection.commit()
            logger.info("事务提交成功")
            st.success("课程操作成功")

        except pymysql.MySQLError as db_error:
            connection.rollback()
            handle_database_error(db_error)
        except Exception as general_error:
            connection.rollback()
            handle_general_error(general_error)
        finally:
            connection.close()


st.subheader("课程管理")
courses = load_courses()
df_courses = pd.DataFrame(courses)
edited_df = st.data_editor(
    df_courses,
    column_order=["course_name", 'sort', "create_by",
                  'create_at', "updated_by", 'updated_at'],
    use_container_width=True,
    hide_index=True,
    column_config={
        'course_name': "课程名称",
        'sort': st.column_config.NumberColumn(
            "排序",
            min_value=1,
            max_value=100,
            step=1,
            format="%d",
            help="排序"
        ),
        'create_by': "创建人",
        'create_at': "创建时间",
        'updated_by': "更新人",
        'updated_at': "更新时间"
    },
    num_rows="dynamic",
    disabled=["create_by", 'create_at', "updated_by", 'updated_at']
)

if st.button("提交"):
    if not df_courses.equals(edited_df):
        process_course_actions(df_courses, edited_df)
    else:
        st.warning("没有更改")
