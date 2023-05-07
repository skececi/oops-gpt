from enum import Enum
import os


# Define the command output capturing function for Zsh
ZSH_CAPTURE_OUTPUT_FUNC = r"""
export LAST_CMD_OUTPUT_FILE="/tmp/last_cmd_output"

function capture_command_output() {
  if [[ -n $LAST_COMMAND ]]; then
    eval "$LAST_COMMAND" > >(tee >(cat > "$LAST_CMD_OUTPUT_FILE")) 2> >(tee >(cat 1>&2) > "$LAST_CMD_OUTPUT_FILE" 1>&2)
    unset LAST_COMMAND
  fi
}

function set_last_command() {
  LAST_COMMAND=$(fc -ln -1)
}

autoload -Uz add-zsh-hook
add-zsh-hook precmd capture_command_output
add-zsh-hook preexec set_last_command
"""

# Define the command output capturing function for Bash
BASH_CAPTURE_OUTPUT_FUNC = r"""
export LAST_CMD_OUTPUT_FILE="/tmp/last_cmd_output"

function capture_command_output() {
  history -a
  local last_command=$(tail -n 1 $HISTFILE)
  eval "$last_command" > >(tee >(cat > "$LAST_CMD_OUTPUT_FILE")) 2> >(tee >(cat 1>&2) > "$LAST_CMD_OUTPUT_FILE" 1>&2)
}

PROMPT_COMMAND="capture_command_output"
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


