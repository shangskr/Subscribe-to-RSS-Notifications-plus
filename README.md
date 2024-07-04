# Subscribe-to-RSS-Notifications-plus
 - 一款基于gtihub实现的rss订阅通过 gh issues api实现邮箱通知
 - 如果您感兴趣可以看看上一代产品[RSS-Subscription-Email-Notification](https://github.com/shangskr/RSS-Subscription-Email-Notification)
 - 上一代产品是可以为自己订阅一些喜欢的文章，这一代产品可以为其他人或者自己订阅喜欢的文章并且邮箱通知
 - 用户可以通过发送一定格式的issues来实现订阅，也可以发表自己喜欢的rss源在issues中（我将会添加）
 - issues您可以随时关闭，关闭之后您将不会再收到订阅通知。
# 提交issues注意
- issue 标题必须是：订阅 RSS 更新通知
- Issue 必须带有 "subscribe" 标签
- Issue 必须处于打开（open）状态
- Issue 正文：必须有必要的格式
# issues格式（必须含有以下两条）
- 邮箱地址: your_email@example.com
- 订阅原因（或者是：添加rss源）: 我对您的 RSS 更新很感兴趣，希望能及时收到通知.（rss源url）
# 功能
- 自动获取issues中的邮箱
- 定期检查指定的 RSS 源
- 发送电子邮件通知
- 自动更新最近检查时间
- 新增 User-Agent 字段的值表示请求是由一个Windows 10操作系统上的Chrome浏览器发起的请求
# 使用方法(如果您想自己部署)
#### 1. 克隆项目 
#### 2. 删除check文件夹
#### 3. 在rss_list.txt文件内填写需要检查的 RSS URL
#### 3.5 如果有些链接不能正常获取解析，那么你可将其现添加到rss_list.txt文件，然后进入check_rss.py文件的22到28行将不能正常获取解析的链接再填写进去。
#### 4. 设置环境变量
- EMAIL_USER: 发电子邮件的地址
- EMAIL_PASS: 电子邮件‘密码’（我用的outlook的SMTP服务）也就是应用码
- GH_PAT：创建一个github的token（注意勾选repo选项，其他的自己看着办咯~）
- GH_REPO：仓库名称：格式（username/repository-name）
- SMTP_SERVER: SMTP 服务器地址（我用的outlook的，自行百度）SMTP服务器 ：smtp.office365.com
- SMTP_PORT: SMTP 服务器端口（我用的outlook的，自行百度）端口 ：587
#### 5.运行工程流文件
- 需要的设置也就不说了，都是老规矩了！

