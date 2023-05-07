import os
import sys 
import subprocess

from pprint import pformat

from first_time_setup import write_to_config_file
from gpt import send_output_to_llm




LAST_CMD_OUTPUT_FILE = "/tmp/last_cmd"


def get_last_command():
    # Read the last command from the file
    with open(LAST_CMD_OUTPUT_FILE, "r") as file:
        last_command = file.read().strip()
        print("Last command: " + last_command)
        return last_command
    

def run_last_command_and_get_output():
    last_command = get_last_command()
    # Run the command in a new subprocess and capture the output
    result = subprocess.run(last_command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result


def fix_command():
    """Fixes previous command. Used when called without arguments."""
    result = run_last_command_and_get_output()
    print("RESULT: " + result)
    llm_response = send_output_to_llm(result)
    print(llm_response)

def entrypoint():
    print("Hit main. Fixing your command...")    
    fix_command()



if __name__ == '__main__':
    # write_to_config_file()
    entrypoint()