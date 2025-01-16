import streamlit as st
from llama_index.core import SimpleDirectoryReader, GPTVectorStoreIndex, StorageContext, load_index_from_storage
import os

# Définir le chemin pour stocker l'index
INDEX_STORAGE_PATH = 'index_v1'

# Fonction pour charger ou créer un index
def get_index():
    if os.path.exists(INDEX_STORAGE_PATH):
        st.write("Chargement de l'index existant...")
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORAGE_PATH)
        return load_index_from_storage(storage_context)
    else:
        st.write("Création d'un nouvel index...")
        documents = SimpleDirectoryReader('textes_philosophiques').load_data()
        index = GPTVectorStoreIndex.from_documents(documents)
        index.storage_context.persist(INDEX_STORAGE_PATH)
        return index

# Chargement ou création automatique de l'index
index = get_index()

# Interface utilisateur Streamlit
st.title("Recherche dans les textes philosophiques")

# Zone de texte pour saisir une requête
query = st.text_input("Saisissez votre question :", "Dois-je agir avec honneur ?")

# Traitement de la requête si l'utilisateur clique sur le bouton
if st.button("Lancer la requête"):
    st.write("Traitement de la requête...")
    query_engine = index.as_query_engine()
    response = query_engine.query(query)

    # Afficher la réponse principale
    st.write("### Réponse :")
    st.write(response.response)

    # Afficher les sources
    st.write("### Sources :")
    for source in response.source_nodes:
        st.write(f"- Dans {source.metadata['file_name']} à la page {source.metadata['page_label']} :\n\n {source.text}\n")
