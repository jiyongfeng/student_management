#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-26 11:27:04
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-26 11:27:15
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import bcrypt
import sqlite3

# 数据库连接
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# 创建用户表
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')
conn.commit()


def hash_password(password):
    """加密密码"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(hashed_password, password):
    """验证密码"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


def add_user(username, email, password):
    """添加用户"""
    hashed_password = hash_password(password)
    try:
        cursor.execute('INSERT INTO user (username, email, password) VALUES (?, ?, ?)',
                       (username, email, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        print("用户名或邮箱已存在")


def authenticate_user(username_or_email, password):
    """用户认证"""
    cursor.execute('SELECT password FROM user WHERE username=? OR email=?',
                   (username_or_email, username_or_email))
    result = cursor.fetchone()
    if result and check_password(result[0], password):
        return True
    return False


def change_password(username_or_email, new_password):
    """修改密码"""
    hashed_password = hash_password(new_password)
    cursor.execute('UPDATE user SET password=? WHERE username=? OR email=?',
                   (hashed_password, username_or_email))
    conn.commit()

# 关闭数据库连接


def close_connection():
    conn.close()
