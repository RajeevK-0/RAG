from typing import List , Any
from langchain_community.document_loaders import PyPDFLoader,PyMuPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain_community.document_loaders import JSONLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import CSVLoader
from pathlib import Path

def load_document(dir_path:str)->List[Any]:
    """
    loads all kind of files (txt,pdf,csv,json,excel) into langchain supported document structure
    """
    dir_path = Path(dir_path).resolve()
    all_doc = []
    #getting pdf files
    pdf_files = list(dir_path.rglob('*.pdf'))
    for file in pdf_files:
        try:
            loader = PyMuPDFLoader(str(file))
            loaded = loader.load()
            print(f"loaded pdf file of length : {len(loaded)} from file: {file} ")
            all_doc.extend(loaded)
        except Exception as e:
            print(f"error while loading pdf file : {e}")

    #getting txt file
    txt_files = list(dir_path.rglob('*.txt'))
    for file in txt_files:
        try:
            loader = TextLoader(str(file))
            loaded = loader.load()
            print(f"loaded pdf file of length : {len(loaded)} from file: {file} ")
            all_doc.extend(loaded)
        except Exception as e:
            print(f"error while loading txt file : {e}")
    
    #getting csv file
    csv_files = list(dir_path.rglob('*.csv'))
    for file in csv_files:
        try:
            loader = CSVLoader(str(file),encoding='utf-8')
            loaded = loader.load()
            print(f"loaded pdf file of length : {len(loaded)} from file: {file} ")
            all_doc.extend(loaded)
        except Exception as e:
            print(f"error while loading csv file : {e}")

    #getting excel files
    
    excel_files = list(dir_path.rglob('*.xlsx'))
    for file in excel_files:
        try:
            loader = UnstructuredExcelLoader(str(file))
            loaded = loader.load()
            print(f"loaded pdf file of length : {len(loaded)} from file: {file} ")
            all_doc.extend(loaded)
        except Exception as e:
            print(f"error while loading excel file : {e}")
    
    #getting word file

    word_files = list(dir_path.rglob('*.docx'))
    for file in word_files:
        try:
            loader = Docx2txtLoader(str(file))
            loaded = loader.load()
            print(f"loaded pdf file of length : {len(loaded)} from file: {file} ")
            all_doc.extend(loaded)
        except Exception as e:
            print(f"error while loading word file : {e}")
    
    #loading json file
    json_files = list(dir_path.rglob('*.json'))
    for file in json_files:
        try:
            loader = JSONLoader(str(file))
            loaded = loader.load()
            print(f"loaded pdf file of length : {len(loaded)} from file: {file} ")
            all_doc.extend(loaded)
        except Exception as e:
            print(f"error while loading json file : {e}")
    
    return all_doc

if __name__ == "__main__":
    docs = load_document("data")
    print()
    print(f"loaded : {len(docs)} documents")
    print()
    print(f"example doc :{docs[0] if docs else None}" )