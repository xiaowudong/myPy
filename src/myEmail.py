#!/usr/bin/python 
# coding: utf-8

import os
import sys
import smtplib
import hashlib
import json
import urllib.request
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

class tools:
    def send_sms(self, tos, message):
        md5 = hashlib.md5()
        smsApi = 'http://172.16.10.171:9037/notifier-web/notification'
        scretKey = '038a6d27a716d1e1472b1eded07c385d'
        data = {
            'content': json.dumps( {'sms_msg': '%s%s' % (message, '【云宝金服】'.decode('utf-8'))} ),
            'sign': '038a6d27a716d1e1472b1eded07c385d',
            'username': 'notifier_user',
            'recipients': tos.encode('utf-8'),
            'notifyRuleName': '云宝平台短信通知',
            'extNo': '1'
        }
        #print 'notifyRuleName', isinstance(data['notifyRuleName'], str)
        #print 'username', isinstance(data['username'], str)
        #print 'recipients', isinstance(data['recipients'], str)
        #print 'extNo', isinstance(data['extNo'], str)
        #print 'scretKey', isinstance(scretKey, str)
        md5.update( data['username'] + '%s' % data['notifyRuleName'] + data['recipients'] + scretKey + data['extNo'] )
        data['sign'] = md5.hexdigest()
        data = json.dumps(data)
        request = urllib.request.Request(smsApi, data=data)
        request.add_header('Content-Type', 'application/json;charset=UTF-8')
        urllib.request.urlopen(request)
        #res = urllib2.urlopen(request)
        #return res

    def send_mail(self, to_list, to_cc,sub,content, mFile=False):
        to_list = to_list.split(',')
        if to_cc:
            to_cc = to_cc.split(';')
            to_list = to_list + to_list
        mail_host = "smtp.263xmail.com"
        mail_user = 'yunpalsys@hengbao.com'
        mail_pass = 'hengbao123'
        mail_address = 'yunpalsys@hengbao.com'
        #mail_port = 465
        mail_port = 25
        me = mail_address
        msg = MIMEMultipart()
        cont = MIMEText(content,_subtype='plain',_charset='utf-8')
        msg.attach(cont)
        if mFile :
            files = mFile.split(';')
            for f in files:
                att = MIMEText(open(f, 'rb').read(), 'base64', 'utf-8')
                att["Content-Type"] = 'application/octet-stream'
                att["Content-Disposition"] = 'attachment; filename="%s"' % os.path.basename(f)
                msg.attach(att)
        msg['Subject'] = Header(sub,'utf-8')
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            #s = smtplib.SMTP_SSL(mail_host, mail_port)
            s=smtplib.SMTP()
            s.connect(mail_host, mail_port)
            #s.set_debuglevel(1)
            s.starttls()
            s.login(mail_user, ''.join(mail_pass.split('_')))
            s.sendmail(me, to_list , msg.as_string())
            s.close()
            return True
        except Exception :
            return 

    def debug_log(self, logFile, log):
        fh = open(logFile, 'a')
        fh.write(log + '\n')
        fh.close()
        return

if __name__ == '__main__':
    if len(sys.argv) == 6 :
        (to_list, cc_list, sub, content, sendFile) = sys.argv[1:]
        #print to_list, cc_list, sub, content, sendFile 
        content = content.split('\\n')
        content = '\n'.join(content)
        fh = open('/tmp/mail.log', 'a')
        fh.write(content)
        fh.close()
        tools = tools()
        tools.send_mail(to_list, cc_list, sub, content, sendFile)
    else :
        print ('''Usage:
%s 'to_list' 'cc_list' 'sub' 'content' 'sendFile' 
  - to_list: xxx@xxx.com;yyy@xxx.com
  - cc_list: www@xxx.com;zzz@xxx.com
  - sub: 标题
  - content: 正文
  - sendFile: 附件1;附件2''' % sys.argv[0])
