# 贡献指南 (Contributing Guide)

感谢你对 Marathon Calendar 项目的关注！本指南将帮助你了解如何添加和维护马拉松赛事信息。

Thank you for your interest in the Marathon Calendar project! This guide will help you add and maintain marathon event information.

## 📝 添加赛事的步骤 (Steps to Add Events)

### 1. 确定文件路径

根据比赛月份，将赛事添加到对应的 YAML 文件：

```
events/<year>/<year>-<month>.yaml
```

**示例：**
- 2026年3月的赛事 → `events/2026/2026-03.yaml`
- 2026年11月的赛事 → `events/2026/2026-11.yaml`

如果文件不存在，请创建新文件。一个文件可以包含多个赛事。

### 2. 使用模板

参考 `events/TEMPLATE.yaml.example` 文件，复制模板并填写赛事信息。

### 3. 填写赛事信息

#### 必填字段 (Required Fields)

```yaml
- id: unique-marathon-id-2026
  name: 马拉松名称 (Marathon Name)
  date: 2026-03-29
  location:
    city: 城市名
    country: 国家名
```

#### 推荐字段 (Recommended Fields)

```yaml
  time: "07:30:00"
  timezone: Asia/Shanghai
  
  registration:
    open_date: 2025-12-22
    open_time: "10:00:00"
    close_date: 2026-01-25
    close_time: "16:00:00"
    url: https://registration-url.com
  
  categories:
    - name: 全程马拉松 (Full Marathon)
      distance: 42.195
      distance_unit: km
      capacity: 6000
```

## 📋 字段说明 (Field Reference)

### 基本信息 (Basic Information)

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `id` | string | ✅ | 唯一标识符，建议格式：`城市-marathon-年份` | `wuhu-marathon-2026` |
| `name` | string | ✅ | 赛事名称（中英文） | `芜湖马拉松 (Wuhu Marathon)` |
| `date` | date | ✅ | 比赛日期 | `2026-03-29` |
| `time` | string | 推荐 | 开始时间（24小时制） | `"07:30:00"` |
| `timezone` | string | 推荐 | 时区标识 | `Asia/Shanghai` |
| `status` | string | 可选 | 赛事状态 | `confirmed`, `tentative`, `cancelled` |

### 地点信息 (Location)

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `location.city` | string | ✅ | 城市名称（中英文） | `芜湖 (Wuhu)` |
| `location.state` | string | 可选 | 省份/州 | `安徽省 (Anhui)` |
| `location.country` | string | ✅ | 国家 | `China` |
| `location.venue` | string | 推荐 | 起终点位置 | `芜湖航空新城运动中心` |
| `location.coordinates.lat` | float | 推荐 | 纬度 | `31.3560` |
| `location.coordinates.lon` | float | 推荐 | 经度 | `118.3760` |

