from supply_chain_demo.exporter import export_json, export_html
from supply_chain_demo.report import DemoReport, ReportSection


def _sample_report():
    return DemoReport(sections=[ReportSection(title="Sample", body="Hello\nWorld")])


def test_export_json_contains_section():
    payload = export_json(_sample_report())
    assert "Sample" in payload


def test_export_html_escapes_body():
    html_doc = export_html(_sample_report())
    assert "<h2>Sample</h2>" in html_doc
    assert "Hello<br/>World" in html_doc
