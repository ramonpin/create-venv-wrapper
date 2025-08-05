# SmartWrapper Generator for Python Projects

This project provides a simple yet powerful tool to generate a shell script
that acts as a smart wrapper for running Python projects with virtual
environments.

## Why Use This?

This tool solves several common pain points when working with Python virtual environments:

* **No More `source .venv/bin/activate`**: Run your entire project with a
  single, simple command (`./run.sh`).
* **Consistency for Teams**: Ensures everyone on the team runs the project the
  same way, with the correct interpreter and dependencies.
* **Automation-Friendly**: Perfect for cron jobs and CI/CD scripts where
  sourcing an environment can be tricky and error-prone.

## Key Features of the Generated Wrapper

* **Automatic Virtual Environment Detection**: The generated `run.sh` script
  automatically finds the virtual environment directory (`.venv`, `venv`, etc.)
  within the project.
* **Smart Dependency Installation**: If enabled, the wrapper checks if the
  `requirements.txt` file has been modified. It will only reinstall dependencies
  if necessary, saving time on subsequent runs.
* **Transparent Argument Passing**: All command-line arguments passed to the
  `run.sh` script are forwarded directly to the Python script.
* **Configurable**: The generator allows you to specify the entry point script,
  the virtual environment directory, and the output wrapper filename.
* **Portable**: The generated `run.sh` has no external dependencies other than
  `bash`, which is standard on Linux and macOS systems.

## Files in This Repository

* `create_wrapper.py`: The Python script that generates the wrapper.
* `run_template.sh.j2`: The Jinja2 template used by the generator to create the
  `run.sh` script.
* `requirements.txt`: Contains the dependencies required to run the generator
  script itself (i.e., Jinja2).
* `create_wrapper`: This tool's own wrapper, generated to run
  `create_wrapper.py`.

## Setup

To run the generator script, you need to set up its dedicated virtual environment.

1. **Clone this repository** to a permanent location on your machine (e.g., `~/tools/wrapper-generator`).

    ```bash
    git clone https://github.com/ramonpin/create-venv-wrapper ~/tools/wrapper-generator
    cd ~/tools/wrapper-generator
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv .venv
    ```

3. **Activate the virtual environment**:

    ```bash
    source .venv/bin/activate
    ```

4. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5. **(Recommended) Create a global alias**: To run the generator from anywhere,
   you should add an alias to your shell's configuration file (e.g.,
   `~/.bashrc`, `~/.zshrc`).

    First, get the absolute path to the `create_wrapper` script:

    ```bash
    # Make sure you are in the generator's directory
    pwd
    # Example output: /home/user/tools/wrapper-generator
    ```

    Next, open your shell configuration file with your favorite text editor.
    For example:

    ```bash
    nano ~/.bashrc
    ```

    Add the following line at the end of the file. Replace
    `/path/to/wrapper-generator` with the actual path you got from the `pwd`
    command:

    ```bash
    alias create_wrapper='/path/to/wrapper-generator/create_wrapper'
    ```

    Save the file and exit the editor. Finally, reload your shell configuration
    for the alias to be available in your current session:

    ```bash
    source ~/.bashrc
    ```

## How to Use the Generator

After completing the setup and creating the alias, you can easily generate
wrappers for any of your Python projects.

1. Open a terminal and navigate to the root directory of your target Python
   project.
2. Run the `create_wrapper` command.

### Command-Line Options

* `--entry-point`: The main Python script to execute. (Default: `main.py`)
* `--venv`: The path to the virtual environment directory. If not specified, it
  will be auto-detected.
* `-o, --output`: The filename for the generated wrapper script. (Default:
  `run.sh`)
* `--install-deps`: A flag to include the logic for installing dependencies
  from `requirements.txt`.

### Examples

#### Basic Usage

(Assumes your venv is auto-detectable and your entry point is `main.py`)

```bash
create_wrapper
```

#### Specifying an Entry Point and Enabling Dependency Installation

```bash
create_wrapper --entry-point app.py --install-deps
```

#### Specifying Everything: Venv, Entry Point, and Output Filename

```bash
create_wrapper --venv my_env --entry-point src/cli.py -o start.sh --install-deps
```

### Using the Generated Wrapper

Once the generator has run, you will have a new shell script in your project
(e.g., run.sh). You can use it to run your Python application as follows:

```bash
# Simply execute the project
./run.sh

# Execute the project and pass arguments to your Python script
./run.sh --user admin --action process
```
