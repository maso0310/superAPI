#google drive api
from __future__ import print_function
import httplib2
import os
import io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload

#google drive的相關文件位置
#如果要修改這些範圍，請刪除以前保存的憑據
#at~ / .credentials / drive-python-quickstart.json

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

#google drive獲得認證函數

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join('.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'drive-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def google_drive():#查看檔案
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
    #檔案上傳
    file_metadata = {
        'name' : dist_name,
        'mimeType' : 'image/jpeg'
    }
    media = MediaFileUpload(path,mimetype='img/jpeg',resumable=True)
    file = service.files().create(body=file_metadata,media_body=media,fields='id').execute()
    file_id = file.get('id')
    print(file_id)
    print ('File ID: %s' % file.get('id'))

def downloadFile(credentials,file_id):

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    #下載檔案至根目錄
    #file_id = '1ltXFMCEpGwgMyevrepGTch95VH9Wx1if'
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_id+'.jpg','wb')
    downloader = MediaIoBaseDownload(fh, request)
    print(downloader)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))