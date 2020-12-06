from . import api

from datetime import datetime
# import os 
# import time 
from flask import render_template
import psutil 
# import socket
import platform 

import smtplib 
from email.mime.text import MIMEText
from email.header import Header

# 发送邮件
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


@api.route('/sys')
def sys():
    # 现在时间
    now_time = datetime.now()
    #开机时间
    start_time=datetime.fromtimestamp(psutil.boot_time())
    syss = {
        'system':platform.system(), #操作系统 Darwin
        'version':platform.version(), # 系统版本号 	Darwin Kernel Version 19.5.0: Tue May 26 20:41:44 PDT 2020; root:xnu-6153.121.2~2/RELEASE_X86_64
        'architecture':platform.architecture(), # 操作系统的位数 	('64bit', '')
        'machine':platform.machine(), # 计算机类型 	x86_64
        'processor':platform.processor(), # 处理器信息 	i386
        'run_time':str(now_time-start_time).split('.')[0] # 运行时间
    }
    return render_template('sys.html', now_time=str(now_time).split('.')[0], start_time=start_time, syss=syss)


@api.route('/cpu')
def cup():
    cpu={
        'p_CPU':psutil.cpu_count(logical=False), # 默认 logical=True
        'CPU':psutil.cpu_count(),
        'averageload_1':psutil.cpu_percent(interval=1), # cpu 使用率 最近一分钟平均负载 
        'averageload_5':psutil.cpu_percent(interval=5),
        'averageload_15':psutil.cpu_percent(interval=15),
        'user':psutil.cpu_times_percent().user, # 用户使用cpu时间 百分比
        'system':psutil.cpu_times_percent().system, # 系统内核使用cpu时间 百分比
        'idle':psutil.cpu_times_percent().idle, # 空闲 百分比
        'nowfrequency':psutil.cpu_freq().current, # 正在运行频率
        'minfrequency':psutil.cpu_freq().min, # 最小运行频率
        'maxfrequency':psutil.cpu_freq().max # 最大运行频率
    }
    mes = 'cpu使用超过阈值'
    # print(mes)
    if cpu['averageload_1']>=50:
        send_mail(mes)
    return render_template('cpu.html', cpu=cpu)

    

@api.route('/ram')
def ram(): # round()返回浮点数的四舍五入值 保留2位小数
    ram = {
        'memorySize':round(psutil.virtual_memory().total/(1024**3),2),
        'available':round(psutil.virtual_memory().available/(1024**3),2),
        'percent':psutil.virtual_memory().percent,
        'used':round(psutil.virtual_memory().used/(1024**3),2),
        'free':round(psutil.virtual_memory().free/(1024**3),2)
    }
    return render_template('ram.html', ram=ram)

@api.route('/disk')
def disk():
    # disks = psutil.disk_partitions()
    disks={
        'total':round(psutil.disk_usage('/').total/(1024**3),2),
        'used':round(psutil.disk_usage('/').used/(1024**3),2),
        'free':round(psutil.disk_usage('/').free/(1024**3),2),
        'percent':psutil.disk_usage('/').percent
    }
    
    # disks = psutil.disk_usage('/')
    return render_template('disk.html', disks=disks)

@api.route('/process')
def process():
    pid = psutil.pids()[1:]
    # print(pid,'this is pid............')
    processes = []
    for i in pid:
        try:
            p=psutil.Process(i) # 获取指定进程信息
            # 进程名字 进程状态  进程创建时间 进程使用的内存百分比 
            processes.append((p.name(), p.status(), datetime.fromtimestamp(p.create_time()), round(p.memory_percent(), 3)))
        
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return render_template('process.html', processes=processes)
