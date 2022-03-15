# 创建应用实例
import sys
from flask import render_template,redirect,request,url_for,session,json
from itemcf.api import *
from wxcloudrun import app

# 启动Flask Web服务
if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2])
