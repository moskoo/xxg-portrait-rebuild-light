<div align="center">
  <img src="assets/skill-icon.png" width="120" alt="xxg-portrait-rebuild-light skill-logo">
</div>
<h1 align="center">XXG Portrait Rebuild Light</h1>
<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-red?style=flat-square" alt="MIT License"></a>
  <a href=""><img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square" alt="Python"></a>
  <a href=""><img src="https://img.shields.io/badge/CodeX-Skill-green.svg?style=flat-square" alt="codex"></a>
  <a href=""><img src="https://img.shields.io/badge/Claude-Skill-yellow.svg?style=flat-square" alt="Claude"></a>
  <a href=""><img src="https://img.shields.io/badge/Open-Claw-8A2BE2.svg?style=flat-square" alt="OpenClaw"></a>
</p>

[English](README.md) | 简体中文 | [日本語](README.ja.md) | [한국어](README.ko.md)


`xxg-portrait-rebuild-light` 是用于现有人像照片的 image edit Skill。它以“导演式布光”重建主光、补光、阴影和背景氛围，同时恢复干净、健康、低对比的真实皮肤微纹理。

它强调改变光影，而不是重画人物：保持同一人物、原有五官结构与比例、自然轻微不对称、表情、姿势、镜头和构图；避免塑料皮、颗粒皮、脏灰色差和靠加深皱褶制造的假立体。

## 主要功能

- 修复塑料般平滑、过度磨皮和蜡像感；
- 保留原有唇纹、眼周层次、克制皮脂反光与尺度相符的微纹理；
- 修复逆光、室内窗光割裂、平光、非预期死黑和无来源高光；
- 支持柔和窗光、商业柔光、伦勃朗光、低调电影光、黄金时刻、双色霓虹和斜向硬光；
- 可加入一种物理一致的窗影、树影、背景 Bokeh、夕阳光晕、轻微体积光或主体全黑逆光剪影；
- 主体与背景分层控制：先定义主光与曝光意图，再定义 Fill、阴影、背景环境光和色温；
- 保持人物身份、五官大小与位置、表情、姿势、服装、背景结构和原画幅；
- 面部较小时自动降低微纹理目标，但不会因此取消用户指定的光影变化；
- 默认调用当前智能体自己的图片生成/编辑能力，不要求配置单独 API；
- 当前智能体没有 image edit 能力，或生成结果没有达到目标时，直接输出一段紧凑完整提示词；
- 禁止用 Pillow、NumPy、OpenCV、ImageMagick 或临时滤镜脚本制作交付图片。

![演示图片](/assets/skill-demo1.jpg "skill-demo")
![演示图片](/assets/skill-demo2.jpg "skill-demo")
![演示图片](/assets/skill-demo3.jpg "skill-demo")
![演示图片](/assets/skill-demo4.jpg "skill-demo")

## 核心方法

Skill 先在内部完成导演式决策：

```text
Key 主光 → Exposure 曝光意图 → Fill 补光 → Shadow 阴影 → Subject 主体 → Background 背景 → Atmosphere 氛围
```

真正送入图片模型的提示固定压缩为四行，通常 120–220 个中文字符：

```text
编辑：同一人物与原构图，只重建光影和肤质。
光影：一个主光 + 曝光意图 + 补光/阴影关系 + 背景响应 + 可选单一氛围。
肤质：与面部尺度匹配的干净、低对比真实微纹理。
限制：不换脸、不磨皮、不颗粒化、不脏化、不重绘背景。
```

不会把身份审计、物体清单、同义负向词和多套摄影风格全部堆进提示，以免互相抵消或直接复制原图。

光源效果优先于“所有内容都必须清楚”。Skill 会在 `source-matched`、`balanced`、`highlight-priority`、`shadow-priority`、`low-key`、`silhouette` 和 `high-key` 中选择曝光意图。夕阳逆光可以让面部背光侧自然变暗或成为剪影；低调与硬光可以出现近黑阴影；只有原本应当可读却发生无来源暗部丢失时才使用 Fill 修复。

`A6` 是强制覆盖项：只要选中，就切换为剪影曝光，把有效主光移到人物后方，取消全部补光与眼神光，并让整个人物内部落为全黑。所选 L 与 T 只控制背光和背景响应，S 不再产生可见肤质。

## 配方

一次只选择：

```text
一个 L 主光 + 一个 S 皮肤 + 一个 T 色温 + 零个或一个 A 氛围
```

### 主光 L

