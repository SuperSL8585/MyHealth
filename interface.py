import streamlit as st
from analyzer import analyze_pdf, chat_bot

# ==========================================
# Setup
# ==========================================

if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'report_analysis' not in st.session_state:
    st.session_state.report_analysis = None
if 'pdf' not in st.session_state:
    st.session_state.pdf = None
if 'raw_pdf' not in st.session_state:
    st.session_state.raw_pdf = None


def make_dash():
    st.session_state.submitted = True
    st.rerun()


popular_languages = [
    "English (English)",
    "简体中文 (Simplified Chinese)",
    "繁體中文 (Traditional Chinese)",
    "हिन्दी (Hindi)",
    "Español (Spanish)",
    "Français (French)",
    "العربية (Arabic)",
    "বাংলা (Bengali)",
    "Português (Portuguese)",
    "Русский (Russian)",
    "اردو (Urdu)",
    "Bahasa Indonesia (Indonesian)",
    "Deutsch (German)",
    "日本語 (Japanese)",
    "Kiswahili (Swahili)",
    "Türkçe (Turkish)",
    "한국어 (Korean)",
    "Tiếng Việt (Vietnamese)",
    "Italiano (Italian)",
]

models = {
    "Gemini 3.6 Flash": "gemini-3.6-flash",
    "Gemini 3.5 Flash": "gemini-3.5-flash",
    "Gemini 2.5 Flash": "gemini-2.5-flash",
    "Gemini 2.0 Flash": "gemini-2.0-flash",
    "Gemini 3.1 Flash Lite": "gemini-3.1-flash-lite",
    "Gemini 2.5 Flash Lite": "gemini-2.5-flash-lite",
    "Gemini 2.0 Flash Lite": "gemini-2.0-flash-lite",
    "Gemini 2.5 Pro": "gemini-2.5-pro",
    "Gemini 1.5 Flash": "gemini-1.5-flash",
    "Gemini 1.5 Pro": "gemini-1.5-pro"
}

max_retries = 3

# ==========================================
# Interface
# ==========================================

if not st.session_state.submitted:
    # Home Screen
    st.title('Welcome to MyHealth!', anchor=False, text_alignment='center')
    st.header('An AI analyzer to summarize your medical report',
              anchor=False, divider='gray', text_alignment='center')
    st.subheader('Please upload your medical report below:',
                 anchor=False, text_alignment='center')

    st.space('small')

    upload = st.container(border=True)

    # File Upload and Settings Selection
    left, right = upload.columns(2)
    with left:
        language = upload.selectbox(
            '🌎 Select a language for your report', popular_languages)
    with right:
        model = upload.selectbox(
            '🤖 Select a model to generate your report', models.keys())

    uploaded_file = upload.file_uploader(
        '**Upload file here!**', type=['pdf'])

    st.session_state.pdf = uploaded_file

    # AI Processing
    if st.button('Submit file', type='primary'):
        if uploaded_file is None:
            upload.write('**Please Upload a Valid File**')
        else:
            with upload.spinner('Analyzing your medical file to generate insights', width='stretch'):
                report_analysis, raw_pdf = analyze_pdf(
                    uploaded_file, language, models[model])
                st.session_state.raw_pdf = raw_pdf
                st.session_state.report_analysis = report_analysis
                make_dash()

    # About Section
    about = st.container(border=True)
    about.subheader('About MyHealth:', anchor=False, divider='gray')
    about.write("""**The Problem:** During doctor visits, patients often struggle to recall key medical details
                or ask clarifying questions. Post-visit summaries and medical reports are typically dense, jargon-heavy,
                and confusing, leading to miscommunication, patient anxiety, and unclear aftercare instructions.
                """)
    about.write("""**The Solution:** MyHealth translates complex medical reports into plain, accessible language.
                By simplifying clinical documentation, MyHealth helps patients quickly understand their diagnosis
                and care plans while streamlining physician handoffs and patient communication.""")

else:
    # Analysis page
    st.title('Your Summarized Analysis is Here!',
             anchor=False, text_alignment='center')
    report = st.session_state.report_analysis

    name = report.name
    age = report.age
    summary = report.summary
    insights = report.vital_insights
    next_steps = report.next_steps
    gender = report.gender

    # Personal Details
    personal_details = st.container(border=True)
    personal_details.subheader(
        'Personal Details', anchor=False, divider='gray')
    personal_details.write(
        f'**Name:** {name}\n\n**Age:** {age}\n\n**Gender:** {gender}')

    left, right = st.columns(2)

    with left:
        # Action Plan
        action_plan = st.container(border=True)
        action_plan.header('Action Plan', anchor=False,
                           divider='gray', text_alignment='center')
        counter = 0
        for next_step in next_steps:
            counter += 1
            action_plan.write(f'{counter}. {next_step.step}')

    with right:
        # Main Points
        insight_container = st.container(border=True)
        insight_container.header(
            'Main Points', anchor=False, divider='gray', text_alignment='center')
        for insight in insights:
            insight_container.write(f'➡️ {insight.insight}')

    summary_container = st.container(border=True)
    summary_container.header('Summary of Visit', anchor=False, divider='gray')
    summary_container.write(summary)

    # Chatbot
    ask_ai = st.container(border=True)
    ask_ai.subheader(
        'Got Questions? Ask AI for more specific analysis', anchor=False, divider='gray')
    language = ask_ai.selectbox(
        '🌎 Please select a language for your response', popular_languages)
    model = ask_ai.selectbox(
        '🤖 Select a model to generate your response', models.keys())
    prompt = ask_ai.chat_input(
        'Ask AI any questions you have about your medical report')
    if prompt:
        with ask_ai.spinner('Please wait for a response'):
            response = chat_bot(
                prompt, st.session_state.raw_pdf, language, models[model])
        ask_ai.write(response)

    # PDF Report
    st.subheader('Your uploaded report:', anchor=False, divider='gray')
    st.pdf(st.session_state.pdf)

    if st.button('Analyze a New Report', type='primary'):
        st.session_state.submitted = False
        st.rerun()
