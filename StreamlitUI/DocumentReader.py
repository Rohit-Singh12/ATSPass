import PyPDF2
import docx
import os

class DocumentReader:
    def __init__(self, filename):
        self.filename = filename
        self.extension = os.path.splitext(filename)[1].lower()
        self.text = self.read_document()

    def read_document(self):
        print("File extension: " + self.filename + " "+ self.extension)
        if self.extension == '.pdf':
            return self.read_pdf()
        elif self.extension == '.txt':
            return self.read_txt()
        elif self.extension == '.docx':
            return self.read_docx()
        elif self.extension == '.doc':
            return self.read_doc()
        else:
            return "Unsupported file type."

    def read_pdf(self):
        text = ""
        try:
            with open(self.filename, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text() or ""
            return text
        except FileNotFoundError:
            return "File not found."
        except Exception as e:
            return f"An error occurred: {e}"

    def read_txt(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return "File not found."
        except Exception as e:
            return f"An error occurred: {e}"

    def read_docx(self):
        text = ""
        try:
            doc = docx.Document(self.filename)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except FileNotFoundError:
            return "File not found."
        except Exception as e:
            return f"An error occurred: {e}"