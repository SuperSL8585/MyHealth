import streamlit as st
from analyzer import analyze_pdf


if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if "report_analysis" not in st.session_state:
    st.session_state.report_analysis = None


def make_dash():
    st.session_state.submitted = True
    st.rerun()


if not st.session_state.submitted:
    st.title('Welcome to MyHealth!')
    st.header('Please upload your medical report below:')

    uploaded_file = st.file_uploader(
        'Upload medical report here!', type=['pdf'])

    if st.button('Submit file'):
        if uploaded_file is None:
            st.write('Please Upload a Valid File')
        else:
            with st.spinner('Analyzing your medical file to generate insights', width='stretch'):
                report_analysis = analyze_pdf(uploaded_file)
                st.session_state.report_analysis = report_analysis
                make_dash()

else:
    st.title('Your Summarized Analysis is Here!')
    report = st.session_state.report_analysis

    name = report.name
    age = report.age
    summary = report.summary
    insights = report.vital_insights

    left, right = st.columns(2)

    with left:
        personal_details = st.container(border=True)
        personal_details.write(f'Name: {name}')
        personal_details.write(f'Age: {age}')

    with right:
        insight_container = st.container(border=True)
        for insight in insights:
            insight_container.write(f'➡️ {insight.insight}')

    summary_container = st.container(border=True)
    summary_container.header('Summary')
    summary_container.write(summary)
