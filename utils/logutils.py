#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import logging
import time
import logging.handlers
from urllib2 import urlopen

reload(sys) # Python2.5初始化会删除setdefaultencoding()这个方法，需要重新载入
sys.setdefaultencoding('utf8')

# logging.INFO默认为20
def getLogger(filename,level = logging.INFO, logout = False,logsize = 1024*1024):
    curPath = os.path.normpath(os.path.dirname(os.path.abspath(__file__))) #规范化路径
    rootPath = os.sep.join(curPath.split(os.sep)[:-2]) #默认只有三层结构
    logHome = os.path.normpath(os.path.join(rootPath, 'logs')) # 根路径下创建logs文件夹用来存放日志文件
    if not os.path.exists(logHome):
        os.makedirs(logHome)
    logpath = os.path.normpath(os.path.join(logHome, filename)) # 组合成filename.log日志文件的全路径
    if not logpath.endswith('.log'):
        logpath = ('%s.log' % logpath)

    npaiLogger = NPAILogger('')
    npaiLogger.init(logpath, logout, level, logsize)
    return npaiLogger

class NPAILogger(logging.Logger):
    FOMMATER = '[%(asctime)s](%(levelname)s) {pid:%(process)d, tid:%(thread)d, %(filename)s}, %(module)s.%(funcName)s %(lineno)d: %(message)s\r'
    def init(self, logpath, logout, level,logsize):
        if(logout):
            ch = logging.StreamHandler(sys.stdout) # 设置为标准输出流
            ch.setLevel(level) # 设置被处理的信息级别

        if(logout):
            ch.setFormatter(logging.Formatter(NPAILogger.FOMMATER)) # 给handler选择一个格式
            self.addHandler(ch)

        #最多生成3个日志文件，每个文件大小为1M 追加文件模式2^20，.1 .2 .3
        hdlr_Rotating = logging.handlers.RotatingFileHandler(logpath, mode = 'a', maxBytes = logsize, backupCount = 3, encoding = 'utf-8')
        hdlr_Rotating.setFormatter(logging.Formatter(NPAILogger.FOMMATER))
        hdlr_Rotating.setLevel(level)
        self.addHandler(hdlr_Rotating)

if __name__ == '__main__':
    ''' Usage: from logutils import getLogger '''

    # 参数:日志文件名，控制台不可显(False)
    logger = getLogger("logmodule", logging.INFO, False)
    logger1 = getLogger("logmodule1", logging.INFO, True)
    try:
        logger.error('ioerror')
        logger.info('output')
        logger.debug('enter proc')
        raise BaseException('for test')
    except BaseException, e:
        logger1.exception(e)
        print str(e)

