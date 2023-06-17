import base64
import io
import os
from urllib import request
import PyPDF2
import tempfile
from PIL import Image
from app_web import ask
from db import create_table, insert_wallet
import streamlit as st
from PIL import Image
from gtts import gTTS
from poppler import load_from_data, PageRenderer
from pdf2image import convert_from_bytes
from resume.resume import run
from wallet_connect import wallet_connect
from ipfs import estuary, lighthouse, nft_port, store_on_ipfs, w3_store
from pydub import AudioSegment
import requests
from nft_store import *


st.set_page_config(
    page_title="DCR Setup Assistant",
    page_icon="❄️️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "This app generates scripts for data clean rooms!"
    }
)


create_table()
st.sidebar.image("bear_snowflake_hello.png")
action = st.sidebar.radio("What action would you like to take?", ("Eaudio Maker", "Eanswer Maker", "E-Analyzer", "Check My Files"))

def wallet_con():
    with st.sidebar:
        st.markdown('##')
        wallet = wallet_connect(label="wallet", key='wallet')
        return wallet
    

wallet = wallet_con()



def convert(pdf_document, start, end):
    try:
        text = ''
        for x in range(start - 1, end):
            page_current = pdf_document.create_page(x)
            text += page_current.text()
        # initialize tts, create mp3 and play
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang='en', slow=False, lang_check=False, tld='co.in')
        tts.write_to_fp(mp3_fp)
        return mp3_fp
    except AssertionError:
        st.error('The PDF does not seem to have text and maybe its a scanned')




if action == "Eaudio Maker":
    st.title('Eaudio Maker')
    st.header(
        "[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E226KBO)&nbsp;[![GitHub release ("
        "latest by date)](https://img.shields.io/github/v/release/deadmantfa/audiobookmaker?style=for-the-badge)]")
    # st.header('Preview Uploaded PDF')
    st.warning('Before switching pages be sure to download any converted pages or you will need to reconvert')
    with st.form("my_form"):
        uploaded_file = st.file_uploader("Upload a PDF", type=['pdf'])
        start_page = st.number_input("Start Page", 1)
        end_page = st.number_input("End Page", 1)

        genre = st.radio(
        "Push the file to IPFS via",
        ("NOT",'Web3_Storage', 'NFT_Storage', 'Moralis/Pinata', 'NFTPORT', 'LightHouse', 'Estuary'),horizontal=True)

        st.info('Conversion takes time, so please be patient')
        convert_to_audio = st.form_submit_button("Convert")
    if uploaded_file is not None:
        pdf_document = load_from_data(uploaded_file.read())
    if start_page > end_page:
        st.error('Start Page cannot be greater than end page')
    elif start_page <= end_page:
        if convert_to_audio and uploaded_file is not None:
            audio_file = convert(pdf_document, start_page, end_page)
            st.audio(audio_file, format='audio/mp3')
            with tempfile.NamedTemporaryFile(suffix=".mp3",delete=False) as temp:
                    temp.write(audio_file.getvalue())
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
            
            if wallet != None:
                insert_wallet(new_url,str(wallet))
                st.success("Pushed to DB")

 

elif action == "Eanswer Maker":
    ask(wallet)

elif action == "E-Analyzer":
    run()
elif action == "Check My Files":
    import sqlite3

    conn = sqlite3.connect('wallets.db')
    cursor = conn.cursor()

    st.info(wallet)

    cursor.execute('SELECT ipfs_url FROM wallets where name = ?', (wallet,))
    results = cursor.fetchall()

    st.write(results)



