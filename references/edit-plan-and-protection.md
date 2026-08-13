# 编辑计划、保护清单与蒙版门

## 目录

- 五种交付模式
- 全图保护项盘点
- 编辑计划
- 蒙版零交集门
- 清单驱动验收
- 目标改善门

## 五种交付模式

- `strict-final`：默认模式。身份、构图、保护项和宽高比必须保持；允许等比例缩小。只能使用 `strict-local` 后端证明冻结像素直通。
- `best-effort`：严格能力不可用时自动进入。仍须生成图片，但只能声称尽量保持身份、构图和保护项，不能声称像素冻结。
- `invocation-handoff`：已经完成工具注册表发现，并确认不存在兼容图片生成/编辑 callable 时进入。完成保护项盘点并展开完整提示词，但不创建虚假的结果审计。发现了正确工具但尚未调用、或因错误函数名/参数产生本地 `TypeError` 时不得进入。
- `prompt-only`：存在真实图片工具调用记录，且该调用明确返回不可用/失败时进入。仍需完成保护项盘点，但不创建虚假的编辑蒙版或结果审计；把保护项和真实错误摘要直接展开进交付说明与完整 image edit 提示词。
- `prompt-handoff`：图片工具已运行但必需目标、身份/保护项或宽高比/构图门失败。等比例缩小不是失败。告知失败，并把基于原图的完整提示词作为主要交付物。

不要用 `exact_identity_required` 决定是否生成。严格身份由 `strict-final` 表达；原生 imagegen 选中的语义图片能力无法满足严格条件时由决策脚本自动降级为 `best-effort`。先从工具注册表发现真实 callable；Codex 发现 `image_gen__imagegen` 后使用 `referenced_image_paths` 调用。只有确认无兼容工具时交付 `invocation-handoff`，正确工具有真实调用记录且明确失败时才交付 `prompt-only`；图片结果未通过目标或硬门时交付 `prompt-handoff`。临时 Pillow/NumPy/OpenCV 脚本或命令行滤镜不得登记为图片后端，只能做只读量测与审计。

## 全图保护项盘点

在创建编辑蒙版前，把完整画面均分为 3×3 九个区域，按 `r1c1` 到 `r3c3` 逐格查看。全部九格看完后才可设置 `inventory_complete: true`。

逐个登记而不是合并成宽泛类别：

- 五官和身份边界：每只眼及眼睑、眉、鼻孔/鼻翼、唇线/嘴角、下颌、耳、发际线；
- 头发、辫子、散发、服装、肩带、饰品、手与姿势边界；
- 每一本书、每个书页/书脊/封面文字、电脑、手机、杯子、灯具和商品；
- 门、桌、椅、书架、植物、墙面、地面、窗户及其他背景物体；
- 接触画面边缘的主体或重要物体。

同类物体也必须逐个登记。例如手持书、桌上书、右侧立书和书架书籍是不同条目；不得只登记“书籍”。每个条目记录唯一 `id`、具体描述、所在 tile、`bbox`，必要时提供精确 `mask_path`。

使用 [edit-plan-template.json](edit-plan-template.json) 建立计划。`protected_item_count` 和 `inventory_counts` 必须与条目精确相符。

## 编辑计划

严格成品计划必须包含：

- 源图内部像素尺寸，仅用于蒙版坐标和同尺寸严格像素审计，不作为最终交付分辨率要求；
- 已验证的 `strict-local` 后端能力；
- 完整九格盘点与逐项保护清单；
- `editable_mask` 和全部冻结条目联合形成的 `protected_mask`；
- 与目标光型一致的 `exposure_intent`、`fill_policy`、`shadow_policy` 和 `highlight_policy`；不得直接沿用模板示例值；
- 与用户问题对应的必需感知目标及具体通过标准。

