# 一、导入模块
import functools
from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
	)
from werkzeug.security import check_password_hash, generate_password_hash

# 数据库配置五、导入构造函数 __init__.py 中的变量或属性（这里需要导入与数据库相关的变量 db）；
from sqlalchemy import text
from flaskr import db

# 导入 Flask 应用上下文，current_app 代表了当前的 app 应用；
import logging
#from flask import current_app
# 创建一个 Logger对象；
logger = logging.getLogger(__name__)


# 二、蓝图
# 2.1 创建蓝图（创建一个蓝图实例）
# 蓝图需要知道是在哪里定义的，因此把 __name__ 作为函数的第二个参数。 url_prefix 会添加到所有与该蓝图关联的 URL 前面。
bp = Blueprint('auth', __name__, url_prefix='/auth')

# 2.2 在 APP 中导入模块并注册蓝图

# 2.3 创建第一个视图函数，注册
# @bp.route 关联了 URL /register 和 register 视图函数。当 Flask 收到一个指向 /auth/register 的请求时就会调用 register 视图并把其返回值作为响应。
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
				# 定义SQL
				#sql = text("insert into user (username, password) values ('abc', 'abc')")
				sql = text(
						f"insert into user (username, password) values ('{username}', '{generate_password_hash(password)}')"
						)
				# 执行SQL
				db.session.execute(
				#text(f"insert into user (username, password) values ('{username}', '{generate_password_hash(password)}')")
				sql
				)
				# 提交SQL
				db.session.commit()
				logger.info(f"user {username} is created.")
			except Exception as e:
				# 如果 try 执行失败，则在日志中添加如下错误日志；
				logger.error(f"Create user error: {e}")
			else:
				# 如果 try 中的代码执行成功，即用户创建成功，则返回登陆页面；
				return redirect(url_for('auth.login'))
				
		# 3. 如果 error 值不为 None，即用户输入数据不符合要求，则返回错误；
		flash(error)
	
	# 如果接收到的不是 POST 请求，则返回注册页面；
	return render_template('auth/register.html')
	

# 2.4 创建第二个视图函数，登陆，登陆视图和注册视图函数的原理相同；
@bp.route('/login', methods=('GET', 'POST'))
def login():
	# 如果用户端请求是 POST 请求，则走下面的逻辑；
	if request.method == 'POST':
		# 获取用户端输入的用户名和密码；
		username = request.form['username']
		password = request.form['password']
		# 定义错误为 None
		error = None
		
		# 获取数据库中的用户
		sql = text(f"select * from user where username = '{username}'")
		user = db.session.execute(sql).fetchone()
		
		# 直接通过位置索引获取密码字段
		hashed_password = user[2]

		#print(hashed_password)
		# 如果数据库中没有对应的用户，则为无此用户	
		if user is None:
			#logger.error(f"{user[1]} is Incorrect username.")
			error = f"{username} is not exist!!!"
        # 安全地检查之前使用生成的给定存储的密码哈希是否与给定的密码匹配（参数为之前设置密码的哈希值以及当前的新密码）；
		elif not check_password_hash(hashed_password, password):
			#logger.error("Incorrect password.")
			error = "Incorrect password."
			
		# 如果 error 值为空，说明用户是存在的，则执行如下逻辑；
		if error is None:
			session.clear()
			session['user_id'] = user[0]
			logger.info(f"用户 {username} is login.")
			return redirect(url_for('index'))
			
		flash(error)
		
	# 如果用户请求不是 POST 请求，则返回登陆页面
	return render_template('auth/login.html')
			
# bp.before_app_request() 注册一个 在视图函数之前运行的函数，不论其 URL 是什么。
# load_logged_in_user 检查用户 id 是否已经储存在 session 中，并从数据库中获取用户数据，
# 然后储存在 g.user 中。 g.user 的持续时间比请求要长。 如果没有用户 id ，或者 id 不存在，那么 g.user 将会是 None 。	
@bp.before_app_request
def load_loggged_in_user():
	user_id = session.get('user_id')	
	
	if user_id is None:
		g.user = None
	else:
		g.user = db.session.execute(
									text(f'select * from user where id = "{user_id}"')
									).fetchone()
									
# 2.5 定义注销功能的路由规则及视图函数
# 注销的时候需要把用户 id 从 session 中移除。 然后 load_logged_in_user 就不会在后继请求中载入用户了。
@bp.route('/logout')
def logout():
	# 获取当前登陆用户
	#print(session['user_id'])
	user_id = session['user_id']
	
	sql = text(f"select username from user where id = {user_id}")
	user = db.session.execute(sql).fetchone()
	#print(user[0])
	logger.info(f"user {user[0]} is logout.")
	
	session.clear()
	return redirect(url_for('index'))
		
# 用户登录以后才能创建、编辑和删除博客帖子。在每个视图中可以使用 装饰器 来完成这个工作。
def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))
			
		return view(**kwargs)
	return wrapped_view

