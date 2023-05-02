Tutorials From Runoob
=====================

这是一个网络爬虫项目，功能是从[菜鸟教程](http://www.runoob.com)网站下载所有HTML网页教程。


## 主要特性 ##

1. 适合初学者，支持离线学习
2. 教程内容支持网页内的链接跳转
3. 爬虫项目，适合python初学者实战练手，通过这个项目，可以了解：

   - 爬虫原理，正则表达式语法
   - 在访问链接时使用cache
   - 绝对路径和相对路径的转换
   - 递归调用下载网页资源


## 快速开始 ##

``` shell
git clone https://github.com/znsoooo/tutorials-from-runoob
cd tutorials-from-runoob
python download_tutorials.py
```


## 版本记录 ##

- [v1.0.0](https://github.com/znsoooo/tutorials-from-runoob/releases/tag/v1.0.0)

  作者[lryong](https://github.com/lryong)的原始版本，通过`lxml`库的`xpath`方法获取[菜鸟教程](http://www.runoob.com)官网首页下的所有二级链接，然后访问二级网页并获取边栏的三级目录，然后遍历访问三级网页，将二级目录下的三级网页保存成一个HTML文件。

- [v2.0.0](https://github.com/znsoooo/tutorials-from-runoob/releases/tag/v2.0.0)

  fork的版本，由[znsoooo](https://github.com/znsoooo)完成，更新了2023年的网站API和CSS资源文件，采用下载所有HTML文件，并通过相对链接实现在浏览器内的点击跳转。文档入口为`html/index.html`。

- [v2.1.0](https://github.com/znsoooo/tutorials-from-runoob/releases/tag/v2.1.0)

  采用了递归遍历的方法查找HTML文件href属性内的所有属于当前站点的HTML文件链接，递归完成下载。避免二级以上目录死链，HTML文件中的所有链接可在浏览器内访问跳转。菜鸟网站中存在部分错误链接，按照错误路径和重定向路径本地双备份，避免无法访问或循环递归。文档入口为`html/index.html`。
