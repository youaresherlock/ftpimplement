# coding: utf-8

import os
import socket
import ftplib
from tools import getConf
from logutils import getLogger

logger = getLogger("ftp")

con = Canon('xxxx.xxxx.xxxx.xxxx', 21, 'ubuntu', '...................')

class Canon():
    '''
    Controls the amount of debugging output printed
    0  - produces no debugging output
    1  - produces a moderate amount of debugging output
    2+ - produces the maximum amount of debugging output
    '''

    debuglevel = 2
    timeout = 30
    appConf = getConf()
        
    def __init__(self, host, port, username, password):
        print host,port,username,password
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.f = None
        self._initftp()
        
    def _initftp(self):
        try:
            self.f = ftplib.FTP()
            self.f.set_pasv(1)
            self.f.connect(host=self.host, port=self.port, timeout=self.timeout)
            logger.debug("Success on Connect To FTP Server: %s:%s" % (self.host, self.port))
            self.f.login(user=self.username, passwd=self.password)
            print self.f.getwelcome()
            logger.debug("Success on Login To FTP Server: %s:%s" % (self.host, self.port))
        except (socket.error, socket.gaierror):
            print "Error: cannot reach %s" % (self.host)
            logger.error("Fail on Connect To FTP Server: %s:%s" % (self.host, self.port))
        except ftplib.error_perm:
            print "Error: cannot login"
            logger.error("Fail on Login To FTP Server: %s:%s" % (self.host, self.port))
            self._done()

    def _done(self):
        if self.f:
            try:
                self.f.quit()
                logger.debug("Success on Quit From FTP Server: %s:%s" % (self.host, self.port))
            except Exception, e:
                logger.debug("Success on Close Connection to FTP Server: %s:%s - %s" % (self.host, self.port, str(e)))
                self.f.close()
            finally:
                logger.debug("Force Close Connect To FTP Server: %s:%s" % (self.host, self.port))
                self.f = None

    def _delete_file(self, file_path):
        if os.path.isfile(file_path):
            os.unlink(file_path)

    def mkdir(self, dirname):
        ret = True
        try:
            self.f.mkd(dirname)
        except Exception, e:
            ret = False
            print str(e)
        return ret

    def upload(self, localpath, dirname=''):
        ret = False
        try:
            filename = os.path.basename(localpath)
            filepath = os.path.join(dirname, filename)
            self.f.storbinary('STOR %s' % filepath, open(localpath, 'rb'))
            ret = True
        except ftplib.error_perm, e:
            logger.error("Fail On Upload File %s to %s:%s - %s" % (localpath, self.host, self.port, str(e)))
        except Exception, e:
            logger.error("Fail On Upload File %s to %s:%s - %s" % (localpath, self.host, self.port, str(e)))
            print str(e)
        return ret

    def download(self, remotepath, localpath):
        ret = False
        try:
            self.f.retrbinary('RETR %s' % remotepath, open(localpath, 'wb').write)
            ret = True
        except ftplib.error_perm, e:
            self._delete_file(localpath)
            logger.error("Fail On Download File %s to %s - %s" % (remotepath, localpath, str(e)))
        except Exception, e:
            self._delete_file(localpath)
            logger.error("Fail On Download File %s to %s - %s" % (remotepath, localpath, str(e)))
        return ret

    def delete(self, remotefilename):
        ret = False
        try:
            self.f.delete(remotefilename)
            ret = True
        except ftplib.error_perm, e:
            logger.error("Fail On Delete File: %s:%s:%s - %s" % (self.host, self.port, remotefilename, str(e)))
        except Exception, e:
            logger.error("Fail On Delete File %s to %s:%s - %s" % (remotefilename, self.host, self.port, str(e)))
            print str(e)
        return ret

    def list(self,dirname = ''):
        ret = []
        dirs = self.f.nlst(dirname)
        for dir in dirs:
            try:
                size = self.f.size(dir)
                type = "file"
            except Exception, e:
                type = "dir"
                size = 0
            ret.append({
                "filename": dir,
                "filesize": size,
                "type": type
            })
        return ret


def main():
	con.download('/home/ubuntu/Clarence/zookeeper/zookeeperinstalllocation/conf/zoo.cfg',
		'E:\\download\\test.json')

if __name__ == '__main__':
	main()