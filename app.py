import os
import shutil
import re


categories = {
    "Images": [".jpg", ".png", ".jpeg"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".mkv"],
    "Code": [".py", ".c", ".cpp", ".java"],
    "Audio": [".mp3", ".wav"]
}

base_folder = "organized_files"


def get_category(filename):
    ext = os.path.splitext(filename)[1].lower()
    for folder, exts in categories.items():
        if ext in exts:
            return folder
    return "Others"


def clean_name(filename):
    name, ext = os.path.splitext(filename)
    name = name.lower().replace(" ", "_")
    name = re.sub(r"[^a-z0-9_]", "", name)
    return name + ext.lower()


def organize(files):
    if not files:
        return "No files uploaded", None

    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    result = []
    count = 0

    for file in files:
        original = os.path.basename(file.name)
        new_name = clean_name(original)

        category = get_category(original)
        folder_path = os.path.join(base_folder, category)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        dest = os.path.join(folder_path, new_name)

        i = 1
        while os.path.exists(dest):
            name, ext = os.path.splitext(new_name)
            dest = os.path.join(folder_path, f"{name}_{i}{ext}")
            i += 1

        shutil.copy(file.name, dest)

        result.append(f"{original} → {category}")
        count += 1

    zip_file = shutil.make_archive("organized_files", "zip", base_folder)

    summary = f"Total files processed: {count}\n\n"
    summary += "\n".join(result)

    return summary, zip_file


with gr.Blocks() as demo:
    gr.Markdown("# Smart File Organizer Agent")

    files = gr.File(file_count="multiple", label="Upload your files")
    btn = gr.Button("Organize Files")

    output = gr.Textbox(label="Result", lines=15)
    download = gr.File(label="Download ZIP")

    btn.click(fn=organize, inputs=files, outputs=[output, download])

demo.launch()