from selenium import webdriver
import os
import time
import shutil
import csv
import datetime
old_path = input('请输入待整理的文件夹路径：')
old_path = old_path + '/'
new_path = input('请输入存放文献的文件夹路径：')
new_path = new_path + '/'
initial_time = datetime.datetime.now()
Chorme_options = webdriver.ChromeOptions()
# 设置为无图模式
prefs = {'profile.managed_default_content_settings.images': 2}
Chorme_options.add_experimental_option('prefs', prefs)
# 设置为无头模式
Chorme_options.add_argument('headless')
browser = webdriver.Chrome(options=Chorme_options)
# 启动知网手机版主页
browser.get('http://wap.cnki.net/touch/web/guide')
# 点击搜索框，进行待命
browser.find_element_by_id('keyword').click()
data_list = []


def start(name):
    try:
        # 打印显示提取出的文件名
        print(name)
        # 选择搜索方式为“篇名”
        browser.find_element_by_id('selecttype_a').click()
        # 我没有在爬虫 :)
        time.sleep(1)
        # 按下载量进行排行，能过滤掉一些重名但非目标文献
        browser.find_element_by_xpath("//div[@id='selecttypemenu']/div/a[2]").click()
        # 输入文献名，并搜索
        browser.find_element_by_id('keyword_ordinary').send_keys(name)
        browser.find_element_by_class_name('btn-search').click()
        # 提取基本信息进行判断
        basic_info = browser.find_element_by_class_name('c-company__body-name').text
        '''
        这里多说一点：之所以要提取basic_info，是因为会出现以下情况：
        （1）同名文献为硕博论文；
        （2）同名文献为会议论文
        当出现这种情况时，再引入第三个维度：期刊维度
        '''
        if '硕士' in basic_info:
            browser.find_element_by_id('selectorder_a').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="selectordermenu"]/div/a[2]').click()
        elif '博士' in basic_info:
            browser.find_element_by_id('selectorder_a').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="selectordermenu"]/div/a[2]').click()
        elif '会议' in basic_info:
            browser.find_element_by_id('selectorder_a').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="selectordermenu"]/div/a[2]').click()
        # 提取作者信息
        author = browser.find_element_by_class_name('c-company__body-author').text
        # 经过以上操作后，基本上第一个条目就是目标文献了
        browser.find_element_by_class_name('c-company-top-link').click()
        # 提取标题
        title = browser.find_element_by_class_name('c-card__title2').text
        # 将标题中的所有“:” 和“/”进行替换（只在Mac下通过测试，Windows未测试）
        if ':' and '/' in title:
            title = title.replace(':', '：').replace('/', '、')
        elif '/' in title:
            title = title.replace('/', '、')
        elif ':' in title:
            title = title.replace(':', '：')
        # 提取摘要
        abstract = browser.find_element_by_class_name('c-card__aritcle').text
        # 提取关键字，有的文献关键字排布不唯一，所以采用了两种写法以确保不报错
        try:
            keywords = browser.find_element_by_xpath(
                "//div[@class='c-card__paper-item'][3]/div[@class='c-card__paper-content c-card__paper-content-normal']"
            ).text
        except:
            keywords = browser.find_element_by_xpath(
                "/html/body/div[4]/div[1]/div[4]/div[2]/div[2]"
            ).text
        # 提取期刊名称、发表时间
        source = browser.find_element_by_xpath(
            "//div[@class='c-book__content']/div[@class='c-book__title']"
        ).text
        date_time = browser.find_element_by_xpath(
            "//div[@class='c-book__content']/div[@class='c-book__time']"
        ).text

        # 写入
        data_dict = {}
        data_dict['title'] = title
        data_dict['author'] = author
        data_dict['abstract'] = abstract
        data_dict['keywords'] = keywords
        data_dict['source'] = source
        data_dict['datetime'] = date_time
        data_list.append(data_dict)
        # 处理完一个，等待两秒继续
        time.sleep(2)
        browser.find_element_by_xpath(
            "//div[@class='c-nav--right c-nav--right-double']/a[@class='c-nav--right-icon c-nav--right-icon0']"
        ).click()
        # 返回文献名和来源，后续用
        return title, source
    except:
        write()
        print(name+'出错')


# 对文件名进行粗整理，方便后续剪贴使用
def file_names():
    # 提取待整理的文献名称
    final_names = []
    file_name = os.listdir(old_path)
    for name in file_name:
        # Mac下的文件会出现.DS的隐藏文件，所以要进行排除。Windows可删除此句
        if not name.startswith('.'):
            final_names.append(name)
    return final_names


# 对文件名进行精细整理，供爬虫使用
def abstract_file():
    all_names = []
    names = os.listdir(old_path)
    count = 0
    for name in names:
        # Mac的隐藏文件处理
        if not name.startswith('.'):
            # 处理掉文献中的“_第一作者”以及后面的PDf后缀名
            if '_' in name:
                index = name.rfind('_')
                name = name[:index]
                all_names.append(name)
                count += 1
            # 有些文献没有第一作者，为防止报错，只处理后缀名
            else:
                index = name.rfind('.')
                name = name[:index]
                all_names.append(name)
                count += 1
    print('提取出'+str(count)+'条文献')
    return all_names


def main():
    start_time = datetime.datetime.now()
    file_name = abstract_file()
    origin_name = file_names()
    count = 0
    # 分别提取精细处理的文件名和原始文件名
    for x, y in zip(file_name, origin_name):
        # 有些文献会有“省略”的字样，进行消除处理
        if str('省略') in x:
            x = x.replace('省略', '')
        # 启动爬虫
        result = start(x)
        # 将爬虫函数中的整理好的文献名进行接受，方便打印查看是否处理正确
        new_name = format(result[0])
        source = format(result[1])
        # 创建文件夹或移动文件至已有文件夹
        if os.path.exists(new_path+str(source)):
            shutil.copyfile(old_path+y, new_path+str(source)+'/'+new_name+'.pdf')
            print(y, '-->', new_name, '', source)
            count += 1
            print('第'+str(count)+'条完毕')
        else:
            os.makedirs(new_path+str(source))
            shutil.copyfile(old_path + y, new_path + str(source) + '/' + new_name + '.pdf')
            print(y, '-->', new_name, '', source)
            count += 1
            print('第' + str(count) + '条完毕')
        # 删除原文件
        os.remove(old_path+y)
        end_time = datetime.datetime.now()
        print(end_time - start_time)
        start_time = datetime.datetime.now()
    # 进行csv的写入
    write()
    finish_time = datetime.datetime.now()
    print('总共整理了'+str(count)+'条文献', '，', '总共耗时：', finish_time-initial_time)
    browser.quit()


def write():
    """
    将所有整理好的文献进行归类处理，文件存放在整理好的文件夹下
    这里使用的写入方式是向后添加，这样处理不会抹掉上次已写入的数据，但坏处是csv中会出现Title等字样
    暂时没有更好的处理方式，希望大神们进行指点
    """
    with open(new_path+'归类.csv', 'a+', encoding='GB18030', newline='')as f:
        # 文件头
        title = data_list[0].keys()
        writer = csv.DictWriter(f, title)
        writer.writeheader()
        writer.writerows(data_list)


if __name__ == '__main__':
    main()
