 # Logic for reading and analyzing text files


def load_text(file_path):
    if file_path.suffix == ".txt":
        return load_txt(file_path)
    elif file_path.suffix == ".docx":
        return load_docx(file_path)
    elif file_path.suffix == ".pdf":
        return load_pdf(file_path)
    else:
        raise ValueError("Unsupported file type.")

def load_txt(file_path):
    pass

def load_docx(file_path):
    pass

def load_pdf(file_path):
    pass

def split_text():
    pass

def words_analyze():
    pass