import os
import sys
import subprocess
import venv

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(error.decode())
        sys.exit(1)
    return output.decode()

def create_venv():
    venv_dir = os.path.join(os.getcwd(), "venv")
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)
    return venv_dir

def get_venv_python(venv_dir):
    if sys.platform == "win32":
        python_path = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        python_path = os.path.join(venv_dir, "bin", "python")
    return python_path

def install_dependencies(python_path):
    print("Installing dependencies...")
    run_command(f'"{python_path}" -m pip install -e .')

def run_ocr_script(python_path):
    print("Running OCR script...")
    run_command(f'"{python_path}" scan.py')

def main():
    venv_dir = create_venv()
    python_path = get_venv_python(venv_dir)
    install_dependencies(python_path)
    run_ocr_script(python_path)
    print("OCR process completed.")

if __name__ == "__main__":
    main()