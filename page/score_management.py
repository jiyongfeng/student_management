#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-12 09:50:27
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-15 22:57:49
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import logging

import matplotlib.pyplot as plt
import pandas as pd
import pymysql
import streamlit as st
import seaborn as sns
from utils.database import get_connection, check_and_insert

# 配置日志记录
logging.basicConfig(level=logging.DEBUG)

= "config.ini"


@st.experimental_dialog("添加成绩")
def add_score():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_student"
            cursor.execute(sql)
            students = cursor.fetchall()
        student_dict = {student['student_name']: student['stu_id'] for student in students}
        selected_student = st.selectbox("选择学生", list(student_dict.keys()))

        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_exam"
            cursor.execute(sql)
            exams = cursor.fetchall()
        exam_dict = {exam['exam_name']: exam['exam_id'] for exam in exams}
        selected_exam = st.selectbox("选择考试项目", list(exam_dict.keys()))

        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_course"
            cursor.execute(sql)
            courses = cursor.fetchall()
        course_dict = {course['course_name']: course['cou_id']
                       for course in courses}
        selected_course = st.selectbox("选择课程", list(course_dict.keys()))

        score = st.number_input("成绩", min_value=0.0, max_value=100.0)
        create_by = st.text_input("创建者")
        if st.button("提交"):
            with connection.cursor() as cursor:
                sql = "INSERT INTO tb_scores (student_id, exam_id, course_id, score, create_by) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(
                    sql, (student_dict[selected_student], exam_dict[selected_exam], course_dict[selected_course], score, create_by))
            connection.commit()
            st.success("成绩登记成功")
            st.rerun()
    finally:
        connection.close()


# 查询成绩函数


def view_scores():

    # 获取所有项目和学科信息
    connection = get_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                # 查询所有项目和学科
                cursor.execute("SELECT * FROM tb_exam order by exam_name asc")
                exams = cursor.fetchall()
                cursor.execute("SELECT * FROM tb_course")
                courses = cursor.fetchall()
        finally:
            connection.close()

    # 显示筛选器：选择项目或学科
    selected_exam = st.selectbox(
        "选择项目", ["所有项目"] + [exam['exam_name'] for exam in exams])
    selected_course = st.selectbox(
        "选择学科", ["所有学科"] + [course['course_name'] for course in courses])

    # 根据选择的项目和学科进行筛选
    connection = get_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                if selected_exam == "所有项目" and selected_course == "所有学科":
                    # 显示所有成绩
                    cursor.execute("SELECT s.score_id, st.student_name, e.exam_name, c.course_name, s.score FROM tb_scores s "
                                   "INNER JOIN tb_student st ON s.student_id = st.stu_id "
                                   "INNER JOIN tb_exam e ON s.exam_id = e.exam_id "
                                   "INNER JOIN tb_course c ON s.course_id = c.cou_id")
                elif selected_exam == "所有项目" and selected_course != "所有学科":
                    # 根据学科筛选成绩
                    cursor.execute("SELECT s.score_id, st.student_name, e.exam_name, c.course_name, s.score FROM tb_scores s "
                                   "INNER JOIN tb_student st ON s.student_id = st.stu_id "
                                   "INNER JOIN tb_exam e ON s.exam_id = e.exam_id "
                                   "INNER JOIN tb_course c ON s.course_id = c.cou_id "
                                   "WHERE c.course_name = %s", (selected_course,))
                elif selected_exam != "所有项目" and selected_course == "所有学科":
                    # 根据项目筛选成绩
                    cursor.execute("SELECT s.score_id, st.student_name, e.exam_name, c.course_name, s.score FROM tb_scores s "
                                   "INNER JOIN tb_student st ON s.student_id = st.stu_id "
                                   "INNER JOIN tb_exam e ON s.exam_id = e.exam_id "
                                   "INNER JOIN tb_course c ON s.course_id = c.cou_id "
                                   "WHERE e.exam_name = %s", (selected_exam,))
                else:
                    # 根据项目和学科筛选成绩
                    cursor.execute("SELECT s.score_id, st.student_name, e.exam_name, c.course_name, s.score FROM tb_scores s "
                                   "INNER JOIN tb_student st ON s.student_id = st.stu_id "
                                   "INNER JOIN tb_exam e ON s.exam_id = e.exam_id "
                                   "INNER JOIN tb_course c ON s.course_id = c.cou_id "
                                   "WHERE e.exam_name = %s AND c.course_name = %s", (selected_exam, selected_course))

                scores = cursor.fetchall()
        finally:
            connection.close()

    # 显示成绩表格
    if scores:
        df_scores = pd.DataFrame(scores)
        # 对 exam_name 列按名称排序
        df_scores_sorted = df_scores.sort_values(by='exam_name')
        st.dataframe(df_scores_sorted, use_container_width=True)

        if selected_course != '所有学科' and selected_exam == '所有项目':
            # 显示直方图
            st.subheader(f"{selected_course}学科的成绩分布")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(ax=ax, data=df_scores_sorted,
                         x='exam_name', y='score', marker='o')
            ax.set_xlabel('项目', fontproperties='SimHei')
            ax.set_ylabel('成绩', fontproperties='SimHei')
            plt.title(f"{selected_course}学科的成绩分布",
                      fontproperties='SimHei')
            plt.xticks(rotation=45)
            st.pyplot(fig)
    else:
        st.write("暂无符合条件的成绩记录")


