# jingxue

用 Codex 开发的项目中使用短视频爆款解析与 AI 视频生成 Skill：解析来自短视频平台的视频链接或文案，提取爆款公式，匹配用户自拍素材，生成新脚本、AI 分镜和 AI 视频片段，最后与自拍素材并线剪辑合成。

## 内置 Codex Skill

```text
.codex/skills/short-video-viral-studio/
```

在支持 Codex project skills 的环境中调用：

```text
使用 $short-video-viral-studio 执行全链路。
```

Skill 强制保留原始来源、用户素材约束、阶段状态和最终视频溯源；未确认付费 API 时只允许执行 `validate`、`estimate` 或 `dry-run`。
