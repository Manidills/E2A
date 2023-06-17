import w3storage
from moralis import evm_api
import base64
import requests
#from lighthouseweb3 import Lighthouse



def w3_store(File):

    w3 = w3storage.API(token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweEVjNzgyNDczRWU1RDI3NjkyYzFhNjRCMzkzMGMyOTU1QjEwQjVBOUQiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2ODY5MTY3NDQwNTQsIm5hbWUiOiJtYW5pIn0.l9nJGxycmoW9pP3EkJPEi_cJZ8THbCVjp1EV21SFCX4')

    some_uploads = w3.user_uploads(size=25)

    # limited to 100 MB
    cid = w3.post_upload(('audio.mp3',open(File, 'rb')))
    return cid
    #readme_cid = w3.post_upload(('README.md', open('README.md', 'rb')))





api_key = "7hstobdqT97qzSbNkW6Spq227cMCBXEPsKBAM7yk70Wqhiygi3uHD7snLqupcL46"

def store_on_ipfs(knn_template):

    encoded_content = base64.b64encode(knn_template).decode('utf-8')

    body = [{
        "path": f'dummy',
        "content": encoded_content,
    }]

    cid = evm_api.ipfs.upload_folder(
        api_key=api_key,
        body=body,
    )

    print(cid)
    return cid

def nft_port(file):
    file = open(file, "rb")

    response = requests.post(
        "https://api.nftport.xyz/v0/files",
        headers={"Authorization": 'f6ce3372-a928-4947-8f50-87649f60cee2'},
        files={"file": file}
    )

    return response

def lighthouse(file):
    file = open(file, "rb")
    response = requests.post(
        "https://node.lighthouse.storage/api/v0/add",
        headers={"Authorization": f"Bearer {'97cef50c.2579ee5d584d4dc69855caa30d3b582c'}"},
        files={"file": file}
    )

    return response\
    
def estuary(file):
    file = open(file, "rb")
    response = requests.post(
        "https://upload.estuary.tech/content/add",
        headers={"Authorization": f"Bearer {'ESTb4e2b39a-6435-4a5a-9a84-6f34df047ad3ARY'}"},
        files={"data": file}
    )

    return response