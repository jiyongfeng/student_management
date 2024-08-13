#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-12 09:50:27
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-08-13 16:32:58
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
from datetime import datetime

import pandas as pd
import pymysql
import streamlit as st

from utils import auth
from utils.database import (get_connection, handle_database_error,
                            handle_general_error)
from utils.logger import logger

st.subheader("学生管理")


def load_students():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_student"
            cursor.execute(sql)
            result = pd.DataFrame(cursor.fetchall())
            return result

    except pymysql.MySQLError as db_error:
        handle_database_error(db_error)
    except Exception as general_error:
        handle_general_error(general_error)
    finally:
        connection.close()


def insert_student(student):
    # 初始密码123456
    default_password = '123456'
    hashed_password = auth.hash_password(default_password)
    connection = get_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO tb_student (student_name,user_name, email, hashed_password,create_by,updated_by,create_at,updated_at) VALUES (%s, %s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(
                    sql, (student['student_name'], student['user_name'], student['email'], hashed_password, st.session_state.user_name, st.session_state.user_name, datetime.now(), datetime.now()))
                connection.commit()
                logger.info("学生 %s 添加成功", student['user_name'])
        except pymysql.MySQLError as db_error:
            handle_database_error(db_error)
        except Exception as general_error:
            handle_general_error(general_error)
        finally:
            connection.close()


def update_student(student):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE tb_student SET student_name=%s, user_name=%s, email=%s, create_by = %s, updated_by = %s, updated_at = %s WHERE stu_id = %s"
            cursor.execute(sql, (student['student_name'], student['user_name'], student['email'], student['create_by'],
                                 st.session_state.user_name, datetime.now(), student['stu_id']))
        connection.commit()
        logger.info("学生 %s 更新成功", student['user_name'])
    except pymysql.MySQLError as db_error:
        handle_database_error(db_error)
    except Exception as general_error:
        handle_general_error(general_error)
    finally:
        connection.close()


def delete_student(student):
    connection = get_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM tb_student WHERE stu_id = %s"
                cursor.execute(sql, (student['stu_id']))
                connection.commit()
                logger.info("学生 %s 删除成功", student['user_name'])
        except pymysql.MySQLError as db_error:
            handle_database_error(db_error)
        except Exception as general_error:
            handle_general_error(general_error)
        finally:
            connection.close()


df_students = load_students()
display_df = df_students
edited_df = st.data_editor(df_students, column_order=[
                           "student_name", "user_name", "email", "create_by", 'create_at', "updated_by", 'updated_at'],
                           use_container_width=True, hide_index=True, num_rows="dynamic",
                           disabled=["create_by", 'create_at', "updated_by", 'updated_at'])


if st.button("提交"):

    if not display_df.equals(edited_df):
        # 新增
        new_rows = edited_df[
            (~edited_df["stu_id"].isin(df_students["stu_id"]))]

        update_rows = edited_df[
            (edited_df["stu_id"].isin(df_students["stu_id"]))]

        for index, row in update_rows.iterrows():
            original_row = df_students[df_students['stu_id']
                                       == row['stu_id']].iloc[0]

            if not row.equals(original_row.drop(columns=['created_at', 'updated_at'])):
                update_student(row)
                st.success("更新成功")
        delete_rows = df_students[~df_students['stu_id'].isin(
            edited_df['stu_id'])]

        for index, row in new_rows.iterrows():
            insert_student(row)
            st.success("新增成功")

        for index, row in delete_rows.iterrows():
            delete_student(row)
            st.success("删除成功")

    else:
        st.warning("没有更改")
