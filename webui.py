import gradio as gr

# 占位的模型加载函数，仅用于展示接口形态，不实际下载权重

def load_model():
    """返回一个伪模型对象，真实部署时可在此处加载 Tarsier2-Recap-7b。"""

    class DummyModel:
        def __call__(self, video_path: str, text_prompt: str):
            return {
                "recap": "【演示结果】该示例强调 DREAM-1K 场景下对长视频的细粒度描述能力。",
                "key_frames": [
                    "DREAM-1K 片段 1：出现复杂人物互动与动作组合。",
                    "DREAM-1K 片段 2：场景切换引入新的语义单元。",
                    "DREAM-1K 片段 3：视频末尾给出事件收束与情节总结。",
                ],
            }

    return DummyModel()


model = load_model()


def analyze_video(video, prompt):
    if video is None:
        return "请先上传一段用于 DREAM-1K 风格评测的视频片段。", ["尚未检测到关键帧。"], ""

    outputs = model(str(video), prompt or "请从评测角度对该视频进行细粒度描述。")
    recap_text = outputs["recap"]
    key_frames = outputs["key_frames"]
    key_frames_markdown = "\n".join(f"- {item}" for item in key_frames)
    return recap_text, key_frames, key_frames_markdown


with gr.Blocks(title="Tarsier2-Recap-7b DREAM-1K WebUI（演示版）") as demo:

    gr.Markdown(
        """# Tarsier2-Recap-7b DREAM-1K WebUI（演示版）\n\n"
        "界面设计与主仓库保持一致，仅在文案层面突出 DREAM-1K 评测场景，便于在论文复现实验中直接演示。"""
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 1. 输入区")
            video_input = gr.Video(label="上传 DREAM-1K 风格视频", sources=["upload"], interactive=True)
            prompt_input = gr.Textbox(
                label="文本指令（可选）",
                value="请从评测指标角度描述该视频中的关键事件与时间片段。",
                lines=3,
            )
            run_btn = gr.Button("开始分析（演示，不进行真实推理）", variant="primary")

        with gr.Column(scale=1):
            gr.Markdown("### 2. 结果区：评测视角下的描述")
            recap_output = gr.Textbox(
                label="视频长篇描述（DREAM-1K 示意输出）",
                lines=10,
                interactive=False,
            )
            keyframe_gallery = gr.HighlightedText(
                label="时间轴关键片段（文本示意）",
                combine_adjacent=True,
            )

    with gr.Accordion("可选：Markdown 形式结果与后处理", open=False):
        keyframe_md = gr.Markdown(
            "尚未检测到关键帧。可将伪推理结果复制至评测报告或实验记录。"
        )

    def _wrapped_analyze(video, prompt):
        recap, key_frames, key_md = analyze_video(video, prompt)
        highlighted = [(kf, "关键片段") for kf in key_frames]
        return recap, highlighted, key_md

    run_btn.click(
        _wrapped_analyze,
        inputs=[video_input, prompt_input],
        outputs=[recap_output, keyframe_gallery, keyframe_md],
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861, show_error=True)
