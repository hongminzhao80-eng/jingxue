---
name: short-video-viral-studio
description: End-to-end short-video viral formula analysis, user-selfie asset matching, script and shot planning, gated AI clip generation, and final edit delivery with full provenance.
---

# Short Video Viral Studio

在 Codex 项目中执行“参考短视频/文案 → 爆款公式 → 用户自拍素材匹配 → 新脚本与 AI 分镜 → AI 片段 → 并线剪辑 → 审计成片”的生产流程。

## 适用场景

- 输入短视频平台链接、已授权的视频文件、字幕、转录文本或用户提供的文案。
- 输入必选的用户自拍视频/图片素材。
- 需要独立执行某一阶段，也需要执行全链路。
- 需要每一步输出可直接交给下一步的结构化产物。

## 硬性规则

1. **用户自拍素材是必选输入。** 没有素材时立即返回 `needs_input`，不得继续做素材匹配、脚本定稿、视频生成或成片合成。
2. **复用公式，不复制表达。** 只提取钩子、节奏、情绪递进、镜头功能和转化结构；不得照搬原文案、人物、品牌、口号、受保护画面或可识别表达，除非用户拥有相应权利。
3. **不得伪造成功。** 没有真实文件、元数据和状态记录，不得声称已下载、分析、生成、配音或渲染完成。
4. **不得绕过平台访问控制。** 仅处理用户已提供或有权访问的内容；链接无法访问时，保存失败记录并要求上传文件、字幕、文案或截图。
5. **不得改变用户身份。** 不得改变自拍素材中用户的身份、脸型、年龄呈现和关键外貌特征，不得用陌生人物替代用户。
6. **付费 API 必须显式确认。** 未明确确认前，AI 生成阶段只允许 `validate`、`estimate`、`dry-run`，禁止提交付费任务。
7. **全部结果可追溯。** 每个阶段输出必须记录 `source_ids`、`asset_ids`、`formula_ids`、`constraint_ids`、`created_at`、`generator`。
8. **状态必须明确。** 只能使用 `completed`、`partial`、`blocked`、`needs_input`、`failed`。

## 开始前确认

确认或记录：

- `source`：视频链接、文件、字幕、转录文本或原始文案
- `source_platform`：抖音、快手、TikTok 等
- `user_assets_dir`：用户自拍素材目录
- `target_platform`
- `aspect_ratio`：如 `9:16`
- `duration_seconds`
- `paid_api_confirmed`
- `video_provider` / `video_model`
- 是否需要旁白、字幕、BGM、音效
- `cta_goal`

缺少 `source`、`user_assets_dir`、目标画幅或目标时长时，停止并返回 `needs_input`。

## 推荐项目结构

```text
project/
├── manifest.json
├── source/
│   ├── source.json
│   ├── original-url.txt
│   ├── original-copy.txt
│   └── transcript.json
├── user-assets/
│   ├── asset-manifest.json
│   └── files/
├── analysis/
│   ├── viral-report.json
│   ├── hook-map.json
│   ├── pacing-map.json
│   ├── emotion-map.json
│   ├── conversion-map.json
│   └── formula.json
├── matching/asset-shot-mapping.json
├── scripts/
│   ├── script.json
│   └── voiceover.txt
├── shots/shot-*.json
├── generations/
│   ├── requests.json
│   ├── results.json
│   └── clips/
├── edit/
│   ├── timeline.json
│   ├── subtitles.srt
│   └── ffmpeg-command.txt
└── output/
    ├── final.mp4
    ├── final-audit.json
    ├── source-trace.json
    └── production-report.md
```

## 阶段 1：爆款解析

### 输入处理

1. 保存原始链接、原始文案或视频文件，不覆盖原始输入。
2. 记录平台、获取时间、获取方式、文件 hash 和授权/访问状态。
3. 对可访问视频提取字幕、关键帧、镜头边界和音频信息。
4. 无法读取链接时返回 `blocked` 或 `needs_input`，不得根据标题猜测视频内容。

### 必须分析

- 前 3 秒钩子及类型：结果前置、冲突、反常识、痛点、悬念等；
- 亮点、爆点和信息密度；
- 首次切镜时间、平均镜头时长、切换频率；
- 口播节奏、视觉节奏和情绪曲线；
- 情绪触发点：好奇、焦虑、认同、惊喜、信任、稀缺等；
- 问题 → 放大 → 解决 → 证明 → CTA 的转化结构；
- 可迁移规则与不得复制的具体表达。

### 输出

```text
source/source.json
source/transcript.json
analysis/viral-report.json
analysis/hook-map.json
analysis/pacing-map.json
analysis/emotion-map.json
analysis/conversion-map.json
analysis/formula.json
```

`formula.json` 必须抽象成可复用模板，例如：

