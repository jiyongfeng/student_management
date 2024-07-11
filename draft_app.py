#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-06-26 21:30:53
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-11 11:59:02
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import configparser
import pymysql
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


# 创建ConfigParser对象
config = configparser.ConfigParser()

# 读取配置文件
config.read('db_config.ini')

# 从配置文件中获取数据库配置信息
db_config = {
    'host': config.get('database', 'host'),
    'port': config.getint('database', 'port'),
    'user': config.get('database', 'user'),
    'password': config.get('database', 'password'),
    'database': config.get('database', 'name')

}

# 检查必要的配置项是否齐全
if not all(db_config.values()):
    raise ValueError("Missing required database configuration.")

# 连接到MySQL数据库的函数


def get_connection():
    try:
        conn = pymysql.connect(**db_config)
        return conn
    except pymysql.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# 学科管理
def add_subject():
    st.subheader("增加学科")
    subject_name = st.text_input("学科名称")
    if st.button("提交"):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO subjects (name) VALUES (%s)"
                cursor.execute(sql, (subject_name,))
            connection.commit()
            st.success("学科添加成功")
        finally:
            connection.close()


def view_subjects():
    st.subheader("显示学科")
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM subjects"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                st.write(f"ID: {row['id']}, 名称: {row['name']}")
    finally:
        connection.close()


def edit_subject():
    st.subheader("编辑学科")
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM subjects"
            cursor.execute(sql)
            subjects = cursor.fetchall()
        subject_dict = {subject['name']: subject['id'] for subject in subjects}
        selected_subject = st.selectbox("选择学科", list(subject_dict.keys()))
        new_name = st.text_input("新名称")
        if st.button("提交"):
            with connection.cursor() as cursor:
                sql = "UPDATE subjects SET name=%s WHERE id=%s"
                cursor.execute(sql, (new_name, subject_dict[selected_subject]))
            connection.commit()
            st.success("学科更新成功")
    finally:
        connection.close()

# 考试项目管理


def add_exam():
    st.subheader("增加考试项目")
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM subjects"
            cursor.execute(sql)
            subjects = cursor.fetchall()
        subject_dict = {subject['name']: subject['id'] for subject in subjects}
        exam_name = st.text_input("考试项目名称")
        selected_subject = st.selectbox("选择学科", list(subject_dict.keys()))
        if st.button("提交"):
            with connection.cursor() as cursor:
                sql = "INSERT INTO exams (name, subject_id) VALUES (%s, %s)"
                cursor.execute(
                    sql, (exam_name, subject_dict[selected_subject]))
            connection.commit()
            st.success("考试项目添加成功")
    finally:
        connection.close()


def view_exams():
    st.subheader("显示考试项目")
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT exams.id, exams.name, subjects.name as subject_name
            FROM exams
            JOIN subjects ON exams.subject_id = subjects.id
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                st.write(f"ID: {row['id']}, 名称: {
                         row['name']}, 学科: {row['subject_name']}")
    finally:
        connection.close()


def edit_exam():
    st.subheader("编辑考试项目")
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM exams"
            cursor.execute(sql)
            exams = cursor.fetchall()
        exam_dict = {exam['name']: exam['id'] for exam in exams}
        selected_exam = st.selectbox("选择考试项目", list(exam_dict.keys()))
        new_name = st.text_input("新名称")
        if st.button("提交"):
            with connection.cursor() as cursor:
                sql = "UPDATE exams SET name=%s WHERE id=%s"
                cursor.execute(sql, (new_name, exam_dict[selected_exam]))
            connection.commit()
            st.success("考试项目更新成功")
    finally:
        connection.close()

# 成绩管理


def add_score():
    st.subheader("登记成绩")
    student_name = st.text_input("学生姓名")
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM exams"
            cursor.execute(sql)
            exams = cursor.fetchall()
        exam_dict = {exam['name']: exam['id'] for exam in exams}
        selected_exam = st.selectbox("选择考试项目", list(exam_dict.keys()))
        score = st.number_input("成绩", min_value=0, max_value=100)
        if st.button("提交"):
            with connection.cursor() as cursor:
                sql = "INSERT INTO scores (student_name, exam_id, score) VALUES (%s, %s, %s)"
                cursor.execute(
                    sql, (student_name, exam_dict[selected_exam], score))
            connection.commit()
            st.success("成绩登记成功")
    finally:
        connection.close()


def view_scores():
    st.subheader("查询成绩")
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT scores.id, scores.student_name, exams.name as exam_name, scores.score
            FROM scores
            JOIN exams ON scores.exam_id = exams.id
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                st.write(f"ID: {row['id']}, 学生: {row['student_name']}, 考试项目: {
                         row['exam_name']}, 成绩: {row['score']}")
    finally:
        connection.close()


def edit_score():
    st.subheader("修改成绩")
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM scores"
            cursor.execute(sql)
            scores = cursor.fetchall()
        score_dict = {
            f"{score['student_name']} - {score['id']}": score['id'] for score in scores}
        selected_score = st.selectbox("选择成绩记录", list(score_dict.keys()))
        new_score = st.number_input("新成绩", min_value=0, max_value=100)
        if st.button("提交"):
            with connection.cursor() as cursor:
                sql = "UPDATE scores SET score=%s WHERE id=%s"
                cursor.execute(sql, (new_score, score_dict[selected_score]))
            connection.commit()
            st.success("成绩更新成功")
    finally:
        connection.close()


# 主界面
st.title("学生考试成绩管理系统")

menu = ["学科管理", "考试项目管理", "成绩管理"]
choice = st.sidebar.selectbox("菜单", menu)

if choice == "学科管理":
    st.sidebar.subheader("操作")
    operation = st.sidebar.selectbox("选择操作", ["增加学科", "显示学科", "编辑学科"])
    if operation == "增加学科":
        add_subject()
    elif operation == "显示学科":
        view_subjects()
    elif operation == "编辑学科":
        edit_subject()

elif choice == "考试项目管理":
    st.sidebar.subheader("操作")
    operation = st.sidebar.selectbox("选择操作", ["增加考试项目", "显示考试项目", "编辑考试项目"])
    if operation == "增加考试项目":
        add_exam()
    elif operation == "显示考试项目":
        view_exams()
    elif operation == "编辑考试项目":
        edit_exam()

elif choice == "成绩管理":
    st.sidebar.subheader("操作")
    operation = st.sidebar.selectbox("选择操作", ["登记成绩", "查询成绩", "修改成绩"])
    if operation == "登记成绩":
        add_score()
    elif operation == "查询成绩":
        view_scores()
    elif operation == "修改成绩":
        edit_score()
