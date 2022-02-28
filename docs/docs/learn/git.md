# Git

## Git子模块简易操作

不妨令: 
子模块的git地址为: https://github.com/HenryJi529/OpenMorningstar.wiki.git
大项目的git地址为: https://github.com/HenryJi529/OpenMorningstar.git

### 添加子模块
```bash
$ git submodule add https://github.com/HenryJi529/OpenMorningstar.wiki.git wiki/
```

### 查看子模块
```bash
$ git submodule
```


### 删除子模块

#### 删除子模块内容
```bash
$ git rm --cached wiki/ # 删除缓存区中的子模块
$ rm -rf wiki/          # 删除工作区中的子模块
```
#### 清理子模块信息
* `.gitmodules`
* `.git/config`
* `.git/modules/wiki/`


### 克隆含子模块的项目

#### 递归克隆
```bash
$ git clone https://github.com/HenryJi529/OpenMorningstar.git --recursive
```

#### 分步克隆
1. 克隆大项目
```bash
$ git clone https://github.com/HenryJi529/OpenMorningstar.git 
```

2. 初始化子模块
```bash
$ git submodule init
```

3. 更新子模块
```bash
$ git submodule update
```