#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-26 11:27:04
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-08-13 16:07:41
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""

import bcrypt
import pymysql

from utils.database import (get_connection, handle_database_error,
                            handle_general_error)


def hash_password(password: str):
    """
    Hashes a given password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(hashed_password: str, password: str):
    """
    Checks if a given password matches a hashed password.

    Args:
        hashed_password (str): The hashed password to compare against.
        password (str): The password to check.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def add_user(user_name, email, password):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            hashed_password = hash_password(password)
            cursor.execute('INSERT INTO tb_student (user_name, email, hashed_password) VALUES (?, ?, ?)',
                           (user_name, email, hashed_password))
        conn.commit()
    except pymysql.MySQLError as db_error:
        handle_database_error(db_error)
    except Exception as general_error:
        handle_general_error(general_error)
    finally:
        conn.close()


def authenticate_user(user_name_or_email, password):
    """用户认证"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM tb_student WHERE user_name=%s OR email=%s',
                           (user_name_or_email, user_name_or_email))
            result = cursor.fetchone()
            hashed_password = result['hashed_password']
            user_name = result['user_name']
            if result and check_password(hashed_password, password):
                return user_name
            else:
                return False
    except pymysql.MySQLError as db_error:
        handle_database_error(db_error)
    except Exception as general_error:
        handle_general_error(general_error)
    finally:
        conn.close()


def change_password(user_name, new_password):
    """修改密码"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            hashed_password = hash_password(new_password)
            cursor.execute('UPDATE tb_student SET hashed_password=%s WHERE user_name=%s',
                           (hashed_password, user_name))
        conn.commit()
    except pymysql.MySQLError as db_error:
        handle_database_error(db_error)
    except Exception as general_error:
        handle_general_error(general_error)
    finally:
        conn.close()
