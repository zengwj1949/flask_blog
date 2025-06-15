# 一、导入模块
import functools
from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
	)
from werkzeug.security import check_password_hash, generate_password_hash
# 数据库配置五、导入构造函数 __init__.py 中的变量或属性（这里需要导入与数据库相关的变量 db）；
from flaskr import db


# 二、蓝图
# 2.1 创建蓝图（创建一个蓝图实例）
# 蓝图需要知道是在哪里定义的，因此把 __name__ 作为函数的第二个参数。 url_prefix 会添加到所有与该蓝图关联的 URL 前面。
bp = Blueprint('auth', __name__, url_prefix='/auth')

# 2.2 在 APP 中导入模块并注册蓝图

# 2.3 创建第一个视图函数，注册
@bp.route('/register', methods=('GET', 'POST'))
def register():
	# 如果接收到的是 POST 请求，则走如下逻辑；
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		
		# 首先定义错误日志为 None; 
		error = None
		
		# 1. 如果用户输入为空，则重新给 error 变量赋值；
		if not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'
			
		# 2. 如果 error 值为 None，则说明用户输入了用户名和密码，则走下面的逻辑；
		if error is None:
			try:
				db.session.execute(text("insert into user (username, password) values (?, ?)"),
				(username, generate_password_hash(password)),
				)
				app.logger.info(f"user {username} is created.")
			except db.IntegrityError:
				app.logger.error(f"user {username} is already registered.")
			else:
				# 如果 try 中的代码执行成功，即用户创建成功，则返回登陆页面；
				return redirect(url_for('auth.login'))
				
		# 3. 如果 error 值不为 None，即用户输入数据不符合要求，则返回错误；
		flash(error)
	
	# 如果接收到的不是 POST 请求，则返回注册页面；
	return render_template('auth/register.html')
	

# 2.4 创建第二个视图函数，注册
@bp.route('/login', methods=('GET', 'POST'))
def login():
	
			
			
		
		
	

