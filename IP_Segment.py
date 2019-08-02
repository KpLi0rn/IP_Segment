from socket import gethostbyname
import sqlite3
import os
# 将域名变成 ip
domains = []
ips = []
IP_finally = []

# 将每一个域名都转换成对应的ip
def Get_domainsIP(host_list):
    for i in host_list:
        try:
            ip = gethostbyname(i)
            ips.append(ip)
        except:
            pass
    return ips

# 从文件中读取域名
def Read_hosts(path):
    with open(path,'r+') as file:
        content = file.readlines()
        for i in content:
            i = i.strip('\n')     # 删除空行 空格 和换行符号
            i = i.strip()
            if len(i) != 0:
                #print(i)
                domains.append(i)
        return domains

# 将每一个ip转换成ip网段
def IP_Segment(ips):
    for ip in ips:
        ip = ip.split('.')[0] +'.'+ ip.split('.')[1] +'.'+ ip.split('.')[2]+'.' + "0/24"
        IP_finally.append(ip)
    #print(IP_finally)
    return IP_finally

# 创建数据库 数据表
def Create_database():
    conn =sqlite3.connect('Segment.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE DATA
    (Segment TEXT primary key NOT NULL,
     Weight INT               NOT NULL ); ''')
    conn.commit()
    conn.close()

# 向数据表中添加网段 并且设置权重
def Load_database(IP_finally):
    conn = sqlite3.connect('Segment.db')
    c = conn.cursor()
    SELECT_SQL = "SELECT Weight FROM DATA WHERE Segment = \"" + IP_finally + "\" "      # 查询数据需要用到的sql语句
    ADD_SQL = "INSERT INTO DATA(Segment,Weight) VALUES (\"" + IP_finally + "\",1)"   # 添加新的ip网段需要用到的sql语句
    UPDATE_SQL = "UPDATE DATA SET Weight=Weight+1 WHERE Segment = \"" + IP_finally + "\" "   # 增加权重所需要用到的sql语句
    c.execute(SELECT_SQL)
    IP_res = c.fetchall()   # 返回一个二维的数据表
    if len(IP_res) > 0:    # 存在ip网段
        c.execute(UPDATE_SQL)
    else:
        c.execute(ADD_SQL)
    conn.commit()
    conn.close()

# 将sqlite3 里面的数据显示出来
def Show_database():
    conn = sqlite3.connect('Segment.db')
    c= conn.cursor()
    SELECT_SQL = "SELECT * FROM DATA "
    INFO_res=c.execute(SELECT_SQL)
    ALL_res = INFO_res.fetchall()
    #print(ALL_res)
    return ALL_res

# 将最终的网段信息进行导入
def Load_message(IP_finally):
    for ip in IP_finally:
        Load_database(ip)

# 删除数据库
def Delete_databae():
    DB_path = os.getcwd() + os.sep + "Segment.db"
    try:
        os.remove(DB_path)
    except:
        return 0

# 固定字符串的长度
def fix_length(All_res,path):
    max=5
    for value in All_res:
        first = value[0]
        length = len(first)
        if length>=max:
            max=length+1
    for value in All_res:
        i = value[0]
        while len(i) < max:
            i = i + ' '
            if len(i) == max:
                print(i+'   '+str(value[1]))
                with open(path,'a+') as file:
                    file.write(i+'   '+str(value[1]))
                    file.write('\n')
                continue

if __name__ == '__main__':
    Delete_databae()
    Create_database()
    path1 = input("请输入文件的路径")
    path2 = input("请输入输出文件的路径")
    li = Read_hosts(path1)
    ip_new=Get_domainsIP(li)
    Sements = IP_Segment(ip_new)
    Load_message(Sements)
    re=Show_database()
    fix_length(re,path2)
    Delete_databae()
