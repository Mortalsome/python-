import re
import pandas
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib import font_manager

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"
}


def get_html(url):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '错误'


def save(html):
    # 解析网页
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)

    with open('./data/B_data.txt', 'r+', encoding='UTF-8') as f:
        f.write(soup.text)

    name = []  # 动漫名字
    bfl = []  # 播放量
    scs = []  # 收藏数

    # ********************************************  动漫名字存储
    for tag in soup.find_all('div', class_='info'):
        # print(tag)
        bf = tag.a.string
        name.append(str(bf))
    print(name)

    # ********************************************  播放量存储
    for tag in soup.find_all('div', class_='detail'):
        # print(tag)
        # bf = tag.find('span', class_='data-box').get_text()
        bf = tag.find('div', class_='detail-state').get_text()
        # print(bf)
        if '亿' in bf:
            num = float(re.search(r'\d(.\d)?', bf).group()) * 10000
            # print(num)
            bf = num
        else:
            bf = re.search(r'\d*(\.)?\d', bf).group()
        bfl.append(float(bf))
    print(bfl)
    # ********************************************  收藏数
    for tag in soup.find_all('div', class_='detail-state'):
        # print(tag)
        sc = tag.find('span', class_='data-box').next_sibling.next_sibling.get_text()
        sc = re.search(r'\d*(\.)?\d', sc).group()
        scs.append(float(sc))
    print(scs)

    # 存储至excel表格中
    info = {'动漫名': name, '播放量(万)': bfl, '收藏数(万)': scs}
    dm_file = pandas.DataFrame(info)
    dm_file.to_excel('Dongman.xlsx', sheet_name="动漫数据分析")
    # 将所有列表返回
    return name, bfl, scs


def view(info):
    my_font = font_manager.FontProperties(fname='./data/STHeiti Medium.ttc')  # 设置中文字体
    dm_name = info[0]
    dm_play = info[1]
    dm_favorite = info[2]
    # print(dm_com_score)

    # 为了坐标轴上能显示中文
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 图像绘制
    # **********************************************************************播放量和收藏数对比
    # ********评论数条形图
    fig, ax1 = plt.subplots()
    plt.bar(dm_name, dm_play, color='green')
    plt.title('番剧播放量和收藏数分析')
    plt.ylabel('播放量（万）')
    ax1.tick_params(labelsize=6)
    plt.xticks(rotation=90, color='green')

    # *******收藏数折线图
    ax2 = ax1.twinx()  # 组合图必须加这个
    ax2.plot(dm_favorite, color='yellow')  # 设置线粗细，节点样式
    plt.ylabel('收藏数（万）')

    plt.plot(1, label='播放量', color="green", linewidth=5.0)
    plt.plot(1, label='收藏数', color="yellow", linewidth=1.0, linestyle="-")
    plt.legend()
    plt.savefig(r'D:\Tools\elements\1.png', dpi=1000, bbox_inches='tight')

    plt.show()


def main():
    url = 'https://www.bilibili.com/v/popular/rank/bangumi'
    html = get_html(url)
    # print(html)
    info = save(html)
    view(info)


if __name__ == '__main__':
    main()
