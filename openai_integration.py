import openai
from config import  MODEL, FUNCTIONALITY_MARKER, CODE_MARKER, COMPONENTS_MARKER, SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
import os
# Set the OpenAI API key from the configuration
openai.api_key = os.getenv('OPENAI_API_KEY')

def clean_text(text):
    """Remove unwanted Markdown and other formatting."""
    # Replace known unwanted characters
    cleaned_text = text.replace("```python", "").replace("```", "").strip()
    # Further strip leading and trailing asterisks and whitespace
    cleaned_text = cleaned_text.strip('*').strip()
    return cleaned_text

def extract_details_from_response(response_text):
    """Extract functionality description, SKiDL code, and components list from OpenAI response."""
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

def get_openai_response(description):
    """Generate a response from the OpenAI API based on the provided description."""
    # Format the system and user prompts with the provided description
    system_prompt = SYSTEM_PROMPT
    user_prompt = USER_PROMPT_TEMPLATE.format(description=description)

    # Generate the response using OpenAI's Chat Completion API
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message['content']
