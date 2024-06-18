import requests
import re
from lxml import etree
import os
import time
import random
import math
from fake_useragent import UserAgent
import pandas as pd
#//div[@id="search_result_container"]//a/@data-ds-appid
def fetch_url(url, headers):
    try:
        response = session.get(url, headers=headers,stream=True)
        response.raise_for_status()  # 如果响应状态码不是 200，就抛出异常
    except requests.RequestException as e:
        print(f"请求失败，错误信息：{e}")
        print("正在退出程序！")
        exit()
        # return None
    else:
        print("获取网页成功！")
        response.encoding = response.apparent_encoding
        return response
def user_chooes(game_count):
    print("共获取到" + str(game_count) + "个游戏")
    print("共有" + str(math.ceil(game_count / 25)) + "页数据")
    print("请输入爬取的页数，输入除数字外的任意字符退出！")
    user_input_ = input("请输入爬取的页数：")
    if user_input_.isalnum():
        num_int = int(user_input_)
        if 1 <= num_int <= math.ceil(game_count):
            print("您的选择是：" + str(num_int)+"页")
            game_page(num_int)
        else:
            print("输入错误，请重新输入！")
            user_chooes(game_count)
    else:
        print("感谢您的使用！")
        exit()

all_game = []

def game_page(number):
    for i in range(1,number+1):
        game_name = []
        game_date = []
        game_href = []
        game_img = []
        url_page = "https://store.steampowered.com/search/?page="+str(i)+"&ndl=1"
        url_html = fetch_url(url_page,headers)
        xpath_t = etree.HTML(url_html.text)
        all_game_name = xpath_t.xpath(
            '//div[@class="responsive_page_content"]//div[@class="responsive_page_template_content"]'
            '//form[@id="advsearchform"]//div[@id="search_results"]//div[@id="search_result_container"]/div/a/'
            'div[@class="responsive_search_name_combined"]/div/span[@class="title"]')
        all_game_date = xpath_t.xpath(
            '//div[@class="responsive_page_content"]//div[@class="responsive_page_template_content"]'
            '//form[@id="advsearchform"]//div[@id="search_results"]//div[@id="search_result_container"]/div/a/'
            'div[@class="responsive_search_name_combined"]/div[2]')
        # 链接，无需处理
        all_game_href = xpath_t.xpath(
            '//div[@class="responsive_page_content"]//div[@class="responsive_page_template_content"]'
            '//form[@id="advsearchform"]//div[@id="search_results"]//div[@id="search_result_container"]/div/a/@href')
        # 链接，无需处理
        all_img_src = xpath_t.xpath('//div[@class="responsive_page_content"]//div[@class="responsive_page_template_content"]'
                              '//form[@id="advsearchform"]//div[@id="search_results"]//div[@id="search_result_container"]/div/a/'
                              'div/img/@src')
        print("游戏名有",len(all_game_name))
        for name in range(len(all_game_name)):
            all_game_name[name] = etree.tostring(all_game_name[name], encoding="utf-8", method="text").decode("utf-8")
            all_game_name[name] = all_game_name[name].replace(u'\u2122', "").replace(u'\xae', "").replace(u'\xa0','').replace(u'\n',"").replace(" ", "").replace(u"\r","")
            game_name.append(all_game_name[name])
            # print(all_game_name[i])
        print("图片链接有",len(all_img_src))
        print("游戏链接有",len(all_game_href))
        print("上架日期有",len(all_game_date))
        for date in range(len(all_game_date)):
            all_game_date[date] = etree.tostring(all_game_date[date], encoding="utf-8", method="text").decode("utf-8")
            all_game_date[date] = all_game_date[date].replace(u'\u2122', "").replace(u'\xae', "").replace(u'\xa0','').replace(" ","").replace(u"\n", "").replace(u"\r","")
            game_date.append(all_game_date[date])
        for src in all_img_src:
            game_img.append(src)
        for href in all_game_href:
            game_href.append(href)
        if len(game_name) == len(game_img) == len(game_date)  == len(game_href):
            for number in range(len(game_href)):
                all_game_1 = []
                all_game_1.append(game_name[number])
                all_game_1.append(game_img[number])
                all_game_1.append(game_date[number])
                all_game_1.append(game_href[number])
                print("正在获取："+all_game_name[number])
                game_part = game_content(game_href[number])
                # 此处失效，暂不处理
                #begin===================================
                if game_part ==None:
                    all_game.append(all_game_1)
                    print(game_name[number]+":获取失败！")
                    continue
                else:
                    print(game_name[number] + "：获取成功")
                    for game in range(len(game_part)):
                        all_game_1.append(game_part[game])
                all_game.append(all_game_1)
                #end=======================================
        print("第"+str(i)+"页完成")
        time.sleep(random.randint(5,10))
def data_clean(ls):
    for i in range(len(ls)):
        ls[i] = etree.tostring(ls[i], encoding="utf-8", method="text").decode("utf-8")
        ls[i] = ls[i].replace(u'\u2122', "").replace(u'\xae', "").replace(u'\xa0', '').replace(
            u"\t", "").replace(u'\n', '').replace(' ','').replace(u'\r','')
    return ls
