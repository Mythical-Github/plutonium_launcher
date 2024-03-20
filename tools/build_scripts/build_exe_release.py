import os
import sys
import shutil
import pathlib
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
os.chdir("../..")
cwd = os.getcwd()
output_dir = f"{cwd}/tools/build_scripts/output"
destination_path = f"{output_dir}/plutonium_launcher"
main_py = f"{cwd}/main.pyw"
built_exe = f"{destination_path}/plutonium_launcher.exe"

def cleanup_before_build():
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

def copy_files_to_build():
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    if not os.path.isdir(destination_path):
        os.mkdir(destination_path)
    before_settings_json = f"{cwd}/settings.json"
    after_settings_json = f"{destination_path}/settings.json"
    shutil.copy(before_settings_json, after_settings_json)

def build_exe():
    subprocess.run(f"pyinstaller --onefile --distpath {destination_path} {main_py}")

def make_release():
    before_exe = f"{destination_path}/main.exe"
    shutil.move(before_exe, built_exe)
    shutil.make_archive(destination_path, "zip", destination_path)

def cleanup_after_build():
    dir_to_cleanup = f"{cwd}/build"
    if os.path.isdir(dir_to_cleanup):
        shutil.rmtree(dir_to_cleanup)
    file_to_cleanup = f"{cwd}/main.spec"
    if os.path.isfile(file_to_cleanup):
        pathlib.Path.unlink(file_to_cleanup)

def run_exe():
    subprocess.Popen(built_exe)

def main():
    cleanup_before_build()
    copy_files_to_build()
    build_exe()
    make_release()
    cleanup_after_build()
    run_exe()
    sys.exit()

if __name__ == "__main__":
    main()