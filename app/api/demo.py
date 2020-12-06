from . import api
from datetime import datetime
from flask import request, jsonify
import platform
import psutil 


import smtplib 
from email.mime.text import MIMEText
from email.header import Header



def send_mail(message):
    sender = 'estelle_day@163.com'
    receiver = ['estelle.zhong@awkvector.com']
    subject = 'Warning'
    username = 'estelle_day@163.com'
    password = 'YOBZHMVELUFAUWPV'    # 授权码
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject']=Header(subject, 'utf-8')
    msg['From'] = 'estelle_day@163.com'
    msg['To'] = 'estelle.zhong@awkvector.com'
    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


@api.route('/sysinfo', methods=['POST'])
def sysinfo():
    # # 现在时间
    now_time = datetime.now()
    #开机时间
    start_time=datetime.fromtimestamp(psutil.boot_time())
    sys = {
        'now_time':now_time,
        'start_time':start_time,
        'system':platform.system(), #操作系统 Darwin
        'version':platform.version(), # 系统版本号 	Darwin Kernel Version 19.5.0: Tue May 26 20:41:44 PDT 2020; root:xnu-6153.121.2~2/RELEASE_X86_64
        'architecture':platform.architecture(), # 操作系统的位数 	('64bit', '')
        'machine':platform.machine(), # 计算机类型 	x86_64
        'processor':platform.processor(), # 处理器信息 	i386
        'run_time':str(now_time-start_time).split('.')[0] # 运行时间
    }
    return sys

# 查询cpu使用率
@api.route('/cpuinfo', methods=['POST'])
def cpuinfo():
    '''
    interval : 1 5 15
    percpu: 0 1(0 表示计算每个cpu的使用率，1表示计算总cpu使用率)
    usage = psutil.cpu_percent(interval,percpu)
    '''
    
    args = request.args
    interval = int(args.get('interval'))
    percpu_num = int(args.get('percpu_num'))
    
    if percpu_num==0:
        usage = psutil.cpu_percent(interval=interval,percpu=True)
    else:
        usage = psutil.cpu_percent(interval=interval, percpu=False)
    usageinfo={
        'usage':usage,
        'cpu':psutil.cpu_count(),
        'idle':psutil.cpu_times_percent().idle,
        'cur_frequency':psutil.cpu_freq().current,
        'max_freq':psutil.cpu_freq().max,
        'min_freq':psutil.cpu_freq().min,
        'user':psutil.cpu_times_percent().user,
        'system':psutil.cpu_times_percent().system
    }
    # if usageinfo['usage']>=70:
    #     message = 'cpu使用率已达到 %s %%' % usageinfo['usage']
    #     send_mail(message)
        
    return (usageinfo)


# 内存
@api.route('/raminfo',methods=['POST'])
def raminfo():
    raminfo = {
        'memorySize':round(psutil.virtual_memory().total/(1024**3),2),
        'available':round(psutil.virtual_memory().available/(1024**3),2),
        'percent':psutil.virtual_memory().percent,
        'used':round(psutil.virtual_memory().used/(1024**3),2),
        'free':round(psutil.virtual_memory().free/(1024**3),2)
    }  
    # if raminfo['percent']>=80:
    #     message = '内存使用率已到达 %s %%' % raminfo['percent']
    #     send_mail(message)
    # return raminfo

# 磁盘信息
@api.route('/diskinfo',methods=['POST'])
def diskinfo():
    diskinfo={
        'total':round(psutil.disk_usage('/').total/(1024**3),2),
        'used':round(psutil.disk_usage('/').used/(1024**3),2),
        'free':round(psutil.disk_usage('/').free/(1024**3),2),
        'percent':psutil.disk_usage('/').percent
    }
    # if diskinfo['percent']>=80:
    #     message = '磁盘使用率已达到 %s %%' % diskinfo['percent']
    #     send_mail(message)
    return diskinfo



# 进程信息
@api.route('/processinfo', methods=['post'])
def processinfo():
    # 本机进程 0 1 拒绝访问 切片进程pid=2开始
    pid = psutil.pids()[1:]
    processes = []
    for i in pid:
        try:
            p = psutil.Process(i) # 获取进程信息
            processes.append((p.name(), p.status(), datetime.fromtimestamp(p.create_time()), round(p.memory_percent(), 3)))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return jsonify(processes)
