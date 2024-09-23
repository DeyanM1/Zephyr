# Run: python createBuild.py build

from cx_Freeze import setup, Executable
import zipfile, os


def zip_folder_with_content(folder_path, zip_name):
    # Ensure the specified folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Walk through the folder and add files and subfolders
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if not file_path.endswith(".zip"):
                    # Add file to the ZIP file, maintaining the folder structure
                    zip_file.write(file_path, arcname=os.path.relpath(file_path, os.path.dirname(folder_path)))
                    print(f"Added {file_path} to {zip_name}")

        # Add the folder itself (empty entry for the folder)
        zip_file.write(folder_path, arcname=os.path.basename(folder_path))
        print(f"Added folder '{folder_path}' to {zip_name}")



build_exe_options = {
    "zip_filename": "ZephyrC.zip",
}


setup(
    name="Zephyr",
    author="DeyanM1",
    version="0.2.0",
    url="https://github.com/DeyanM1/Zephyr/",
    description="Zephyr programming language compiler",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py")]
)

os.rename("./build/exe.win-amd64-3.11/main.exe", "./build/exe.win-amd64-3.11/zephyrC.exe")
os.rename("./build/exe.win-amd64-3.11", "./build/zephyrC-win-amd64.3.11")

folder_to_zip = './build/'  
zip_file_name = './build/zephyrC-win.and64-3.11.zip'

zip_folder_with_content(folder_to_zip, zip_file_name)