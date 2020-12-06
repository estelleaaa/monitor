# from . import api

# import smtplib 
# from email.mime.text import MIMEText
# from email.header import Header


# def send_mail(message):
#     sender = 'estelle_day@163.com'
#     receiver = ['estelle.zhong@awkvector.com']
#     subject = 'Warning'
#     username = 'estelle_day@163.com'
#     password = 'estelle0113'
#     msg = MIMEText(message, 'plain', 'utf-8')
#     msg['Subject']=Header(subject, 'utf-8')
#     msg['From'] = 'estelle_day@163.com'
#     msg['To'] = 'estelle.zhong@awkvector.com'
#     smtp = smtplib.SMTP()
#     smtp.connect('smtp.163.com')
#     smtp.login('estelle_day@163.com', 'estelle0113')
#     smtp.sendmail(sender, recever, msg.as_string())
#     smtp.quit()