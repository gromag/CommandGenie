# CommandGenie

CommandGenie is a Python-based command-line tool that uses [OpenAI GPT3](https://openai.com/api/) to generate commands and automate common tasks by converting plain English into shell commands. With CommandGenie, you can inspect the generated command, see an explanation of why the model took those steps, and execute the command.

## Disclaimer

- CommandGenie is an early prototype and may contain bugs or unfinished features.
- Please make sure you understand what the generated command is doing before executing it, don't assume it will be 100% correct.
- Do not rely solely on the model's own explanation; do your own research if you are not sure.
- By using CommandGenie, you accept that I am not responsible for any consequences that may result from using this tool, including but not limited to data loss, system instability, or other issues.

I believe that even in its current state, CommandGenie can provide value to developers looking to automate their command-line tasks and increase their productivity. Thank you for trying out my tool, and I hope you find it useful in your work!"""



## Install

Please see build, not published to Pypy yet.
```bash
#pip install command_genie
```

## Usage

```bash
#export OPENAI_API_KEY=<my-key>
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

## Build
```bash
cd CommandGenie
source .venv/bin/activate
pip install build
python -m build .
deactivate
python -m venv .venv2 #installation is done on within a different venv to the development venv
source .venv2/bin/activate
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