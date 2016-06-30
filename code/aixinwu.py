# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import pytesseract
import Image as im
import os
from Tkinter import *
import time

if __name__ == '__main__':
    os.environ['REQUESTS_CA_BUNDLE'] = "cacert.pem"
    r=requests.session()

    while True:
        try:
            r.get("https://jaccount.sjtu.edu.cn/jaccount/captcha")
            break
        except:
            time.sleep(1000)

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36"
    }
    url="http://aixinwu.sjtu.edu.cn/index.php/login"

    soup=BeautifulSoup(r.get(url,headers=headers).content,"html.parser")
    url=soup.meta.attrs['content'][7:] #获得确切的url
    print(url)

    soup=BeautifulSoup(r.get(url,headers=headers).content,"html.parser")
    headers['Referer'] = url

    with open("jaccount.json","r") as f:
        temp=json.load(f)
        jaccount=temp["jaccount"]
        passwd=temp["passwd"]

    while True:
        captcha_url = "https://jaccount.sjtu.edu.cn/jaccount/captcha"
        with open("captcha.jpg","wb") as f:
            f.write(r.get(captcha_url,headers=headers).content)
        img =im.open('captcha.jpg')
        img.load()
        captcha_list = pytesseract.image_to_string(img)
        captcha_list=list(str(captcha_list))
        captcha_list=filter(lambda x:x.isalpha() or x.isdigit(),captcha_list)
        captcha=''.join(captcha_list)
        print(captcha)
        print(len(captcha))

        data = {
              'sid':soup.find("input", attrs={'name':'sid'}).attrs['value'],
              'returl':soup.find("input", attrs={'name':'returl'}).attrs['value'],
              'se':soup.find("input", attrs={'name':'se'}).attrs['value'],
              'v':soup.find("input", attrs={'name':'v'}).attrs['value'],
              'captcha':captcha,
              'user':jaccount,
              'pass':passwd,
              'imageField.x':"55",
              'imageField.y':"3"
        }
        login_url = "https://jaccount.sjtu.edu.cn/jaccount/ulogin"
        req_post1=r.post(login_url,data=data,headers=headers)

        ptn = re.compile(r'\'https.*\'')
        next_url = ptn.findall(req_post1.content)[0][1:-1]
        if next_url.find("loginfail")!=-1: #fail,
            print("fail")
        else:
            # headers['Referer'] = url
            break

    print(next_url)
    req_get=r.get(next_url)
    soup=BeautifulSoup(req_get.content,"html.parser")
    element=soup.meta.attrs['content'][7:]
    print("element"),   # http://aixinwu.sjtu.edu.cn/jaccount/redirect.php
    print(element)
    req_get=r.get(element)
    print(req_get.content)

    reobj=re.compile("(?<=\*).*(?=\*&nbsp)")
    result=reobj.findall(req_get.content)

    reobj=re.compile("您已连续登陆&nbsp;\d+&nbsp;天")
    result1=reobj.findall(req_get.content)
    result1=result1[0].replace("&nbsp;"," ")

    reobj=re.compile("您剩余的爱心币：.*(?=<span)")
    result2=reobj.findall(req_get.content)
    result2=result2[0].replace("&nbsp;"," ")

    root=Tk()
    root.title("爱心屋签到脚本")
    root.geometry('300x200')

    t = Text(root)
    t.insert(1.0,result[0]+"\n")
    t.insert(END,result2+"\n")
    t.insert(END,result1+"\n")
    t.pack()
    root.mainloop()