def game_content(game_link):
    time.sleep(random.randint(5,10))
    game_price_xpath = []
    game_about_xpath = []
    game_publ_xpath = []
    game_develo_xpath = []
    game_price_2   = []
    game_price_3   = []
    user_tag_xpath = []
    game_price     = []
    game_tag_xpath = []
    response_count_get = fetch_url(game_link,headers)
    response_count = etree.HTML(response_count_get.text)
    #Game Price
    game_price_xpath = response_count.xpath(
        '//div[@class="responsive_page_template_content"]//div[@id="game_area_purchase"]/div[1]//div//div[1]//div[1]')
    #Dlc Or Mod Name
    game_price_2 = response_count.xpath(
        '//div[@class="responsive_page_content"]//div[@id="responsive_page_template_content"]/div[3]/div[@id="tabletGrid"]'
        '//div[@class="page_content"]/div[2]//div[@class="game_area_purchase"]/div[@class="game_area_purchase_game_wrapper"]/div/h1')
    #Dlc Or Mod price
    game_price_3 = response_count.xpath(
        '//div[@class="responsive_page_content"]//div[@id="responsive_page_template_content"]/div[3]/div[@id="tabletGrid"]//div'
        '[@class="page_content"]/div[2]//div[@class="game_area_purchase"]/div[@class="game_area_purchase_game_wrapper"]/div/div/div/div[1]')
    #游戏简介
    game_about_xpath = response_count.xpath(
        '//div[@class="responsive_page_template_content"]/div[3]/div[@id="tabletGrid"]/div[1]/div[@class="page_content"]'
        '/div[2]/div[@class]//div[@id="game_area_description"]')
    # 发行商
    game_publ_xpath = response_count.xpath(
        '//div[@class="responsive_page_content"]//div[@class="responsive_page_template_content"]/div[3]/div[3]/div['
        '@class="page_content_ctn"]/div[4]/div/div[2]/div/div/div[3]/div[4]/div[2]')
    # 开发商
    game_develo_xpath = response_count.xpath(
         '//div[@class="responsive_page_content"]//div[@class="responsive_page_template_content"]/div[3]/div[3]/div'
         '[@class="page_content_ctn"]/div[4]/div/div[2]/div/div/div[3]/div[3]/div[2]')
    #用户定义标签
    user_tag_xpath = response_count.xpath(
        '//div[@class="responsive_page_content"]//div[@id="responsive_page_template_content"]/div[3]/div[@id="tabletGrid"]//div['
        '@class="game_background_glow"]/div[2]/div[1]//div[@id="glanceCtnResponsiveRight"]//div[@class="glance_tags popular_tags"]')
    #游戏定义标签
    game_tag_xpath = response_count.xpath(
        '//div[@class="responsive_page_content"]//div[@class="responsive_page_template_content"]/div[3]/div[3]/div[1]//'
        'div[@class="page_content"]/div[1]/div[@id="appDetailsUnderlinedLinks"]//div[@id="genresAndManufacturer"]/span')
    if len(game_price_xpath) == 0 and len(user_tag_xpath) == 0 and len(game_tag_xpath):
        print("该页获取失败！")
        return None
    game_price_xpath = data_clean(game_price_xpath)
    game_price_2 = data_clean(game_price_2)
    game_price_3 = data_clean(game_price_3)
    game_about_xpath = data_clean(game_about_xpath)
    game_publ_xpath = data_clean(game_publ_xpath)
    game_develo_xpath = data_clean(game_develo_xpath)
    user_tag_xpath = data_clean(user_tag_xpath)
    game_tag_xpath = data_clean(game_tag_xpath)
    game_price.append(game_price_xpath)
    if len(game_price_2) == len(game_price_3) and len(game_price_2)!=0:
        game_price_it = []
        for i in range(len(game_price_3)):
            game_price_it.append(game_price_2[i])
            game_price_it.append(game_price_3[i])
        game_price.append(game_price_it)
    else:
        game_price_it=["NULL "]
        game_price.append(game_price_it)
    return [game_price,game_about_xpath,game_publ_xpath,game_develo_xpath,user_tag_xpath,game_tag_xpath]

url = "https://store.steampowered.com/search/?page=1&ndl=1"
ua = UserAgent()
def user_Agent():
    user_Agent = ua.random
    return user_Agent
headers ={    "user-Agent": user_Agent(),
              'Accept-Language':'zh-CN',
              'Connection': 'close'}
session = requests.session()
response = fetch_url(url,headers)
r = etree.HTML(response.text)
game_num = r.xpath('//div[@class="responsive_page_content"]//div[@class="responsive_page_template_content"]'
                   '//form[@id="advsearchform"]//div[@id="search_results"]/div')
# print(len(game_num))
#获取总页数
ex_game_ls=[]
a = re.findall(r"\d+\.?\d*", etree.tostring(game_num[0], encoding="utf-8", method="text").decode("utf-8"))
game_count = int(a[0]+a[1])
user_chooes(game_count)
for item in all_game:
    new_item =item
    new_item_ordered  = [new_item[0],new_item[1],new_item[2],new_item[3],new_item[4][0],new_item[4][1],new_item[5],new_item[6],new_item[7],new_item[8],new_item[9]]
    ex_game_ls.append(new_item_ordered)
ex_game_headers = ['游戏名称', '游戏图片链接', '上架日期', '游戏链接', '本体价钱', 'MOD和价钱','游戏简介', '发行商', '开发商', '玩家标签', '游戏标签']
df = pd.DataFrame(ex_game_ls, columns=ex_game_headers)
df.to_excel('Steam_games.xlsx', index=False)