import logging

import gradio as gr
from rich.logging import RichHandler
from research_manager import ResearchManager

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, markup=True, show_path=False)],
)


async def run(query: str, deliver: bool):
    if not query.strip():
        yield "Please enter a research topic before running."
        return
    async for chunk in ResearchManager().run(query, deliver=deliver):
        yield chunk


with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research — Music")
    query_textbox = gr.Textbox(label="What music topic would you like to research?")
    deliver_checkbox = gr.Checkbox(label="Send report via email", value=True)
    run_button = gr.Button("Run", variant="primary")
    report = gr.Markdown(label="Report")

    run_button.click(fn=run, inputs=[query_textbox, deliver_checkbox], outputs=report)
    query_textbox.submit(fn=run, inputs=[query_textbox, deliver_checkbox], outputs=report)

ui.launch(inbrowser=True)
