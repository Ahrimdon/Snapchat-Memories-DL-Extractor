import os
import subprocess
import venv

def create_venv():
    venv.create('venv', with_pip=True)
    # Create activation scripts
    with open("venv.ps1", "w") as f:
        f.write("venv\\Scripts\\Activate.ps1")

    with open("venv.bat", "w") as f:
        f.write("venv\\Scripts\\activate")

def install_pip():
    subprocess.check_call([os.path.join('venv', 'Scripts', 'python'), '-m', 'pip', 'install', '--no-index', '--find-links=requirements', 'pip==23.3.1'])

def install_wheel_in_venv():
    subprocess.check_call([os.path.join('venv', 'Scripts', 'pip'), 'install', '--no-index', '--find-links=requirements', 'wheel'])

def install_requirements_in_venv():
    subprocess.check_call([os.path.join('venv', 'Scripts', 'pip'), 'install', '--no-index', '--find-links=requirements', '-r', 'requirements.txt'])

if __name__ == "__main__":
    print("Creating virtual environment...")
    create_venv()
    print("Upgrading pip...")
    install_pip()
    print("Installing wheel in the virtual environment...")
    install_wheel_in_venv()
    print("Installing packages in the virtual environment...")
    install_requirements_in_venv()