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
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/Version-2.0.0-black?style=flat-square" alt="Version 2.0.0"></a>
</p>

[English](README.md) | [简体中文](README.zh-CN.md) | 日本語 | [한국어](README.ko.md)


`xxg-portrait-rebuild-light` は、既存のポートレート写真を対象とする image edit Skill です。V2 は、光、肌の広い色調、局所反射、スケールと焦点に応じた微細質感、肌の写真的仕上がりを分離して制御し、汚れ、暗さ、粒子、ランダムな欠点に頼らずリアリティを作ります。

人物を描き直すのではなく、光を変えることを重視します。同一人物であること、顔の構造と比率、自然なわずかな左右差、表情、ポーズ、カメラ視点、構図を維持し、プラスチック肌、粒状肌、汚れた色むら、しわを強調して作る偽の立体感を避けます。

## 主な機能

- `texture-only` により、元の光、色、焦点、被写界深度、シーン内容を変えずに肌の忠実度だけを回復。
- 清潔な広域色調、元の光源に沿う限定的なハイライト、部位別の微細質感を分離してプラスチック感を解消。
- 元画像一致、サテンマット、柔らかな昼光、エディトリアル、直射フラッシュ、ビューティー、環境光の `P0–P6` を搭載。
- プラスチックのような平滑さ、過度な美肌処理、蝋人形のような質感を修正。
- 元の唇のしわ、目元の階調、控えめな皮脂反射、顔の表示サイズに合う微細質感を保持。
- 弱い逆光、室内の不自然に分断された窓光、平板な光、意図しない黒つぶれ、光源のないハイライトを修正。
- 柔らかな窓光、商業用ソフトライト、レンブラント光、映画的ローキー、ゴールデンアワー、2 色ネオン、斜めの硬い光に対応。
- 物理的に整合する窓影、木漏れ日、背景ボケ、夕日のフレア、微かなボリュームライト、または人物全体の黒い逆光シルエットを最大 1 種類追加。
- 主体と背景を分けて制御し、キーライトと露出意図を先に決め、その後にフィル、影、背景環境光、色温度を定義。
- 人物の同一性、顔パーツの大きさと位置、表情、ポーズ、衣装、背景構造、元のフレーミングを保持。
- 顔が小さい場合は肌の微細質感の目標だけを自動的に下げ、指定された光の変化は維持。
- 現在のエージェントが持つ画像生成・編集機能を既定で使用し、別 API の設定は不要。
- image edit 機能がない場合、または編集結果が目標未達の場合は、完全で簡潔な image edit プロンプトを直接出力。
- Pillow、NumPy、OpenCV、ImageMagick、仮設フィルタースクリプトで納品画像を作成しない。

![演示图片](/assets/skill-demo1.jpg "skill-demo")
![演示图片](/assets/skill-demo2.jpg "skill-demo")
![演示图片](/assets/skill-demo3.jpg "skill-demo")
![演示图片](/assets/skill-demo4.jpg "skill-demo")

## 基本方式

Skill は最初に内部でディレクター式の判断を行います。

```text
Scope 作用範囲 → Key キーライト → Exposure 露出意図 → Fill フィル → Shadow 影 → Skin scale 肌スケール → Skin finish 肌仕上げ → Background 背景 → Atmosphere 雰囲気
```

画像モデルへ渡すプロンプトは、英語 45〜95 語の 4 行に圧縮します。

```text
EDIT: Choose texture-only or relight-and-skin; retain source identity, geometry, expression, pose, focal plane, depth of field, camera view, and composition.
LIGHT: One key with explicit direction, exposure consequence, shadow transition, background response, color, and at most one source-consistent atmosphere.
SKIN: One scale-aware S behavior plus one source-consistent P finish, with continuous tone and bounded highlights.
AVOID: Identity drift, whole-face gloss, repeated texture, or structural scene redraw.
```

同一性監査、物体一覧、重複するネガティブ語、複数の撮影スタイルを一つのプロンプトに詰め込みません。制約同士が相殺されたり、元画像がそのまま複製されたりするのを防ぐためです。

