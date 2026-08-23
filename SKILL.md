---
name: xxg-portrait-rebuild-light
description: "Relight an existing JPG, JPEG, PNG, or WebP portrait and restore clean photographic skin texture while preserving identity, natural asymmetry, proportions, expression, pose, composition, and framing. Use for 真实肤质、去塑料感、光影重建、人物补光、逆光修复、窗光/窗影、树影、Bokeh、黄金时刻、霓虹、影棚柔光、暗调写真、主体全黑剪影, relight, silhouette, or Higgsfield-Relight-like edits. Discover the host image-edit tool first; in Codex use discovered image_gen__imagegen with referenced_image_paths. Never guess image_gen/input_image, make the final with local pixel scripts, or refuse for small faces or complex scenes."
---

# XXG 人像真实光影重建

## 目标

把输入视为同一张摄影原片，只重建光影与皮肤呈现：

- 保持身份、自然不对称、面部结构与比例、表情、姿势、镜头和构图；
- 用一个物理明确的主光统一人物、衣物与背景，允许符合曝光意图的深暗、溢出和剪影；
- 让受光皮肤干净健康、低对比且有尺度相符的相机微纹理，不用颗粒、色差或加深皱褶制造真实感。

目标变化必须在正常观看下可辨。不要为了“全部清楚”把逆光、低调或硬光补成平均曝光。

## 调用宿主图片能力

1. 查看源图并读取宿主原生图片生成/编辑 Skill。
2. 从工具注册表发现真实 callable；Codex 从 `ALL_TOOLS` 查找，并优先选择准确名称 `image_gen__imagegen`。
3. Codex 编辑本地源图只使用已发现工具及真实参数：

```js
const result = await tools.image_gen__imagegen({
  referenced_image_paths: ["/absolute/path/source.png"],
  prompt: "四行紧凑 image edit 提示词"
});
generatedImage(result);
```

禁止猜测 `tools.image_gen` 或 `input_image`。错误函数名、参数或 `TypeError` 是调度错误，应按真实签名重试，不能据此判定工具不可用。Claude、OpenClaw 等使用其注册表明确暴露的等价原生 image-edit 动作。

## 状态分流

| 状态 | 动作 |
| --- | --- |
| 发现兼容工具 | 必须调用；小脸、复杂背景、文字或主体触边只降低纹理目标，不停止生成 |
| 正确工具真实调用失败 | 说明真实错误，进入 `prompt-only`，输出完整短提示词 |
| 完成发现且无兼容工具 | 进入 `invocation-handoff`，输出完整短提示词 |
| 已生成但近乎原图、改脸、脏化或光影失败 | 告知“本次图片结果未达到目标改善”，进入 `prompt-handoff`，从原图重编提示词 |

读取 Skill、查看图片、创建任务或输出“正在调用”都不算图片工具调用。

## 禁止本地制作成片

不得用 Pillow、NumPy、OpenCV、ImageMagick、FFmpeg、`sips` 或自写脚本生成、补光、调色、磨皮、锐化、加纹理、裁切、扩边、缩放、合成或修复交付图。它们仅可执行只读比例、蒙版和结果审计；依赖见 `requirements.txt`。

## 编译图片提示词

读取 [配方](references/lighting-skin-color-temperature-recipes.md) 和 [提示词编译器](references/prompt-recipes.md)，内部按 `Key → Exposure → Fill → Shadow → Subject → Background → Atmosphere` 决策。每次只选：

```text
一个 L + 一个 S + 一个 T + 零个或一个 A
```

只保留一套主光；Atmosphere 必须服从主光。A6 是唯一覆盖项：选中后强制 `silhouette`、主光在人物后方、无 Fill/眼神光/内部受光；整个人物内部全黑，L/T 只控制背光与背景，S 不显示。

实际发送内容固定为四行：

```text
编辑：身份与结构不变量。
光影：主光、曝光、暗部、背景、色温及可选氛围。
肤质：一个尺度相符的 S 目标；A6 改为内部全黑。
限制：4 个最高风险禁止项。
```

- 默认 100–180 个中文字符；复杂场景最多 260 个；
- 身份只锁定一次，保护物最多点名三类；
- 正向可见结果优先，不写审计、编号、置信度或后端说明；
- 不堆同义负向词，不使用“完全不变、最小变化”压制编辑；
- 重试时替换失败行，不在旧提示后追加约束。

所有 handoff 使用同一四行结构且不得留占位符。

## 编辑边界

- **结构不变量**：身份、脸型/头脸比例、五官位置与大小、自然不对称、表情、视线、发际线、姿势、相机视角、构图与人物占画比例；禁止美型或对称化。
- **允许变化**：皮肤、头发、衣物和邻近背景的同源亮度、反射、投影、色温及用户指定氛围。
- **A6 例外**：内部五官按授权不可见；改用头发/头部外轮廓、头身比例、姿态和位置判断结构保持。

## 皮肤与光影底线

- 按配方选择 S0/S1/S2；正常观看先干净连续，放大后才见低对比、非重复微纹理。黑头、痣、卡粉等默认只保留源图已有内容。
- Fill 只在曝光意图要求暗部可读时使用；低调、高光优先和剪影可无 Fill。
- 阴影软硬服从光源面积和距离；人物、衣物与背景共享方向、衰减和反射。
- 窗/树影需跨主体与邻近表面，Bokeh 仅在离焦区，光束需有介质和方向，霓虹需有主次。
- A6 暂停肤质可见性：脸、皮肤、头发、衣物及身体内部必须干净全黑，不得残留面光、肤色、眼神光、发丝或衣纹；仅允许不侵入内部的极窄同源轮廓溢光。

## 画幅

保持方向、宽高比、构图和人物占画比例；允许后端等比例缩小，不要求原像素尺寸。有本地结果时只读检查：

```bash
python3 "$XXG_SKILL_DIR/scripts/check_aspect_ratio.py" SOURCE_IMAGE EDITED_IMAGE
```

相对比例偏差 `≤5%` 通过。不得用本地脚本修正尺寸、裁切或补边。

## 结果验收

生成后读取 [身份与细节审计](references/identity-and-detail-audit.md)，按正常观看倍率先检查：

1. 目标主光、曝光和氛围是否直接可辨且物理一致；
2. 身份、结构、姿势与构图是否稳定；A6 改查外轮廓、比例与姿态；
3. 受光皮肤是否干净、真实且无颗粒/脏灰/假立体；A6 改查人物内部是否连续全黑；
4. 背景与主体是否同源，窗影、树影、Bokeh、霓虹或光束是否有合理落点；
5. 方向、比例与人物占画是否保持；等比例缩小不算失败。

近乎原图时加强唯一主光和一个可观察结果；脏化时把肤质行替换为“干净连续肤色 + 低对比反射微纹理”。失败图不得冒充成片。

## 按需读取

- 每次编译提示：`references/prompt-recipes.md`、`references/lighting-skin-color-temperature-recipes.md`
- 调用、能力分级或失败分流：`references/backend-and-clean-realism.md`
- 生成后验收：`references/identity-and-detail-audit.md`
- 仅严格局部后端：`references/edit-plan-and-protection.md`
