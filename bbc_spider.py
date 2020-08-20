import time
from collections import defaultdict
from bbc_init import sleeptime,home,headers,rule,res_path
from tools import is_number,clean_str
import requests
import re
import csv
from bs4 import BeautifulSoup

def check_exist(key,val, list_name):
    for i in range(len(list_name[key])):
        if val == list_name[key][i]:
            # print("exist")
            return True

def csv_writer(context):
    f = open(res_path, 'a', encoding='utf-8', newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow(context)

def verify(str):
    if re.search(rule, str):
        # if not re.search("account", str):
            return True


def resolve_url(str):
    if str.startswith("http"):
        if verify(str) == 0:
            url = str
            return url
    elif str.startswith("//"):
        if verify(str) == 0:
            url = "https:" + str
            return url
    elif str.startswith("/"):
        url = home + str
        return url


def find_res(url):
    res = requests.get(url=url, headers=headers)
    res.encoding = 'utf-8'
    bs = BeautifulSoup(res.text, 'html.parser')
    return bs

site_list = defaultdict(list)

def get_res(url, bs, type):
    head = get_head(bs)
    date = get_date(bs)
    image = get_image(bs)
    text = get_text(bs)
    article = [url,type, head, date, image, text]
    return article


def verify_res(bs):
    if get_head(bs) and get_image(bs) and get_date(bs) and get_text(bs):
        return True


def save_res(url,bs, type):
    time.sleep(sleeptime)
    if verify_res(bs) is True:
        article = get_res(url, bs, type)
        csv_writer(article)



def get_head(bs):
    head = str
    for item in bs.find_all(class_='story-body'):
        for h1 in item.find_all("h1"):
            # print(h1.text)
            head = clean_str(h1.text)
    return head


def get_date(bs):
    date = str

    for item in bs.find_all(class_="mini-info-list-wrap"):
        for date2v2 in item.find_all(class_="date date--v2"):
            # print(date.get("data-seconds"))
            date = date2v2.get("data-seconds")
    return date


def get_image(bs):
    image = str

    for item in bs.find_all(class_='story-body__inner'):
        for img in item.find_all("img"):
            # print(img.get("src"))
            image = img.get("src")
    return image


def get_text(bs):
    text = str
    text_list = []
    for item in bs.find_all(class_='story-body__inner'):
        for p in item.find_all("p"):
            # print(p.text)
            text_list.append(clean_str(p.text))
            text = (' '.join(text_list))
    return text


def url2site(url):
    site = url.split("/")[len(url.split("/")) - 1]
    site = site.split("?")[0]
    return site


def site2type(site,context):
    type =site.rstrip(context)
    type=type.rstrip("-")
    return type




def site2context(site):
    if len(site.split("-") )>=1:
        context = site.split("-")[len(site.split("-")) - 1]
        if is_number(context) is True:
            return context
        else:return None
    else:
        return None




def bbc_start(url):
    bs = find_res(url)
    for item in bs.find_all("a"):
        s = item.get("href")
        s = str(s)
        if s is not None:
            if resolve_url(s) is not None:
                url = resolve_url(s)
                site=url2site(url)
                context=site2context(site)
                type=site2type(site,context)
                if check_exist(type,context, site_list) is not True and verify(url) is True:
                    print("site:", site," type:", type," context:",context)
                    if context is not None:
                        save_res(url,bs,type)
                    site_list[type].append(context)
                    # time.sleep(sleeptime)
                    bbc_start(url)

bs=find_res("https://www.bbc.com/news/world-europe-53106444")
# print(get_head(bs))
# print(get_image(bs))
# print(get_date(bs))
# print(get_text(bs))