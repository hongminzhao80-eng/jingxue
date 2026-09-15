# jingxue

一个可在 Codex 项目中直接调用的「短视频爆款公式解析与 AI 视频生成流水线 Skill」。

## 能力

- 阶段 1：解析短视频链接或文案，输出爆款解析报告
- 阶段 2：分析并匹配用户自拍素材，输出结构化映射表
- 阶段 3：复用原视频爆款公式，生成新视频脚本与 AI 分镜提示词
- 阶段 4：输出可直接驱动生成模型的 AI 视频片段 prompt 包
- 阶段 5：将 AI 片段与用户自拍素材并线，输出最终成片时间线

## 运行方式

```bash
python /home/runner/work/jingxue/jingxue/jingxue_skill.py --stage pipeline --input '{
  "reference_text": "先给你看结果，再告诉你为什么普通人拍不出这种反差感。",
  "goal": "用用户自拍素材制作带转化力的短视频",
  "user_assets": [
    {"id": "selfie-1", "type": "video", "duration_seconds": 6, "style": "口播"},
    {"id": "selfie-2", "type": "image", "duration_seconds": 3, "style": "前后对比"}
  ]
}'
```

支持独立调用的阶段：

- `analyze`
- `match`
- `script`
- `generate`
- `compose`
- `pipeline`

## 输出

Skill 输出固定包含以下结构化结果：

1. `爆款解析报告`
2. `素材匹配方案`
3. `新视频脚本 + 分镜提示词`
4. `AI 视频片段`
5. `最终成片`
