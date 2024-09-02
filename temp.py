#!/usr/bin/env python
# coding=utf-8

"""
 * @Author       : JIYONGFENG jiyongfeng@163.com
 * @Date         : 2024-08-21 10:39:23
 * @LastEditors  : JIYONGFENG jiyongfeng@163.com
 * @LastEditTime : 2024-08-21 10:55:13
 * @Description  :
 * @Copyright (c) 2024 by ZEZEDATA Technology CO, LTD, All Rights Reserved.
"""

from utils.database import get_connection

# 连接到数据库
connection = get_connection()
cursor = connection.cursor()

# 查询所有表和字段
cursor.execute("""
    SELECT TABLE_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'student_management'
    AND COLUMN_NAME IN ('create_at', 'updated_at');
""")

tables = cursor.fetchall()

# 修改字段类型
for table in tables:
    table_name = table['TABLE_NAME']
    alter_query = f"""
    ALTER TABLE {table_name}
    MODIFY COLUMN create_at DATETIME,
    MODIFY COLUMN updated_at DATETIME;
    """
    cursor.execute(alter_query)
    print(f"Updated table: {table_name}")

# 提交更改并关闭连接
connection.commit()
cursor.close()
connection.close()
