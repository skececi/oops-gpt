import os
import subprocess
import sys
from pprint import pformat
import re


import inquirer

from first_time_setup import write_to_config_file
from gpt import send_output_to_llm

LAST_CMD_OUTPUT_FILE = "/tmp/last_cmd"


def get_last_command():
    # Read the last command from the file
    with open(LAST_CMD_OUTPUT_FILE, "r") as file:
        last_command = file.read().strip()
        return last_command


def run_last_command_and_get_output() -> str:
    skip_commands = ["python3", "oops", "fix_command"]

    last_command = get_last_command()
    if last_command is None:
        print("No last command found. Exiting.")
        sys.exit(1)
    # error handling to avoid recursion from skip commands. check if any of the skip command strings are in the last command
    if any(skip_command in last_command for skip_command in skip_commands):
        print("Skipping command: " + last_command)
        sys.exit(0)
    # Run the command in a new subprocess and capture the output
    output = subprocess.run(
        last_command,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return output

def extract_placeholders(input_string):
    # Define a regular expression pattern to match placeholders between angle brackets
    pattern = r'<(.*?)>'
    # Use re.findall() to find all occurrences of the pattern in the input string
    placeholders = re.findall(pattern, input_string)
    # Return the list of extracted placeholders
    return placeholders

def prompt_and_substitute(input_string, placeholders):
    # Create a dictionary to store the user's input for each placeholder
    user_inputs = {}
    # Prompt the user for input for each placeholder
    for placeholder in placeholders:
        user_input = input(f"Enter value for <{placeholder}>: ")
        user_inputs[placeholder] = user_input
    # Substitute the user's input back into the original string
    for placeholder, user_input in user_inputs.items():
        input_string = input_string.replace(f"<{placeholder}>", user_input)
    return input_string


def parse_response(llm_response: str):
    """Parses the response from LLM into a summary and a list of suggested commands."""
    split_response = llm_response.split("\n")
    summary = split_response[0]
    suggested_commands = split_response[1:]
    commands_with_descriptors = []
    for suggested_command in suggested_commands:
        try:
            command = suggested_command.split(":")[0].split("`")[1]
            command_descriptor = suggested_command.split(":")[1]
            commands_with_descriptors.append(suggested_command)
        except:
            print("Error parsing command: " + suggested_command)
                        
    return (summary, commands_with_descriptors)



def get_user_selection(commands_with_descriptors):
    # Define the list of commands

    # Create a list prompt using inquirer
    questions = [
        inquirer.List(
            'selected_command',
            message='Select a command to run (ctrl+C to cancel)',
            choices=commands_with_descriptors,
        ),
    ]

    # Prompt the user and get the selected command
    try:
        answers = inquirer.prompt(questions)
        if answers is None:
            print("No command selected. Exiting.")
            sys.exit(1)

        selected_command_with_descriptor = answers['selected_command']

        # get the command itself
        selected_command = selected_command_with_descriptor.split("`")[1]

        placeholders = extract_placeholders(selected_command)
        # if placeholders is not empty
        if placeholders:
            substituted_string = prompt_and_substitute(selected_command, placeholders)
        else:
            substituted_string = selected_command

        print(f'Running command: {substituted_string}')

        # run the command in the current shell
        os.system(substituted_string)
    except KeyboardInterrupt:
        print("Exiting.")


def fix_command():
    """Analyzes previous command."""
    output = run_last_command_and_get_output()
    output_str = output.__str__()

    llm_response = send_output_to_llm(output_str)
    summary, commands_with_descriptors = parse_response(llm_response)
    print("Summary of last command: " + summary)
    print("\n")
    get_user_selection(commands_with_descriptors)


def entrypoint():
    print("Hit main. Fixing your command...")
    fix_command()


if __name__ == "__main__":
    # write_to_config_file()
    entrypoint()
