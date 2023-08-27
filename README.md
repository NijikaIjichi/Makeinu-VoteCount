# 挺好萌计票网页（非官方）

## 前端

使用`react`编写，非常简陋，能用就行

使用时请将`src/index.js`中第10行的`baseURL`修改为后端的地址

如有必要可以`npm run build`编译并使用Caddy进行反向代理

## 后端

同样非常简陋，能用就行，包含：

- 爬取投票楼并生成结果JSON的脚本`vote.py`（配置方法见文件夹内的`README.md`）
- 定时自动运行上述脚本的`dovote.py`
- 将结果JSON提供给前端的服务器`server.py`（使用`flask`，如无请先使用`pip`安装）

使用时需要在后台运行`dovote.py`和`server.py`
