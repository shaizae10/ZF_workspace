# config.py

MODEL = 'gpt-3.5-turbo'

# Markers for parsing the response
FUNCTIONALITY_MARKER = "Functionality Description:"
CODE_MARKER = "SKiDL Python Code:"
COMPONENTS_MARKER = "Components List:"

# Static text for prompts, broken into shorter lines


SYSTEM_PROMPT = (
    "You are a helpful assistant adept at electronic circuit design with SKiDL. "
    "Clearly separate the functionality description, SKiDL code, and components list "
    "using the provided markers."
)

USER_PROMPT_TEMPLATE = (
    "Based on this description: '{description}', describe the functionality, "
    "generate SKiDL Python code, and list all components needed. Use "
    "'Functionality Description:', 'SKiDL Python Code:', and 'Components List:' as "
    "markers for each section."
)
