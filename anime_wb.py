import pymysql
import pprint
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
import time

import threading

conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="your database password", db="your db")  # 连接数据库
cursor = conn.cursor()  # 创建游标
options = webdriver.ChromeOptions()

options.add_argument('--ignore-certificate-errors') #忽略CERT证书错误

options.add_argument('--ignore-ssl-errors') #忽略SSL错误

options.add_argument('--disable-gpu')

options.add_argument('--ignore-certificate-errors-spki-list')

options.add_argument('--ignore-urlfetcher-cert-requests')

capability = options.to_capabilities()

capability["acceptInsecureCerts"] = True

capability['acceptSslCerts'] = True

driver = webdriver.Chrome(options=options, desired_capabilities=capability)




# options.add_argument('-ignore-certificate-errors')
# # options.add_argument('-ignore -ssl-errors')
# driver = webdriver.Chrome(chrome_options=options)

options = ChromeOptions()
# root_url = 'http://cj.lziapi.com'  # 爬取目标网站,一共43页
root_url = 'http://lzizy.com/'

read_begin_page = 1     # 开始的页面
read_end_page = 2     # 结束的页面
read_end_page = read_end_page + 1

page_index = range(read_begin_page, read_end_page, 1)


def download_all_htmls():      # 获取主页面的url
    resps = []

    for idx in page_index:
        # url = f'http://cj.lziapi.com/index.php/vod/type/id/30/page/{idx}.html'
        url = f'http://lzizy.com/index.php/vod/type/id/30/page/{idx}.html'
        print('craw html:', url)
        # r = requests.get(url)
        driver.refresh()
        driver.get(url)
        # if r.status_code != 200:
        #     raise Exception('error')
        time.sleep(10)
        resp = driver.page_source
        resps.append(resp)

    return resps



# htmls2 = download_all_htmls2()
# print(htmls[0])


