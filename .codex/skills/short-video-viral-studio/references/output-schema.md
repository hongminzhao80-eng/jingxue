# short-video-viral-studio 输出结构

所有阶段都应输出结构化结果，便于独立调用与全链路串联。

## 1. `viral_analysis`

```json
{
  "source_type": "video_url",
  "source_value": "https://example.com/video",
  "highlights": ["亮点 1"],
  "hooks": ["前 3 秒结果前置"],
  "pacing": ["每 2-3 秒一次视觉变化"],
  "emotion_curve": ["好奇", "痛点放大", "解决方案", "证明", "行动号召"],
  "viral_formula": {
    "structure": ["hook", "problem", "solution", "proof", "cta"],
    "reusable_rules": ["必须复用结构与节奏，而不是照抄内容"]
  },
  "source_trace": {
    "source_url": "https://example.com/video"
  },
  "constraint_trace": {
    "must_reuse_formula": true
  }
}
```

## 2. `asset_mapping`

```json
{
  "selfie_assets_required": true,
  "assets": [
    {
      "asset_id": "selfie-001",
      "type": "video",
      "usable_ranges": [{"start": 0, "end": 3.2}],
      "style_tags": ["口播", "正面看镜头"]
    }
  ],
  "mapping": [
    {
      "target_stage": "hook",
      "asset_id": "selfie-001",
      "reason": ["人物正面出镜，适合结果前置"],
      "fallback": "缺少结果展示时才允许补充 AI 插片"
    }
  ],
  "source_trace": {
    "derived_from": ["viral_analysis"]
  },
  "constraint_trace": {
    "selfie_asset_must_appear_in_final_cut": true
  }
}
```

## 3. `script_and_storyboard`

```json
{
  "script": [
    {
      "stage": "hook",
      "voiceover": "先给你看结果",
      "onscreen_text": "3 秒抓住注意力"
    }
  ],
  "storyboard": [
    {
      "shot_id": "shot-001",
      "stage": "hook",
      "visual_source": "selfie_asset",
      "asset_id": "selfie-001",
      "ai_prompt": "补充竖屏结果展示镜头，节奏紧凑"
    }
  ],
  "source_trace": {
    "derived_from": ["viral_analysis", "asset_mapping"]
  },
  "constraint_trace": {
    "matched_to_selfie_assets": true
  }
}
```

## 4. `generation_plan_or_results`

```json
{
  "paid_api_approved": false,
  "status": "blocked_until_confirmed",
  "planned_generations": [
    {
      "shot_id": "shot-002",
      "prompt": "竖屏产品特写，适合作为证明镜头"
    }
  ],
  "source_trace": {
    "derived_from": ["script_and_storyboard"]
  },
  "constraint_trace": {
    "paid_api_gating_enforced": true
  }
}
```

如已获授权，也可返回 `generated_clips` 结果，但必须保留镜头级来源。

## 5. `parallel_edit_timeline`

```json
{
  "timeline": [
    {
      "start": 0,
      "end": 2.5,
      "track": "selfie",
      "asset_id": "selfie-001",
      "purpose": "hook"
    },
    {
      "start": 2.5,
      "end": 4.0,
      "track": "ai_insert",
      "shot_id": "shot-002",
      "purpose": "proof"
    }
  ],
  "source_trace": {
    "derived_from": ["asset_mapping", "script_and_storyboard", "generation_plan_or_results"]
  },
  "constraint_trace": {
    "parallel_editing_used": true
  }
}
```

## 6. `final_audit`

```json
{
  "formula_reused": true,
  "selfie_assets_present": true,
  "paid_api_gating_respected": true,
  "lineage_complete": true,
  "constraint_violations": [],
  "ready_for_delivery": true,
  "source_trace": {
    "derived_from": [
      "viral_analysis",
      "asset_mapping",
      "script_and_storyboard",
      "generation_plan_or_results",
      "parallel_edit_timeline"
    ]
  },
  "constraint_trace": {
    "final_audit_completed": true
  }
}
```
