from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


DEFAULT_FORMULA_BEATS = [
    ("hook", "3秒钩子", "用反差问题或结果前置抓住注意力"),
    ("pain", "痛点放大", "快速建立用户代入感与紧迫感"),
    ("turn", "方法反转", "给出与常规不同的关键做法"),
    ("proof", "结果证明", "用过程、对比或证据完成信任闭环"),
    ("cta", "行动收口", "用明确指令促成关注、咨询或转化"),
]


class SkillInputError(ValueError):
    """Raised when skill input is incomplete."""


@dataclass(frozen=True)
class StageResult:
    stage: str
    data: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {"stage": self.stage, **self.data}


def _require_reference(payload: Dict[str, Any]) -> str:
    reference_text = (payload.get("reference_text") or "").strip()
    reference_url = (payload.get("reference_url") or "").strip()
    if reference_text:
        return reference_text
    if reference_url:
        return f"参考链接：{reference_url}"
    raise SkillInputError("reference_text or reference_url is required")


def _require_user_assets(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    assets = payload.get("user_assets") or []
    if not assets:
        raise SkillInputError("user_assets is required and must contain自拍素材")
    return assets


def _split_sentences(text: str) -> List[str]:
    normalized = (
        text.replace("！", "。")
        .replace("？", "。")
        .replace("!", ".")
        .replace("?", ".")
        .replace("\n", "。")
    )
    parts = [part.strip("。.,;；：: ") for part in normalized.split("。")]
    return [part for part in parts if part]


def _build_formula(reference: str) -> Dict[str, Any]:
    beats = []
    for index, (beat_id, name, reuse_rule) in enumerate(DEFAULT_FORMULA_BEATS, start=1):
        beats.append(
            {
                "index": index,
                "beat_id": beat_id,
                "name": name,
                "reuse_rule": reuse_rule,
                "rhythm_target_seconds": 4 if beat_id != "proof" else 6,
            }
        )
    return {
        "signature": "hook>pain>turn>proof>cta",
        "source_reference": reference,
        "beats": beats,
        "emotion_curve": ["好奇", "焦虑", "期待", "信任", "行动"],
    }


def analyze_viral_formula(payload: Dict[str, Any]) -> Dict[str, Any]:
    reference = _require_reference(payload)
    sentences = _split_sentences(reference)
    formula = _build_formula(reference)
    highlights = sentences[:3] or [reference]
    viral_points = [
        "开头结果前置，先给收益再解释原因",
        "中段用痛点与反转形成停留",
        "结尾加入明确行动指令提高转化",
    ]
    if len(sentences) > 1:
        viral_points.append("参考文案存在多段推进，适合按分镜节奏逐步释放信息")
    return {
        "爆款解析报告": {
            "reference_summary": reference,
            "亮点": highlights,
            "爆点": viral_points,
            "节奏结构": [beat["name"] for beat in formula["beats"]],
            "钩子设计": formula["beats"][0]["reuse_rule"],
            "情绪曲线": formula["emotion_curve"],
            "公式拆解": formula,
        }
    }


def match_user_assets(
    payload: Dict[str, Any], analysis_report: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    assets = _require_user_assets(payload)
    if analysis_report is None:
        analysis_report = analyze_viral_formula(payload)
    formula = analysis_report["爆款解析报告"]["公式拆解"]
    mapped_assets = []
    for beat, asset in zip(formula["beats"], _cycle(assets)):
        mapped_assets.append(
            {
                "beat_id": beat["beat_id"],
                "formula_step": beat["name"],
                "user_asset_id": asset["id"],
                "user_asset_type": asset.get("type", "video"),
                "recommended_usage": _usage_for_beat(beat["beat_id"]),
                "must_keep_in_final_cut": True,
            }
        )
    return {
        "素材匹配方案": {
            "formula_signature": formula["signature"],
            "用户素材_爆款结构映射表": mapped_assets,
            "素材摘要": [
                {
                    "id": asset["id"],
                    "type": asset.get("type", "video"),
                    "duration_seconds": asset.get("duration_seconds"),
                    "style": asset.get("style"),
                }
                for asset in assets
            ],
        }
    }


def generate_script(
    payload: Dict[str, Any],
    analysis_report: Optional[Dict[str, Any]] = None,
    match_report: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if analysis_report is None:
        analysis_report = analyze_viral_formula(payload)
    if match_report is None:
        match_report = match_user_assets(payload, analysis_report)
    formula = analysis_report["爆款解析报告"]["公式拆解"]
    mapping = match_report["素材匹配方案"]["用户素材_爆款结构映射表"]
    objective = payload.get("goal") or "复用爆款公式生成适配用户自拍素材的新短视频"
    script_beats = []
    prompts = []
    for beat, asset_map in zip(formula["beats"], mapping):
        narration = _narration_for_beat(beat["beat_id"], objective)
        script_beats.append(
            {
                "beat_id": beat["beat_id"],
                "formula_step": beat["name"],
                "narration": narration,
                "user_asset_id": asset_map["user_asset_id"],
                "rhythm_target_seconds": beat["rhythm_target_seconds"],
            }
        )
        prompts.append(
            {
                "beat_id": beat["beat_id"],
                "prompt": (
                    f"{beat['name']}，围绕“{objective}”生成竖屏9:16分镜，"
                    f"与用户素材 {asset_map['user_asset_id']} 并线衔接，"
                    f"突出{asset_map['recommended_usage']}，节奏 {beat['rhythm_target_seconds']} 秒。"
                ),
            }
        )
    return {
        "新视频脚本 + 分镜提示词": {
            "formula_signature": formula["signature"],
            "script_strategy": "严格复用参考爆款的结构、节奏、钩子与收口顺序，只替换为用户素材可承载的新内容",
            "新视频脚本": script_beats,
            "AI分镜头提示词": prompts,
        }
    }


def generate_ai_video_segments(
    payload: Dict[str, Any], script_report: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    if script_report is None:
        script_report = generate_script(payload)
    package = script_report["新视频脚本 + 分镜提示词"]
    clips = []
    for prompt_entry, script_entry in zip(package["AI分镜头提示词"], package["新视频脚本"]):
        clips.append(
            {
                "clip_id": f"ai-{script_entry['beat_id']}",
                "beat_id": script_entry["beat_id"],
                "generation_prompt": prompt_entry["prompt"],
                "target_duration_seconds": script_entry["rhythm_target_seconds"],
                "status": "ready_for_generation",
            }
        )
    return {
        "AI 视频片段": {
            "formula_signature": package["formula_signature"],
            "generation_mode": "prompt_package",
            "生成结果": clips,
        }
    }


def compose_final_video(
    payload: Dict[str, Any],
    match_report: Optional[Dict[str, Any]] = None,
    script_report: Optional[Dict[str, Any]] = None,
    clips_report: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if match_report is None:
        match_report = match_user_assets(payload)
    if script_report is None:
        script_report = generate_script(payload)
    if clips_report is None:
        clips_report = generate_ai_video_segments(payload, script_report)
    mapping = match_report["素材匹配方案"]["用户素材_爆款结构映射表"]
    script_beats = script_report["新视频脚本 + 分镜提示词"]["新视频脚本"]
    clips = clips_report["AI 视频片段"]["生成结果"]
    timeline = []
    for asset_map, script_entry, clip in zip(mapping, script_beats, clips):
        timeline.append(
            {
                "beat_id": script_entry["beat_id"],
                "formula_step": script_entry["formula_step"],
                "user_asset_id": asset_map["user_asset_id"],
                "ai_clip_id": clip["clip_id"],
                "edit_pattern": "parallel_cut",
                "duration_seconds": script_entry["rhythm_target_seconds"],
            }
        )
    return {
        "最终成片": {
            "formula_signature": match_report["素材匹配方案"]["formula_signature"],
            "production_line": "并线剪辑",
            "timeline": timeline,
            "用户自拍素材已融入": True,
            "render_status": "ready_for_nle_or_renderer",
        }
    }


def run_pipeline(payload: Dict[str, Any]) -> Dict[str, Any]:
    analysis = analyze_viral_formula(payload)
    match = match_user_assets(payload, analysis)
    script = generate_script(payload, analysis, match)
    clips = generate_ai_video_segments(payload, script)
    final_video = compose_final_video(payload, match, script, clips)
    return {
        **analysis,
        **match,
        **script,
        **clips,
        **final_video,
    }


def run_stage(stage: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    stage_map = {
        "analyze": lambda: analyze_viral_formula(payload),
        "match": lambda: match_user_assets(payload),
        "script": lambda: generate_script(payload),
        "generate": lambda: generate_ai_video_segments(payload),
        "compose": lambda: compose_final_video(payload),
        "pipeline": lambda: run_pipeline(payload),
    }
    if stage not in stage_map:
        raise SkillInputError(f"unsupported stage: {stage}")
    return stage_map[stage]()


def _usage_for_beat(beat_id: str) -> str:
    return {
        "hook": "最强开场表情或动作",
        "pain": "能体现困扰或反差的自拍片段",
        "turn": "展示解决动作的过渡镜头",
        "proof": "结果对比或细节特写",
        "cta": "正视镜头发出行动号召",
    }[beat_id]


def _narration_for_beat(beat_id: str, objective: str) -> str:
    return {
        "hook": f"先抛出结果，让观众立刻知道这条视频和“{objective}”有关。",
        "pain": "补充用户常见痛点，让观众继续停留。",
        "turn": "给出反常识转折，说明为什么这次方法更有效。",
        "proof": "用过程或结果证明前面的说法可信。",
        "cta": "用一句简洁指令收尾，推动关注或咨询。",
    }[beat_id]


def _cycle(items: List[Dict[str, Any]]) -> Iterable[Dict[str, Any]]:
    while True:
        for item in items:
            yield item


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="短视频爆款解析与AI视频生成流水线 Skill")
    parser.add_argument("--stage", default="pipeline", choices=["analyze", "match", "script", "generate", "compose", "pipeline"])
    parser.add_argument("--input", help="JSON string or @/absolute/path/to/json")
    args = parser.parse_args(argv)
    payload = _load_payload(args.input)
    print(json.dumps(run_stage(args.stage, payload), ensure_ascii=False, indent=2))
    return 0


def _load_payload(raw_input: Optional[str]) -> Dict[str, Any]:
    if not raw_input:
        return json.load(__import__("sys").stdin)
    if raw_input.startswith("@"):
        with open(raw_input[1:], "r", encoding="utf-8") as handle:
            return json.load(handle)
    return json.loads(raw_input)


if __name__ == "__main__":
    raise SystemExit(main())