```text
目标受众 → 3 秒钩子 → 痛点/冲突 → 情绪放大 → 解决方案 → 证据/结果 → CTA
```

## 阶段 2：用户自拍素材分析与匹配

逐个记录素材的路径、hash、类型、时长、分辨率、画幅、人物数量、露脸状态、动作、表情、景别、角度、光线、清晰度、可用区间、口播适配度和隐私/版权限制。

输出：

```text
user-assets/asset-manifest.json
matching/asset-shot-mapping.json
```

每个映射必须说明：

- 对应哪个公式阶段和镜头；
- 文件及源时间区间；
- 匹配理由；
- 裁切、缩放、变速、调色等处理；
- 用户素材约束；
- 缺失镜头的补拍或 AI 补充方案。

最终时间线必须真实使用至少一个用户自拍素材；优先将自拍素材放在开场信任建立、关键观点或结尾 CTA。

## 阶段 3：AI 总策划、脚本和分镜

保留原公式的钩子机制、节奏比例、情绪递进和转化结构，但改写主题、场景、人物表达、文案、产品和证据。

输出：

```text
scripts/script.json
scripts/voiceover.txt
shots/shot-*.json
```

每个镜头至少包含：

```json
{
  "shot_id": "shot-001",
  "duration": 4,
  "aspect_ratio": "9:16",
  "formula_stage": "solution",
  "purpose": "展示解决方案",
  "visual_prompt": "主体、动作、场景、镜头和结果的完整描述",
  "camera": "medium close-up",
  "lens": "35mm",
  "movement": "slow push-in",
  "composition": "subject centered",
  "lighting": "soft key light",
  "continuity": "保持人物、服装和道具连续",
  "reference_assets": ["selfie-001"],
  "negative_constraints": ["不得改变用户身份", "不得生成错误文字"],
  "transition_in": "hard_cut",
  "transition_out": "match_cut",
  "source_formula_id": "formula-001"
}
```

提示词必须自包含，不得依赖未写入文件的上下文。

## 阶段 4：AI 视频片段生成

生成前检查：用户自拍素材存在、镜头绑定公式阶段、提示词完整、约束通过、模型和画幅已配置、付费确认有效。

未确认付费时只做：

```text
validate / estimate / dry-run
```

输出：

```text
generations/requests.json
generations/results.json
generations/clips/
```

每个结果记录：`generation_id`、`shot_id`、`provider`、`model`、`status`、请求文件、参考素材、输出路径、时长、分辨率、音频是否存在、时间戳、错误信息和重试次数。失败必须保留错误，不得伪造完成状态。

## 阶段 5：并线剪辑、合成与审计

1. 建立视频、旁白、字幕、BGM 和音效轨道。
2. 先放置用户自拍主素材，再按公式节奏插入 AI 片段。
3. 根据口播时间对齐画面，执行裁切、缩放、调色和转场。
4. 生成字幕和音频混音，保留 ffmpeg 命令或等价编辑记录。
5. 检查黑帧、冻结帧、时长、音视频流、字幕越界、音画冲突、人物身份一致性、CTA 和来源溯源。

输出：

```text
edit/timeline.json
edit/subtitles.srt
edit/ffmpeg-command.txt
output/final.mp4
output/final-audit.json
output/source-trace.json
output/production-report.md
```

`source-trace.json` 必须逐段记录时间线来源：用户素材路径和源区间，或 AI 片段的 `shot_id`、`generation_id`、提示词文件、模型和约束检查结果。

## 阶段状态

每个阶段返回：

```json
{
  "status": "completed",
  "stage": "viral_analysis",
  "input_files": [],
  "output_files": [],
  "next_stage": "asset_matching",
  "blocking_reasons": [],
  "warnings": [],
  "source_ids": [],
  "asset_ids": [],
  "formula_ids": [],
  "constraint_ids": [],
  "created_at": "",
  "generator": ""
}
```

只有当原始来源、爆款公式、自拍素材分析、至少一个自拍素材时间线绑定、脚本、分镜、生成状态、编辑时间线、审计和溯源文件齐全，且 `output/final.mp4` 存在时，才能返回 `completed`；否则返回 `partial`、`blocked` 或 `needs_input`。

## 调用示例

```text
使用 $short-video-viral-studio 执行全链路。
参考来源：<视频链接或文案>
用户自拍素材：./project/user-assets
目标平台：抖音
画幅：9:16
时长：25 秒
付费 API：否
模式：hybrid
```

也支持单阶段调用：

```text
解析参考来源并输出爆款公式
分析并匹配用户自拍素材
根据 formula.json 生成脚本和分镜
执行 dry-run 并记录 AI 片段请求
根据 timeline.json 合成并审计成片
```
