#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-12 09:50:27
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-18 14:59:53
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

st.subheader("考试管理")


@st.cache_data
def load_exams():
    """加载考试项目

    Returns:
        tuple: 考试项目信息
    """
    connection = get_connection()
    try:
        sql = "SELECT * FROM tb_exam"
        exams = execute_sql(connection, sql)
        return exams
    finally:
        connection.close()


def insert_exam(exam: dict):
    """
    插入考试信息到数据库。

    :param exam: 包含考试信息的字典，键值对为考试名和考试日期。
    """

    # 获取数据库连接
    connection = get_connection()

    # 检查数据库连接是否成功
    if connection:
        try:
            # 使用with语句确保数据库游标正确关闭
            sql = "INSERT INTO tb_exam (exam_name, exam_date,create_by,updated_by,create_at,updated_at) VALUES (%s, %s, %s, %s,%s,%s)"
            # 执行SQL语句，插入考试信息
            execute_sql(connection, sql, (
                exam['exam_name'],
                exam['exam_date'],
                st.session_state.username,
                st.session_state.username,
                datetime.now(),
                datetime.now()
            ), commit=True)
            # 提交事务，确保数据插入数据库
            logger.info("add %s exam success", exam['exam_name'])
        finally:
            # 关闭数据库连接
            connection.close()


def update_exam(exam: dict):
    """update exams

    Args:
        exam (dict): exam info
    """
    connection = get_connection()
    try:
        sql = "UPDATE tb_exam SET exam_name=%s, exam_date=%s, create_by = %s, updated_by = %s, updated_at = %s WHERE exam_id = %s"
        execute_sql(connection, sql, (
            exam['exam_name'],
            exam['exam_date'],
            exam['create_by'],
            st.session_state.username,
            datetime.now(),
            exam['exam_id']
        ), commit=True)
        logger.info("update %s exam success", exam['exam_name'])
    finally:
        connection.close()


def delete_exam(exam: dict):
    """delete exam

    Args:
        exam (dict): exam info
    """
    connection = get_connection()
    if connection:
        try:
            sql = "DELETE FROM tb_exam WHERE exam_id = %s"
            execute_sql(connection, sql, (exam['exam_id'],), commit=True)
            logger.info("delete %s exam success", exam['exam_name'])
        finally:
            connection.close()


df = pd.DataFrame(load_exams())

original_df = df.copy()
edited_df = df.copy()

edited_df = st.data_editor(edited_df, column_order=[
                           "exam_name", 'exam_date', "create_by", 'create_at', "updated_by", 'updated_at'], use_container_width=True, hide_index=True, num_rows="dynamic")

col0, col1, col2, col3 = st.columns([1, 1, 1, 1], gap='small')
with col1:
    if st.button("提交修改"):

        if not original_df.equals(edited_df):
            new_rows = edited_df[~edited_df["exam_id"].isin(
                df['exam_id'])]

            update_rows = edited_df[edited_df["exam_id"].isin(
                df['exam_id'])]
            for index, row in update_rows.iterrows():
                original_row = df[df['exam_id']
                                  == row['exam_id']].iloc[0]
                if not row.equals(original_row.drop(columns=['created_at', 'updated_at'])):
                    update_exam(row)
                    st.success("更新成功")

            delete_rows = df[~df['exam_id'].isin(
                edited_df['exam_id'])]

            for index, row in new_rows.iterrows():
                insert_exam(row)
                st.success("新增成功")

            for index, row in delete_rows.iterrows():
                delete_exam(row)
                st.success("删除成功")
        else:
            st.warning("没有更改")

with col2:
    if st.button('重置'):
        # 将编辑后的DataFrame还原为原始DataFrame
        st.warning("已重置")
        st.rerun()
