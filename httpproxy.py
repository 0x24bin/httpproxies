
import requests
import re
import threading

class startextract(threading.Thread):
    def __init__(self,i):
        super(startextract,self).__init__()
        self.i = i
    def run(self):
        global proxylist,num,z
        url='http://www.xicidaili.com/wt/%s'%(self.i)
        ret=requests.get(url=url,headers=headers,timeout=10)
        proxies=re.findall('<td class=\"country\"><img.*?<td>(.*?)</td>.*?<td>(.*?)</td>',ret.text,re.S)
        for i in proxies:
            proxy = ":".join(tuple(i))
            proxylist.append(proxy)
        num=num+1
        if num ==z:  #判断线程是否全部运行完
            m = len(proxylist)
            data = "\n".join(list(proxylist))
            savefile=open('D:/poxies.dic','wb+')
            savefile.write(data.encode('gbk','ignore'))
            print('*爬取完成，文件位于D:/poxies.dic\n*含有%s个HTTP代理'%m)
            savefile.close()
            num=0
            proxylist.clear()

class startvalidate(threading.Thread):
    def __init__(self,proxylist,s,f):
        super(startvalidate,self).__init__()
        self.proxylist = proxylist
        self.s = s
        self.f = f
    def run(self):
        global num,z
        truelist = []
        for i in proxylist[self.s:self.f]:
            proxies = { "http": "http://"+i, "https": "http://" + i, }
            print('正在验证:%s                       '%i,end='\r')
            try:
                res = requests.get(url='http://ip.chinaz.com/getip.aspx',proxies=proxies,timeout=10)
            except:
                continue
            else:
                truelist.append(i)
        num=num+1
        if num >=z//20:   #   20个为一个线程
            p= len(truelist)
            print('*验证结束,成功%s个HTTP代理.'%p)
            num=0
            proxylist.clear()
            for i in truelist:
                print(i)


def extract():
    global z
    threadss=[]
    z = 2        # 爬取的页数
    for i in range(1,z+1):
            thread = startextract(i)
            threadss.append(thread)
    for t in threadss:
        t.start()
    for t in threadss:
        t.join()
    main()

def validate():
    for line in open('D:/poxies.dic','rt'):
        dic = line.replace('\n','')
        proxylist.append(dic)
    global z
    z =len(proxylist)
    print('*含有%s个HTTP代理\n*开始验证有效性.'%z)
    threads=[]
    for i in range(0,z,20):
        if i < z-20:
            thread = startvalidate(proxylist,i,i+20)
            threads.append(thread)
        else:
            thread = startvalidate(proxylist,i,z)
            threads.append(thread)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    main()


def main():
    command= input('#root:> ')
    if command =='extract':
        extract()
    elif command =='validate':
        validate()
    elif command =='exit':
        exit()
    else:
        print('Please input a true command!')
        main()


if __name__ == '__main__':
    global proxylist,num,z
    num=0
    proxylist = []
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0','Content-Type':'application/x-www-form-urlencoded'}
    logo='''
 _   _  ____  ____  ____    ____  ____  _____  _  _  _  _
( )_( )(_  _)(_  _)(  _ \  (  _ \(  _ \(  _  )( \/ )( \/ )
 ) _ (   )(    )(   )___/   )___/ )   / )(_)(  )  (  \  /
(_) (_) (__)  (__) (__)    (__)  (_)\_)(_____)(_/\_) (__)

 https://kfire.net/ 多线程版本
'''
    print(logo)
    print('  Command:\n  <extract>  - 提取http代理（来源：西刺代理）\n  <validate> - 验证http代理（D:/proxies.dic）\n  <exit>     - 退出\n ----------------------------------------------\n')
    main()
