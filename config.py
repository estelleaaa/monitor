class Config(object):
    SECRET_KEY = 'AADSFJLADJALSDFJASLDFJ'
    
    # 数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://estellekk@127.0.0.1:3306/monitor'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

config_map = {
    'develop': DevelopmentConfig,
    'product': ProductionConfig
}