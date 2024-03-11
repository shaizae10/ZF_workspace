import os
import openai
import importlib

# Dynamic Configuration Loader
def load_configuration(config_module_name):
    config_module = importlib.import_module(config_module_name)
    config = {
        'MODEL': config_module.MODEL,
        'FUNCTIONALITY_MARKER': config_module.FUNCTIONALITY_MARKER,
        'CODE_MARKER': config_module.CODE_MARKER,
        'COMPONENTS_MARKER': config_module.COMPONENTS_MARKER,
        'SYSTEM_PROMPT': config_module.SYSTEM_PROMPT,
        'USER_PROMPT_TEMPLATE': config_module.USER_PROMPT_TEMPLATE
    }
    return config

# OpenAIElectronicDesignAssistant Class
class OpenAIapi:
    def __init__(self, config):
        self.model = config['MODEL']
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

        self.functionality_marker = config['FUNCTIONALITY_MARKER']
        self.code_marker = config['CODE_MARKER']
        self.components_marker = config['COMPONENTS_MARKER']
        self.system_prompt = config['SYSTEM_PROMPT']
        self.user_prompt_template = config['USER_PROMPT_TEMPLATE']

    @staticmethod
    def clean_text(text: str) -> str:
        cleaned_text = text.replace("```python", "").replace("```", "").strip()
        cleaned_text = cleaned_text.strip('*').strip()
        return cleaned_text

    def extract_details_from_response(self, response_text: str) -> tuple:
        try:
            functionality_start = response_text.index(self.functionality_marker) + len(self.functionality_marker)
            code_start = response_text.index(self.code_marker)
            functionality_description = response_text[functionality_start:code_start].strip()

            code_end = response_text.index(self.components_marker)
            code_segment = response_text[code_start + len(self.code_marker):code_end].strip()

            components_segment = response_text[code_end + len(self.components_marker):].strip()

            functionality_description = self.clean_text(functionality_description)
            code = self.clean_text(code_segment)
            components = self.clean_text(components_segment)

            return functionality_description, code, components
        except ValueError as e:
            print("Error extracting details:", e)
            return None, None, None

    def get_openai_response(self, description: str) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": self.user_prompt_template.format(description=description)}
            ]
        )
        return response.choices[0].message['content']
