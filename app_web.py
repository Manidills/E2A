import tempfile
import os
from db import insert_wallet
from extract_text import extract_text_from_pdf
from call2llm import get_response, get_continued_response
from ipfs import estuary, lighthouse, nft_port, store_on_ipfs, w3_store
from nft_store import nft_storage_store  # Import specific functions instead of importing everything from call2llm
import streamlit as st
from wallet_connect import wallet_connect
# from streamlit_app import wallet_con


def ask(wallet):
    st.title("Eanswer Maker")
    with st.form("my_form"):
        uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type=["pdf"])
        genre = st.radio(
        "Push the file to IPFS via",
        ("NOT",'Web3_Storage', 'NFT_Storage', 'Moralis/Pinata', 'NFTPORT', 'LightHouse', 'Estuary'),horizontal=True)

        
        pdf_files = []

        # Process uploaded PDFs
        if uploaded_files:
            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(uploaded_file.read())
                    temp_file_path = temp_file.name

                pdf_files.append((uploaded_file.name, temp_file_path))
            
            # Two-column layout for start and end pages
            col1, col2 = st.columns(2)

            # Convert PDFs to text
            converted_texts = []
            for i, (file_name, file_path) in enumerate(pdf_files):
                # Input fields for start and end pages
                with col1:
                    start_page = st.number_input(f"Start Page ({file_name})", min_value=1, value=1, key=f"start_page_{i}")
                with col2:
                    end_page = st.number_input(f"End Page ({file_name})", min_value=start_page, value=start_page, key=f"end_page_{i}")

                # Convert PDF to text
                text = extract_text_from_pdf(file_path, start_page, end_page)
                converted_texts.append(text)

        query = st.text_input("Enter your question")
        ask_pdf = st.form_submit_button("Ask")

        if ask_pdf :
            response_placeholder = st.empty()
            print("calling llm")
            combined_text = "\n".join(converted_texts)
            response = ""

            response = get_response(combined_text + query, response_placeholder)
        
            with tempfile.NamedTemporaryFile(suffix=".txt",delete=False) as temp:
                        with open(temp.name, 'w') as temp:
                            temp.write(response) 
            if genre == 'NOT':
                pass
            elif genre == 'Web3_Storage':
                cid = w3_store(temp.name)
                web3_storage = f'https://{cid}.ipfs.w3s.link/'
                new_url = web3_storage
                st.info(f"Can download/view data from {new_url}")
            elif genre == 'NFT_Storage':
                store_nft = nft_storage_store(temp.name)
                audio_cid = store_nft['value']['cid']
                new_url = f'https://{audio_cid}.ipfs.nftstorage.link'
                st.write(f'Can download/view data from {new_url}')
            elif genre == 'Moralis/Pinata':
                store_date = store_on_ipfs(temp.name)
                ipfs_gateway = 'https://ipfs.moralis.io'

                # Concatenate the IPFS gateway URL with the CID
                new_url = f"https://ipfs.moralis.io/ipfs/{store_date}"
                st.write(f'Can download/view data from {new_url}')
            elif genre == 'NFTPORT':
                store_data = nft_port(temp.name)
                new_url = store_data.json()['ipfs_url']
                st.write(f'Can download/view data from {new_url}')
            elif genre == "LightHouse":
                store_data = lighthouse(temp.name)
                url = store_data.json()['Hash']
                new_url = f'https://gateway.lighthouse.storage/ipfs/{url}'
                st.write(f'Can download/view data from {new_url}')
            elif genre == "Estuary":
                store_data = estuary(temp.name)
                url = store_data.json()['cid']
                new_url = f'https://api.estuary.tech/gw/ipfs/{url}'
                st.write(f'Can download/view data from {new_url}')

                # Delete temporary files
            for _, file_path in pdf_files:
                os.remove(file_path)

            if wallet != None:
                insert_wallet(new_url,str(wallet))
                st.success("Pushed to DB")

 


