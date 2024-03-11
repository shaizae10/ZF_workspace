import os
import openai
from config import  MODEL, FUNCTIONALITY_MARKER, CODE_MARKER, COMPONENTS_MARKER, SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
# Set the OpenAI API key from the configuration
openai.api_key = os.getenv('OPENAI_API_KEY')

def clean_text(text: str) -> str:
    """Remove unwanted Markdown and other formatting."""
    # Replace known unwanted characters
    cleaned_text = text.replace("```python", "").replace("```", "").strip()
    # Further strip leading and trailing asterisks and whitespace
    cleaned_text = cleaned_text.strip('*').strip()
    return cleaned_text


def extract_details_from_response(response_text: str) -> tuple:
    functionality_marker = "Functionality Description:"
    code_marker = "SKiDL Python Code:"
    components_marker = "Components List:"
    try:
        # Find and extract the segments of interest
        functionality_start = response_text.index(FUNCTIONALITY_MARKER) + len(FUNCTIONALITY_MARKER)
        code_start = response_text.index(CODE_MARKER)
        functionality_description = response_text[functionality_start:code_start].strip()

        code_end = response_text.index(COMPONENTS_MARKER)
        code_segment = response_text[code_start + len(CODE_MARKER):code_end].strip()

        components_segment = response_text[code_end + len(COMPONENTS_MARKER):].strip()

        # Clean up extracted segments
        functionality_description = clean_text(functionality_description)
        code = clean_text(code_segment)
        components = clean_text(components_segment)

        return functionality_description, code, components
    except ValueError as e:
        print("Error extracting details:", e)
        return None, None, None


def get_openai_response(description: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    enhanced_prompt = f"Based on this description: '{description}', describe the functionality, generate SKiDL Python code, and list all components needed. Use 'Functionality Description:', 'SKiDL Python Code:', and 'Components List:' as markers for each section."

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_TEMPLATE}
        ]
    )

    return response.choices[0].message['content']
