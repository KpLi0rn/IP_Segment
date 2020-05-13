#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
    Ip_Segment v0.11 python3
    author KpLi0rn 基于原作者rtcatc进行改编
"""
from gevent.pool import Pool
from socket import gethostbyname
from lib.common import store_domains
import xlwt
from tqdm import tqdm
import time
import sqlite3
import os
import sys


# 将域名变成 ip
class Ip_Segment(object):  # 之前由于类的命名和文件一样 所以就一直不行报错

    def __init__(self,*params):
        self.res = params
        self.domains = []
        self.ips = []
        self.segments = []

    # 从文件中进行域名的读取
    def Get_Domains(self):
        path = os.getcwd() + os.sep + "domains.txt"
        store_domains(path)  # 进行剪贴板文件的复制
        with open(path, 'r+') as file:
            content = file.readlines()
            if len(content) == 0:
                sys.stdout.write('[!]请复制域名信息\n')
                sys.exit(0)
            for value in content:
                value = value.strip('\n')  # 删除空行 空格 和换行符号
                value = value.strip()
                if len(value) != 0:
                    self.domains.append(value)

    # 获取域名字典中对应的ip
    def Get_Ips(self):
        for value in self.domains:
            try:
                ip = gethostbyname(value)
                self.ips.append(ip)
            except Exception as e:
                continue

    def Get_Segments(self):
        for ip in self.ips:
            ip = ip.split('.')[0] +'.'+ ip.split('.')[1] +'.'+ ip.split('.')[2]+'.' + "0/24"
            self.segments.append(ip)

    # 数据库的创建
    def Create_Db(self):
        conn = sqlite3.connect('Segment.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE DATA
            (Segment TEXT primary key NOT NULL,
             Weight  INT              NOT NULL );
        ''')
        conn.commit()
        conn.close()

    def Load_Data(self):
        for host in self.segments:
            conn = sqlite3.connect('Segment.db')
            cursor = conn.cursor()
            INSERT_SQL = "INSERT INTO DATA(Segment,Weight) VALUES (\"" + host + "\",1)"  # values 后面跟了一个等号所以报错了
            UPDATE_SQL = "UPDATE DATA SET Weight=Weight+1 WHERE Segment = \"" + host + "\""
            SELECT_SQL = "SELECT Weight FROM DATA WHERE Segment = \"" + host + "\" "
            cursor.execute(SELECT_SQL)
            res = cursor.fetchall()
            if len(res) > 0:
                cursor.execute(UPDATE_SQL)  # 如果已经存在改ip就把权重加1
            else:
                cursor.execute(INSERT_SQL)  # 如果不存在这个ip那么就把host添加进去
            conn.commit()
            conn.close()

    def Show_Data(self):
        conn = sqlite3.connect('Segment.db')
        cursor = conn.cursor()
        SELECT_SQL = "SELECT * FROM DATA"
        info = cursor.execute(SELECT_SQL)
        res = info.fetchall()
        self.res = res

    # 对数据库进行清除
    def Clean(self):
        path = os.getcwd() + os.sep + "Segment.db"
        try:
            os.remove(path)
        except:
            return 0

    # 进度条动画
    def Stat(self):
        status = tqdm(self.domains,ascii=True)
        for _ in status:
            time.sleep(0.01)
            status.set_description("Processing" )
        sys.stdout.write('\n')

    def Show(self):
        for value in self.res:
            print(value[0].ljust(20),value[1])
        sys.stdout.write('\n')

    def Write_Excel(self):
        try:
            filename = xlwt.Workbook()
            sheet = filename.add_sheet('Segment')
            i=0
            for value in self.res:
                sheet.write(i,0,value[0])
                sheet.write(i,1,value[1])
                i+=1
            name = str(time.time()).split('.')[0]
            filename.save('./result/{}.xls'.format(name))
            sys.stdout.write('搜集结果为result/{}.xls\n'.format(name))
        except Exception as e:
            print(e)

    def start(self):
        self.Clean()
        self.Get_Domains()
        self.Stat()
        self.Get_Ips()
        self.Get_Segments()
        self.Create_Db()
        self.Load_Data()
        self.Show_Data()
        self.Show()
        self.Clean()
        self.Write_Excel()

def run():
    ip_segment = Ip_Segment()
    ip_segment.start()

if __name__ == '__main__':
    print("""
        企业IP段信息搜集工具V1.1
                            -----原作者: Poc Sir  改版: KpLi0rn
        1. 增加了对域名重复对判断
        2. 对代码结构进行了改进加快了程序运行对速度,美化了运行界面增加了进度条
        
    """)
    if os.path.exists('./result'):
        pass
    else:
        os.mkdir('./result')
    run()