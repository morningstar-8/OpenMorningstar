# Open Morningstar 👋

[![Django CI](https://github.com/HenryJi529/OpenMorningstar/actions/workflows/django.yml/badge.svg)](https://github.com/HenryJi529/OpenMorningstar/actions/workflows/django.yml) ![docker-passing](https://img.shields.io/badge/docker-passing-brightgreen) [![coverge-badge](https://img.shields.io/badge/coverge-click-brightgreen)](https://coverage.morningstar529.com/) ![Version](https://img.shields.io/github/v/tag/HenryJi529/OpenMorningstar) ![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg) ![Documentation](https://img.shields.io/badge/documentation-yes-brightgreen.svg) ![License](https://img.shields.io/badge/License-AGPLv3-yellow.svg) ![visitors](https://visitor-badge.laobi.icu/badge?page_id=HenryJi529.OpenMorningstar) [![Twitter: HenryJi529](https://img.shields.io/twitter/follow/HenryJi529.svg?style=social)](https://twitter.com/HenryJi529)

- [Open Morningstar 👋](#open-morningstar-)
  - [✨ 演示](#-演示)
  - [🚀 部署&开发](#-部署开发)
    - [源码获取](#源码获取)
    - [本地开发](#本地开发)
    - [远程部署](#远程部署)
  - [👉 FAQ](#-faq)
  - [🤝 维护人员](#-维护人员)
  - [🙈 欢迎支持～](#-欢迎支持)
  - [📝 License](#-license)

## ✨ 演示

**官网**: [https://morningstar529.com](https://morningstar529.com)

## 🚀 部署&开发

详细内容参考: [📖 官方文档](https://docs.morningstar529.com)

### 源码获取

```bash
$ git clone git@github.com:HenryJi529/OpenMorningstar.git
# or: git clone https://hub.fastgit.xyz/HenryJi529/OpenMorningstar.git
```

### 本地开发

```bash
$ cd OpenMorningstar/; virtualenv env
$ source env/bin/activate; pip install -r requirements.txt
$ python manage.py runserver 0:8000
```

### 远程部署

```bash
$ cd OpenMorningstar/;
$ docker-compose -f deploy/docker-compose.yml up --build -d
```

## 👉 常见问题

呜呜呜呜，还没人提问～～

## 🤝 维护人员

👤 **[Henry Ji](https://www.morningstar529.com)**

## 🙈 欢迎支持～

1. 欢迎提 issue👀 ～

2. 赏颗 ⭐️ 呗!

3. 如果对你有帮助，打赏也行! (~~我们的宗旨是不退款！~~)
   <img width="70%" src="https://cdn.jsdelivr.net/gh/HenryJi529/OpenMorningstarStatic@main/base/img/收款.png" alt="pycharm">

<!-- <div style="display:flex;align-items:center;justify-content: space-around;">
	<div style="width:40%">
		<div style="text-align:center">支付宝</div>
	</div>
	<div style="width:40%">
		<div style="text-align:center">微信</div>
	</div>
</div>
<div style="display:flex;align-items:center;justify-content: space-around;">
	<div style="width:40%">
		<img src="https://cdn.jsdelivr.net/gh/HenryJi529/OpenMorningstarStatic@main/base/img/支付宝收款码.png" alt="支付宝收款码">
	</div>
	<div style="width:40%">
		<img src="https://cdn.jsdelivr.net/gh/HenryJi529/OpenMorningstarStatic@main/base/img/微信收款码.png" alt="微信收款码">
	</div>
</div> -->

## 📝 许可证

Copyright © 2021 [Henry Ji](https://github.com/HenryJi529).<br/>
This project is [AGPL v3](https://raw.githubusercontent.com/HenryJi529/OpenMorningstar/main/LICENSE) licensed.

## 🙏 感谢

<a href="https://www.jetbrains.com/">
	<img width="30%"
		src="https://cdn.jsdelivr.net/gh/HenryJi529/OpenMorningstar@main/Morningstar/static/base/img/pycharm.svg"
		alt="pycharm">
</a>
