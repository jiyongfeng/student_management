#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-14 15:18:45
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-07-16 18:21:08
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""

import streamlit as st

st.subheader("用户设置")

st.write(f"You are logged in as {st.session_state.username}.")
