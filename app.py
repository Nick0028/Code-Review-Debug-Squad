import streamlit as st
from dotenv import load_dotenv
from core.orchestrator import review_code
from core.report_generator import build_markdown_report

load_dotenv()
st.set_page_config(page_title="Code Review & Debug Squad", page_icon="🛠️", layout="wide")
st.title("🛠️ Code Review & Debug Squad")
st.caption("A multi-agent AI code assistant for debugging, style review, fixes and tests.")

with st.sidebar:
    st.header("Review settings")
    mode = st.selectbox("Review mode", ["Full Code Review", "Debug Code", "Review Code Style", "Explain Code", "Generate Test Cases"])
    language = st.selectbox("Language", ["Python"])

uploaded = st.file_uploader("Upload a Python file (optional)", type=["py"])
default_code = "def average(numbers):\n    total = 0\n    for i in range(len(numbers) + 1):\n        total += numbers[i]\n    return total / len(numbers)\n"
code = st.text_area("Or paste your code here", value=default_code, height=300)
if uploaded is not None:
    try:
        code = uploaded.getvalue().decode("utf-8")
        st.success(f"Loaded {uploaded.name}")
    except UnicodeDecodeError:
        st.error("The uploaded file is not valid UTF-8 text.")

if st.button("Run review", type="primary"):
    if not code.strip():
        st.warning("Please paste or upload code.")
    else:
        with st.spinner("Agents are reviewing your code..."):
            try:
                st.session_state["review_result"] = review_code(code, mode, language)
                st.session_state["review_code"] = code
            except Exception as exc:
                st.error(f"Review failed: {exc}")
                st.exception(exc)

if "review_result" in st.session_state:
    result = st.session_state["review_result"]
    st.divider()
    st.subheader("Review summary")
    a, b, c, d = st.columns(4)
    a.metric("Quality score", f'{result.get("quality_score", "N/A")}/100')
    b.metric("Bugs", len(result.get("bugs", [])))
    c.metric("Style findings", len(result.get("style", [])))
    d.metric("Tests passed", result.get("tests", {}).get("passed", 0))
    tabs = st.tabs(["Bug analysis", "Style review", "Fixed code", "Tests", "Full report"])
    with tabs[0]:
        st.markdown(result.get("bug_summary", ""))
        for item in result.get("bugs", []):
            st.markdown(f'**{item.get("severity", "Medium")} — {item.get("title", "Finding")}**')
            st.write(item.get("description", ""))
            if item.get("line") is not None:
                st.caption(f'Line: {item["line"]}')
            st.write(item.get("suggestion", ""))
        if result.get("static_analysis", {}).get("syntax_error"):
            st.error(result["static_analysis"]["syntax_error"])
        elif result.get("static_analysis", {}).get("ruff_output"):
            st.code(result["static_analysis"]["ruff_output"])
    with tabs[1]:
        st.markdown(result.get("style_summary", ""))
        for item in result.get("style", []):
            st.write(f'**{item.get("rule", "Style issue")}** — {item.get("message", "")}')
    with tabs[2]:
        st.code(result.get("fixed_code", ""), language="python")
        st.write(result.get("fix_explanation", ""))
    with tabs[3]:
        st.markdown(result.get("test_summary", ""))
        st.code(result.get("generated_tests", ""), language="python")
        tests = result.get("tests", {})
        st.write(f'Passed: {tests.get("passed", 0)} | Failed: {tests.get("failed", 0)}')
        if tests.get("output"):
            st.code(tests["output"])
        if tests.get("warning"):
            st.warning(tests["warning"])
    with tabs[4]:
        report = build_markdown_report(st.session_state["review_code"], result)
        st.markdown(report)
        st.download_button("Download review report", report, "code_review_report.md", "text/markdown")
