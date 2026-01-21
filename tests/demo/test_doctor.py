from supply_chain_demo.doctor import run_diagnostics, as_text


def test_doctor_reports_python():
    diagnostics = run_diagnostics()
    names = {diag.name for diag in diagnostics}
    assert "python" in names


def test_doctor_text_output():
    diagnostics = run_diagnostics()
    output = as_text(diagnostics)
    assert "Doctor Report" in output
