import urllib.request
import datetime
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
import pprint
from imageai.Detection.Custom import CustomObjectDetection

def detection(inp):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'eminent-maker-315608-496b6cc217f7.json'
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    pp = pprint.PrettyPrinter(indent=4)
    download = 'https://drive.google.com/u/0/uc?id=' + str(inp.split('/d/')[1].split('/view')[0]) + '&export=download'
    logo = urllib.request.urlopen(download).read()
    name_input = str(datetime.datetime.now()) + ".jpg"
    f = open(name_input, "wb")
    f.write(logo)
    f.close()
    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath("detection_model-ex-046--loss-0017.722.h5")
    detector.setJsonPath("detection_config.json")
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=name_input, output_image_path="det-"+name_input)
    folder_id = '1uUyRBDJ5-FsuCBIx5p8Ndi9W0-Z6JiU3'
    name = "det-" + name_input
    file_path = name
    file_metadata = {
                'name': name,
                'parents': [folder_id]
            }
    media = MediaFileUpload(file_path, resumable=True)
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    result = 'https://drive.google.com/file/d/' + r['id'] + '/view'
    return result
