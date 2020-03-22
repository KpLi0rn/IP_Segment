#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pyperclip
# 对复制对域名进行一个存储 到文本中 方便 后续读取
def store_domains(path):
    domains = []
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




