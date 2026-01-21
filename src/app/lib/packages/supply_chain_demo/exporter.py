"""Export demo reports to multiple formats."""

from __future__ import annotations

import html
import json
from dataclasses import asdict
from typing import Dict

from .report import DemoReport


def export_markdown(report: DemoReport) -> str:
    return report.as_markdown()


def export_json(report: DemoReport) -> str:
    payload = {"sections": [asdict(section) for section in report.sections]}
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def export_html(report: DemoReport) -> str:
    blocks = []
    for section in report.sections:
        title = html.escape(section.title)
        body = html.escape(section.body).replace("\n", "<br/>")
        blocks.append(f"<section><h2>{title}</h2><p>{body}</p></section>")
    html_doc = "\n".join(
        [
            "<!doctype html>",
            "<html><head><meta charset='utf-8'><title>Demo Report</title></head><body>",
            "<h1>Demo Report</h1>",
            *blocks,
            "</body></html>",
        ]
    )
    return html_doc + "\n"
