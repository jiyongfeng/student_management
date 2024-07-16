#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-12 09:50:27
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-17 00:45:28
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
from datetime import datetime

import pandas as pd
import pymysql
import streamlit as st

from utils.database import (get_connection, handle_database_error,
                            handle_general_error)
from utils.logger import logger

st.subheader("考试管理")


def load_exams():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_exam"
            cursor.execute(sql)
            df = pd.DataFrame(cursor.fetchall())
            return df
    except pymysql.MySQLError as db_error:
        handle_database_error(db_error)
    except Exception as general_error:
        handle_general_error(general_error)
    finally:
        connection.close()


def insert_exam(exam):
    connection = get_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO tb_exam (exam_name, exam_date,create_by,updated_by,create_at,updated_at) VALUES (%s, %s, %s, %s,%s,%s)"
                cursor.execute(
                    sql, (exam['exam_name'], exam['exam_date'], st.session_state.username, st.session_state.username, datetime.now(), datetime.now()))
                connection.commit()
                logger.info("add %s exam success", exam['exam_name'])
        except pymysql.MySQLError as db_error:
            handle_database_error(db_error)
        except Exception as general_error:
            handle_general_error(general_error)
        finally:
            connection.close()


def update_exam(exam):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE tb_exam SET exam_name=%s, exam_date=%s, create_by = %s, updated_by = %s, updated_at = %s WHERE exam_id = %s"
            cursor.execute(sql, (exam['exam_name'], exam['exam_date'], exam['create_by'],
                                 st.session_state.username, datetime.now(), exam['exam_id']))
        connection.commit()
    except pymysql.MySQLError as db_error:
        handle_database_error(db_error)
    except Exception as general_error:
        handle_general_error(general_error)
    finally:
        connection.close()


def delete_exam(delete_exam_id):
    connection = get_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM tb_exam WHERE exam_id = %s"
                cursor.execute(sql, (delete_exam_id))
                connection.commit()
        except pymysql.MySQLError as db_error:
            handle_database_error(db_error)
        except Exception as general_error:
            handle_general_error(general_error)
        finally:
            connection.close()


df = load_exams()

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
                delete_exam(row['exam_id'])
                st.success("删除成功")
        else:
            st.warning("没有更改")

with col2:
    if st.button('重置'):
        # 将编辑后的DataFrame还原为原始DataFrame
        st.warning("已重置")
        st.rerun()