**如何获取坐标：**
- 打开 [Google Maps](https://maps.google.com)
- 搜索地点并右键点击
- 选择坐标复制

### 报名信息 (Registration)

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `registration.open_date` | date | 推荐 | 报名开始日期 | `2025-12-22` |
| `registration.open_time` | string | 可选 | 报名开始时间 | `"10:00:00"` |
| `registration.close_date` | date | 推荐 | 报名结束日期 | `2026-01-25` |
| `registration.close_time` | string | 可选 | 报名结束时间 | `"16:00:00"` |
| `registration.url` | url | 推荐 | 报名网址 | `https://...` |
| `registration.lottery_date` | date | 可选 | 抽签结果公布日期 | `2026-02-05` |
| `registration.requirements` | list | 可选 | 报名要求列表 | 见下方示例 |
| `registration.cost` | object | 可选 | 费用信息 | 见下方示例 |
| `registration.packet_pickup` | object | 可选 | 领物信息 | 见下方示例 |

**报名要求示例：**
```yaml
requirements:
  - "采用抽签方式确定参赛资格 (Lottery selection)"
  - "全程马拉松: 20周岁及以上 (Full: Age 20+)"
  - "半程马拉松: 16周岁及以上 (Half: Age 16+)"
```

**费用信息示例：**
```yaml
cost:
  full: "¥160"
  half: "¥120"
```

**领物信息示例：**
```yaml
packet_pickup:
  start: 2026-03-26
  end: 2026-03-28
  note: "须本人凭身份证领取"
```

### 赛事项目 (Categories)

用于列出全程马拉松、半程马拉松等项目信息。

```yaml
categories:
  - name: 全程马拉松 (Full Marathon)
    distance: 42.195
    distance_unit: km
    capacity: 6000
  - name: 半程马拉松 (Half Marathon)
    distance: 21.0975
    distance_unit: km
    capacity: 10000
```

| 字段 | 说明 | 示例 |
|------|------|------|
| `name` | 项目名称 | `全程马拉松 (Full Marathon)` |
| `distance` | 距离数值 | `42.195` |
| `distance_unit` | 距离单位 | `km` 或 `mi` |
| `capacity` | 参赛人数 | `6000` |

### 详细信息 (Details)

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `details.type` | string | 赛事类型 | `Road`, `Trail`, `Virtual` |
| `details.surface` | string | 路面类型 | `Paved`, `Trail`, `Mixed` |
| `details.website` | url | 官方网站 | `https://example.com` |
| `details.description` | string | 赛事描述（多行） | 见下方示例 |
| `details.contact` | object | 联系方式 | 见下方示例 |

**赛事描述示例：**
```yaml
description: |
  2026芜湖马拉松
  起终点: 芜湖航空新城运动中心
  
  竞赛项目:
  • 全程马拉松 (42.195公里) - 6000人
  • 半程马拉松 (21.0975公里) - 10000人
```

**联系方式示例：**
```yaml
contact:
  wechat: 航空芜马
  email: wuhumarathon@163.com
  phone: "+86 XXX XXXX XXXX"
```

### 标签 (Tags)

用于分类和筛选赛事。

```yaml
tags:
  - china
  - anhui
  - lottery
  - road-race
  - flat-course
  - scenic
```

**常用标签：**
- **国家/地区：** `china`, `usa`, `japan`, `korea`, etc.
- **省份/州：** `beijing`, `shanghai`, `guangdong`, etc.
- **赛事特点：** `lottery`（抽签）, `qualifying`（资格赛）
- **路线类型：** `road-race`, `trail-run`
- **难度：** `flat-course`, `hilly-course`, `mountain`
- **特色：** `scenic`, `historic`, `coastal`, `urban`
- **级别：** `major`, `world-marathon-majors`

## 🌍 常用时区 (Common Timezones)

| 地区 | 时区标识 |
|------|----------|
| 中国 | `Asia/Shanghai` |
| 日本 | `Asia/Tokyo` |
| 韩国 | `Asia/Seoul` |
| 新加坡 | `Asia/Singapore` |
| 美国东部 | `America/New_York` |
| 美国西部 | `America/Los_Angeles` |
| 英国 | `Europe/London` |
| 法国 | `Europe/Paris` |
| 德国 | `Europe/Berlin` |

完整列表：https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

## ✅ 提交前检查清单 (Pre-submission Checklist)

在提交 Pull Request 之前，请确认：

- [ ] YAML 语法正确（可使用在线工具验证）
- [ ] 所有必填字段已填写
- [ ] 日期格式正确 (`YYYY-MM-DD`)
- [ ] 时间格式正确 (`"HH:MM:SS"` 带引号)
- [ ] URL 可访问且正确
- [ ] 信息来源可靠（官方网站或公告）
- [ ] 中英文信息准确
- [ ] 坐标位置准确（如果提供）
- [ ] 文件保存为 UTF-8 编码

## 🧪 本地测试 (Local Testing)

提交前建议在本地测试：

```bash
# 安装依赖
pip install -r requirements.txt

# 生成日历
python scripts/generate_calendar.py

# 检查输出
ls -lh output/marathon-calendar.ics
```

如果生成成功，说明 YAML 格式正确。

## 📮 提交流程 (Submission Process)

1. **Fork 本仓库**
   
2. **克隆到本地**
   ```bash
   git clone https://github.com/YOUR_USERNAME/marathon-calendar.git
   cd marathon-calendar
   ```

3. **创建分支**
   ```bash
   git checkout -b add-marathon-name
   ```

4. **添加/编辑赛事文件**
   ```bash
   # 创建或编辑文件
   nano events/2026/2026-03.yaml
   ```

5. **本地测试**
   ```bash
   python scripts/generate_calendar.py
   ```

6. **提交更改**
   ```bash
   git add events/2026/2026-03.yaml
   git commit -m "Add Marathon Name 2026"
   ```

7. **推送到 GitHub**
   ```bash
   git push origin add-marathon-name
   ```

8. **创建 Pull Request**
   - 访问你的 Fork 仓库
   - 点击 "Pull Request"
   - 填写说明并提交

## 💡 最佳实践 (Best Practices)

### 1. 信息准确性
- 从官方网站获取信息
- 注明信息来源
- 及时更新变动信息

### 2. 命名规范
- ID 使用小写字母和连字符：`city-marathon-year`
- 名称包含中英文：`城市马拉松 (City Marathon)`

### 3. 描述质量
- 提供有用的赛事信息
- 包含赛道特点
- 提及重要注意事项

### 4. 持续维护
- 关注赛事官方公告
- 及时更新报名信息
- 标注已取消的赛事

## ❓ 常见问题 (FAQ)

### Q: 一个月有多个赛事怎么办？
A: 在同一个 YAML 文件中添加多个赛事，每个赛事以 `- id:` 开头。

### Q: 赛事取消了怎么办？
A: 将 `status` 字段改为 `cancelled`，并在 description 中说明。

### Q: 没有报名窗口的赛事怎么处理？
A: 可以省略 `registration` 字段，只保留比赛日信息。

### Q: 如何添加虚拟马拉松？
A: 设置 `details.type: Virtual`，location 可以填写 `Online` 或主办方所在地。

### Q: YAML 语法错误怎么检查？
A: 使用在线工具如 [YAML Lint](http://www.yamllint.com/) 验证语法。

## 📧 联系方式 (Contact)

如有疑问：
- 提交 GitHub Issue
- 在 Pull Request 中提问
- 参考已有的赛事 YAML 文件

感谢你的贡献！🙏

