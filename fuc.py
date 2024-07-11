#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-06-29 10:31:24
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-06-29 10:36:33
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
from argon2 import PasswordHasher

hasher = PasswordHasher()
hashed_password = hasher.hash("84qrSS1fWgbm1PySWZQXNw")
print(hashed_password)

try:
    hasher.verify("84qrSS1fWgbm1PySWZQXNw", hashed_password)
    print("密码验证成功!")
except:
    print("密码验证失败!")
