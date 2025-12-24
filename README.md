# Marathon Calendar

一个基于 iCalendar 格式的马拉松赛事日历系统，通过 YAML 文件维护赛事信息，自动生成可订阅的日历文件。

A marathon event calendar system based on iCalendar format. Maintain event data in YAML files and automatically generate subscribable calendar files.

## 📅 功能特性 (Features)

- ✅ 使用 YAML 格式维护马拉松赛事信息
- ✅ 一个赛事自动生成两个日历事件：比赛日 + 报名窗口
- ✅ 支持全程马拉松和半程马拉松信息
- ✅ 生成标准 iCalendar (RFC 5545) 格式文件
- ✅ 可被 iPhone、Android、Google Calendar、Outlook 等订阅
- ✅ GitHub Actions 自动构建

## 🚀 快速开始 (Quick Start)

### 1. 订阅日历 (Subscribe to Calendar)

将以下 URL 添加到你的日历应用：

```
https://raw.githubusercontent.com/YOUR_USERNAME/marathon-calendar/main/output/marathon-calendar.ics
```

或使用 webcal 协议（点击后自动打开日历应用）：

```
webcal://raw.githubusercontent.com/YOUR_USERNAME/marathon-calendar/main/output/marathon-calendar.ics
```

#### iPhone/iPad 订阅方法：
1. 在 Safari 中打开 webcal 链接
2. 点击"订阅"
3. 日历会自动更新

#### Google Calendar 订阅方法：
1. 设置 → "添加日历" → "通过 URL"
2. 粘贴 HTTPS URL
3. 每 24 小时自动更新

### 2. 本地生成日历 (Generate Calendar Locally)

```bash
# 安装依赖
pip install -r requirements.txt

# 生成日历文件
python scripts/generate_calendar.py

# 输出文件：output/marathon-calendar.ics
```

## 📁 项目结构 (Project Structure)

```
marathon-calendar/
├── events/                      # 赛事数据目录
│   └── <year>/                  # 按年份分类
│       └── <year>-<month>.yaml  # 按月份的赛事文件
├── scripts/
│   └── generate_calendar.py    # 日历生成脚本
├── output/
│   └── marathon-calendar.ics   # 生成的日历文件
├── .github/
│   └── workflows/
│       └── generate-calendar.yml  # 自动构建配置
├── requirements.txt            # Python 依赖
└── README.md
```

## 📝 添加赛事 (Adding Events)

### 文件命名规则

赛事文件路径：`events/<year>/<year>-<month>.yaml`

例如：`events/2026/2026-03.yaml` 存放 2026 年 3 月的赛事

### YAML 格式示例

```yaml
- id: wuhu-marathon-2026
  name: 芜湖马拉松 (Wuhu Marathon)
  date: 2026-03-29
  time: "07:30:00"
  timezone: Asia/Shanghai
  
  location:
    city: 芜湖 (Wuhu)
    state: 安徽省 (Anhui)
    country: China
    venue: 芜湖航空新城运动中心
    coordinates:
      lat: 31.3560
      lon: 118.3760
  
  registration:
    open_date: 2025-12-22
    open_time: "10:00:00"
    close_date: 2026-01-25
    close_time: "16:00:00"
    url: https://example.com/register
    lottery_date: 2026-02-05
    requirements:
      - "采用抽签方式确定参赛资格"
      - "全程马拉松: 20周岁及以上"
    cost:
      full: "¥160"
      half: "¥120"
    packet_pickup:
      start: 2026-03-26
      end: 2026-03-28
  
  categories:
    - name: 全程马拉松 (Full Marathon)
      distance: 42.195
      distance_unit: km
      capacity: 6000
    - name: 半程马拉松 (Half Marathon)
      distance: 21.0975
      distance_unit: km
      capacity: 10000
  
  details:
    type: Road
    surface: Paved
    website: https://example.com
    description: |
      赛事详细描述
      可以多行
    
    contact:
      wechat: 微信公众号名称
      email: contact@example.com
  
  tags:
    - china
    - anhui
    - lottery
  
  status: confirmed
```

### 必填字段 (Required Fields)

- `id`: 唯一标识符
- `name`: 赛事名称
- `date`: 比赛日期 (YYYY-MM-DD)
- `location`: 地点信息
  - `city`: 城市
  - `country`: 国家

### 可选但推荐的字段 (Optional but Recommended)

- `registration`: 报名信息
  - `open_date`: 报名开始日期
  - `close_date`: 报名截止日期
  - `url`: 报名网址
  - `cost`: 费用
- `categories`: 赛事项目（全马、半马等）
- `details`: 详细信息
  - `description`: 赛事描述
  - `contact`: 联系方式

## 🔄 自动更新 (Auto Update)

项目配置了 GitHub Actions，当 `events/` 目录下的 YAML 文件发生变化时：

1. 自动运行 `generate_calendar.py`
2. 生成新的 `marathon-calendar.ics`
3. 提交到仓库
4. 订阅者的日历应用会自动获取更新

## 🎯 日历事件说明

每个 YAML 赛事会生成 **2 个日历事件**：

### 1. 📝 报名窗口事件
- **时间**：从报名开始到报名结束
- **显示为**：多日事件条
- **包含信息**：报名链接、费用、要求、抽签日期

### 2. 🏃 比赛日事件
- **时间**：比赛当天（估计 6 小时）
- **显示为**：单日事件
- **包含信息**：赛事详情、项目、地点、联系方式

## 🛠️ 技术栈 (Tech Stack)

- **Python 3.10+**
- **icalendar**: iCalendar 格式生成
- **PyYAML**: YAML 文件解析
- **pytz**: 时区处理
- **GitHub Actions**: 自动化构建

## 🤝 贡献指南 (Contributing)

1. Fork 本仓库
2. 在 `events/<year>/` 下添加或编辑 YAML 文件
3. 确保 YAML 格式正确
4. 提交 Pull Request

### 贡献要求

- ✅ YAML 语法正确
- ✅ 信息准确可靠
- ✅ 包含报名窗口信息
- ✅ 提供官方网站链接

## 📋 待办事项 (TODO)

- [ ] 添加更多中国主要城市马拉松
- [ ] 添加国际六大满贯马拉松
- [ ] 支持多语言（中文/英文）
- [ ] 添加赛事筛选标签系统
- [ ] 创建 Web 页面展示
- [ ] 支持用户自定义筛选订阅

## 📜 许可证 (License)

MIT License

## 📞 联系方式 (Contact)

如有问题或建议，请：
- 提交 GitHub Issue
- 发送 Pull Request

---

**注意**: 请确保添加的赛事信息来源可靠，并尊重各赛事组委会的知识产权。

