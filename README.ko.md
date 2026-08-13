<div align="center">
  <img src="assets/skill-icon.png" width="120" alt="xxg-portrait-rebuild-light skill-logo">
</div>
<h1 align="center">XXG Portrait Rebuild Light</h1>
<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-red?style=flat-square" alt="MIT License"></a>
  <a href=""><img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square" alt="Python"></a>
  <a href=""><img src="https://img.shields.io/badge/CodeX-Skill-green.svg?style=flat-square" alt="codex"></a>
  <a href=""><img src="https://img.shields.io/badge/Claude-Skill-yellow.svg?style=flat-square" alt="Claude"></a>
  <a href=""><img   src="https://img.shields.io/badge/Open-Claw-8A2BE2.svg?style=flat-square" alt="OpenClaw"></a>
</p>

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | 한국어

`xxg-portrait-rebuild-light`는 기존 인물 사진을 위한 image edit Skill입니다. 디렉터 관점의 조명 설계로 키 라이트, 필 라이트, 그림자, 배경 분위기를 재구성하면서 깨끗하고 건강한 저대비 사진 피부 미세 질감을 복원합니다.

인물을 다시 그리는 것이 아니라 조명을 바꾸는 데 중점을 둡니다. 동일 인물, 기존 얼굴 구조와 비율, 자연스러운 미세 비대칭, 표정, 자세, 카메라 시점, 구도를 유지하며 플라스틱 피부, 거친 입자 피부, 지저분한 색 얼룩, 주름을 과장해 만든 가짜 입체감을 방지합니다.

![演示图片](/assets/skill-demo1.jpg "skill-demo")
![演示图片](/assets/skill-demo2.jpg "skill-demo")
![演示图片](/assets/skill-demo3.jpg "skill-demo")
![演示图片](/assets/skill-demo4.jpg "skill-demo")

## 주요 기능

- 플라스틱처럼 매끈한 피부, 과도한 보정, 밀랍 인형 같은 질감을 수정합니다.
- 원래의 입술 결, 눈가 단계, 절제된 피지 반사, 얼굴 표시 크기에 맞는 미세 질감을 유지합니다.
- 약한 역광, 분리되어 보이는 실내 창문광, 평면적인 조명, 의도하지 않은 암부 뭉개짐, 출처 없는 하이라이트를 수정합니다.
- 부드러운 창문광, 상업용 소프트 라이트, 렘브란트 조명, 시네마틱 로우키, 골든아워, 이중 컬러 네온, 사선 하드 라이트를 지원합니다.
- 물리적으로 일관된 창문 그림자, 나뭇잎 그림자, 배경 보케, 석양 플레어, 은은한 볼류메트릭 라이트 또는 피사체 전체의 검은 역광 실루엣 중 최대 하나를 추가합니다.
- 피사체와 배경을 계층적으로 제어합니다. 먼저 키 라이트와 노출 의도를 정하고 필, 그림자, 배경 주변광, 색온도를 정의합니다.
- 인물 정체성, 얼굴 요소의 크기와 위치, 표정, 자세, 의상, 배경 구조, 원본 프레이밍을 유지합니다.
- 얼굴이 작으면 피부 미세 질감 목표만 자동으로 낮추고 요청된 조명 변화는 유지합니다.
- 별도 API 없이 현재 에이전트가 보유한 이미지 생성·편집 기능을 기본으로 사용합니다.
- 현재 에이전트에 image edit 기능이 없거나 결과가 목표에 미달하면 완전하고 간결한 image edit 프롬프트를 직접 출력합니다.
- Pillow, NumPy, OpenCV, ImageMagick 또는 임시 필터 스크립트로 최종 이미지를 만들지 않습니다.

## 핵심 방식

Skill은 먼저 내부에서 디렉터식 결정을 수행합니다.

```text
Key 키 라이트 → Exposure 노출 의도 → Fill 필 → Shadow 그림자 → Subject 피사체 → Background 배경 → Atmosphere 분위기
```

이미지 모델에 전달하는 프롬프트는 다음 네 줄로 압축합니다.

```text
편집: 동일 인물과 원본 구도를 유지하고 조명과 피부 표현만 재구성한다.
조명: 하나의 키 라이트 + 노출 의도 + 필/그림자 관계 + 배경 반응 + 선택적 단일 분위기 효과.
피부: 화면에 보이는 얼굴 크기에 맞는 깨끗한 저대비 사진 미세 질감.
제한: 인물 변경, 미형화, 스무딩, 입자 추가, 지저분한 색 얼룩, 배경 재작성을 하지 않는다.
```

