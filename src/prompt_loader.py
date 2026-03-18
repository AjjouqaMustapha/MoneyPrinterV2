import os
from config import ROOT_DIR

PROMPTS_DIR = os.path.join(ROOT_DIR, "prompts")

def load_prompt(name: str, **kwargs) -> str:
    """
    Loads a prompt template from the prompts/ directory and fills in variables.

    Args:
        name: The prompt template filename (without .txt extension)
        **kwargs: Variables to substitute in the template

    Returns:
        The formatted prompt string
    """
    path = os.path.join(PROMPTS_DIR, f"{name}.txt")
    with open(path, "r", encoding="utf-8") as f:
        template = f.read()
    return template.format(**kwargs)
