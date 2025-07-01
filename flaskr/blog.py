# 一、导入模块
from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required

# 导入数据库模块
from sqlalchemy import text
from flaskr import db

# 导入日志模块
import logging
#from flask import current_app
# 创建一个 Logger对象；
logger = logging.getLogger(__name__)


# 二、蓝图
# 2.1 创建蓝图
bp = Blueprint('blog', __name__)

# 2.2 在 app 中导入模块并注册蓝图

# 2.3 定义默认页面的路由规则和视图函数
# 默认页面会显示所有博客帖子；
@bp.route('/')
def index():
	# 1. 获取数据；
	# 定义SQL
	sql = text("""
			select p.id, title, body, created, author_id, username
			from post p join user u on p.author_id = u.id
			order by created desc
			""")
	
	# 执行SQL
	posts = db.session.execute(sql).fetchall()
	
	# 2. 把数据传递给前端页面进行展示；
	return render_template('blog/index.html', posts=posts)
	
	
# 2.4 定义创建博客的路由规则和视图函数
# create 视图与 register 视图原理相同。要么显示表单，要么发送内容 已通过验证且内容已加入数据库，或者显示一个出错信息。	
@bp.route('/create', methods=('GET', 'POST'))
def create():
	# 如果 HTTP 请求是 POST 请求，则走下面的逻辑；
	if request.method == 'POST':
		# 获取请求的数据
		title = request.form['title']
		body = request.form['body']
		
		error = None
		
		# 如果 title 为空，则重新定义错误信息
		if not title:
			error = 'Title is required.'
			
		if error is not None:
			flash(error)
		else:
			sql = text(f"insert into post (title, body, author_id) values ({title}, {body}, {g.user['id']})")
			db.session.execute(sql)
			db.session.commit()
			
			return redirect(url_for('blog.index'))
		
	
	# 如果 HTTP 请求不是 POST 请求，则返回创建博客的页面
	return render_template('blog/create.html')

# update 和 delete 视图都需要通过 id 来获取一个 post ，并且 检查作者与登录用户是否一致。
# 为避免重复代码，可以写一个函数来获取 post ， 并在每个视图中调用它。
def get_post(id, check_author=True):
	'''
	通过 id 来获取一个 post
	
	:param id:
	:param check_author:
	:return 
	'''
	sql = text(f"select p.id, title, body, created, author_id, username from post p JOIN user on p.author_id = u.id where plid = {id}")
	post = db.session.execute(sql).fetchone()
	
	if post is None:
		# abort() 会引发一个特殊的异常，返回一个 HTTP 状态码。
		abort(404, f"Post id {id} doesn't exist.")
		
	if check_author and post['author_id'] != g.user['id']:
		abort(403)
	
	return post 

# 2.5 定义更新的路由规则和视图函数
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
	'''
	传入博客ID号，主要是用来区分博客文章;
	
	:param id: 
	:return:
	'''
	# 获取函数的返回值；
	post = get_post(id)
	
	# 如果请求方式是 POST，则走如下逻辑：
	if request.method == "POST":
		title = request.form['title']
		body = request.form['body']
		error = None
		
		# 如果标题不存在，则重新定义错误信息
		if not title:
			error = 'Title is required.'
			
		if error is not None:
			flash(error)
			
		else:
			sql = text(f"update post set title = {title}, body = {body} where id = {id}")
			db.session.execute(sql)
			db.session.commit()
			return redirect(url_for('blog.index'))
			
	
	# 如果请求方式不是 POST，则返回更新页面；
	return render_template('blog/update.html', post=post)


# 2.6 定义路由规则及删除视图函数
@bp.route('/<int:id>/delete', methods=('POST', ))
@login_required
def delete(id):
	get_post(id)
	db.session.execute(text(f'delete from post where id = {id}'))
	db.session.commit()
	
	return redirect(url_for('blog.index'))

















	
	
	
	
	
	
	
	
	
