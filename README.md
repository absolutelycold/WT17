# WT17
* 使用前请先使用一下命令搭配好环境(在工程目录下运行)
```
pip install -r requirments.txt
```
* 配置文件为config.py, 可在此文件中设置数据库配置以及Debug模式等.
我们默认已经设置为Project要求的内网数据库。如果需要本地搭建， 请修改数据库地址和相关信息

* 部署数据库
```angular2html
python manager.py db init
python manager.py db migrate
python manager.py db upgrade
```
* flask内置服务器运行网页
```angular2html
python manager.py runserver
```

* 首页轮播图图片大小要求为700*400, 请自行调整图片大小再上传
