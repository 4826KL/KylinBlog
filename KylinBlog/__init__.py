# 项目启动的第一个文件 主要用于配置数据库引擎
# Django默认数据库引擎是SQllite
# 如需使用MySQL需要在此文件中importpymysql 并安装

import pymysql
pymysql.install_as_MySQLdb()  # 为本项目安装mysql引擎支持