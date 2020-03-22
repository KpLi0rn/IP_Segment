#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# 通过dns服务器来进行ip的判定
import dns.resolver
from gevent.pool import Pool
import pyperclip


# 对复制对域名进行一个存储 到文本中 方便 后续读取
def store_domains(path):
    # import platform
    # system_plateform = platform.system()
    domains = []
    # path = os.path.abspath('../') + '/domains.txt'
    # path = path + '/domains.txt'
    try:
        with open(path, 'w+') as file:
            for value in pyperclip.paste().split('\n'):
                value = value.replace('\r','')
                if len(value) == 0 or value in domains:   # 进行一个重复的判断
                    continue
                domains.append(value)
                file.write(value)
                file.write('\n')
    except Exception as e:
        print(e)


# def test_server(server,dns_servers):
#     resolver = dns.resolver.Resolver(configure=False)
#     resolver.lifetime = resolver.timeout = 5.0
#     try:
#         resolver.nameservers = [server]
#         answers = resolver.query('public-dns-a.baidu.com')
#         # for i in answers.response.answer:   # answer的应答响应的结果是这样的  public-dns-a.baidu.com. 526 IN A 180.76.76.76
#         if answers[0].address != '180.76.76.76':   # 只有加了 address 类型才会变成str 不然就是class 所以这里一定要加address
#             raise Exception('Incorrect DNS response')
#
#         # 防止dns劫持
#         try:
#             bad = resolver.query('KpLi0rn-Not-Existalltest.wjlshare.xyz')
#             if bad[0]:
#                 print('Found Bad DNS Server')
#         except:
#             dns_servers.append(server)
#             # return server
#
#     except Exception as e:
#         print('Found %s Server Failed' % server)
#
# def load_server():
#     print("Validate DNS Server")
#     dns_servers = []
#     pool = Pool()
#     for server in open('../dict/DNSServer.txt').readlines():
#         server = server.strip().strip('\n')
#         if server and not server.startswith('#'):
#             pool.apply_async(test_server,(server,dns_servers))
#         pool.join()
#
#     dns_count = len(dns_servers)
#     print(dns_count)
#
# if __name__ == '__main__':
#     # load_server()
#     store_domains()
#