def parse_single_html(html, count):

    # count = 0
    # global key_one
    # hrefs = []
    # time.sleep(10)


    # 设置空变量，否则可能报错
    soup = BeautifulSoup(html[count], 'html.parser')  # 解析网站
    href_items = (soup.find('div', class_='container').find('div', class_='addition-content').find('ul',class_='videoContent'))
    poster_href = ''
    anime_name = ''
    anime_area = ''
    anime_year = ''
    video_info = ''
    anime_episode_to = ''
    is_new = 0
    anime_id = 0
    target_anime_id = 0

    anime_lists = href_items.find_all('li')
    for anime_list in anime_lists:
        time.sleep(30)
        jump = 0
        datas = []
        # anime_name = anime_list.find('a', class_='videoName').getText()
        anime_episode_to = anime_list.find('a', class_='videoName').find('i').getText()
        anime_href = anime_list.find('a', class_='videoName').get('href')  # 获取一部动漫的逻辑链接
        anime_area = anime_list.find('span', class_='region').getText()   # 获取动漫地区
        anime_real_href = (root_url + anime_href)  # 拼接链接，得到真正的链接
        anime_update_time = anime_list.find('span', class_='time1').getText()  # 获取动漫的更新日期（本地）

        driver.refresh()
        driver.get(anime_real_href)  # 加载某一部动漫的具体信息页面
        time.sleep(0.5)
        r = driver.page_source
        soupx = BeautifulSoup(r, 'html.parser')
        info_target = (soupx.find('div', class_='width1200 white').find('div', class_='people'))
        anime_poster = info_target.find('div', class_='left').find('img').get('src')  # 获取动漫的封面
        anime_infos = info_target.find('div', class_='right')
        year_find_ranges = range(1, 9, 1)
        anime_name_fake = anime_infos.find('p').get_text()
        anime_name = anime_name_fake.replace('片名：', '')  # 去除动漫名字中的多余元素
        print(anime_name)
        for year_find_range in year_find_ranges:
            anime_infos = anime_infos.find_next('p')
        anime_year_fake = anime_infos.get_text()
        anime_year = anime_year_fake.replace('年代：', '')  # 获取动漫年份
        anime_info = soupx.find('div', id='content').get_text()   # 获取动漫简介，但是带有很多转义符
        # anime_info = str(json.loads(anime_info_fake))   # 去除转义符,他喵的一整块一整块的转义符，去不掉


        anime_name_sql = f"""SELECT * FROM drf_animebigwuhureal WHERE video_title="{anime_name}";"""   #查询获取到的这部动漫是否在库中
        cursor.execute(anime_name_sql)  # 执行sql
        resp_anime = cursor.fetchall()  # 获取查询到的二维元组
        # print(resp_anime)
        anime_url_targets = soupx.find('div', class_='playlist wbox liangzi').find('div', class_='playlist wbox lzm3u8').find_all('li')  # 找到每一集动漫的位置
        if resp_anime != ():  # 若获取到的元组不为空（即存在）
            is_new = 0   # is_new代表该动漫是否为新动漫，0为旧动漫，1为新动漫
            # print('wuhubig可修改')
            is_title_real = resp_anime[0][3]   # 获取旧动漫的title
            anime_id = resp_anime[0][0]  # 获取旧动漫的主键id，即anime_id
            cursor.execute(f"""UPDATE drf_animebigwuhureal SET video_episodes='{anime_episode_to}' WHERE id='{anime_id}';""")
            conn.commit()
            cursor.execute(f"""UPDATE drf_animebigwuhureal SET video_episodes_count='{len(anime_url_targets) - 1}' WHERE id='{anime_id}';""")
            conn.commit()
            cursor.execute(f"""UPDATE drf_animebigwuhureal SET video_update='{anime_update_time}' WHERE id='{anime_id}';""")
            conn.commit()   #更新animebigwuhureal中需要更新的项
        else:    # 元组为空，即该动漫为新动漫
            # print('wuhubig可创建')
            is_new = 1   # 表示新动漫
            cursor.execute(f"""INSERT INTO drf_animebigwuhureal(video_episodes_count,video_episodes,video_title,video_area,video_year,poster,video_info,video_update) VALUES('{len(anime_url_targets)-1}','{anime_episode_to}','{anime_name}','{anime_area}','{anime_year}','{anime_poster}','{anime_info}','{anime_update_time}')""")
            conn.commit()   # 创建一个大的动漫信息，并提交
            find_add_anime_sql = f"""SELECT id FROM drf_animebigwuhureal WHERE video_title = "{anime_name}";"""  # 马上找刚才创建的动漫的主键id
            cursor.execute(find_add_anime_sql)
            target_anime_id = cursor.fetchall()[0][0]  # 得到新建的动漫的主键id

        # cursor.execute(f"""INSERT INTO drf_animebigwuhureal(video_episodes_count,video_episodes,video_title,video_area,video_year,poster,video_info,video_update) VALUES('{len(anime_url_targets)-1}','{anime_episode_to}','{anime_name}','{anime_area}','{anime_year}','{anime_poster}','{anime_info}','{anime_update_time}')""")
        # conn.commit()
        for anime_url_target in anime_url_targets:  # 此乃一部动漫里所有剧集的集合，遍历这个集合（这个集合的最后一个li是无用项）
            jump = jump + 1
            if jump == len(anime_url_targets):  # 到了最后一个无用项，直接跳出
                continue
            anime_url_fake = anime_url_target.find('a').get('href')    # 获取m3u8的视频链接
            anime_episode_name = anime_url_target.find('a').get('title')  # 获取该集动漫是第几集
            anime_url_real = ('https://lziplayer.com/?url=' + anime_url_fake)   # 用爬取网站提供的解析器拼接成可以播放的动漫，将来前端使用videojs可以更换链接
            # time.sleep(3)
            # print(anime_episode_name)
            # print(anime_url_real)

            if is_new == 0:  # 如果不是新的动漫，即可添加新剧集
                # print('wuhusmall可更新')
                anime_episode_sql = f"""SELECT video_episode FROM drf_animebigwuhureal,drf_animesmallwuhureal WHERE drf_animebigwuhureal.id=drf_animesmallwuhureal.anime_key_id AND drf_animebigwuhureal.id={anime_id};"""   # 用刚才获取旧的id去搜索该动漫的所有剧集信息
                cursor.execute(anime_episode_sql)
                find_anime_episode = cursor.fetchall()   # 获取剧集元组
                when = True   # 设置when为True，代表这一集不在所有剧集里
                for find_anime_episode_one in find_anime_episode:   # 用获取到的剧集信息遍历整个二维元组，若存在，则when改为False，跳出循环
                    if anime_episode_name in find_anime_episode_one:
                        when = False
                        continue
                if when:   # 如果when为True，则该剧集不存在宇所有剧集中，则可添加
                    # print('smallwuhu可添加')
                    cursor.execute(f"""insert into drf_animesmallwuhureal(video_episode,video_title,video_area,video_year,video_url,anime_key_id) values("{anime_episode_name}","{anime_name}","{anime_area}","{anime_year}","{anime_url_real}","{anime_id}");""")
                    conn.commit()  # 添加新剧集进数据库
                else:   # 如果when为False，则代表该剧集存在与原来的所有剧集中，直接跳过即可
                    pass
                    # print('smallwuhu已存在')

            else:  # 如果is_new为1，则该动漫是新动漫，可以直接创建，并获取刚才新创建的大动漫的主键，并关联
                # print('wuhusmall可创建')
                cursor.execute(f"""insert into drf_animesmallwuhureal(video_episode,video_title,video_area,video_year,video_url,anime_key_id) values("{anime_episode_name}","{anime_name}","{anime_area}","{anime_year}","{anime_url_real}","{target_anime_id}");""")
                conn.commit()
            # cursor.execute(f"""insert into drf_animesmallwuhureal(video_episode,video_title,video_area,video_year,video_url,anime_key_id) values("{anime_episode_name}","{anime_name}","{anime_area}","{anime_year}","{anime_url_real}","{key_one+1501}");""")
            # conn.commit()
        #  打印测试数据
        datas.append({'title': anime_name, 'poster': anime_poster, 'area': anime_area, 'episode': len(anime_url_targets)-1, 'year': anime_year, 'episode2': anime_episode_to, 'video_info': anime_info})  # '''eval(area)'''
    #     pprint.pprint(datas)

