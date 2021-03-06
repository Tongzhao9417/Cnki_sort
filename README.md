# 知网中文文献整理工具



## 本工具主要用于：

* 对从知网下载到本地的中文文献进行重命名

* 将中文文献按照期刊来源进行分类，统一整理进文件夹内

* 将文献的标题、作者、来源、摘要、关键字等信息填写至csv中，方便日后寻找，查看

# python所需库
```
selenium

# 需要提前配置webdriver

shutil

csv
```

# 使用方法
```
python cnki_sort.py
```

# 效果展示

![image](https://github.com/Tongzhao9417/Cnki_sort/blob/master/images/15849305741855.jpg)

![image](https://github.com/Tongzhao9417/Cnki_sort/blob/master/images/15849306579994.jpg)


![image](https://github.com/Tongzhao9417/Cnki_sort/blob/master/images/15849308944383.jpg)

# 注意事项
* 只能对PDF文献进行处理，暂时不支持caj格式

* 只能处理期刊文献，不支持会议论文、硕博士论文（硕博论文有另一个工具）

# 目前存在的Bug

* 由于本人学艺不精，所以无法确保文献100%的识别率

* csv部分，由于采用了**追加写入**的方式，故每次整理会出现表头持续的情况。但如果不再次写入表头，会使得新数据格式混乱的情况。望有大神可以指点迷津。

![image](https://github.com/Tongzhao9417/Cnki_sort/blob/master/images/15849311784393.jpg)
（Bug展示）


# 特别鸣谢
灵感来源自CSDN的@文明的小爬虫， 很多代码也是从他那里借（chao）鉴（xi）过来的。我作为一个初学者，从他的代码中学习了很多，在此表示感谢！（Link: https://blog.csdn.net/weixin_44024393/article/details/89221821?biz_id=0&ops_request_misc=%7B%22request_id%22:%22158357419919724811854552%22,%22scm%22:%2220140713.130056874..%22%7D&request_id=158357419919724811854552）
