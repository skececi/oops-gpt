import os
import openai

from config import Config

config = Config()

PROMPT_PREPEND = r"""
you are a helpful CLI tool suggesting followup commands to run next. the following is the output of the process that just ran. tell me what happened in the output, and suggest 3 options for commands that could be run directly after this one (and a short comment - no longer than 25 words - on what each of your suggested commands will do).

output in the following format. DO NOT include any headers of prefacing text, get right into it. 
<SUMMARY OF OUTPUT, 2-3 sentences>
1. `first command` : summary of FIRST OPTION
2. `second command` : summary of SECOND OPTION
3.  `third command` : summary of THIRD OPTION

Always surround the actual command in backticks (`). Always separate the command from the description with a colon (:).

always refer to the output as "the previous command". i need to be able to parse this into code so follow the instructions precisely. 
the three commands must be able to be executed right away without any additional input from the user. avoid commands with placeholders.
if you must use a placeholder (avoid at all costs!), it must be between angle brackets <placeholder>. MAKE SURE Each placeholder is a unique string.
However, AVOID PLACEHOLDERS AT ALL COSTS. DO NOT USE PLACEHOLDERS.

Here is the output of the previous command:
"""


def truncate_from_beginning(input_string, max_length=4000, keep_start=500):
    """Truncate a string from the beginning, keeping the first n characters."""

    if len(input_string) > max_length:
        start_part = input_string[:keep_start]
        end_part = input_string[-(max_length - keep_start):]
        return start_part + end_part
    return input_string


def send_output_to_llm(output: str):
    print("Sending output to LLM...")
    prompt = PROMPT_PREPEND + output
    # truncate the prompt to 3000 words.
    prompt = truncate_from_beginning(prompt)
    try:
        completion = openai.ChatCompletion.create(
            model=config.model, 
            messages=[{"role": "user", "content": prompt}]
        )
        return completion["choices"][0]["message"]["content"]
    except openai.error.AuthenticationError:
        print("Authentication error. Check your OpenAI API key in the .env file")
        exit()
    # except all other openai errors
    except openai.error.OpenAIError as e:
        # print the error message'
        print(e)
        exit()

