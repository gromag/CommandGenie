# CommandGenie

_CommandGenie_ is a Python-based command-line tool that uses the power of artificial intelligence to generate commands and automate common tasks. With _CommandGenie_, you can save time and streamline your workflow, all while impressing your colleagues with your newfound command-line wizardry.

Please note that this is an early prototype, which means it will contain bugs and unfinished features. However, I believe that even in its current state, _CommandGenie_ can provide value to developers looking to automate their command-line tasks and increase their productivity.

By using CommandGenie, you accept that I am not responsible for any consequences that may result from using this tool, including but not limited to data loss, system instability, or other issues.

## Install

Please see build, not published to Pypy yet.
```bash
#pip install command_genie
#export OPENAI_API_KEY=<my-key>
```

## Usage



```bash
genie find all txt files containing the word openai in current directory

# Expected output:

# ls
# find . -name "*.txt" -exec grep -l "openai" {} \;

# Would you like to execute? [Y/n/(e)xplain] 

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