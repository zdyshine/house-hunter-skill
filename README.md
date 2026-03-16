# 🏠 house-hunter — 专属租房助手 Skill

> 一个为 [WorkBuddy](https://www.codebuddy.cn/docs/workbuddy/Overview) 设计的租房全流程辅助 Skill，帮你搜房、对比、记录、看房、避坑，一站搞定。

---

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 🔍 **搜索房源** | 联网检索链家、58同城、安居客、自如等主流平台实时房源 |
| 📊 **分析对比** | 多维度评分对比（价格性价比、采光朝向、交通便利性等） |
| 📋 **看房清单** | 生成个性化看房检查清单 & 问房东问题列表 |
| 💾 **追踪记录** | 本地保存已看房源，支持状态管理和 CSV/Markdown 导出 |
| ⚠️ **合同避坑** | 签约前必看的避坑指南，高风险情况自动提醒 |

---

## 🚀 安装方式

### 方法一：下载 zip 安装（推荐）

1. 在本仓库 [Releases](../../releases) 页面下载最新的 `house-hunter.zip`
2. 打开 WorkBuddy，进入 Skill 管理页面
3. 选择「导入 Skill」，上传 `house-hunter.zip`
4. 安装完成，直接对话即可触发

### 方法二：手动复制目录

将本仓库克隆或下载到本地，把 `house-hunter` 文件夹复制到：

```
# Windows
C:\Users\<你的用户名>\.workbuddy\skills\house-hunter\

# macOS / Linux
~/.workbuddy/skills/house-hunter/
```

重启 WorkBuddy 后即可使用。

---

## 💬 使用示例

安装后，直接在 WorkBuddy 对话框中说：

```
帮我找太阳宫附近整租两室，南向，近地铁
```

```
对比这三套房，哪套性价比更高？
```

```
明天去看房，给我生成一个看房清单
```

```
帮我记录这套房源：新纪家园，2室1厅，南向，8500元/月
```

```
我准备签合同了，需要注意什么？
```

```
把我看过的所有房源导出成表格
```

---

## 📁 文件结构

```
house-hunter/
├── SKILL.md                    # Skill 核心指令文件
├── README.md                   # 本文件
├── references/
│   ├── platforms.md            # 各平台搜索策略 & 时效规则
│   └── checklist.md            # 看房清单 & 合同避坑指南
└── scripts/
    └── save_listings.py        # 房源记录管理脚本（增删改查 & 导出）
```

---

## ⚙️ 默认配置

Skill 内置了以下默认偏好，开箱即用：

- 🌍 **主要城市**：北京（也支持其他城市）
- 📍 **默认区域**：太阳宫附近
- 💡 **核心偏好**：价格性价比 + 南向采光优先
- 📅 **时效要求**：仅推荐近 1 个月内房源，超期房源会标注提示
- 🤖 **交互风格**：平时高效直出，重要决策时主动确认

---

## 🛠️ 房源记录脚本用法

`scripts/save_listings.py` 可以独立运行：

```bash
# 新增房源
python save_listings.py add --title "新纪家园主卧" --price 2500 --area 太阳宫 --type 合租 --rooms 3室1厅 --direction 南 --subway 8分钟

# 查看所有房源
python save_listings.py list

# 按状态筛选（待看/已看/心仪/已排除）
python save_listings.py list --status 心仪

# 更新状态和备注
python save_listings.py update --id 1 --status 心仪 --notes "采光好，价格合适"

# 导出为 Markdown 或 CSV
python save_listings.py export --format markdown
python save_listings.py export --format csv
```

房源数据默认保存在：`~/.house-hunter/listings.json`

---

## 📋 适用场景

- 在北京找租房，尤其是朝阳区太阳宫、芍药居、三元桥一带
- 需要同时对比多个平台房源
- 经常看房但容易忘记之前看过哪些
- 第一次租房，不知道看房和签合同需要注意什么

---

## 🤝 贡献 & 反馈

欢迎提 Issue 或 PR，改进搜索策略、补充看房清单或完善合同避坑条款。

---

## 📄 License

MIT License