def time_handler():
    # global html2_error_count
    # global html1_error_count
    global driver
    # api_url = 'http://webapi.http.zhimacangku.com/getip?num=5&type=3&pro=&city=0&yys=0&port=1&pack=296705&ts=0&ys=0&cs=0&lb=1&sb=0&pb=5&mr=1&regions='
    # driver = webdriver.Chrome()  # 浏览器类型
    # driver.get(api_url)  # 将ip池塞进浏览器
    # api_resp = driver.page_source  # 获取ip
    # soup666 = BeautifulSoup(api_resp, 'html.parser')  # 解析ip
    # url_string = soup666.get_text()
    # print(url_string)
    # url_lists = url_string.split()  # 将获取的ip设置为代理
    # for url_list in url_lists:
    #     options.add_argument(('--proxy-server=http://' + url_list))
    # driver = webdriver.Chrome(options=options)
    try:

        htmls = download_all_htmls()
    except:

        time.sleep(5)
        driver.close()
        driver = webdriver.Chrome(chrome_options=options)
        # driver = webdriver.Chrome()
        print(time.asctime())
        print('html1 error')
        time_handler()

    page_numbers = range(1, read_end_page - read_begin_page + 1, 1)
    counts = 0  # 页面的第几面的面数
    # key_one = 0
    for page_number in page_numbers:
        try:
            parse_single_html(htmls, counts)
        except:
            time.sleep(5)
            driver.close()
            driver = webdriver.Chrome(chrome_options=options)
            # driver = webdriver.Chrome()
            print(time.asctime())
            print('html2 error')
            time_handler()
        counts = counts + 1
    # 关闭连接，关闭游标
    # conn.close()
    # cursor.close()
    # driver.close()
    timer = threading.Timer(3600, time_handler)
    # html1_error_count = 0
    # html2_error_count = 0
    print('更新成功，当前时间为：' + str(time.asctime()))
    timer.start()


time_handler()
