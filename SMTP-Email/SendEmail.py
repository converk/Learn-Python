from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

#qq邮箱的SMTP服务器
host_server = 'smtp.qq.com'
#发件人qq号码
sender_qq = '843951249@qq.com'
#授权码
pwd='aepqwvytjggnbejf'
#发件人邮箱
sender_qq_mail = '843951249@qq.com'
#收件人邮箱
receiver = ''

#邮件的正文内容
mail_content = '李安政同学,你好.\
想必你已经收到了数字信号处理的成绩,我知道这一刻我们都不愿面对\
可是,事实在眼前,我认为你可以做的更好,但不是而这一次,而是下一次!,\
我只能对你说,你能做的,岂止于此!\
                        依然相信你的注册中心'
#邮件标题
mail_title = 'HUB系统课程成绩通知单'

#ssl登录
smtp = SMTP_SSL(host_server)
#set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
smtp.set_debuglevel(1)
smtp.ehlo(host_server)
smtp.login(sender_qq, pwd)

msg = MIMEText(mail_content, "plain", 'utf-8')
msg["Subject"] = Header(mail_title, 'utf-8')
msg["From"] = sender_qq_mail
msg["To"] = receiver
smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
smtp.quit()
