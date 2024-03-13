import openai
import os


# OpenAIApi Class
class OpenAiApi:
    def __init__(self, config):
        self._api_key = self._read_api_key()
        self.model = config['MODEL']
        openai.api_key = self.api_key
        self.functionality_marker = config['FUNCTIONALITY_MARKER']
        self.code_marker = config['CODE_MARKER']
        self.components_marker = config['COMPONENTS_MARKER']
        self.system_prompt = "".join(config['SYSTEM_PROMPT'])
        self.user_prompt_template = "".join(config['USER_PROMPT_TEMPLATE'])

    @staticmethod
    def _read_api_key():
        # Assuming the API key is stored in 'openai_api_key.txt' within a 'keys' folder
        # located one directory above the current file's directory
        api_key_path = os.path.join(os.path.dirname(__file__), "..", "keys", "openai_api_key.txt")
        with open(api_key_path, 'r') as file:
            return file.readline().strip()

    @property
    def api_key(self):
        return self._api_key

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


