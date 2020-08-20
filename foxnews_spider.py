import time
from collections import defaultdict
from foxnews_init import sleeptime,home
from tools import csv_writer,clean_str


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
    for item in bs.find_all('h1'):

        head = clean_str(item.text)
    return head


def get_date(bs):
    date = str

    for item in bs.find_all("time"):
            date = item.text
    return date


def get_image(bs):
    image = str
    image_list=[]
    for item in bs.find_all("img"):
        # for src in item.get("src"):
            image_list.append(item.get("src"))
        # for img in item.find_all("img"):
        #     # print(img.get("src"))
        #     image = img.get("src")
            image=(" ".join(image_list))
        # print(item.get("src"))
    return image


def get_text(bs):
    text = str
    text_list = []
    for item in bs.find_all(class_='article-body'):
        # print(item.text)
        for p in item.find_all("p"):
            text_list.append(clean_str(p.text))
            text = (' '.join(text_list))
    return text


def url2site(url):
    site = url.lstrip(home+"/")
    site = site.split("?")[0]
    return site


def site2type(site):
    type =site.split("/")[0]
    # type=type.rstrip("-")
    return type




def site2context(site):
    type =site.split("/")[1]
    return type




def find_url(url):
    # save_res(url)
    bs = find_res(url)
    for item in bs.find_all("a"):
        s = item.get("href")
        s = str(s)
        if s is not None:
            if resolve_url(s) is not None:
                url = resolve_url(s)
                site=url2site(url)
                context=site2context(site)
                type=site2type(site)
                if check_exist(type,context, site_list) is not True and verify(url) is True:
                    print("site:", site," type:", type," context:",context)
                    # if context is not None:
                        # save_res(url,bs,type)
                    site_list[type].append(context)
                    # time.sleep(sleeptime)
                    find_url(url)

# bs=find_res("https://www.foxnews.com/politics/tulsa-mayor-implements-federal-exclusion-zone-curfew-ahead-of-trumps-rally")
# print(get_head(bs))
# print(get_text(bs))
# print(get_date(bs))
# print(get_image(bs))