정체성 감사, 물체 목록, 반복되는 부정어, 여러 사진 스타일을 하나의 프롬프트에 쌓지 않습니다. 제약이 서로 상쇄되거나 원본이 그대로 복제되는 현상을 줄이기 위해서입니다.

모든 내용을 선명하게 보이게 하는 것보다 광원의 물리적 효과를 우선합니다. 노출 의도는 `source-matched`, `balanced`, `highlight-priority`, `shadow-priority`, `low-key`, `silhouette`, `high-key` 중에서 선택합니다. 석양 역광에서는 얼굴의 비조명면이 자연스럽게 어두워지거나 부분 실루엣이 될 수 있습니다. 로우키와 하드 라이트에서는 검정에 가까운 그림자도 허용합니다. 원래 읽혀야 할 정보가 타당한 원인 없이 암부에서 사라질 때만 필 라이트를 사용합니다.

`A6`은 강제 덮어쓰기 항목입니다. 선택하면 항상 실루엣 노출로 전환하고 유효한 주광을 인물 뒤로 옮기며 모든 필 라이트와 캐치라이트를 제거해 인물 내부 전체를 검정으로 만듭니다. 선택한 L과 T는 역광과 배경 반응만 제어하고 S 피부 질감은 화면에 표시하지 않습니다.

## 레시피

한 번에는 다음만 선택합니다.

```text
L 조명 하나 + S 피부 하나 + T 색온도 하나 + A 분위기 0개 또는 1개
```

### 조명 L

| 코드 | 용도 |
| --- | --- |
| `L0` | 원본에 맞추고 평면광, 출처 없는 암부 뭉개짐, 비정상 하이라이트, 거친 전이만 수정 |
| `L1` | 자연스러운 역광. 기본은 하이라이트 우선이며 명시적으로 요청할 때만 얼굴 필 추가 |
| `L2` | 부드러운 자연 창문광 |
| `L3` | 대형 상업용 소프트 라이트 |
| `L4` | 야외 스카이라이트 |
| `L5` | 실내 실경 조명과 혼합광 |
| `L6` | 단일 지점 하드 라이트 또는 직사광 |
| `L7` | 로우키 사선의 좁은 광선 |
| `L8` | 클래식 에디토리얼 렘브란트 조명 |
| `L9` | 시네마틱 로우키의 따뜻한 키 라이트와 차가운 주변광 |
| `L10` | 골든아워 석양 측면 역광 |
| `L11` | 사이버펑크 시안/마젠타 이중 네온 |
| `L12` | 깨끗하고 균일한 상업용 소프트 라이트 |

### 피부 S

| 코드 | 용도 |
| --- | --- |
| `S0` | 얼굴이 작거나 원경일 때 깨끗한 피부색과 자연스러운 반사만 복원 |
| `S1` | 중경 기본값. 저대비 미세 질감과 원래의 입술·눈가 디테일 |
| `S2` | 고해상도 클로즈업. 부위별 모공, 가는 솜털, 기존 디테일 |

### 색온도 T

| 코드 | 용도 |
| --- | --- |
| `T0` | 원본 화이트 밸런스 유지 |
| `T1` | 중립적인 자연광 |
| `T2` | 건강하고 중립적인 피부 영역을 유지하는 골든 웜 라이트 |
| `T3` | 따뜻한 키 라이트와 차가운 배경 주변광 |
| `T4` | 시안/마젠타 네온 관계 |

### 분위기 A

| 코드 | 용도 |
| --- | --- |
| `A0` | 분위기 효과를 추가하지 않음 |
| `A1` | 부드러운 창문 그림자 |
| `A2` | 성긴 자연 나뭇잎 그림자 |
| `A3` | 초점이 흐린 배경에만 적용하는 부드러운 보케 |
| `A4` | 석양 방향과 일치하는 은은한 렌즈 플레어 |
| `A5` | 매우 약한 볼류메트릭 라이트와 성긴 먼지 입자 |
| `A6` | 인물 전체를 깨끗한 검은 역광 실루엣으로 강제하며 내부의 얼굴, 피부, 머리카락, 의상 디테일을 모두 숨김 |

자세한 프롬프트 문구는 [조명·피부·색온도·분위기 레시피](references/lighting-skin-color-temperature-recipes.md)를 참고하세요.

## 에이전트별 이미지 기능

