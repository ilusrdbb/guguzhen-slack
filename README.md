# guguzhen-slack

没做完，这是个半成品，先别用！  
咕咕镇摆烂小工具，自动化出击翻牌许愿日活，支持多账号和定时执行  
请注意由于代码充斥大量神秘正则，每次咕咕镇版本更新后本工具可能会有不可预料的问题，如有问题请停止程序等待更新  
本项目基于pycharm开发，开发环境为python 3.9  

## 使用说明
### Windows
解压release最新版本的压缩包，根据template.yaml修改配置文件，将配置文件复制到config文件夹内，有几个账号就放几个配置文件，配置文件的文件名随意但是后缀名一定要是.yaml，最后双击slack.exe运行程序  
或使用Pyinstaller从源代码中打包，环境准备见下方Linux说明  
~~~bash
Pyinstaller -F slack.py
~~~
### Linux
Linux下暂时需要从源代码运行  
安装python3环境，建议3.9及以上  
安装requirements.txt下依赖  
~~~bash
pip install -r requirements.txt
~~~
下载源代码  
~~~bash
git clone https://github.com/ilusrdbb/guguzhen-slack.git
~~~
按照如上Windows的说明修改配置文件，运行
~~~bash
python3 slack.py &
~~~

## 如何抓cookie
打开f12控制台，切换到网络（network）选项卡  
访问[咕咕镇首页](https://www.momozhen.com/fyg_index.php#)  
控制台下方左侧会有一排请求，选择点击第一个，在右侧下拉找到Cookie: xxxxx，把xxxxx粘到yaml配置文件中  

## QA
Q:那个slack.db是什么玩意，可以删吗  
A:存储战斗记录的数据库，如果不需要导出战斗记录可以删  
Q:如何导出战斗记录  
A:使用另一个压缩包内的export.exe，可以导入至收割机脚本中查看  
Q:我的沙滩和宝石工坊可以搞自动化么  
A:纯后端搞这种有些麻烦，建议使用前端脚本（比如光头佬的新数据采集）挂浏览器  
Q:出击自动切装备护符啥的能做么  
A:同样纯后端很难搞，而且这个功能可能会被恶意利用，不会做的  
Q:好屎的代码，我要提pr羞辱你吔  
A:非常欢迎，快点来罢  

## TODO
打野战斗记录解析和导出，目前战斗记录暂只支持打人