| 编号 | 用途 |
| --- | --- |
| `L0` | 匹配原片，只修平光、无来源死黑、异常高光与生硬过渡 |
| `L1` | 自然逆光，默认高光优先；明确要求补面时才增加 Fill |
| `L2` | 柔和窗边自然光 |
| `L3` | 商业大型柔光 |
| `L4` | 户外天空柔光 |
| `L5` | 室内实景灯与混合光 |
| `L6` | 单点硬光或直射阳光 |
| `L7` | 暗调斜向窄光带 |
| `L8` | 经典杂志伦勃朗光 |
| `L9` | 电影低调暖主光/冷环境 |
| `L10` | 黄金时刻夕阳侧逆光 |
| `L11` | 赛博朋克青/洋红双色霓虹 |
| `L12` | 商业极简均匀柔光 |

### 皮肤 S

| 编号 | 用途 |
| --- | --- |
| `S0` | 小脸或远景，只恢复干净肤色与自然反射 |
| `S1` | 中景默认，低对比微纹理、原唇纹和眼周层次 |
| `S2` | 高分辨率近景，分区孔理、细绒毛和原有细节 |

### 色温 T

| 编号 | 用途 |
| --- | --- |
| `T0` | 保持源图白平衡 |
| `T1` | 中性自然日光 |
| `T2` | 黄金暖光，保留健康肤色中性区 |
| `T3` | 暖色主光与冷色背景环境 |
| `T4` | 青/洋红霓虹关系 |

### 氛围 A

| 编号 | 用途 |
| --- | --- |
| `A0` | 不新增氛围效果 |
| `A1` | 柔软窗影 |
| `A2` | 稀疏自然树影 |
| `A3` | 仅限离焦背景的柔焦 Bokeh |
| `A4` | 夕阳方向一致的轻柔镜头光晕 |
| `A5` | 极轻体积光与稀疏微尘 |
| `A6` | 强制整个人物成为干净的逆光全黑剪影，内部不显示五官、肤色、发丝或衣物细节 |

详细提示句见[光影、皮肤、色温与氛围配方](references/lighting-skin-color-temperature-recipes.md)。

## 平台图片能力

| 智能体 | 默认方式 |
| --- | --- |
| Codex | 读取 `$imagegen` 规则，从 `ALL_TOOLS` 发现真实工具；优先调用 `tools.image_gen__imagegen`，源图使用 `referenced_image_paths` |
| Claude Code | 使用当前环境已安装或内置的图片生成/编辑能力 |
| OpenClaw | 使用当前 Agent 已启用的 imagegen Skill 或原生图片动作 |
| 其他智能体 | 使用工具注册表明确暴露的等价 image edit 能力 |

Codex 不猜测 `tools.image_gen` 或 `input_image`。只有工具发现确认不存在兼容图片能力时才输出提示词交接。图片工具真实失败，或生成结果近乎原图、改脸、脏化时，也会直接给出可复制的短提示词。

## 环境要求

- 支持目录型 `SKILL.md` 的智能体；
- 当前智能体的图片生成或图片编辑能力；
- Python 3.9 或更高版本，仅用于只读宽高比、蒙版与区域检查；
- Pillow 9.1 或更高版本，仅用于只读分析，不用于制作成片。

安装只读脚本依赖：

```bash
python3 -m pip install -r ./xxg-portrait-rebuild-light/requirements.txt
```

## 安装到 Codex

个人 Skill：

```bash
mkdir -p ~/.codex/skills
cp -R ./xxg-portrait-rebuild-light ~/.codex/skills/
```

通用 Agent Skills 目录：

```bash
mkdir -p ~/.agents/skills
cp -R ./xxg-portrait-rebuild-light ~/.agents/skills/
```

项目级安装可放入项目根目录 `.agents/skills/`。安装后输入 `$xxg-portrait-rebuild-light` 显式调用。

## 安装到 Claude Code

个人安装：

```bash
mkdir -p ~/.claude/skills
cp -R ./xxg-portrait-rebuild-light ~/.claude/skills/
```

项目安装：

```bash
mkdir -p .claude/skills
cp -R ./xxg-portrait-rebuild-light .claude/skills/
```

使用时输入 `/xxg-portrait-rebuild-light`。

## 安装到 OpenClaw

本地安装：

```bash
openclaw skills install ./xxg-portrait-rebuild-light \
  --as xxg-portrait-rebuild-light
```

共享安装：

