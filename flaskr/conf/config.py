# 服务器监听地址和端口
SERVER_NAME = '127.0.0.1:9000'
#SERVER_NAME = '172.16.1.100:9000'
DEBUG = True

# DB MySQL数据库配置
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://test:0bee89b07@192.168.111.128:3306/blog_dev?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = "False"

# Redis
REDIS_URL = "redis://:abcdef123@192.168.111.128:6379/0"
'''
# 连接池配置
REDIS_MAX_CONNECTIONS = 100      # 连接池最大连接数
REDIS_IDLE_TIMEOUT = 30          # 空闲连接超时(秒)
REDIS_CONNECT_TIMEOUT = 5        # 连接超时(秒)
REDIS_READ_TIMEOUT = 10          # 读操作超时(秒)
REDIS_WRITE_TIMEOUT = 10         # 写操作超时(秒)
REDIS_RETRY_ON_TIMEOUT = True    # 超时自动重试
REDIS_HEALTH_CHECK_INTERVAL = 30 # 健康检查间隔(秒)
# 连接池回收策略
REDIS_POOL_RECYCLE = 3600        # 连接回收时间(秒)
'''
