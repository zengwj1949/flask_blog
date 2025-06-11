# 一、导入模块
import os
from flask import Flask

# 二、编写工厂函数，此函数返回值是一个 Flask 实例；
def create_app(test_config=None):
	# 1、创建 Flask 应用，__name__是一个内置变量，用于确定应用的根路径，影响Flask如何查找资源，如静态文件和模板等‌；
	app = Flask(__name__)
	
	# 2、加载配置文件
	
	# 3、数据库关联 Flask 应用；
	
	# 4、定义日志配置
