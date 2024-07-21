#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-11 22:39:38
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-21 16:17:51
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import configparser
import bcrypt

import pymysql
import streamlit as st

from utils.logger import logger


def get_db_config(config_path: str = "config.ini"):
    """读取并返回数据库配置信息

    args:
        config_path:配置文件路径，默认为"config.ini"

    returns:
        dict:包含数据库配置信息的字典
    """
    # 创建ConfigParser对象，用于解析配置文件
    config = configparser.ConfigParser()
    # 读取配置文件'db_config.ini'，并解析其中的配置信息
    config.read(config_path)
    # 返回配置文件中'database'部分的配置信息
    return config['database']

# 连接到MySQL数据库的函数


def get_connection():
    """
    读取并返回数据库配置信息。

    该函数从名为'secrets.toml'的配置文件中读取数据库配置信息。
    返回一个字典，包含配置文件中'database'部分的所有键值对。

    args:
        config_path (str): 配置文件路径，默认为'config.ini'

    returns:
        dict: 包含数据库配置信息的字典
    """

    try:
        connection = pymysql.connect(
            host=st.secrets.database.host,
            user=st.secrets.database.user,
            port=st.secrets.database.port,
            password=st.secrets.database.password,
            db=st.secrets.database.db,
            charset=st.secrets.database.charset,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        st.error(f"数据库连接失败: {str(e)}")
        logger.error("数据库连接失败: %s", str(e))


def execute_sql(connection, sql, params=None, commit=False):
    """
    执行SQL语句的通用函数，用于减少重复代码
    """
    try:
        with connection.cursor() as cursor:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            if commit:
                connection.commit()
            return cursor.fetchall()
    except pymysql.MySQLError as db_error:
        handle_database_error(db_error)
    except Exception as general_error:
        handle_general_error(general_error)


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
                logger.debug("成功插入 %s 到表 %s", value, table_name)
            return value
    except pymysql.MySQLError as e:
        st.error(f"操作失败：{str(e)}")
        logger.error("操作失败：%s", str(e))


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
    logger.error("发生错误：%s", message)


def log_error(prefix, error):
    # 记录错误日志，包括错误前缀和错误详细信息
    logger.error("%s %s", prefix, str(error))


# 加密密码


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# 验证密码


def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)
