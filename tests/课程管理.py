#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-12 09:50:27
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-12 17:14:28
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import logging

import pandas as pd
import pymysql
import seaborn as sns
import streamlit as st

from utils.database import get_connection

CONFIG_FILE = "config.ini"

# 设置Seaborn样式
sns.set_theme(style="whitegrid")

# 配置日志记录
logging.basicConfig(level=logging.DEBUG)


def view_courses():
    """课程管理
    """
    st.subheader("课程管理")

    # 获取所有课程信息
    connection = get_connection(CONFIG_FILE)
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM tb_course"
                cursor.execute(sql)
                courses = cursor.fetchall()
                df_courses = pd.DataFrame(courses)
        except pymysql.MySQLError as e:
            st.error(f"操作失败：{str(e)}")
            logging.error("操作失败：%s", str(e))
            return
        finally:
            connection.close()

    # 显示表格并添加、编辑、删除功能
    if courses:
        # 显示课程信息的表格
        # df_course_name_sorted = df_courses.sort_values(by='course_name')
        # st.dataframe(df_course_name_sorted, hide_index=True)

        st.dataframe(df_courses, column_order=[
                     "course_name", "create_by", 'create_at', "updated_by", 'updated_at'], hide_index=True)
        # 添加新课程
        st.subheader("添加课程")
        new_course_name = st.text_input("请输入新课程名称")
        create_by = st.text_input("请输入创建者")
        if st.button("添加"):
            connection = get_connection(CONFIG_FILE)
            if connection:
                try:
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO tb_course (course_name, create_by) VALUES (%s, %s)"
                        cursor.execute(sql, (new_course_name, create_by))
                        connection.commit()
                        st.success("课程添加成功")
                        st.rerun()
                except pymysql.MySQLError as e:
                    st.error(f"发生错误: {str(e)}")
                finally:
                    connection.close()

        # 编辑课程
        st.subheader("编辑课程")
        edit_course_name = st.selectbox(
            "选择要编辑的课程", [course['course_name'] for course in courses])
        selected_course = next(
            (course for course in courses if course['course_name'] == edit_course_name), None)
        if selected_course:
            new_course_name = st.text_input(
                "请输入新的课程名称", selected_course['course_name'])
            updated_by = st.text_input("请输入更新者")
            if st.button("更新"):
                connection = get_connection(CONFIG_FILE)
                if connection:
                    try:
                        with connection.cursor() as cursor:
                            sql = "UPDATE tb_course SET course_name = %s, updated_by = %s WHERE course_name = %s"
                            cursor.execute(
                                sql, (new_course_name, updated_by, edit_course_name))
                            connection.commit()
                            st.success("课程信息更新成功")
                            st.rerun()
                    except pymysql.MySQLError as e:
                        st.error(f"发生错误: {str(e)}")
                    finally:
                        connection.close()

        # 删除课程
        st.subheader("删除课程")
        delete_course_name = st.selectbox(
            "选择要删除的课程", [course['course_name'] for course in courses])
        if st.button("删除"):
            connection = get_connection(CONFIG_FILE)
            if connection:
                try:
                    with connection.cursor() as cursor:
                        sql = "DELETE FROM tb_course WHERE course_name = %s"
                        cursor.execute(sql, (delete_course_name,))
                        connection.commit()
                        st.success("课程删除成功")
                except pymysql.MySQLError as e:
                    st.error(f"发生错误: {str(e)}")
                finally:
                    connection.close()
    else:
        st.write("暂无课程信息")

# 获取所有课程


def get_courses():
    connection = get_connection(CONFIG_FILE)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tb_course")
            courses = cursor.fetchall()
            df_courses = pd.DataFrame(courses)
            return df_courses
    except Exception as e:
        st.error(f"获取课程数据失败：{str(e)}")
        return pd.DataFrame()
    finally:
        connection.close()


def main():
    st.title("课程管理")

    view_courses()


if __name__ == "__main__":

    main()