肌だけを直す場合、V2 は `L0 + T0 + A0` を強制し、元のハイライト位置、露出、ホワイトバランス、焦点、被写界深度を維持します。再照明では `source-matched`、`balanced`、`highlight-priority`、`shadow-priority`、`low-key`、`silhouette`、`high-key` から露出意図を選択します。指定がなければ清潔な元画像一致または均衡露出を使い、劇的な暗さは明示された場合だけ適用します。

`A6` は強制上書きです。選択すると必ずシルエット露出へ切り替え、有効な主光を人物の後方へ移し、すべてのフィルとキャッチライトをなくして人物内部全体を黒にします。L と T は逆光と背景だけを制御し、S と P は無効になります。

## レシピ

一度に選ぶのは次の組み合わせだけです。

```text
L ライティングを 1 つ + S 肌スケールを 1 つ + P 肌仕上げを 1 つ + T 色温度を 1 つ + A 雰囲気を 0 または 1 つ
```

### ライティング L

| コード | 用途 |
| --- | --- |
| `L0` | 元画像に合わせ、平板な光、根拠のない黒つぶれ、異常なハイライト、硬い遷移だけを修正 |
| `L1` | 自然な逆光。既定はハイライト優先で、明示された場合だけ顔にフィルを追加 |
| `L2` | 柔らかな自然窓光 |
| `L3` | 大型の商業用ソフトライト |
| `L4` | 屋外のスカイライト |
| `L5` | 室内の実景照明と混合光 |
| `L6` | 単一点の硬い光、または直射日光 |
| `L7` | ローキーの斜めに走る細い光帯 |
| `L8` | クラシックなエディトリアル用レンブラント光 |
| `L9` | 映画的ローキーの暖色キー／寒色環境光 |
| `L10` | ゴールデンアワーの夕日による側面逆光 |
| `L11` | サイバーパンクのシアン／マゼンタ 2 色ネオン |
| `L12` | 清潔で均一な商業用ソフトライト |

### 肌スケール S

| コード | 用途 |
| --- | --- |
| `S0` | 顔が小さい、または遠景。清潔な肌色と自然な反射のみを回復 |
| `S1` | 中景の既定。低コントラストの微細質感と元の唇・目元のディテール |
| `S2` | 高解像度のクローズアップ。部位ごとの毛穴、産毛、既存ディテール |

### 肌仕上げ P

| コード | 用途 |
| --- | --- |
| `P0` | 元画像の拡散反射と鏡面反射を正確に維持。texture-only の既定値 |
| `P1` | 自然なサテンマット。キーライト側だけに限定的なハイライト |
| `P2` | 柔らかな昼光。明るい中間調と幅広いハイライトのロールオフ |
| `P3` | エディトリアルなサテン。T ゾーンのハイライトを制御 |
| `P4` | 直射フラッシュ。小さく分離したハイライトで全顔を油光にしない |
| `P5` | 清潔なビューティー仕上げ。陶器のような均一さは作らない |
| `P6` | 環境光。元の焦点減衰を維持し、粒子や新しい欠点を追加しない |

### 色温度 T

| コード | 用途 |
| --- | --- |
| `T0` | 元画像のホワイトバランスを保持 |
| `T1` | ニュートラルな自然光 |
| `T2` | 健康的で中立な肌色領域を残すゴールデン暖色光 |
| `T3` | 暖色キーライトと寒色の背景環境光 |
| `T4` | シアン／マゼンタのネオン関係 |

### 雰囲気 A

| コード | 用途 |
| --- | --- |
| `A0` | 雰囲気効果を追加しない |
| `A1` | 柔らかな窓影 |
| `A2` | まばらで自然な木漏れ日の影 |
| `A3` | ピントが外れた背景だけに置く柔らかなボケ |
| `A4` | 夕日の方向と一致する穏やかなレンズフレア |
| `A5` | ごく微かなボリュームライトと少量の浮遊塵 |
| `A6` | 人物全体を清潔な黒い逆光シルエットに固定し、内部の顔、肌、髪、衣服のディテールをすべて非表示にする |

詳しいプロンプト句は[光・肌・色温度・雰囲気レシピ](references/lighting-skin-color-temperature-recipes.md)を参照してください。

