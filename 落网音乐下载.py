#目标:http://www.luoo.org/music.php?id=01
import re
from multiprocessing import Pool
import requests

head={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

def gethtml(url):
    resp=requests.get(url,headers=head)
    resp.encoding=resp.apparent_encoding
    #用上面的encoding把code类型转换
    return resp.text

def getlink(resp):
    pattern=re.compile('<li>.*?class.*?>(.*?)</a>.*?href="(.*?)".*?</li>',re.S)
    try:
        links=re.findall(pattern,resp)
        for item in links:
            yield {'曲名':item[0][4:],'link':item[1][5:]}
        #以上的getlink(resp)就是一个生成器
        #此处能否将yield{}  更改为  yield []   岂不是更方便???
    except:
        print('??期无下载链接')
        pass
def dload(quming,link):
    try:
        with open(r'C:\PycharmProjects\temp\temp项目\xiazaigequ\{}.mp3'.format(quming),'wb') as f:
            resp=requests.get(link,headers=head,stream=True).content
            f.write(resp)
            print("{}已下载".format(quming)+'\n')
    except:
        print('??期的{}未下载'.format(quming))
        pass

def main(qishu):
    url = 'http://www.luoo.org/music.php?id={}'.format(qishu)
    resp=gethtml(url)
    for item in getlink(resp):
        #用for i in 生成器,会自动将生成器的所有值,全部过一遍
        quming = item['曲名']
        link = item['link']
        dload(quming,link)

if __name__=='__main__':
    pool = Pool()
    pool.map(main,[i for i in range(550,551)])
    pool.close()
    pool.join()


#需要添加功能,1\提醒未下载的期数和曲名,2将不同期数放在不同的文件夹
#未能实现指定期数, qishu=i
#未能理解pool
