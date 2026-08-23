# 后端能力与干净真实感

## 交付模式

| 模式 | 进入条件与交付 |
| --- | --- |
| `strict-final` | 已验证 `strict-local`、编辑计划和全部验收；可声明严格成品 |
| `best-effort` | 缺少冻结/蒙版能力仍调用整图语义编辑；标记“非严格尽力编辑”，不声称像素冻结 |
| `invocation-handoff` | 工具发现完成且无兼容 callable；输出完整短提示，不声称调用失败 |
| `prompt-only` | 正确图片工具有真实失败记录；引用错误摘要并输出完整短提示 |
| `prompt-handoff` | 已生成但目标、身份、保护项或比例/构图失败；告知未达标并从原图重编提示 |

面部小、场景复杂、文字或能力不足只触发 `best-effort`，不得拒绝。等比例缩小不是失败。

## 原生工具路由

1. 读取宿主原生图片 Skill，查看源图并搜索工具注册表；Codex 从 `ALL_TOOLS` 优先选 `image_gen__imagegen`。
2. Codex 本地源图使用 `tools.image_gen__imagegen({referenced_image_paths: [绝对路径], prompt})`。
3. 错误成员、函数名、参数或 `TypeError` 只算调度错误；按真实签名重试。
4. 返回后按能力分为 `strict-local` 或 `full-frame-generative`；默认不绕过宿主走 CLI/API。

禁止猜测 `tools.image_gen`/`input_image`。读取 Skill、查看源图、创建任务或输出状态都不是工具调用。

## 调用证据

| 状态 | 必需证据 | 模式 |
| --- | --- | --- |
| 已生成 | 图片工具调用 + 图片/结果 ID/可访问文件 | 验收后 `strict-final` 或 `best-effort` |
| 调用失败 | 正确工具调用 + 同次明确错误 | `prompt-only` |
| 无工具 | `tool_discovery_completed: true`、候选记录、`selected_image_tool_name: null` | `invocation-handoff` |
| 调度错误 | 错函数/参数产生本地错误 | 纠正重试，不得交接 |
| 结果失败 | 图片存在 + 视觉/文件验收失败 | `prompt-handoff` |

## 后端分级

匹配 [backend-capabilities.json](backend-capabilities.json)；未知路径归为 `full-frame-generative`。使用登记档案时运行 `scripts/evaluate_backend_gate.py`。

`strict-local` 必须同时具备：任务前已暴露的语义图片编辑、编辑/保护蒙版、未编辑像素直通、可验证固定画布，以及本地结果文件。提示中的“冻结”不是工具能力；任一能力缺失就降级生成，不停止。

Pillow、NumPy、OpenCV、ImageMagick、FFmpeg、`sips` 和临时滤镜不算语义后端，只能只读量测/审计，不能制作交付图。

## 生成决策

| 场景 | 策略 |
| --- | --- |
| 已验证 `strict-local` | 按已验证编辑计划局部编辑，全部门通过才交付严格成品 |
| `full-frame-generative` | 整图生成并标记尽力；降低重绘/纹理，保留目标光影 |
| 脸 `<256 px` | 关闭新增微纹理，不降低场景级光影 |
| 文字/商品/复杂物体/多人/触边 | 点名最高风险保护物，降低背景重绘；同源亮度/反射仍可变化 |
| A6 | 不因脸小降强度；授权完整人物内部变黑，冻结外轮廓、比例、姿态、构图和背景 |

整图提示区分 `structural_invariants`、`authorized_appearance_changes` 和一个正常观看可辨的 `minimum_visible_improvement`。近乎原图不能以“克制”通过。

## 干净真实感

| 频率 | 通过 | 禁止 |
| --- | --- | --- |
| 低频肤色 | 原肤色基准连续，亮度服从光源，脸耳颈胸宽缓过渡 | 红黄灰斑、脏灰、局部漂白、脸颈断层 |
| 中频体积 | 颧鼻下颌颈肩由受光、遮挡和投影塑形 | 加深眼袋/法令纹/鼻翼沟，局部 clarity、HDR、强 dodge-and-burn |
| 高频表面 | 毛孔/绒毛/浅纹/唇纹低对比、低密度、非重复 | 黑点毛孔、全局颗粒、色噪、锐化砂感、粉屑和重复纹理 |

黑头、痣、雀斑、卡粉、浮粉和干皮默认只保留源图已有内容；明确新增黑头也仅限高分辨率近景的极少量低对比点。A6 跳过肤质可见性，改查人物内部是否干净连续全黑且无颗粒/彩污/残留面光。

## 光影边界

- 先定 `exposure_intent`，再定 Fill、阴影和高光；Fill 只在暗部需可读时使用。
- 柔光宽缓、硬光边缘清楚；不得新增第二鼻影/眼神光或用烧暗制造体积。
- 逆光保亮源/背景/轮廓；低调与剪影可近黑，高光优先可自然溢出。
- 室内窗光需同时解释人物、衣物、墙桌、反射物和房间衰减；证据不足则 `match-source`。
- A6 强制 `silhouette + fill none`，人物内部全黑；极窄同源轮廓溢光不得侵入内部。

画外窗光置信度：`high`=可见窗或至少三类一致证据，可明确 relight；`medium`=两类证据，只低幅修正；`low`=证据不足/冲突，使用 `match-source`。不要把推测写成事实。

## 失败映射

| 失败 | 动作 |
| --- | --- |
| 后端缺严格能力 | `best-effort` 继续生成并说明缺失能力 |
| 无工具/真实调用失败 | 分别用 `invocation-handoff` / `prompt-only` |
| 近乎原图、目标/身份/保护/比例失败 | `prompt-handoff`；不得本地修图补救 |
| 皮肤脏粗或假立体 | 肤质行改为清洁连续 + 低对比，删除局部加深/颗粒 |
| A6 残留内部细节或灰填 | 删除普通 S、Fill/catchlight/人物受光，明确内部连续全黑 |