```bash
openclaw skills install ./xxg-portrait-rebuild-light \
  --as xxg-portrait-rebuild-light \
  --global
```

也可完整复制到当前 Agent 工作区的 `skills/` 或共享目录 `~/.openclaw/skills/`。

## 安装到其他智能体

将整个 `xxg-portrait-rebuild-light/` 目录复制到该工具的个人或项目 Skill 根目录，保留 `SKILL.md`、`requirements.txt`、`references/`、`scripts/` 和 `agents/` 的相对结构，然后重新加载 Skill 列表。

## 使用范例

### 经典时尚杂志

```text
使用 $xxg-portrait-rebuild-light 编辑这张人像，L8 + S2 + T1 + A0。
侧前上方大型柔光塑造克制伦勃朗光，轻微补光保留眼窝，一侧面颊阴影深柔，只有一处同源眼神光；皮肤干净健康、低对比真实微纹理。
```

### 电影低调冷暖

```text
使用 $xxg-portrait-rebuild-light 编辑这张人像，L9 + S1 + T3 + A5。
暖色侧主光塑造明暗面，采用低调曝光并取消正面补光，背光侧可接近黑色；冷色只留在背景与轮廓，加入极轻体积微尘，不要脏灰或加深皱褶。
```

### 黄金时刻逆光

```text
使用 $xxg-portrait-rebuild-light 编辑这张人像，L10 + S1 + T2 + A4。
暖色夕阳从侧后方勾勒发丝与肩部，按夕阳高光曝光且不加正面补光；面部背光侧自然压暗成局部剪影，受光边缘可轻微溢出，背景同步出现斜射暖光与长阴影。
```

### 赛博朋克霓虹

```text
使用 $xxg-portrait-rebuild-light 编辑这张夜景人像，L11 + S1 + T4 + A3。
青色轮廓光和洋红主光方向分明，面部中央保留自然肤色；Bokeh 只在背景离焦区，不覆盖眼睛与皮肤。
```

### 主体全黑逆光剪影

```text
使用 $xxg-portrait-rebuild-light 编辑这张人像，L10 + S1 + T2 + A6。
把有效主光置于人物后方并按明亮背景曝光，取消全部正面/侧面补光、眼神光和人物内部受光；脸、皮肤、头发、衣物与身体内部统一成为干净连续的全黑剪影，同时保持原人物外轮廓、头身比例、姿态、镜头和构图。
```

### 柔和窗边自然光与窗影

```text
使用 $xxg-portrait-rebuild-light 编辑这张室内人像，L2 + S1 + T1 + A1。
左前上方柔窗光形成宽缓左明右暗，微弱室内补光保留暗侧；一层低对比窗影连续落在人物和邻近墙面，不像贴纸。
```

### 树影人像

```text
使用 $xxg-portrait-rebuild-light 编辑这张户外人像，L4 + S1 + T1 + A2。
宽广天空柔光照亮人物，稀疏树影随面部与衣物曲率轻柔断续，可按真实落点跨过局部眼睛与面颊，并在背景出现同向响应；阴影保持干净，不形成无来源脏斑。
```

## 输出标准

- 目标主光、明暗关系或氛围效果在正常观看下直接可辨；
- 人物仍是输入照片中的同一个人，五官不被美型或对称化；
- 主体、衣物和背景服从同一组光源；
- 暗部深度、高光滚降与剪影程度服从选定曝光意图，不为“全部清楚”而破坏逆光或低调关系；
- 皮肤白皙健康、干净连续，有低对比真实微纹理但不粗糙、不斑驳；
- 不用颗粒、色差、脏灰阴影、局部锐化或加深皱褶冒充真实感；
- 窗影、树影、Bokeh、夕阳光晕和光束具有来源与落点；
- 选择 `A6` 时，整个人物内部必须干净全黑，不显示五官、肤色、发丝、衣物或眼神光细节；身份连续性改由外轮廓、比例、姿态和构图判断；
- 保持原构图、方向、宽高比和主体占画比例；允许图片模型按其最大分辨率等比例缩小，不要求原始像素尺寸一致。

## 相关文件

- [Skill 主规则](SKILL.md)
- [紧凑提示词编译器](references/prompt-recipes.md)
- [光影、皮肤、色温与氛围配方](references/lighting-skin-color-temperature-recipes.md)
- [后端能力说明](references/backend-and-clean-realism.md)
- [Python 依赖](requirements.txt)
- [贡献指南](CONTRIBUTING.md)
- [更新日志](CHANGELOG.md)

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
