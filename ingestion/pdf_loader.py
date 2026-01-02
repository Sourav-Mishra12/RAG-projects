from pypdf import PdfReader
from logging import logger 

def load_pdf(path : str) -> list[str]:
    reader = PdfReader(path)
    pages_text = []

    for i,page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            cleaned = " ".join(text.split())
            pages_text.append(cleaned)
        else:
            logger.warning(f"No text found on page {i}")
    
    logger.info(f"loaded PDF : {path} | Pages : {len(pages_text)}")
    return pages_text