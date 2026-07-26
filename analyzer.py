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


class Report(BaseModel):
    name: str = Field(description='The pateint\'s name')
    age: int = Field(description='The patient\'s age')
    vital_insights: List[Insights]
    summary: str = Field(description='The summary of the medical report in concise terms '
                         'that a non medical professional could understand')


def analyze_pdf(pdf):
    """
    Analyzes a given medical report pdf by querying gemini to extract vital insights for user
    pdf: a variable associated with the medical report pdf
    """
    client = genai.Client()

    # Create temporary path for given file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf.getvalue())
        temp_path = tmp.name
        print(temp_path)

    report = client.files.upload(file=temp_path)

    interaction = client.interactions.create(
        model='gemini-3.6-flash',
        input=[
            {'type': 'document', 'uri': report.uri, 'mime_type': report.mime_type},
            {'type': 'text', 'text': 'Analyze this pdf and extract the vital most important parts for the patient to know.'}
        ],
        response_format={
            'type': 'text',
            'mime_type': 'application/json',
            'schema': Report.model_json_schema()
        }
    )

    analyzed_report = Report.model_validate_json(interaction.output_text)
    print(analyzed_report)
    return analyzed_report