@st.experimental_dialog("修改成绩")
def edit_score():
    st.subheader("修改成绩")
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT tb_scores.score_id, tb_student.student_name, tb_exam.exam_name, tb_course.course_name, tb_scores.score
            FROM tb_scores
            JOIN tb_student ON tb_scores.student_id = tb_student.stu_id
            JOIN tb_exam ON tb_scores.exam_id = tb_exam.exam_id
            JOIN tb_course ON tb_scores.course_id = tb_course.cou_id
            """
            cursor.execute(sql)
            scores = cursor.fetchall()
        score_dict = {f"{score['student_name']} - {score['exam_name']} - {
            score['course_name']}": score['score_id'] for score in scores}
        selected_score = st.selectbox("选择成绩记录", list(score_dict.keys()))
        new_score = st.number_input("新成绩", min_value=0.0, max_value=100.0)
        updated_by = st.text_input("更新者")
        if st.button("提交"):
            with connection.cursor() as cursor:
                sql = "UPDATE tb_scores SET score=%s, updated_by=%s WHERE score_id=%s"
                cursor.execute(sql, (new_score, updated_by,
                               score_dict[selected_score]))
            connection.commit()
            st.success("成绩更新成功")
    finally:
        connection.close()

# 导入csv格式的成绩文件


@st.experimental_dialog("导入成绩")
def import_scores():

    uploaded_file = st.file_uploader("选择一个 CSV 文件", type=['csv'])
    if uploaded_file is not None:
        st.success('文件上传成功！')

        # 显示上传文件的相关信息
        df = pd.read_csv(uploaded_file)

        # 检查列名合法性
        required_columns = ['exam', 'course', 'score', 'student']
        if not all(col in df.columns for col in required_columns):
            st.error("CSV 文件缺失必要的列名（exam, course, score, student）")

        # 显示数据表格
        st.write("导入的数据预览")
        st.write(df)

        if st.button("导入数据到数据库"):
            connection = get_connection()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        # 导入数据
                        for index, row in df.iterrows():

                            # 分别检查考试、学科和学生是否存在，如果不存在则插入

                            exam_name = check_and_insert(
                                connection, 'tb_exam', 'exam_name', row['exam'])
                            course_name = check_and_insert(
                                connection, 'tb_course', 'course_name', row['course'])
                            student_name = check_and_insert(
                                connection, 'tb_student', 'student_name', row['student'])

                            if exam_name is None or course_name is None or student_name is None:
                                st.error("插入过程中出现错误，终止导入")
                                return

                            # 获取刚插入的或者已经存在的 ID
                            cursor.execute(
                                "SELECT exam_id FROM tb_exam WHERE exam_name = %s", (exam_name,))
                            exam_id = cursor.fetchone()['exam_id']

                            cursor.execute(
                                "SELECT cou_id FROM tb_course WHERE course_name = %s", (course_name,))
                            course_id = cursor.fetchone()['cou_id']

                            cursor.execute(
                                "SELECT stu_id FROM tb_student WHERE student_name = %s", (student_name,))
                            student_id = cursor.fetchone()['stu_id']

                            sql_insert = "INSERT INTO tb_scores (exam_id, course_id, student_id, score) VALUES (%s, %s, %s, %s)"
                            cursor.execute(
                                sql_insert, (exam_id, course_id, student_id, row['score']))
                        connection.commit()
                    st.success("导入数据成功")
                    st.rerun()

                except pymysql.MySQLError as e:
                    st.error(f"导入数据失败: {str(e)}")
                    st.rerun()

                finally:
                    connection.close()


col1, col2, col3, col4 = st.columns([3, 1, 1, 1], vertical_alignment="center")
with col1:
    st.subheader("成绩查询")
with col2:
    if st.button("添加成绩"):
        add_score()

with col3:
    if st.button("修改成绩"):
        edit_score()
with col4:
    if st.button("导入成绩"):
        import_scores()


view_scores()
