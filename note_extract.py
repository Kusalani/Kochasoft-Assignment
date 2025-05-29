
import re
from llama_index.core import Document

def add_sap_notes_to_docs(docs):
    """Add SAP Note info to your documents"""
    sap_pattern = re.compile(r'SAP Note (\d+)')
    new_docs = []
    
    for doc in docs:
        sap_notes = sap_pattern.findall(doc.text)
        for note_id in sap_notes:
            sap_doc = Document(
                text=f"SAP Note {note_id}: Referenced document about SAP HANA configuration. Requires authentication to access.",
                metadata={'sap_note_id': note_id, 'type': 'sap_note'}
            )
            new_docs.append(sap_doc)
    
    return docs + new_docs