## エージェント別の画像機能

| エージェント | 既定の方式 |
| --- | --- |
| Codex | `$imagegen` の規則を読み、`ALL_TOOLS` から実在するツールを検出。`tools.image_gen__imagegen` を優先し、元画像は `referenced_image_paths` で渡す |
| Claude Code | 現在の環境に組み込み済み、またはインストール済みの画像生成・編集機能を使用 |
| OpenClaw | 現在の Agent で有効な imagegen Skill またはネイティブ画像アクションを使用 |
| その他 | ツールレジストリに明示された同等の image edit 機能を使用 |

Codex では `tools.image_gen` や `input_image` を推測しません。ツール検出によって互換画像機能が存在しないと確認した場合にのみ、プロンプト引き継ぎへ移行します。実際の画像ツールが失敗した場合、結果がほぼ元画像のままの場合、別人化した場合、肌が汚れた場合にも、コピー可能な短いプロンプトを返します。

## 動作要件

- ディレクトリ型 `SKILL.md` に対応するエージェント。
- 現在のエージェントで利用できる画像生成または画像編集機能。
- Python 3.9 以降。アスペクト比、マスク、領域の読み取り専用チェックにのみ使用。
- Pillow 9.1 以降。読み取り専用解析にのみ使用し、完成画像の作成には使用しない。

読み取り専用スクリプトの依存関係をインストールします。

```bash
python3 -m pip install -r ./xxg-portrait-rebuild-light/requirements.txt
```

## Codex へのインストール

個人用 Skill：

```bash
mkdir -p ~/.codex/skills
cp -R ./xxg-portrait-rebuild-light ~/.codex/skills/
```

共通 Agent Skills ディレクトリ：

```bash
mkdir -p ~/.agents/skills
cp -R ./xxg-portrait-rebuild-light ~/.agents/skills/
```

プロジェクト単位では、プロジェクトルートの `.agents/skills/` に配置します。`$xxg-portrait-rebuild-light` で明示的に呼び出します。

## Claude Code へのインストール

個人用：

```bash
mkdir -p ~/.claude/skills
cp -R ./xxg-portrait-rebuild-light ~/.claude/skills/
```

プロジェクト用：

```bash
mkdir -p .claude/skills
cp -R ./xxg-portrait-rebuild-light .claude/skills/
```

`/xxg-portrait-rebuild-light` で呼び出します。

## OpenClaw へのインストール

ローカルインストール：

```bash
openclaw skills install ./xxg-portrait-rebuild-light \
  --as xxg-portrait-rebuild-light
```

共有インストール：

```bash
openclaw skills install ./xxg-portrait-rebuild-light \
  --as xxg-portrait-rebuild-light \
  --global
```

現在の Agent ワークスペースの `skills/`、または共有ディレクトリ `~/.openclaw/skills/` に全体をコピーすることもできます。

## その他のエージェントへのインストール

`xxg-portrait-rebuild-light/` ディレクトリ全体を、そのツールの個人用またはプロジェクト用 Skill ルートへコピーします。`SKILL.md`、`requirements.txt`、`references/`、`scripts/`、`agents/` の相対構造を維持し、Skill 一覧を再読み込みしてください。

## 使用例

### クラシックなファッション誌風

```text
$xxg-portrait-rebuild-light でこのポートレートを L8 + S2 + P3 + T1 + A0 として編集する。
前方斜め上の大型ソフトライトで控えめなレンブラント光を作り、弱いフィルで眼窩を残す。片側の頬は深く柔らかな影にし、光源と一致するキャッチライトを一つだけ入れる。肌は清潔で健康的な低コントラストの写真的微細質感にする。
```

### 映画的なローキーの寒暖

```text
$xxg-portrait-rebuild-light でこのポートレートを L9 + S1 + P3 + T3 + A5 として編集する。
暖色のサイドキーで選択した面を照らし、ローキー露出では正面フィルを使わない。寒色は背景とリムだけに残し、光源方向に沿うごく薄いヘイズを加える。照明された肌は連続して清潔に保ち、立体感は光だけで作る。
```

