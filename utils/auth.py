#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-26 11:27:04
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-08-15 11:47:27
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""

import re
import bcrypt
import pymysql

from utils.database import (get_connection, handle_database_error,
                            handle_general_error)
from utils.logger import logger


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


def add_user(user_name: str, email: str, password: str = '123456'):
    """
    Adds a new user to the database.

    Args:
        user_name (str): The username of the new user.
        email (str): The email address of the new user.
        password (str): The password for the new user.

    Returns:
        None

    Raises:
        pymysql.MySQLError: If a database error occurs.
        Exception: If any other error occurs.
    """

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
    """
    Authenticates a user based on their username or email and password.

    Args:
        user_name_or_email (str): The username or email of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        str: The username of the authenticated user, or False if authentication fails.
    """

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


def update_user_info(user_name, **kwargs):
    """
    Updates the information of a user in the database.
    """
    if not user_name:
        raise ValueError("user_name cannot be None or empty")
    if not kwargs:
        raise ValueError("No changes to update")

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE tb_student SET "
            sql_params = []
            for key, value in kwargs.items():
                if value is None:
                    raise ValueError(f"{key} cannot be None")
                sql += f"{key} = %s, "
                sql_params.append(value)
            sql = sql.rstrip(", ") + " WHERE user_name = %s"
            sql_params.append(user_name)  # Add user_name as the last parameter
            logger.debug(f"Executing SQL: {sql} with params: {
                sql_params}")  # Debugging line
            cursor.execute(sql, sql_params)
        connection.commit()
    except pymysql.MySQLError as db_error:
        logger.error(f"Database error: {db_error}")
        handle_database_error(db_error)
    except Exception as general_error:
        logger.error(f"An error occurred: {general_error}")
        handle_general_error(general_error)
    finally:
        connection.close()

# Email validation,有效返回true，无效返回false


def is_valid_email(email):
    """
    Validate email address
    """
    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True
