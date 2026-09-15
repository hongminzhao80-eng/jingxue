# jingxue

这是一个供 Codex 项目调用的 **Skill**，不是独立智能体。

Skill 名称：`short-video-viral-studio`

能力范围：

- 解析短视频链接或文案中的爆款公式
- 强制要求并分析用户自拍素材
- 将自拍素材与爆款结构做匹配映射
- 生成新脚本与 AI 分镜提示词
- 在得到明确授权后再进入付费 API 生成阶段
- 将 AI 片段与用户自拍素材并线剪辑
- 输出最终审计结果，以及来源/约束溯源信息

主要文件：

- `.codex/skills/short-video-viral-studio/SKILL.md`
- `.codex/skills/short-video-viral-studio/agents/openai.yaml`
- `.codex/skills/short-video-viral-studio/references/output-schema.md`
