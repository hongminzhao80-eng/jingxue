# Short Video Viral Studio 输出规范

## 全局追溯字段

所有阶段输出必须包含：

```json
{
  "source_ids": [],
  "asset_ids": [],
  "formula_ids": [],
  "constraint_ids": [],
  "created_at": "",
  "generator": ""
}
```

## 状态

允许值：

```text
completed | partial | blocked | needs_input | failed
```

## source.json

```json
{
  "source_id": "source-001",
  "source_type": "video_url|video_file|copy|transcript",
  "source_url": "",
  "platform": "",
  "raw_copy_path": "",
  "local_file_path": "",
  "content_hash": "",
  "captured_at": "",
  "access_status": "provided|retrieved|blocked|unknown",
  "rights_status": "user_provided|authorized|unknown"
}
```

## formula.json

```json
{
  "formula_id": "formula-001",
  "source_ids": ["source-001"],
  "hook": {
    "type": "result_first|conflict|contrarian|pain|curiosity|other",
    "duration_seconds": 3,
    "mechanism": "",
    "visual_pattern": "",
    "copy_pattern": ""
  },
  "beats": [
    {
      "stage": "hook|problem|agitation|solution|proof|cta",
      "duration_ratio": 0.2,
      "purpose": "",
      "emotion": "",
      "visual_change": "",
      "reusable_rule": ""
    }
  ],
  "pacing": {
    "average_shot_duration": 0,
    "first_cut_time": 0,
    "cut_frequency": "",
    "energy_curve": []
  },
  "conversion": {
    "problem": "",
    "promise": "",
    "proof": "",
    "cta": ""
  },
  "adaptation_rules": [],
  "do_not_copy": []
}
```

## asset-shot-mapping.json

```json
{
  "mapping_id": "mapping-001",
  "formula_id": "formula-001",
  "formula_stage": "hook",
  "asset_id": "selfie-001",
  "source_in": 0.8,
  "source_out": 3.6,
  "timeline_duration": 2.8,
  "match_reason": [],
  "edits": [],
  "constraints": [],
  "fallback": "retake|generate_ai_insert|none"
}
```

## shot.json

```json
{
  "shot_id": "shot-001",
  "formula_id": "formula-001",
  "formula_stage": "solution",
  "duration": 4,
  "aspect_ratio": "9:16",
  "purpose": "",
  "visual_prompt": "",
  "camera": "",
  "lens": "",
  "movement": "",
  "composition": "",
  "lighting": "",
  "continuity": "",
  "reference_assets": [],
  "negative_constraints": [],
  "transition_in": "",
  "transition_out": ""
}
```

## generation-result.json

```json
{
  "generation_id": "gen-001",
  "shot_id": "shot-001",
  "provider": "",
  "model": "",
  "status": "pending|submitted|completed|failed",
  "request_file": "shots/shot-001.json",
  "output_path": "",
  "duration": 0,
  "width": 0,
  "height": 0,
  "audio_present": false,
  "retry_count": 0,
  "created_at": "",
  "error": null
}
```

## timeline.json

```json
{
  "timeline": [
    {
      "track": "video|voice|subtitle|music|sfx",
      "timeline_in": 0,
      "timeline_out": 3,
      "origin_type": "user|generated|source_reference",
      "origin_path": "",
      "asset_id": "",
      "shot_id": "",
      "generation_id": "",
      "source_in": 0,
      "source_out": 3,
      "operations": [],
      "constraints_checked": [],
      "validation": "passed|warning|failed"
    }
  ]
}
```

## final-audit.json

```json
{
  "status": "passed|warning|failed",
  "checks": {
    "selfie_asset_present": true,
    "hook_in_first_three_seconds": true,
    "duration_valid": true,
    "no_black_frames": true,
    "no_long_freeze": true,
    "audio_video_streams_valid": true,
    "subtitles_in_bounds": true,
    "identity_constraints_passed": true,
    "provenance_complete": true
  },
  "warnings": [],
  "errors": []
}
```
