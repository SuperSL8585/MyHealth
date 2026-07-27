from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional
import tempfile


class Insights(BaseModel):
    """
    Insights for the vital insights part of the report
    """
    insight: str = Field(
        description='An very important point raised in the report regarding the patient\'s health'
        'These insights should be short, concise, and to the point. Any vital extraneous information'
        'not written in the insights should be in the summary')


class Plan(BaseModel):
    """
    The next steps and aftercare plan
    """
    step: str = Field(
        description='One concise step that should be taken for the patient\'s after visit plan.'
        'This should be something the patient should do.'
    )


class Report(BaseModel):
    name: str = Field(description='The pateint\'s name')
    age: int = Field(description='The patient\'s age')
    gender: str = Field(description='The patient\'s gender')
    vital_insights: List[Insights]
    summary: str = Field(description='The summary of the medical report in concise terms '
                         'that a non medical professional could understand')
    next_steps: List[Plan]


def analyze_pdf(pdf, language, model):
    """
    Analyzes a given medical report pdf by querying gemini to extract vital insights for user
    pdf: a variable associated with the medical report pdf
    language: the user's desired language output
    analyzed_report: a pydantic object with analysis on the user's report
    report: the uploaded report used for the chatbot function
    """
    client = genai.Client()

    # Create temporary path for given file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf.getvalue())
        temp_path = tmp.name
        print(temp_path)

    report = client.files.upload(file=temp_path)

    interaction = client.interactions.create(
        model=f'{model}',
        input=[
            {'type': 'document', 'uri': report.uri, 'mime_type': report.mime_type},
            {'type': 'text', 'text': f'Analyze this pdf and extract the vital most important parts for the patient to know.'
             f'Write **all** output in {language}. Do not use any other language. Include page numbers for reference.'}
        ],
        response_format={
            'type': 'text',
            'mime_type': 'application/json',
            'schema': Report.model_json_schema()
        }
    )

    analyzed_report = Report.model_validate_json(interaction.output_text)

    return analyzed_report, report


def chat_bot(prompt, pdf, language, model):
    """
    Given a prompt and the pdf, gemini will answer any question about the medical report
    prompt: the user's given prompt
    pdf: the uploaded pdf from the analyze_pdf function
    language: the user's desired language
    interaction.output_text: the chat bot's response to the user's prompt
    """
    client = genai.Client()

    interaction = client.interactions.create(
        model=f'{model}',
        input=[
            {'type': 'document', 'uri': pdf.uri, 'mime_type': pdf.mime_type},
            {'type': 'text', 'text': f"""Here\'s your prompt: {prompt} Remember to answer as if you are the doctor
            and the user is a non medical professional patient. However don't actually be a doctor. You are just
            informing the patient. So your answers should be in terms easy for non medically trained individuals
            to understand and all responses should be in {language}"""}
        ]
    )

    return interaction.output_text
