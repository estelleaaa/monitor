from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


# 创建flask的应用对象
app = create_app('develop')

manager = Manager(app)
# 使用migrate绑定app db
Migrate(app, db)
# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
