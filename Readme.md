# 运行前
需要安装web/requirements.txt（根目录下的不完整）

# 运行
我个人测试环境是windows 10虚拟机下使用pycharm，运行web/run.py  
linux下可以使用`flask run --host 0.0.0.0 --port 5000`（5000为flask项目默认的测试端口，不适合生产环境，但是对于我们的项目影响不大）


# 服务器端
## 已经安装了：
mysql（并在我的电脑上使用flask项目连通了服务器端）  
iptables（我已经打开了tomcat的端口，和appache的端口）  
tomcat(端口号：28888)  appache（端口号：20022）  
linux运维面板  访问示例：http://server.itstudio.club:20033/c6f113f44c  
**注：需要使用校园网**

我已经将小程序的图片通过tomcat部署完成了，并且小程序可以正常获取

## 服务器远程连接信息
服务器地址：server.itstudio.club（或 10.140.33.49）  
SSH 端口：20022  
SSH 用户名：root 或 itstudio（itstudio 用户有 sudo 权限，建议非必要不使用 root 用户直接登录）  
SSH 密码：Publicitstudio   
如需另外的端口开放，请联系我们  
**注:如果需要新开端口的话，无法使用iptables直接打开（因为分配的是一个虚拟机，外面仍有一层防火墙），可以跟我说**



# Tips

1. equipment/views.py第160行的base_url改为服务器ip和端口（我在windows虚拟机是用IIS web服务使外部访问获取图片资源的，linux上**可能**要继续用tomcat，图片地址放在web/static/uploads下）
2. 我在linux服务器下，自己试过`flask run`并不能直接运行，会报**代码错误**（看看能不能解决，不能解决及时反馈一下，因为我测试用的是windows系统的pycharm直接跑的）

