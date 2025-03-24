from datetime import datetime
import requests

def upload_to_yadisk(file_path: str, name_file: str, oauth_token: str):
    today = datetime.now().strftime("%Y-%m-%d")
    url_for_upload = requests.get("https://cloud-api.yandex.net/v1/disk/resources/upload", 
                                  headers={"Authorization": oauth_token},
                                  params={"path": f"{name_file}_{today}.sql", "overwrite": "true"}).json()
    print(url_for_upload)
    if 'href' in url_for_upload:
        with open(file_path, "rb") as file:
            response = requests.put(url_for_upload['href'], data=file)
            print(response.text)
            if response.status_code == 200:

                return True, "success"
            else:
                return False, f"response error {response.text}"
            
    else:
        return False, f"Error getting upload url: {url_for_upload}"
