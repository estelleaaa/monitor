from flask import Blueprint

# 创建蓝图对象
api = Blueprint('api', __name__)

from . import demo, function, action