# CommandGenie

CommandGenie is a Python-based command-line tool that uses [OpenAI GPT3](https://openai.com/api/) to generate commands and automate common tasks by converting plain English into shell commands. With CommandGenie, you can inspect the generated command, see an explanation of why the model took those steps, and execute the command.

## Disclaimer

- CommandGenie is an early prototype and may contain bugs or unfinished features.
- Please make sure you understand what the generated command is doing before executing it, don't assume it will be 100% correct.
- Do not rely solely on the model's own explanation; do your own research if you are not sure.
- By using CommandGenie, you accept that I am not responsible for any consequences that may result from using this tool, including but not limited to data loss, system instability, or other issues.

I believe that even in its current state, CommandGenie can provide value to developers looking to automate their command-line tasks and increase their productivity. Thank you for trying out my tool, and I hope you find it useful in your work!"""





## Usage

```bash
export OPENAI_API_KEY=<my-openai-api-key>
# start daemon on a separate shell window
genie -start
```

```bash
# ask question
genie find and delete all __pycache__ folders
```

Likely response:
```text
find . -name __pycache__ -type d -exec rm -rf {} +

Would you like to execute? [Y/n/(e)xplain]
```

If you choose `explain` option, it gives an explanation of the command.

```text
I need to take the following actions:
- Find all __pycache__ folders
- Delete all __pycache__ folders
Explanation:
`find` searches for files and directories in a directory hierarchy
`-name` option allows to specify the name of the file or directory to search for
`-type d` option specifies that only directories should be searched
`-exec rm -rf {} +` option executes the command `rm -rf` on each found directory

Would you like to execute? [Y/n/(e)xplain]
```

Please use help for all options.


```text
genie --help
usage: genie [-h] [-v] [-V] [-s] [-c COMMAND]

CommandGenie Utility (version: 0.1.dev9+gdbba154.d20230226). CommandGenie
is a Python-based command-line tool that uses the power of artificial
intelligence to generate commands and automate common tasks. Please start
the daemon `genie -s` on a separate shell window before starting the
client. Example usage: `genie delete all __pycache__ folders`

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Prints the CommandGenie version
  -V, --verbose         Sets high verbosity (DEBUG). To view the file logs
                        see: /Users/gr/Library/Logs/CommandGenie
  -s, --start           Starts the CommandGenie daemon
  -c COMMAND, --command COMMAND
                        Takes an English instruction which will be
                        converted into a shell command
```

## Install

Please see build section below, currently not published to Pypy so you will need to download this project, build and install the wheel file.
```bash
#pip install command_genie
```

## Build
```bash
git clone https://github.com/gromag/CommandGenie.git
cd CommandGenie
source .venv/bin/activate
pip install build
python -m build .
deactivate
#installation should be done on a different venv or your main python environment
# python -m venv .venv2 
# source .venv2/bin/activate
pip install dist/*.whl
cd ..

```

## Calculating test coverage

```bash
cd CommandGenie
source .venv/bin/activate
coverage run --source=. -m pytest 
coverage report
coverage html -d coverage 
```