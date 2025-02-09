from random import uniform
import requests
from requests.exceptions import Timeout,ConnectionError
from concurrent.futures import ThreadPoolExecutor
import os
import argparse
def func(referer,name):
    contId = referer.split("_")[1]
    response = requests.get(
    url='https://www.pearvideo.com/videoStatus.jsp?contId={0}&mrd=0.8324133542997358'.format(contId),
    headers={
        'Referer': referer,
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
    }
)
    json = response.json()
    download_flag = (json["videoInfo"]['videos']["srcUrl"]).replace(json["systemTime"], "cont-{0}".format(contId))
    res = requests.get(
      url=download_flag,
      headers={
          "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
      }
      )
    print(download_flag)
    path=os.path.join("videos",name+".mp4")
    file = open(path,"wb")
    file.write(response.content)
    file.close()
    print(name+".mp4"+ "下载成功")
if __name__ == "__main__":
    Number_threads=0
    parser = argparse.ArgumentParser("处理用户输入参数")
    parser.add_argument("-s", "-start", type=int, required=True)
    parser.add_argument("-e", "-end", type=int, required=True)
    parser.add_argument("-l", type=int, required=True)
    args = parser.parse_args()
    if 1<=args.l and args.l<=3:
        if args.l==1:
            print("level1")
            Number_threads=10
        if args.l==2:
            print("level2")
            Number_threads=20
        if args.l==3:
            print("level3")
            Number_threads=30
    else :
        print("输入错误")
with ThreadPoolExecutor(Number_threads) as t:
       for i in range(args.s,args.e+1):
         t.submit(func,"https://www.pearvideo.com/video_{0}".format(i),"video_{0}".format(i))
print("程序已完毕")