### ゴールデンアワーの逆光

```text
$xxg-portrait-rebuild-light でこのポートレートを L10 + S1 + P2 + T2 + A4 として編集する。
側面後方からの暖かな夕日で髪と肩を縁取る。夕日のハイライト基準で露出し、正面フィルは使わない。顔の非照明側を自然な部分シルエットまで落とし、照明された輪郭には軽いブルームを許容する。背景にも同方向の斜めの暖光と長い影を生じさせる。
```

### サイバーパンク・ネオン

```text
$xxg-portrait-rebuild-light でこの夜景ポートレートを L11 + S1 + P6 + T4 + A3 として編集する。
シアンのリムライトとマゼンタのキーライトの方向を明確に分け、顔の中央には自然な肌色領域を残す。ボケは背景のピント外領域だけに置き、目や肌には重ねない。
```

### 人物全体の黒い逆光シルエット

```text
$xxg-portrait-rebuild-light でこのポートレートを L10 + S1 + P0 + T2 + A6 として編集する。
有効な主光を人物の後方に置き、明るい背景を基準に露出する。正面・側面のフィル、キャッチライト、人物内部の照明をすべてなくし、顔、肌、髪、衣服、身体内部を連続した清潔な黒いシルエットにする。元の外輪郭、頭身比、姿勢、カメラ視点、構図は維持する。
```

### 柔らかな窓光と窓影

```text
$xxg-portrait-rebuild-light でこの室内ポートレートを L2 + S1 + P2 + T1 + A1 として編集する。
左前方上部からの柔らかな窓光で、左から右へ広く緩やかな減衰を作る。弱い室内フィルで影側を残し、低コントラストの窓影を人物から隣接する壁へ連続させる。貼り付けたように見せない。
```

### 木漏れ日の影を使うポートレート

```text
$xxg-portrait-rebuild-light でこの屋外ポートレートを L4 + S1 + P2 + T1 + A2 として編集する。
広いスカイライトで人物を照らす。まばらな木漏れ日の影を顔と衣服の曲面に沿って柔らかく途切れさせ、物理的に妥当なら目や頬の一部を横切らせる。背景にも同じ方向の反応を出し、影の色と縁の遷移をスカイライトと表面曲率に一致させる。
```

## 出力基準

- 目標とするキーライト、明暗関係、または雰囲気効果が通常の表示サイズで直ちに判別できる。
- 入力写真と同じ人物を維持し、顔を美形化したり人工的に左右対称化したりしない。
- 人物、衣服、背景が同じ光源系に従う。
- 影の深さ、ハイライトのロールオフ、シルエットの強さは選択した露出意図に従い、すべてを見せるために逆光やローキーを平板化しない。
- 元の肌色を維持し、肌は健康的で清潔かつ連続する。ハイライトは光源に限定され、部位別の微細質感はスケール、焦点、光が解像する場所だけに現れる。
- 粒子、色ノイズ、汚れた灰色の影、局所的な過剰シャープ、強調したしわでリアリティを偽装しない。
- 窓影、木漏れ日、ボケ、夕日のフレア、光線には妥当な光源と落下位置がある。
- `A6` では人物内部全体を清潔な黒にし、顔、肌、髪、衣服、キャッチライトのディテールを残さない。同一性は外輪郭、比率、姿勢、フレーミングの維持で判定する。
- 元の構図、方向、アスペクト比、画面内の人物比率を維持する。画像モデルの最大解像度に合わせた等比縮小は許容し、元画像と同一のピクセル寸法は要求しない。

## 関連ファイル

- [Skill の主要ルール](SKILL.md)
- [簡潔プロンプトコンパイラ](references/prompt-recipes.md)
- [光・肌・色温度・雰囲気レシピ](references/lighting-skin-color-temperature-recipes.md)
- [バックエンド機能の説明](references/backend-and-clean-realism.md)
- [Python 依存関係](requirements.txt)
- [コントリビューションガイド](CONTRIBUTING.md)
- [変更履歴](CHANGELOG.md)

## ライセンス

本プロジェクトは [MIT License](LICENSE) の下で提供されます。
