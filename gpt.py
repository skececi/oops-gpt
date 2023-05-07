import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7)



PROMPT_PREPEND = r"""
you are a helpful CLI tool suggesting followup commands to run next. the following is the output of the process that just ran. tell me what happened in the output, and suggest 3 options for commands that could be run directly after this one (and a short comment - no longer than 25 words - on what each of your suggested commands will do).

output in the following format. DO NOT include any headers of prefacing text, get right into it. 
<SUMMARY OF OUTPUT, 2-3 sentences>
1. `first command` : summary of FIRST OPTION
2. `second command` : summary of SECOND OPTION
3.  `third command` : summary of THIRD OPTION

always refer to the output as "the previous command". i need to be able to parse this into code so follow the instructions precisely

Here is the output of the previous command:
"""


def send_output_to_llm(stdout, stderr):
    