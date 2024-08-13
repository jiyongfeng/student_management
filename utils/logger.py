#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-07-16 17:39:14
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-08-13 11:18:01
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""
import logging
import os
from datetime import datetime
import streamlit as st

if "logPath" not in st.session_state:
    # 日志文件路径,以log+当前时间戳
    st.session_state.logPath = "log/log_" + \
        datetime.now().strftime("%Y%m%d%H%M%S") + ".log"
    # 判断日志文件是否存在,不存在则创建
    if not os.path.exists('log'):
        os.makedirs('log')
        with open(st.session_state.logPath, "w", encoding="utf-8") as f:
            f.write("")

# 配置全局logging
logging.basicConfig(
    filename=st.session_state.logPath,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 获取logger对象
logger = logging.getLogger()
