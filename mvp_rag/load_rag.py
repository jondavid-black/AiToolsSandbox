import os
import shutil
import time
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import LlamaCppEmbeddings

def clean_up_vectorstores():
    if os.path.exists("./aac_vectorstore"):
        shutil.rmtree("./aac_vectorstore")
    if os.path.exists("./sysml_vectorstore"):
        shutil.rmtree("./sysml_vectorstore")

def load_aac():
    # AaC documentation
    print("Loading AaC documentation...")
    start = time.time()
    aac_doc_path = "./docs_aac"
    md_loaders = []
    for root, dirs, files in os.walk(aac_doc_path):
        for file in files:
            if file.endswith('.md'):
                print(os.path.join(root, file))
                md_loaders.append(UnstructuredMarkdownLoader(os.path.join(root, file)))

    aac_loader = MergedDataLoader(md_loaders)
    aac_data = aac_loader.load()

    aac_vectorstore = FAISS.from_documents(aac_data, embedding_model)
    aac_vectorstore.save_local("aac_vectorstore")
    end = time.time()
    return end-start

def load_sysml():
    # SysML v2 documentation
    print("Loading SysML v2 documentation...")
    start = time.time()
    sysmlv2_doc_path = "./docs_sysml2"
    sysml_loader = PyPDFDirectoryLoader(sysmlv2_doc_path)
    sysml_docs = sysml_loader.load()
    print(f"Loaded {len(sysml_docs)} documents")
    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=50
                    )
    
    # Splitting the documents into chunks and embedding into the vectorstore
    sysml_chunks = text_splitter.split_documents(documents=sysml_docs)
    print(f"Split into {len(sysml_chunks)} chunks")
    sysml_vectorstore = FAISS.from_documents(documents=sysml_chunks, embedding=embedding_model)
    sysml_vectorstore.save_local("sysml_vectorstore")
    end = time.time()
    return end-start

if __name__ == "__main__":
  
    embedding_model = LlamaCppEmbeddings(model_path="./model/mistral-7b-openorca.Q5_K_M.gguf")
    
    # TODO - remove vectorstore saves if they exist
    clean_up_vectorstores()
    aac_time = load_aac()
    sysml_time = load_sysml()
    print("Done")
    print(f"AaC load time: {aac_time:.2f}s")
    print(f"SysML load time: {sysml_time:.2f}s")
    print("Vectorstores saved to disk")
    print(f"Total time: {aac_time + sysml_time:.2f}s")