整图 `best-effort` 不建立虚假的像素冻结计划，但必须另列两组字段：`structural_invariants` 只放身份几何、构图和物体内容；`authorized_appearance_changes` 明确允许皮肤反射、连续色调、目标阴影和场景光照响应发生变化。至少设置一个 `minimum_visible_improvement`，要求在 100% 完整画面直接可辨。不得把全部画面同时写成“保持不变”。

只允许把用户逐项授权改变的对象标为 `authorized-edit`，并记录授权原文。其他条目一律 `frozen` 且 `required_audit: true`。

选择 A6 时，把人物轮廓内部的亮度、肤色、五官可见性、头发、衣物与饰品表面统一登记为 `authorized-edit`；只冻结人物外轮廓几何、头身比例、姿态、构图和背景物体。不得冻结人物内部原像素后又要求其变为全黑，也不得把 A6 缩减为仅面部压暗。严格局部蒙版应覆盖完整人物内部并止于原外轮廓；后端不能可靠完成时转为 `best-effort`，仍保留“全人物内部黑色”的最低可见改善目标。

## 蒙版零交集门

在严格局部编辑前运行：

```bash
python3 "$XXG_SKILL_DIR/scripts/validate_edit_plan.py" EDIT_PLAN.json \
  --output edit-plan-validation.json
```

脚本同时验证：九格盘点、条目计数、后端能力、蒙版尺寸、冻结条目是否进入保护联合蒙版，以及编辑蒙版是否碰到任一冻结条目。只要存在一个重叠像素就不得执行该严格局部方案；修正蒙版，或自动改用整图尽力编辑并继续生成。整图模式降低纹理与背景重绘，但光影强度仍按用户目标选择。

矩形 `bbox` 默认整块受保护。若矩形过于保守，必须提供更精确的条目蒙版；不得通过缩小矩形绕过真实物体。

## 清单驱动验收

严格局部结果生成后只允许用同一编辑计划自动审计：

```bash
python3 "$XXG_SKILL_DIR/scripts/audit_pixel_regions.py" SOURCE EDITED \
  --manifest EDIT_PLAN.json \
  --output pixel-audit.json
```

脚本会重新核对严格后端能力、九格盘点、计数、蒙版零交集和冻结条目覆盖，再自动检查清单中所有 `required_audit` 条目。只有源图与结果恰好同尺寸时才运行精确像素审计；结果等比例缩小时跳过该审计并按 `best-effort` 做全图与人脸视觉对比，不因缩小而判失败。没有 manifest、清单不完整、漏审条目或同尺寸结果中任一冻结像素变化时均不能返回严格 PASS。命令行 `--region` 只可补充观察区，不能替代 manifest。

## 目标改善门

严格局部编辑中，像素局部性通过不等于编辑目标通过。为每个 `perceptual_targets` 条目建立结果记录：

```json
{
  "target_results": [
    {
      "id": "lighting-direction",
      "status": "pass",
      "finding": "完整画面可辨认出指定主光与曝光意图，暗部深度和高光滚降合理，且无新眼神光或接缝",
      "evidence": ["full-comparison.png", "face-100pct.png"]
    }
  ]
}
```

运行：

```bash
python3 "$XXG_SKILL_DIR/scripts/validate_result_assessment.py" \
  EDIT_PLAN.json RESULT_ASSESSMENT.json \
  --output target-validation.json
```

只在正常验收倍率下能明确看出用户问题得到改善时才填 `pass`。只有差分图、极端放大或数值统计能看出变化，正常观看几乎无改善时必须填 `fail`；不得用“处理很克制”代替目标达成。任一必需目标未达标时进入 `prompt-handoff`：用一句话告知失败，并直接输出从原图事实展开的完整提示词；不做本地脚本补救，也不返回失败图作为主要成品。

A6 的必需目标写为：正常观看时整个人物内部连续全黑，无五官、肤色、眼神光、发丝高光或衣纹；原外轮廓、比例、姿态、人物位置与背景结构保持。普通皮肤微纹理目标必须标记为不适用，不能要求同时通过。
