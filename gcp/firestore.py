from google.cloud import firestore

db = firestore.Client()

def doc_to_dict(doc):
    if doc.exists:
        return {'id': doc.id, **doc.to_dict()}
    return None

def docs_to_list(docs):
    return [{'id': doc.id, **doc.to_dict()} for doc in docs]

def docs_to_dict(collection, docs):
    return {collection: docs_to_list(docs)}

