from __future__ import unicode_literals
import os
import socket
from datetime import datetime
import time
import jinja2
import yagmail
import psutil

EMAIL_USER = '18951828651@163.com'
EMAIL_PASSWORD = 'Liu0821xx'
RECIPIENTS = ['xxliu@alauda.io']


def render(tpl_path, **kwargs):
    path, filename = os.path.split(tpl_path)

    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(**kwargs)


def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i,s in enumerate(symbols):
        prefix[s] =  1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)

    return "%sB" %n


def get_cpu_info():
    '''
    cpu info
    :return:
    '''
    cpu_count = psutil.cpu_count()
    cpu_percent = str(psutil.cpu_percent(interval=1)) + '%'

    return dict(cpu_count=str(cpu_count), cpu_percent=cpu_percent)


def get_memory_info():
    virtual_mem = psutil.virtual_memory()
    mem_total = bytes2human(virtual_mem.total)
    mem_percent = str(virtual_mem.percent) + '%'
    mem_free = bytes2human(virtual_mem.free)
    mem_used = bytes2human(virtual_mem.used)

    return dict(mem_total=str(mem_total), mem_percent=mem_percent,
                mem_free=str(mem_free), mem_used=str(mem_used))


def get_dist_info():
    disk_usage = psutil.disk_usage('/')
    disk_total = bytes2human(disk_usage.total)
    disk_percent = str(disk_usage.percent) + '%'
    disk_free = bytes2human(disk_usage.free)
    disk_used = bytes2human(disk_usage.used)

    return dict(disk_total=str(disk_total), disk_percent=disk_percent, disk_free=str(disk_free),
                disk_used=str(disk_used))


def get_boot_info():
    boot_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(psutil.boot_time()))
    return dict(boot_time=boot_time)


def collect_monitor_data():
    data = {}
    data.update(get_boot_info())
    data.update(get_cpu_info())
    data.update(get_memory_info())
    data.update(get_dist_info())

    return data


def main():
    hostname = socket.gethostname()
    data = collect_monitor_data()
    data.update(dict(hostname=hostname))
    content = render('monitor.html', **data)
    with yagmail.SMTP(user=EMAIL_USER, password=EMAIL_PASSWORD,
                      host='smtp.163.com') as yag:
        for recipent in RECIPIENTS:
            yag.send(recipent, "监控信息1", content)

if __name__ == '__main__':
    main()