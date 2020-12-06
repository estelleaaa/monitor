from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy 
from flask_bootstrap import Bootstrap

# 数据库
db = SQLAlchemy()
bootstrap=Bootstrap()



# 工厂模式
def create_app(config_name):


    app = Flask(__name__)
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 使用app初始化db
    db.init_app(app)
    bootstrap.init_app(app)

    from app import api
    app.register_blueprint(api.api, url_prefix='/api/v1.0')

    return app


# from app import routes