import shutil
import os
import zipfile

def zip_directory(source_dir, output_filename):
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            if '__pycache__' in root or '.git' in root or '.idea' in root:
                continue
            for file in files:
                if file.endswith('.pyc') or file == output_filename:
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(source_dir))
                zipf.write(file_path, arcname)

if __name__ == "__main__":
    source = r'c:\Users\Administrator\Desktop\projects\kay-klois-2\school_bus_reservation\schoolbus'
    output = r'c:\Users\Administrator\Desktop\projects\kay-klois-2\school_bus_reservation\schoolbus_deploy.zip'
    print(f"Zipping {source} to {output}...")
    try:
        zip_directory(source, output)
        print("Zip created successfully.")
    except Exception as e:
        print(f"Error: {e}")
