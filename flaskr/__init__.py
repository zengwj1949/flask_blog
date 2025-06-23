# 一、导入模块
import os
from flask import Flask

# 数据库配置一、导入数据库相关模块
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import pymysql

# 日志配置一、导入日志模块
import logging

# 数据库配置二、数据库实例要初始化组件对象（先实例化），延后关联 Flask 应用
db = SQLAlchemy()


# 二、编写工厂函数，此函数返回值是一个 Flask 实例；
def create_app(test_config=None):
	# 1、创建 Flask 应用，__name__是一个内置变量，用于确定应用的根路径，影响Flask如何查找资源，如静态文件和模板等‌；
	app = Flask(__name__)
	app.secret_key = 'abcdefg$'
	#print(__name__)
	
	# 2、加载配置文件
	app.config.from_pyfile('conf/config.py')
	#print(app.config.get('SERVER_NAME'))
	
	# 3、数据库配置三、数据库关联 Flask 应用；
	db.init_app(app)
	
	# 4、日志配置二、定义日志配置
	logging.basicConfig(level = logging.INFO,
                    format = "%(asctime)s-%(threadName)s-%(filename)s[lineno:%(lineno)d]-%(levelname)s-%(message)s)",
                    filename = "logs/blog.log",           # 日志写入文件必须开启此项，否则默认输出到标准输出即终端；
                    filemode = 'a'                        # 日志写入文件必须开启此项，否则默认输出到标准输出即终端；
                    )
	
	# 创建测试页面（简单的路由规则和视图函数）
	# 调用此接口可以得知服务是否正常；
	@app.route('/hello')
	def hello():
		# 日志配置三、写入日志
		app.logger.info('日志记录测试')
		return '<h>Hello, World!</h>'
		
	# 测试数据库连接是否正常
	# 调用此接口可以得知数据库连接是否正常；
	@app.route('/GetDB')
	def db_test():
		# 数据库配置四、执行原生SQL
		# 1. 定义SQL(防止 SQL 注入攻击（当使用参数绑定时）)
		sql = text("select version()")
		
		# 2. 执行SQL（注意，修改语句需要提交）
		res = db.session.execute(sql)
		
		# 3. 获取结果(单行结果)
		version_row = res.fetchone() 
		
		# 多行结果处理
		"""
		# 假设查询返回多行
		result = connection.execute(text("SELECT * FROM users"))

		# 获取所有行
		all_rows = result.fetchall()

		# 逐行处理
		for row in all_rows:
			print(row.id, row.name)
		"""
		
		'''
		绑定参数，防止SQL注入的做法：
		# 创建带参数的 SQL
		sql = text("""
			SELECT id, username, age, email 
			FROM users 
			WHERE age >= :min_age 
			AND username LIKE :username_pattern
		""")
		
		# 绑定参数（安全处理）
		params = {
			'min_age': min_age,
			'username_pattern': f"%{username_filter}%"  # 通配符搜索
		}
		
		# 执行查询
		result = db.session.execute(sql, params)
		
		# 获取所有结果为字典列表
		users = [dict(row) for row in result.mappings()]
		# 或者逐行处理
		for row in all_rows:
			print(row.id, row.name)
		
		'''
		
		# 4. 返回查询结果；
		if version_row:
			app.logger.info(f'返回数据记录 {version_row}')
			return f"<h2>{version_row}</h2>"
		else:
			return "404"
			
	# 在 APP 中导入模块并注册蓝图，使用 app.register_blueprint() 导入并注册 蓝图。新的代码放在工厂函数的尾部返回应用之前。
	from . import auth
	app.register_blueprint(auth.bp)

	# 工厂函数返回 APP 实例；
	return app
