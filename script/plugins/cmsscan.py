import requests
import json, hashlib
import gevent
from gevent.queue import Queue
import time
import os


class CMSscan(object):
    def __init__(self, url):
        self.q = Queue()
        self.url = url.rstrip("/")
        fp = open(os.path.dirname(__file__) + '\\..\\data\\data.json', 'r', encoding='gbk')
        webdata = json.load(fp)
        for i in webdata:
            self.q.put(i)
        fp.close()
        self.nums = "web指纹总数:%d" % len(webdata)
        # print("web指纹总数:%d"%len(webdata))

    def _GetMd5(self, body):
        md5 = hashlib.md5()
        md5.update(body)
        return md5.hexdigest()

    def _clearQueue(self):
        while not self.q.empty():
            self.q.get()

    def _worker(self):
        data = self.q.get()
        scan_url = self.url + data["url"]
        try:
            r = requests.get(scan_url, timeout=20)
            if (r.status_code != 200):
                return
            rtext = r.text
            if rtext is None:
                return
        except:
            rtext = ''

        if data["re"]:
            if (rtext.find(data["re"]) != -1):
                result = data["name"]
                # print("CMS:%s 判定位置:%s 正则匹配:%s" % (result, scan_url, data["re"]))
                self.resultout = "CMS:%s 判定位置:%s 正则匹配:%s" % (result, scan_url, data["re"])
                self._clearQueue()
                return True
        else:
            md5 = self._GetMd5(rtext)
            if (md5 == data["md5"]):
                result = data["name"]
                # print("CMS:%s 判定位置:%s md5:%s" % (result, scan_url, data["md5"]))
                self.resultout = "CMS:%s 判定位置:%s md5:%s" % (result, scan_url, data["md5"])
                self._clearQueue()
                return True

    def _boss(self):
        while not self.q.empty():
            self._worker()

    def outputdatalen(self):
        return self.nums

    def outputreuslt(self):
        return self.resultout

    def runtime(self, maxsize=100):
        start = time.clock()
        allr = [gevent.spawn(self._boss) for i in range(maxsize)]
        gevent.joinall(allr)
        end = time.clock()
        # print("执行用时: %f s" % (end - start))
        self.timeout = "执行用时: %f s" % (end - start)
        return self.timeout


# if __name__ == '__main__':
#     url = input("url:")
#     g = CMSscan(url)
#     g.runtime(100)
#     totalnums = g.outputdatalen()
#     resutltre = g.outputreuslt()
#     timeo = g.runtime()
#     print(totalnums)
#     print(resutltre)
#     print(timeo)

def cmsscan(url):
    g = CMSscan(url)
    g.runtime(100)
    totalnums = g.outputdatalen()
    resutltre = g.outputreuslt()
    timeo = g.runtime()
    print(totalnums)
    print(resutltre)
    print(timeo)
    return [totalnums, resutltre, timeo]
