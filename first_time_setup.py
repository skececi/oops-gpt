from enum import Enum
import os


# Define the command output capturing function for Zsh
ZSH_CAPTURE_OUTPUT_FUNC = r"""
export LAST_CMD_FILE="/tmp/last_cmd"
function set_last_command() {
  echo "$(fc -ln -1)" > "$LAST_CMD_FILE"
}
autoload -Uz add-zsh-hook
add-zsh-hook preexec set_last_command
"""

# Define the command output capturing function for Bash
BASH_CAPTURE_OUTPUT_FUNC = r"""
export LAST_CMD_FILE="/tmp/last_cmd"
function set_last_command() {
  echo "$(tail -n 1 $HISTFILE)" > "$LAST_CMD_FILE"
}
PROMPT_COMMAND="set_last_command;${PROMPT_COMMAND}"
"""

class Shell(Enum):
    ZSH = 1
    BASH = 2
    # TODO add support for other shells

def get_current_shell():
  shell = os.environ.get('SHELL')
  if "zsh" in shell:
    return Shell.ZSH
  elif "bash" in shell:
    return Shell.BASH
  else:
    raise Exception("Unsupported shell: " + shell)


def write_to_config_file():
  print("Testing first time installation...")
  print("Writing to config file... ")

  user_shell = get_current_shell()
  config_file_path = os.path.expanduser('~/.zshrc') if user_shell == Shell.ZSH else os.path.expanduser('~/.bashrc') if user_shell == Shell.BASH else None
  
  print("Config file path: " + config_file_path)

  # Append the appropriate function to the configuration file based on the shell
  with open(config_file_path, 'a') as config_file:
      if user_shell == Shell.ZSH:
          config_file.write(ZSH_CAPTURE_OUTPUT_FUNC)
      elif user_shell == Shell.BASH:
          config_file.write(BASH_CAPTURE_OUTPUT_FUNC)


