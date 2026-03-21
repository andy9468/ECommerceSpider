# ECommerceSpider- 电商爬虫系统

🏷️亚马逊爬虫（Amazon spider）

> ⚠️ **注意**：本项目仅供学习交流使用，请勿用于商业目的或非法用途。

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![DrissionPage](https://img.shields.io/badge/DrissionPage-4.1.1-orange.svg)](https://gitee.com/g1879/DrissionPage)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://www.sqlalchemy.org/)

## 📖 项目简介

ECommerceSpider 是一个基于 **DrissionPage + SQLAlchemy + lxml** 的多线程电商数据采集系统。

项目采用模块化设计，支持异步爬取、自动去重、数据持久化等功能，可高效采集商品信息并存储到 MySQL 数据库。

计划采集目标站点：

1. 亚马逊（已完成 ✅️）
2. eBay
3. Shopee
4. Lazada
5. 速卖通

商品信息：

1. 商品关键词
2. 标题
3. 图片url
4. 价格
5. 链接url
6. 商品描述



## ✨ 核心功能

### 数据采集
- ✅ 商品标题/名称
- ✅ 商品价格（美元）
- ✅ 商品详情页链接
- ✅ 商品图片链接列表（高清大图）
- ✅ 商品描述
- ✅ 搜索关键词分类

### 技术特性
- 🔧 支持协程程并发爬取（可配置最大并发数）
- 🔐 自动获取浏览器 Cookie 和 User-Agent
- 🛡️ 支持 HTTP/HTTPS 代理IP配置
- 🗄️ 基于 SQLAlchemy ORM 的数据库操作
- 🔄 数据自动去重（基于商品标题）
- 📊 支持自定义爬取分类
- 🎯 智能页面解析和元素定位
- 💾 断点续爬支持（通过数据库状态管理）

## 🏗️ 项目结构

```bash
.
├── dbcontrol        # 数据操作
│   ├── GoodsCtr.py
│   └── __init__.py
├── db.sql           # 数据库初始化文件
├── db_model2sql.py
├── db_sql2model.py
├── docs             # 文档
│   └── 部署文档.md   # 使用说明文档
├── LICENSE
├── models           # 数据模型模块
│   ├── GoodsModel.py
│   └── __init__.py
├── README.md        # 项目介绍
├── requirements.txt # Python 依赖包列表
├── settings.py      # 配置
├── .env_template    # 配置文件模板
├── start.py         # 主程序入口
├── .gitignore       # Git 忽略文件配置
├── txt
│   └── requirements_py39_win.txt
└── utils            # 工具包
    ├── MysqlUtil.py
    ├── SqlacodegenUtil.py
    ├── TabSpider.py
    └── tools.py
```



## 🙅‍♀️部署

详解  [部署文档.md](docs/部署文档.md) 