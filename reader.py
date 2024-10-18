import io

from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader

import config


class ProcessPDF:
    @staticmethod
    def fix_paragraphs(text: str) -> str:
        return (text
                .replace(".\n", ".\n\n")
                .replace("?\n", "?\n\n")
                .replace("!\n", "!\n\n"))

    @staticmethod
    def fix_whitespaces(text: str) -> str:
        return (text
                .replace(" \n", " ")
                .replace("\xa0", " "))

    @staticmethod
    def fix_hyphen_usage(text: str) -> str:
        return (text
                .replace("–", "-")
                .replace(" -\n", "")
                .replace("-\n", "-"))

    @staticmethod
    def fix_slash_usage(text: str) -> str:
        return text.replace("/\n", "/")

    @classmethod
    def read_pdf(cls, data: io.BytesIO) -> str:
        result = ""

        reader = PdfReader(data)
        for page in reader.pages:
            raw_text = page.extract_text(extraction_mode="plain")

            raw_text = cls.fix_whitespaces(text=raw_text)
            raw_text = cls.fix_paragraphs(text=raw_text)
            raw_text = cls.fix_hyphen_usage(text=raw_text)
            raw_text = cls.fix_slash_usage(text=raw_text)

            result += raw_text

        return result


class ProcessDOCX:
    @staticmethod
    def read_docx(data: io.BytesIO) -> str:
        doc = Document(data)

        result = ""
        for para in doc.paragraphs:
            result += para.text
        return result


class Reader:
    @staticmethod
    def get_extension_type(filename: str) -> str:
        return filename.split(".")[-1]

    @classmethod
    def process_file(cls, file: io.BytesIO) -> str:
        data_type = cls.get_extension_type(filename=file.name)

        if data_type in config.ALLOWED_FILE_TYPES:
            if data_type == "txt":
                return file.getvalue().decode("utf-8")
            elif data_type == "pdf":
                return ProcessPDF.read_pdf(data=io.BytesIO(file.getvalue()))
            elif data_type == "docx":
                return ProcessDOCX.read_docx(data=io.BytesIO(file.getvalue()))

        else:
            raise TypeError(f"Wrong file extension `{data_type}`. Allowed extensions: {config.ALLOWED_FILE_TYPES}")

    @staticmethod
    def get_text_chunks(text: str) -> list[str]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.TEXT_CHUNK_SIZE,
            chunk_overlap=config.TEXT_CHUNK_OVERLAP
        )
        return text_splitter.split_text(text)