| 에이전트 | 기본 방식 |
| --- | --- |
| Codex | `$imagegen` 규칙을 읽고 `ALL_TOOLS`에서 실제 도구를 찾습니다. `tools.image_gen__imagegen`을 우선 호출하고 원본 이미지는 `referenced_image_paths`로 전달합니다. |
| Claude Code | 현재 환경에 설치되어 있거나 내장된 이미지 생성·편집 기능을 사용합니다. |
| OpenClaw | 현재 Agent에 활성화된 imagegen Skill 또는 네이티브 이미지 동작을 사용합니다. |
| 기타 에이전트 | 도구 레지스트리에 명시적으로 노출된 동등한 image edit 기능을 사용합니다. |

Codex에서는 `tools.image_gen`이나 `input_image`를 추측하지 않습니다. 도구 탐색 결과 호환 이미지 기능이 없음을 확인한 경우에만 프롬프트 인계로 전환합니다. 실제 이미지 도구가 실패하거나 결과가 원본과 거의 같거나, 인물이 바뀌거나, 피부가 지저분해진 경우에도 복사 가능한 짧은 프롬프트를 반환합니다.

## 환경 요구 사항

- 디렉터리형 `SKILL.md`를 지원하는 에이전트.
- 현재 에이전트에서 사용할 수 있는 이미지 생성 또는 이미지 편집 기능.
- Python 3.9 이상. 화면비, 마스크, 영역의 읽기 전용 검사에만 사용.
- Pillow 9.1 이상. 읽기 전용 분석에만 사용하며 최종 이미지 제작에는 사용하지 않음.

읽기 전용 스크립트의 의존성을 설치합니다.

```bash
python3 -m pip install -r ./xxg-portrait-rebuild-light/requirements.txt
```

## Codex에 설치

개인 Skill:

```bash
mkdir -p ~/.codex/skills
cp -R ./xxg-portrait-rebuild-light ~/.codex/skills/
```

공용 Agent Skills 디렉터리:

```bash
mkdir -p ~/.agents/skills
cp -R ./xxg-portrait-rebuild-light ~/.agents/skills/
```

프로젝트 단위 설치는 프로젝트 루트의 `.agents/skills/`에 배치합니다. `$xxg-portrait-rebuild-light`로 명시적으로 호출합니다.

## Claude Code에 설치

개인 설치:

```bash
mkdir -p ~/.claude/skills
cp -R ./xxg-portrait-rebuild-light ~/.claude/skills/
```

프로젝트 설치:

```bash
mkdir -p .claude/skills
cp -R ./xxg-portrait-rebuild-light .claude/skills/
```

`/xxg-portrait-rebuild-light`로 호출합니다.

## OpenClaw에 설치

로컬 설치:

```bash
openclaw skills install ./xxg-portrait-rebuild-light \
  --as xxg-portrait-rebuild-light
```

공유 설치:

```bash
openclaw skills install ./xxg-portrait-rebuild-light \
  --as xxg-portrait-rebuild-light \
  --global
```

현재 Agent 작업 공간의 `skills/` 디렉터리 또는 공유 디렉터리 `~/.openclaw/skills/`에 전체 폴더를 복사해도 됩니다.

## 기타 에이전트에 설치

전체 `xxg-portrait-rebuild-light/` 디렉터리를 해당 도구의 개인 또는 프로젝트 Skill 루트로 복사합니다. `SKILL.md`, `requirements.txt`, `references/`, `scripts/`, `agents/`의 상대 구조를 유지한 뒤 Skill 목록을 다시 불러오세요.

## 사용 예시

### 클래식 패션 에디토리얼

```text
$xxg-portrait-rebuild-light로 이 인물 사진을 L8 + S2 + T1 + A0으로 편집한다.
전면 측상단의 대형 소프트 키 라이트로 절제된 렘브란트 조명을 만들고, 약한 필로 눈두덩을 보존한다. 한쪽 볼은 깊고 부드러운 그림자에 두며 광원과 일치하는 캐치라이트 하나만 만든다. 피부는 깨끗하고 건강한 저대비 사진 미세 질감으로 유지한다.
```

### 시네마틱 로우키 웜/쿨

```text
$xxg-portrait-rebuild-light로 이 인물 사진을 L9 + S1 + T3 + A5로 편집한다.
따뜻한 측면 키 라이트로 명암면을 만든다. 전면 필 없이 로우키로 노출하여 비조명면이 검정에 가까워져도 된다. 차가운 색은 배경과 림에만 남기고 극도로 미세한 볼류메트릭 먼지를 추가한다. 지저분한 회색 피부나 과장된 주름은 만들지 않는다.
```

### 골든아워 역광

```text
$xxg-portrait-rebuild-light로 이 인물 사진을 L10 + S1 + T2 + A4로 편집한다.
측후면의 따뜻한 석양광으로 머리카락과 어깨 윤곽을 만든다. 석양 하이라이트 기준으로 노출하고 전면 필은 사용하지 않는다. 얼굴의 비조명면을 자연스러운 부분 실루엣까지 낮추며 밝은 가장자리에는 약한 블룸을 허용한다. 배경에도 같은 방향의 비스듬한 온광과 긴 그림자를 만든다.
```

