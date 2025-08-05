# create_wrapper.py
# This script generates a smart 'run.sh' wrapper for a Python project.
# It uses the Jinja2 templating engine to create the shell script.

import os
import stat
import argparse
from pathlib import Path
from jinja2 import Template

# --- Constants ---
DEFAULT_ENTRY_POINT = "main.py"
DEFAULT_WRAPPER_NAME = "run.sh"
REQUIREMENTS_FILE = "requirements.txt"
TEMPLATE_FILE_NAME = "run_template.sh.j2"

def find_venv_path(project_path: Path) -> Path | None:
    """
    Searches for a virtual environment directory within the project path.
    It identifies a venv by the presence of a 'bin/python' executable.
    """
    print(f"Searching for a virtual environment in '{project_path}'...")
    for item in project_path.iterdir():
        if item.is_dir():
            python_executable = item / "bin" / "python"
            if python_executable.exists() and python_executable.is_file():
                print(f"Found virtual environment: '{item.name}'")
                return item
    return None

def generate_shell_script(config: dict) -> str:
    """
    Generates the content of the 'run.sh' wrapper script using a Jinja2 template.
    """
    # The template file is expected to be in the same directory as this script.
    script_dir = Path(__file__).parent
    template_path = script_dir / TEMPLATE_FILE_NAME

    try:
        template_content = template_path.read_text()
        template = Template(template_content)
    except FileNotFoundError:
        # Raise the exception to be handled in main()
        raise FileNotFoundError(
            f"Template file '{TEMPLATE_FILE_NAME}' not found in '{script_dir}'."
        )
    
    # Prepare context for the template
    venv_path = config['venv_path']
    project_path = config['project_path']
    entry_point = config['entry_point']
    
    context = {
        'venv_python_rel': Path(venv_path.name) / "bin" / "python",
        'main_script_rel': entry_point.relative_to(project_path),
        'install_deps': config['install_deps'],
        'requirements_file': REQUIREMENTS_FILE,
        'flag_file_rel': Path(venv_path.name) / ".deps_installed"
    }
    
    return template.render(context)


def main():
    """
    Main function to parse arguments and drive the wrapper creation process.
    """
    parser = argparse.ArgumentParser(
        description="Generate a smart 'run.sh' wrapper for a Python project.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--entry-point",
        type=str,
        default=DEFAULT_ENTRY_POINT,
        help="The main Python script to execute."
    )
    parser.add_argument(
        "--venv",
        type=str,
        help="Path to the virtual environment directory. If not provided, searches automatically."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=DEFAULT_WRAPPER_NAME,
        help="The name of the generated wrapper file."
    )
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help=f"Include logic to install dependencies from '{REQUIREMENTS_FILE}'."
    )
    
    args = parser.parse_args()
    
    print("--- Python Project Wrapper Generator ---")
    
    project_path = Path.cwd()

    # --- Configuration Steps ---
    if args.venv:
        venv_path = project_path / args.venv
        if not (venv_path.is_dir() and (venv_path / "bin" / "python").is_file()):
            print(f"\nERROR: Provided venv path '{venv_path}' is not a valid virtual environment.")
            return
        print(f"Using provided virtual environment: '{args.venv}'")
    else:
        venv_path = find_venv_path(project_path)
        if not venv_path:
            print("\nERROR: Could not find a virtual environment.")
            print("Please create one (e.g., 'python -m venv venv') or specify it with --venv.")
            return

    entry_point_path = project_path / args.entry_point
    if not entry_point_path.is_file():
        print(f"\nERROR: Entry point script not found at '{entry_point_path}'.")
        return
    print(f"Using entry point: '{args.entry_point}'")

    # --- Generate and Write Script ---
    config = {
        'project_path': project_path,
        'venv_path': venv_path,
        'entry_point': entry_point_path,
        'install_deps': args.install_deps,
    }

    try:
        print(f"\nGenerating '{args.output}' wrapper...")
        script_content = generate_shell_script(config)
        wrapper_path = project_path / args.output
        
        wrapper_path.write_text(script_content)
        # Make the script executable for the user
        wrapper_path.chmod(wrapper_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        
        print(f"\nSUCCESS: '{args.output}' created at '{wrapper_path}'")
        print(f"You can now run your project using: ./{args.output}")

    except FileNotFoundError as e:
        print(f"\nERROR: Could not generate script. Reason: {e}")
    except IOError as e:
        print(f"\nERROR: Could not write to '{wrapper_path}'. Reason: {e}")


if __name__ == "__main__":
    main()
