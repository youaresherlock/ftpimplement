# coding: utf-8
import os
import sys
import json

def getConf():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # assetproject\src\Asset
    target_path = os.path.join(base_path, 'conf/conf.json')
    ret = None
    try:
        f = file(target_path)
        ret = json.load(f)
    except Exception, e:
        print str(e)
    return ret #将f配置文件对象反序列化

