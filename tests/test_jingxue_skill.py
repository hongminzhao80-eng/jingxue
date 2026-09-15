import unittest

from jingxue_skill import (
    SkillInputError,
    analyze_viral_formula,
    generate_ai_video_segments,
    generate_script,
    match_user_assets,
    run_pipeline,
    run_stage,
)


SAMPLE_PAYLOAD = {
    "reference_text": "先给你看结果，再告诉你为什么普通人拍不出这种反差感。最后我会给你一个可以直接照着拍的动作模板。",
    "goal": "用用户自拍素材制作带转化力的短视频",
    "user_assets": [
        {"id": "selfie-1", "type": "video", "duration_seconds": 6, "style": "口播"},
        {"id": "selfie-2", "type": "image", "duration_seconds": 3, "style": "前后对比"},
    ],
}


class JingxueSkillTests(unittest.TestCase):
    def test_pipeline_returns_all_required_sections(self) -> None:
        result = run_pipeline(SAMPLE_PAYLOAD)

        self.assertEqual(
            set(result.keys()),
            {
                "爆款解析报告",
                "素材匹配方案",
                "新视频脚本 + 分镜提示词",
                "AI 视频片段",
                "最终成片",
            },
        )
        self.assertTrue(result["最终成片"]["用户自拍素材已融入"])

    def test_formula_signature_is_reused_across_stages(self) -> None:
        result = run_pipeline(SAMPLE_PAYLOAD)

        signature = result["爆款解析报告"]["公式拆解"]["signature"]
        self.assertEqual(result["素材匹配方案"]["formula_signature"], signature)
        self.assertEqual(result["新视频脚本 + 分镜提示词"]["formula_signature"], signature)
        self.assertEqual(result["AI 视频片段"]["formula_signature"], signature)
        self.assertEqual(result["最终成片"]["formula_signature"], signature)

    def test_match_stage_requires_user_assets(self) -> None:
        with self.assertRaises(SkillInputError):
            match_user_assets({"reference_text": "只有文案，没有素材"})

    def test_stage_functions_are_independently_callable(self) -> None:
        analysis = analyze_viral_formula(SAMPLE_PAYLOAD)
        script = generate_script(SAMPLE_PAYLOAD, analysis)
        clips = generate_ai_video_segments(SAMPLE_PAYLOAD, script)

        self.assertIn("爆款解析报告", analysis)
        self.assertIn("新视频脚本 + 分镜提示词", script)
        self.assertEqual(clips["AI 视频片段"]["generation_mode"], "prompt_package")

    def test_compose_stage_uses_selfie_assets_in_timeline(self) -> None:
        composed = run_stage("compose", SAMPLE_PAYLOAD)
        timeline_asset_ids = {entry["user_asset_id"] for entry in composed["最终成片"]["timeline"]}

        self.assertTrue(timeline_asset_ids.issubset({"selfie-1", "selfie-2"}))
        self.assertGreater(len(timeline_asset_ids), 0)


if __name__ == "__main__":
    unittest.main()
