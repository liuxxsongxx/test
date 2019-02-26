import yagmail
yg = yagmail.SMTP(user='18951828651@163.com',password='Liu0821xx',host='smtp.163.com')
yg.send(to='xxliu@alauda.io',subject='小旭测试',contents='测试2')
