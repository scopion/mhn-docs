# -*- coding: utf-8 -*-
import smtplib
import datetime
import time
import re
from datetime import date, timedelta
from email.mime.text import MIMEText
import os

today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lastfile = lastMonth.strftime("%Y%m")
print lastMonth.strftime("%Y%m")

mailto_list=['qwerqtwrt@ertwertywe.com','wertwerga@ertwehasd.com']
mail_host="smtp.163.com"  #设置服务器smtpserver = 'smtp.163.com'
mail_user="zwerqwer55"    #用户名
mail_pass="sfasdfa5"   #口令
mail_postfix="163.com"  #发件箱的后缀
#定义发邮件方法
def send_mail(to_list,sub,content):
    me="mhn"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='html',_charset='UTF-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False


 
filename = '/opt/mhn/' + lastfile

print filename
if os.path.exists(filename):
    with open(filename, 'r') as f:
      message = f.read()
      print message
      send_mail(mailto_list,"mhn summary","  http://114.114.114.114:8080/ui/attacks/ 查看"+message)

else:
    print "no alarm summary"
    send_mail(mailto_list,"上月没有蜜罐报警事件","  上月没有蜜罐报警事件")
