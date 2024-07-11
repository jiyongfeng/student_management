#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-11 11:59:32
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-11 20:06:19
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import configparser
import pymysql
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置Seaborn样式
sns.set_theme(style="whitegrid")


def get_db_config():
    """读取并返回数据库配置信息

    returns:
        dict:包含数据库配置信息的字典
    """
    # 创建ConfigParser对象，用于解析配置文件
    config = configparser.ConfigParser()
    # 读取配置文件'db_config.ini'，并解析其中的配置信息
    config.read('db_config.ini')
    # 返回配置文件中'database'部分的配置信息
    return config['database']

# 连接到MySQL数据库的函数


def get_connection():
    """
    读取并返回数据库配置信息。

    该函数从名为'db_config.ini'的配置文件中读取数据库配置信息。
    返回一个字典，包含配置文件中'database'部分的所有键值对。

    returns:
        dict: 包含数据库配置信息的字典
    """
    db_config = get_db_config()
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            port=int(db_config['port']),
            password=db_config['password'],
            db=db_config['db'],
            charset=db_config['charset'],
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        st.error(f"数据库连接失败: {e}")
        return None
# 课程管理

# 检查并插入表数据


def check_and_insert(connection: object, table_name: str, name: str, value: str):
    """检查数据库中是否存在指定名称的记录，如果不存在，则插入该记录

    Args:
        connection (str):数据库连接对象
        table_name (str): 表名
        name (str): 列名
        value (str): 列的值

    Returns:
        str: 插入的值
    """
    try:
        with connection.cursor() as cursor:
            # 查询是否存在该名称
            sql_select = f"SELECT * FROM {table_name} WHERE {name} = %s"
            cursor.execute(sql_select, (value,))
            result = cursor.fetchone()

            if result is None:
                # 如果不存在，则插入新数据
                sql_insert = f"INSERT INTO {table_name} ({name}) VALUES (%s)"
                cursor.execute(sql_insert, (value,))
                connection.commit()
                st.success(f"成功插入 {value} 到表 {table_name}")
            return value
    except pymysql.MySQLError as e:
        st.error(f"操作失败：{str(e)}")


# 显示课程信息的函数（以表格形式）


def view_courses():
    """课程管理
    """
    st.subheader("课程管理")

    # 获取所有课程信息
    connection = get_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM tb_course"
                cursor.execute(sql)
                courses = cursor.fetchall()
                df_courses = pd.DataFrame(courses)
        except pymysql.MySQLError as e:
            st.error(f"操作失败：{str(e)}")
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
            connection = get_connection()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO tb_course (course_name, create_by) VALUES (%s, %s)"
                        cursor.execute(sql, (new_course_name, create_by))
                        connection.commit()
                        st.success("课程添加成功")
                        st.rerun()
                except pymysql.MySQLError as e:
                    st.error(f"发生错误: {e}")
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
                connection = get_connection()
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
                        st.error(f"发生错误: {e}")
                    finally:
                        connection.close()

        # 删除课程
        st.subheader("删除课程")
        delete_course_name = st.selectbox(
            "选择要删除的课程", [course['course_name'] for course in courses])
        if st.button("删除"):
            connection = get_connection()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        sql = "DELETE FROM tb_course WHERE course_name = %s"
                        cursor.execute(sql, (delete_course_name,))
                        connection.commit()
                        st.success("课程删除成功")
                except pymysql.MySQLError as e:
                    st.error(f"发生错误: {e}")
                finally:
                    connection.close()
    else:
        st.write("暂无课程信息")

# 获取所有课程


def get_courses():
    connection = get_connection()
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

# 考试项目管理


def add_exam():
    st.subheader("增加考试项目")
    exam_name = st.text_input("考试项目名称")
    create_by = st.text_input("创建者")
    if st.button("提交"):
        connection = get_connection()
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
    connection = get_connection()
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
    connection = get_connection()
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

# 学生管理


