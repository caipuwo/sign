# PYTHON 签到

### 环境配置

* 本项目使用的是Python3.6.4
* 使用前需要安装插件：requests、bs4
```
pip install requests

pip install bs4
```

### 文件说明
* user.py声明用户密码变量，请自行修改成自己的账号密码

#### 素材火签到
* 网址：http://www.sucaihuo.com/
* 文件：sucaihuo.py、sucaihuo2.py
* sucaihuo.py是用request与bs4写的直接登录签到
* sucaihuo2.py是用到cookie登录的签到，会自动生成一个sucaihuo_cookie.txt的文件