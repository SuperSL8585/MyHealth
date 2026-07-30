# MyHealth
A project to utilize an LLM API to summarize a patient's medical records and simplify medical vocabulary. Grabs valuable insights for users to remember.

## Installation
Clone the repository and download its dependencies:
```bash
git clone https://github.com/SuperSL8585/MyHealth.git
cd MyHealth
pip install google-genai
pip install streamlit
pip install streamlit-pdf
```

## Usage
Run the following command to terminal to run the website:
```bash
streamlit run interface.py
```

## Testing
One of the files in this repo is called test_report.pdf. Feel free to upload this test medical report into the app to see how MyHealth is able to exctract insights and summaries from the file.

## About MyHealth
Users upload their medical documents directly through the app. Powered by the Gemini API, MyHealth analyzes the text to extract and highlight key insights essential for the patient. After reading the simplified summary, users can interact with an integrated chatbot on the analysis page to ask follow-up questions about their report. To maximize accessibility, the app allows users to seamlessly switch languages and select different models based on their needs.

## Disclaimer
MyHealth is an educational tool built to improve patient health literacy. It does not provide medical advice or diagnoses. Always verify AI-generated insights with a licensed medical professional.
