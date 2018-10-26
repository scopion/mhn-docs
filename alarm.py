# -*- coding: UTF-8 -*-
import pymongo
import smtplib
import datetime
import re
from datetime import date, timedelta
from email.mime.text import MIMEText
from bson import BSON 
from bson import json_util as jsonb 

mailto_list=['sem','qie@com']
mail_host="smtp.163.com"  #设置服务器smtpserver = 'smtp.163.com'
mail_user="z955"    #用户名
mail_pass="q255"   #口令
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

#今天时间
yesterday = date.today() - timedelta(1)
#datestring = yesterday.strftime('%Y%m%d')
datestring = date.today().strftime('%Y%m%d')
#date = date.today().strftime('%Y-%m-%d')
#print date
print datestring
#主机映射关系,报告汇总文件名
sumdate = date.today().strftime('%Y%m')
ipyingshe = {'3d3a9ed6-36343b2':'114.114.114.114','ad6bc028-3b8776343b2':'114.114.114.114','ecaf607776343b2':'114.114.114.114','09ac53776343b2':'114.114.114.114'}

conn = pymongo.Connection() # 连接本机数据库
# conn = pymongo.Connection(host="192.168.1.202") # 连接指定IP的数据库
db = conn.mnemosyne # 进入指定名称的数据库
# users = db.users # 获取数据库里的 users 集合
# users = db['users'] # 获取数据库里的 users 集合,也可以用字典来获取
u2 = db.daily_stats.find_one({"date":"%s" %datestring}) #查找今天的数据库记录, 查不到时返回 None
detail = list(db.hpfeed.find().sort("_id", pymongo.DESCENDING).limit(1))# 查找数据库最后一条记录
print u2
type(u2)
print detail
print detail[0]
print jsonb.dumps(detail)
#print jsonb.dumps(detail)[4]
#reg = re.compile(r'ection_protocol": "(.*?)",', re.S)
#正则匹配字段,匹配出需要的字段
ident = re.findall(re.compile(r'ident": "(.*?)",', re.S), jsonb.dumps(detail))
#print ident[0]
identfile = ident[0]
#print identfile
#print type(identfile)
protocol = re.findall(re.compile(r'ection_protocol": "(.*?)",', re.S), jsonb.dumps(detail))
port = re.findall(re.compile(r'ocal_port": (.*?), "', re.S), jsonb.dumps(detail))
host = re.findall(re.compile(r'ote_host": "(.*?)"}', re.S), jsonb.dumps(detail))
sensortype = re.findall(re.compile(r'channel": "(.*?)"}', re.S), jsonb.dumps(detail))
dst = ipyingshe["{0}".format(ident[0])]
#定义邮件消息
message = """\
<html><table width="100%%" border="2"><tr><td>攻击时间</td><td>攻击协议</td><td>攻击端口</td><td>远程主机</td><td>目标主机</td><td>蜜罐类型</td></tr><tr><td>['%s']</td><td>%s</td><td>%s</td><td>%s</td><td>['%s']</td><td>%s</td></tr></table></html>
""" %(datestring,protocol,port,host,dst,sensortype)
print message



with open('/opt/mhn/alarmcontrol', 'r') as f:
    crontrol = f.read().strip()
	
print crontrol,"********"
print identfile,"----------"	
print type(crontrol),type(identfile)

if crontrol == identfile:
   print '====';
   u2 = None

if u2:
   print ('existmail')
   send_mail(mailto_list,"mhn alarm","  http://114.114.114.114:8080/ui/attacks/ 查看"+message)
   with open('/opt/mhn/'+ sumdate, 'a') as f:
     f.write(message+'\n')
   with open('/opt/mhn/alarmcontrol', 'w') as f:
     f.write(identfile)
