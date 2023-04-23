Tutorials From Runoob
=====================

这是一个网络爬虫项目，功能是从[菜鸟教程](http://www.runoob.com)网站下载所有HTML网页教程。


## 主要特性 ##

1. 适合初学者，支持离线学习
2. 教程内容支持网页内的链接跳转
3. 爬虫项目，适合python初学者实战练手，通过这个项目，可以了解：

   - 爬虫原理，`lxml`库与`xpath`语法
   - 对压缩网页的解压处理
   - python对文件的读写操作


## 快速开始 ##

``` shell
git clone https://github.com/znsoooo/tutorials-from-runoob
cd tutorials-from-runoob
pip install lxml
python download_tutorials.py
```


## 版本记录 ##

- [v1.0.0](https://github.com/znsoooo/tutorials-from-runoob/releases/tag/v1.0.0)

  作者[lryong](https://github.com/lryong)的原始版本，通过`lxml`库的`xpath`方法获取[菜鸟教程](http://www.runoob.com)官网首页下的所有二级链接，然后访问二级网页并获取边栏的三级目录，然后遍历访问三级网页，将二级目录下的三级网页保存成一个HTML文件。

- [v2.0.0](https://github.com/znsoooo/tutorials-from-runoob/releases/tag/v2.0.0)

  fork的版本，由[znsoooo](https://github.com/znsoooo)完成，更新了2023年的网站API和CSS资源文件，采用下载所有HTML文件，并通过相对链接实现在浏览器内的点击跳转。文档入口为`html/index.html`。
