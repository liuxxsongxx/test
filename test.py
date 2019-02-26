import yagmail
yg = yagmail.SMTP(user='xxliu@alauda.io',password='Liuxx@0821;',host='smtp.alauda.io')
yg.send(to='18951828651@163.com',subject='小旭测试',contents='测试2')