# 一、导入模块
from flask import Flask

# 二、创建 Flask 实例
app = Flask(__name__)

# 三、创建路由规则及视图函数
@app.route('/')
def hello():
	return 'Hello, World!'

# 四、运行 Flask 项目
if __name__ == "__main__":
	app.run()
	

