# 文件检索系统
基于 Python Flask + Elasticsearch 实现的本地文本代码检索工具

## 功能介绍
- 支持**多文件夹同时索引**，可添加、删除目录
- 自动**去重**、自动处理**父子文件夹包含关系**，避免重复扫描
- 支持几十种常见文本/代码格式检索
- 实时显示索引进度，支持**中断索引**
- 搜索结果**关键词高亮**
- 支持**自定义打开方式**打开文件
- 一键打开文件所在目录
- 界面美观、操作简单、运行稳定

## 支持文件类型
.py .java .js .ts .cs .php .go .rs .rb .c .cpp .h.sql .json .xml .html .css .md .txt .log .ini .conf .yaml .yml

## 项目文件说明
### 必需文件（不可删除）
- `client_core.py`：系统核心服务，负责索引、搜索、文件夹选择
- `web_my.py`：网页前端服务，提供界面访问
- `index.html`：前端界面
- `start.bat`：一键启动脚本
（要下载elasticsearch解压后放在同一个文件夹）
## 使用方法
1. 确保 Elasticsearch 已启动
2. 双击 `start.bat` 启动服务
3. 浏览器访问前端页面
4. 添加文件夹 → 选择文件类型 → 建立索引
5. 输入关键词检索内容

## 核心特性
- 多文件夹索引
- 自动去重、防包含扫描
- 支持中断索引
- 搜索结果高亮
- 文件打开方式自选
- 稳定、高效、无冗余操作

## 版本说明
当前版本：**最终稳定版**
已完成功能调试、BUG修复、代码备份，可长期稳定使用。

elasticsearch使用版本：9.3.1
Downloads: https://elastic.co/downloads/elasticsearch
Release notes: https://www.elastic.co/docs/release-notes/elasticsearch#elasticsearch-9.3.1-release-notes
