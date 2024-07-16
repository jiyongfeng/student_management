#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-12 09:50:27
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-17 00:50:41
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
from datetime import datetime

import pandas as pd
import pymysql
import streamlit as st

from utils.database import get_connection, handle_database_error, handle_general_error
from utils.logger import logger

st.subheader("课程管理")


def load_courses():
    connection = get_connection()
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
        finally:
            connection.close()


def insert_course(course):
    connection = get_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO tb_course (course_name, sort, create_by,updated_by,create_at,updated_at) VALUES (%s, %s, %s,%s,%s)"
                cursor.execute(sql, (course['course_name'], course['sort'],
                                     course['create_by'], st.session_state.username, datetime.now(), datetime.now()))
                connection.commit()
                logger.info("新增课程 %s 成功", course['course_name'])
        except pymysql.MySQLError as db_error:
            handle_database_error(db_error)
        except Exception as general_error:
            handle_general_error(general_error)
        finally:
            connection.close()


def update_coures(course):
    connection = get_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE tb_course SET course_name = %s,sort=%s, create_by = %s, updated_by = %s, updated_at = %s WHERE cou_id = %s"
                cursor.execute(
                    sql, (course['course_name'], course['sort'], course['create_by'], st.session_state.username, datetime.now(), course['cou_id']))
                connection.commit()
                logger.info("更新课程 %s 成功", course['course_name'])
        except pymysql.MySQLError as db_error:
            handle_database_error(db_error)
        except Exception as general_error:
            handle_general_error(general_error)
        finally:
            connection.close()


def delete_course(course):
    connection = get_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM tb_course WHERE cou_id = %s"
                cursor.execute(sql, (course['cou_id']))
                connection.commit()
                logger.info("删除课程 %s 成功", course['course_name'])
        except pymysql.MySQLError as db_error:
            handle_database_error(db_error)
        except Exception as general_error:
            handle_general_error(general_error)
        finally:
            connection.close()


df_courses = load_courses()

display_df = df_courses.drop(columns=['create_at', 'updated_at'])
edited_df = st.data_editor(df_courses, column_order=[
                           "course_name", 'sort', "create_by", 'create_at', "updated_by", 'updated_at'], use_container_width=True, hide_index=True, num_rows="dynamic")

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
            delete_course(row)
            st.success("删除成功")

    else:
        st.warning("没有更改")