### 사이버펑크 네온

```text
$xxg-portrait-rebuild-light로 이 야간 인물 사진을 L11 + S1 + T4 + A3로 편집한다.
시안 림 라이트와 마젠타 키 라이트의 방향을 명확히 분리하고 얼굴 중앙에는 자연스러운 피부색 영역을 유지한다. 보케는 초점이 흐린 배경에만 두고 눈이나 피부 위에는 겹치지 않는다.
```

### 피사체 전체의 검은 역광 실루엣

```text
$xxg-portrait-rebuild-light로 이 인물 사진을 L10 + S1 + T2 + A6으로 편집한다.
유효한 주광을 인물 뒤에 배치하고 밝은 배경을 기준으로 노출한다. 모든 정면·측면 필 라이트, 캐치라이트, 인물 내부 조명을 제거하고 얼굴, 피부, 머리카락, 의상과 신체 내부 전체를 깨끗하고 연속적인 검은 실루엣으로 만든다. 원래 외곽선, 신체 비율, 자세, 카메라 시점과 구도는 유지한다.
```

### 부드러운 창문광과 창문 그림자

```text
$xxg-portrait-rebuild-light로 이 실내 인물 사진을 L2 + S1 + T1 + A1로 편집한다.
좌측 전방 상단의 부드러운 창문광으로 왼쪽에서 오른쪽으로 넓고 완만한 감광을 만든다. 약한 실내 필로 암부를 보존하고, 저대비 창문 그림자 하나를 인물과 인접 벽에 연속적으로 드리운다. 붙여 넣은 것처럼 보이지 않게 한다.
```

### 나뭇잎 그림자 인물 사진

```text
$xxg-portrait-rebuild-light로 이 야외 인물 사진을 L4 + S1 + T1 + A2로 편집한다.
넓은 스카이라이트로 인물을 비춘다. 성긴 나뭇잎 그림자가 얼굴과 의복의 곡률을 따라 부드럽게 끊기게 하고, 물리적으로 타당한 위치라면 눈과 볼 일부를 지나가게 한다. 배경에도 같은 방향의 반응을 만들며 출처 없는 지저분한 얼룩은 만들지 않는다.
```

## 출력 기준

- 목표 키 라이트, 명암 관계, 분위기 효과가 일반적인 표시 크기에서 즉시 구별됩니다.
- 입력 사진과 동일한 인물을 유지하며 얼굴을 미형화하거나 인위적으로 좌우 대칭화하지 않습니다.
- 피사체, 의상, 배경이 같은 광원 체계를 따릅니다.
- 그림자 깊이, 하이라이트 롤오프, 실루엣 강도는 선택한 노출 의도에 따르며 모든 것을 보이게 하려고 역광이나 로우키를 평면화하지 않습니다.
- 피부는 밝고 건강하며 깨끗하고 연속적입니다. 저대비 사진 미세 질감을 가지되 거칠거나 얼룩덜룩하지 않습니다.
- 입자, 색 노이즈, 지저분한 회색 그림자, 국부 과도 샤프닝, 과장된 주름으로 사실감을 흉내 내지 않습니다.
- 창문 그림자, 나뭇잎 그림자, 보케, 석양 플레어, 광선에는 타당한 광원과 투영 위치가 있습니다.
- `A6`에서는 인물 내부 전체가 깨끗한 검정이어야 하며 얼굴, 피부, 머리카락, 의상 또는 캐치라이트 디테일이 남지 않아야 합니다. 동일 인물 여부는 보존된 외곽선, 비율, 자세와 프레이밍으로 판단합니다.
- 원본 구도, 방향, 화면비, 프레임 내 피사체 비율을 유지합니다. 이미지 모델의 최대 해상도에 맞춘 비례 축소는 허용하며 원본과 동일한 픽셀 크기는 요구하지 않습니다.

## 관련 파일

- [Skill 주요 규칙](SKILL.md)
- [간결 프롬프트 컴파일러](references/prompt-recipes.md)
- [조명·피부·색온도·분위기 레시피](references/lighting-skin-color-temperature-recipes.md)
- [백엔드 기능 설명](references/backend-and-clean-realism.md)
- [Python 의존성](requirements.txt)
- [기여 가이드](CONTRIBUTING.md)
- [변경 기록](CHANGELOG.md)

## 라이선스

이 프로젝트는 [MIT License](LICENSE)로 배포됩니다.