def add_student():
    st.subheader("增加学生")
    student_name = st.text_input("学生姓名")
    create_by = st.text_input("创建者")
    if st.button("提交"):
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO tb_student (student_name, create_by) VALUES (%s, %s)"
                cursor.execute(sql, (student_name, create_by))
            connection.commit()
            st.success("学生添加成功")
        finally:
            connection.close()


def view_students():
    st.subheader("显示学生")
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_student"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                st.dataframe(result)
            else:
                st.warning("没有学生")
    finally:
        connection.close()


def edit_student():
    st.subheader("编辑学生")
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_student"
            cursor.execute(sql)
            students = cursor.fetchall()
        student_dict = {student['student_name']                        : student['stu_id'] for student in students}
        selected_student = st.selectbox("选择学生", list(student_dict.keys()))
        new_name = st.text_input("新姓名")
        updated_by = st.text_input("更新者")
        if st.button("提交"):
            with connection.cursor() as cursor:
                sql = "UPDATE tb_student SET student_name=%s, updated_by=%s WHERE stu_id=%s"
                cursor.execute(sql, (new_name, updated_by,
                               student_dict[selected_student]))
            connection.commit()
            st.success("学生更新成功")
    finally:
        connection.close()

# 成绩管理


def add_score():
    st.subheader("登记成绩")
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
    finally:
        connection.close()


def view_scores1():
    st.subheader("查询成绩")
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
            result = cursor.fetchall()
            if result:
                # 表格
                st.table(result)
            else:
                st.write("没有数据")
    finally:
        connection.close()

# 查询成绩函数


def view_scores():
    st.subheader("查询成绩")

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
        st.dataframe(df_scores_sorted)

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


def import_scores():
    st.subheader("导入成绩")
    st.sidebar.subheader("上传 CSV 文件")
    uploaded_file = st.sidebar.file_uploader("选择一个 CSV 文件", type=['csv'])
    if uploaded_file is not None:
        st.sidebar.success('文件上传成功！')

        # 显示上传文件的相关信息
        df = pd.read_csv(uploaded_file)

        # 检查列名合法性
        required_columns = ['exam', 'course', 'score', 'student']
        if not all(col in df.columns for col in required_columns):
            st.error("CSV 文件缺失必要的列名（exam, course, score, student）")

        # 显示数据表格
        st.subheader("导入的数据预览")
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

                except Exception as e:
                    st.error(f"导入数据失败: {e}")

                finally:
                    connection.close()


# Streamlit 应用的主函数


def main():
    st.title("学生管理系统")
    # 一级菜单
    menu_option = st.sidebar.selectbox(
        "选择操作", ["成绩管理", "项目管理", "学生管理", "课程管理"])
    # 二级菜单
    if menu_option == "课程管理":
        view_courses()
    elif menu_option == "项目管理":
        sub_menu_option = st.sidebar.radio(
            "请选择操作",
            ["增加项目", "显示项目", "编辑项目"]
        )
        if sub_menu_option == "增加项目":
            add_exam()
        elif sub_menu_option == "显示项目":
            view_exams()
        elif sub_menu_option == "编辑项目":
            edit_exam()
    elif menu_option == "学生管理":
        sub_menu_option = st.sidebar.radio(
            "请选择操作",
            ["增加学生", "显示学生", "编辑学生"]
        )
        if sub_menu_option == "增加学生":
            add_student()
        elif sub_menu_option == "显示学生":
            view_students()
        elif sub_menu_option == "编辑学生":
            edit_student()
    elif menu_option == "成绩管理":
        sub_menu_option = st.sidebar.radio(
            "请选择操作",
            ["增加成绩", "显示成绩", "编辑成绩", "导入成绩"]
        )
        if sub_menu_option == "增加成绩":
            add_score()
        elif sub_menu_option == "显示成绩":
            view_scores()
        elif sub_menu_option == "编辑成绩":
            edit_score()
        elif sub_menu_option == "导入成绩":
            import_scores()


if __name__ == "__main__":
    main()
