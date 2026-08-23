# 严格局部编辑计划与保护门

仅已验证 `strict-local` 使用本文件；交付模式和工具证据遵循[后端能力契约](backend-and-clean-realism.md)。严格能力不足则转 `best-effort` 继续生成，不创建虚假冻结计划。

## 全图盘点

把画面分成 `r1c1`–`r3c3` 九格，全部查看后才设置 `inventory_complete: true`。逐项登记：

- 每只眼/眼睑、眉、鼻翼/鼻孔、唇线/嘴角、下颌、耳、发际线；
- 头发、辫子、散发、服装、肩带、饰品、手和姿势边界；
- 每一本书及文字、电脑/手机、杯子、灯具、商品；
- 门桌椅、书架、植物、墙地面、窗户和触边物体。

同类物体也分项记录唯一 `id`、描述、tile、`bbox`，必要时加 `mask_path`。用 [edit-plan-template.json](edit-plan-template.json) 建立计划；`protected_item_count`/`inventory_counts` 必须匹配条目。

## 编辑计划

严格计划包含：源图尺寸（仅坐标/同尺寸审计）、已验证后端、九格清单、`editable_mask`、冻结条目联合 `protected_mask`、实际曝光/Fill/阴影/高光策略，以及每个必需感知目标的验收视图和标准。

只有用户授权对象可标 `authorized-edit`；其余均为 `frozen + required_audit`。整图 `best-effort` 改列：

- `structural_invariants`：身份几何、构图和物体内容；
- `authorized_appearance_changes`：皮肤反射、连续色调、目标阴影与场景光响应；
- `minimum_visible_improvement`：完整画面正常观看可辨。

A6 授权人物轮廓内部的亮度、肤色、五官可见性、头发/衣物/饰品表面变黑；冻结外轮廓、比例、姿态、构图和背景。严格蒙版覆盖完整人物内部并止于原轮廓，不得只压暗面部。

## 蒙版门

```bash
python3 "$XXG_SKILL_DIR/scripts/validate_edit_plan.py" EDIT_PLAN.json \
  --output edit-plan-validation.json
```

九格、计数、后端、尺寸、冻结覆盖或编辑/保护蒙版任一验证失败，不执行严格方案；修正计划或转 `best-effort`。`bbox` 默认整块保护，需要更精确时提供条目蒙版，不得缩小矩形绕过物体。

## 冻结区审计

仅同尺寸严格结果运行：

```bash
python3 "$XXG_SKILL_DIR/scripts/audit_pixel_regions.py" SOURCE EDITED \
  --manifest EDIT_PLAN.json --output pixel-audit.json
```

脚本重验计划并自动覆盖全部 `required_audit`。缺 manifest、漏项/漏审、计数不符、蒙版相交或冻结像素变化均不得返回严格 PASS。等比例缩小时跳过像素差分，改做 `best-effort` 视觉检查。

## 目标改善

为每个 `perceptual_targets` 记录 `status`、具体 `finding` 和完整画面/规定倍率 `evidence`，再运行：

```bash
python3 "$XXG_SKILL_DIR/scripts/validate_result_assessment.py" \
  EDIT_PLAN.json RESULT_ASSESSMENT.json --output target-validation.json
```

正常倍率几乎无改善时必须 `fail`，不能用差分图或“处理克制”代替目标达成。A6 必需目标：整个人物内部连续全黑，无五官/肤色/眼神光/发丝高光/衣纹，同时保持外轮廓、比例、姿态、位置和背景；普通肤质目标标为不适用。

任一必需目标未达标就进入 `prompt-handoff`：说明失败并从原图重编完整短提示，不做本地补救，不把失败图作为成品。
