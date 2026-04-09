import streamlit as st
import os
import shutil
import re
import zipfile

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


def organize(uploaded_files):
    if not uploaded_files:
        return "No files uploaded", None

    if os.path.exists(base_folder):
        shutil.rmtree(base_folder)
    os.makedirs(base_folder)

    result = []
    count = 0

    for file in uploaded_files:
        original = file.name
        new_name = clean_name(original)

        category = get_category(original)
        folder_path = os.path.join(base_folder, category)

        os.makedirs(folder_path, exist_ok=True)

        dest = os.path.join(folder_path, new_name)

        i = 1
        while os.path.exists(dest):
            name, ext = os.path.splitext(new_name)
            dest = os.path.join(folder_path, f"{name}_{i}{ext}")
            i += 1

        with open(dest, "wb") as f:
            f.write(file.getbuffer())

        result.append(f"{original} → {category}")
        count += 1

    zip_path = "organized_files.zip"
    shutil.make_archive("organized_files", "zip", base_folder)

    summary = f"Total files processed: {count}\n\n"
    summary += "\n".join(result)

    return summary, zip_path


# 🎨 UI
st.title("📂 Smart File Organizer Agent")

uploaded_files = st.file_uploader("Upload your files", accept_multiple_files=True)

if st.button("Organize Files"):
    summary, zip_file = organize(uploaded_files)

    st.text(summary)

    if zip_file:
        with open(zip_file, "rb") as f:
            st.download_button(
                label="Download ZIP",
                data=f,
                file_name="organized_files.zip"
            )