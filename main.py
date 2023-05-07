import os
import sys 

from pprint import pformat

from first_time_setup import write_to_config_file


LAST_CMD_OUTPUT_FILE = '/tmp/last_cmd_output'

def get_last_command_output():
    with open(LAST_CMD_OUTPUT_FILE, 'r') as file:
        last_cmd_output = file.read()

    print(f"Last command output:\n{last_cmd_output}")
    return last_cmd_output


def fix_command():
    """Fixes previous command. Used when called without arguments."""
    last_command_output = get_last_command_output()


    # try:
    #     command = types.Command.from_raw_script(raw_command)
    # except EmptyCommand:
    #     logs.debug("Empty command, nothing to do")
    #     return

    # corrected_commands = get_corrected_commands(command)
    # selected_command = select_command(corrected_commands)

    # if selected_command:
    #     selected_command.run(command)
    # else:
    #     sys.exit(1)


def entrypoint():
    print("Hit main. Fixing your command...")    
    fix_command()



if __name__ == '__main__':
    write_to_config_file()
    # main()