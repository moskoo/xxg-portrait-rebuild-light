# 身份、肤质与结果验收

## 证据

调用/交付状态遵循 [后端能力契约](backend-and-clean-realism.md)。有结果时查看：原图与结果完整画面、同坐标脸部裁切、200%–400% 并排对比，以及比例检查原始输出。尺寸不同时用归一化位置比较，不做本地缩放；等比例缩小不判失败。

保存最小运行记录：

```yaml
source_size: [W, H]
face_box: [x1, y1, x2, y2]
face_top_y: y_top
chin_y: y_chin
face_height_px: y_chin - y_top
face_height_ratio: face_height_px / H
audit_regions:
  face: [x1, y1, x2, y2]
  hair: [x1, y1, x2, y2]
  clothing: [x1, y1, x2, y2]
  background: [x1, y1, x2, y2]
light:
  mode: match-source | relight
  atmosphere_recipe: A0 | A1 | A2 | A3 | A4 | A5 | A6
  exposure_intent: source-matched | balanced | highlight-priority | shadow-priority | low-key | silhouette | high-key
  fill_policy: none | ambient-reflection | explicit-fill
  shadow_policy: retained-detail | deep-clean | near-black | silhouette
  highlight_policy: retained | soft-rolloff | controlled-clipping
  confidence: low | medium | high
  evidence: [{type, object, observation}]
  contradictions: []
```

`face_height_px` 必须由坐标相减；审计区前后使用相同坐标。光源置信度由证据一致性决定：`low` 用 `match-source`，`medium` 仅低幅修正，`high` 才明确 relight。

## 严格保护门

仅 `strict-local` 使用 [编辑计划](edit-plan-and-protection.md)：九格完整、逐项保护、计数一致、冻结条目均入联合保护蒙版，且编辑/保护蒙版零交集。运行 `scripts/validate_edit_plan.py`；失败则转 `best-effort` 继续生成。

## 面部尺度

| 高度 | 可验收细节 |
| --- | --- |
| `≥512 px` | 低对比孔理、细绒毛、浅纹、唇纹和皮脂反光 |
| `256–511 px` | 克制孔理、唇纹、眼周层次和局部反光 |
| `<256 px` | 连续肤色、宽缓受光和自然反射；微纹理不作硬目标 |

不得要求源图采样不到的毛孔。

## 身份门

| 区域 | 比较项 |
| --- | --- |
| 眼眉 | 眼裂/眼角/眼睑/虹膜与原左右差；眉头峰尾及边缘 |
| 鼻 | 鼻梁/鼻翼宽度、鼻尖、鼻孔轮廓与位置 |
| 唇 | 唇峰/唇线/开合/嘴角及上下唇比例 |
| 外轮廓 | 颧颊、下颌/下巴、耳、发际线 |
| 表情 | 视线、眼睑张力、嘴角和肌肉状态 |

可见边界、开合、尺寸或“更精致”的重解释均失败。A6 内部五官按授权不可见，改查头发/头部/耳/肩颈/肢体外轮廓、头身比例、姿态、位置和构图；不得借黑填改头型、身材或手势。

## 皮肤门

只检查源图可见且分辨率足够的区域：

| 区域 | 通过 | 失败 |
| --- | --- | --- |
| 脸颊 | 低对比、低密度、随曲率的柔和孔理 | 磨皮、重复孔洞、黑点毛孔、噪点 |
| 鼻头/鼻翼 | 略清晰孔理；已有黑头可保留 | 污浊、夸张黑点、鼻翼重绘 |
| 额头 | 克制皮脂反光/极细绒毛 | 大片油亮、塑料高光、统一颗粒 |
| 眼下 | 年龄相符浅纹与色调 | 新增眼袋/皱纹或眼睑变化 |
| 嘴唇 | 原唇线/颜色与自然纵纹 | 改唇形、丰唇、重画唇线 |
| 妆面 | 原妆不变，仅保留已有粉体分离 | 改色、浓妆、新增粉屑/脏化 |
| 颈/锁骨 | 裸露区肤色连续、反光克制 | 新增裸露、色斑、暗纹/假纹理 |

完整画面先见干净连续，放大后才见低对比、低密度、非重复纹理；禁止彩斑、脏灰、漂白、脸颈断层、全局颗粒/色噪/锐化砂感。任何明显失败进入 `prompt-handoff`，不得本地修补。

`<256 px` 不因毛孔不明显失败。A6 将皮肤分区标为 `not-applicable-by-design`，改查内部连续全黑、无彩污/颗粒/灰斑/残留面光。

## 光影门

- 眼神光、鼻/眼窝/颧/下颌/颈影、发丝、服装和背景服从同一光源；无双重阴影、白边或脱节。
- 光可改变亮度/反射，不得移动五官边界或靠局部加深重塑脸。
- 暗部、高光和 Fill 服从曝光意图；low-key/silhouette 可丢内部细节，highlight-priority 可受控溢出。
- 只有 source-matched/balanced 中的无来源死黑、断层或脏灰才算暗部丢失。
- A6 必须 `fill_policy: none` 且内部全黑；任何五官、肤色、眼神光、发丝高光、衣纹/饰品明暗均失败。

## 比例与构图门

运行 `scripts/check_aspect_ratio.py`；相对宽高比偏差 `≤5%` 通过。允许边长取整和等比例缩小；绝对尺寸不比较。拉伸、方向改变、裁切/扩图、比例超差或人物位置/占画变化才失败。禁止本地缩放、裁切或补边修正。

## 严格像素审计

仅结果同尺寸且为 `strict-local` 时运行：

```bash
python3 "$XXG_SKILL_DIR/scripts/audit_pixel_regions.py" SOURCE EDITED \
  --manifest EDIT_PLAN.json --output pixel-audit.json
```

脚本必须覆盖全部 `required_audit`；计划缺失、清单/计数不全、蒙版相交、漏审或冻结像素变化均失败。结果等比例缩小时跳过差分，按 `best-effort` 视觉检查。

## 目标改善门

每个必需目标预先写 `acceptance_view`/`acceptance_criterion`，生成后记录 `pass`、观察和证据。正常倍率无改善，即使差分或极端放大可见，也判失败。

- 光影仍平、冲突或近乎原图：失败；有意低调/剪影/溢出不是缺陷。
- 皮肤仍塑料或只改亮度/色温：失败；`<256 px` 微纹理可不适用。
- A6：皮肤微纹理不适用；必需目标为内部全黑并保持外轮廓/比例/姿态。只压暗脸、残留细节或灰填均失败。

严格结果运行 `scripts/validate_result_assessment.py`。任一必需目标为 `fail`/`not_verifiable`、缺证据或遗漏，进入 `prompt-handoff`。

## 结论

身份、比例/构图、冻结区/清单、必需目标、光影、干净真实感或 A6 任一适用门失败，都取消成片资格。说明“本次图片结果未达到目标改善”并输出从原图重编的完整短提示；失败图不得冒充成片，也不得用本地脚本修复。全部适用门通过才交付。
