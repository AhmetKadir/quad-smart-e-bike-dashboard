from config import Config
import requests

POSITION_UPDATE_URL = "https://quadsmartapi-production.up.railway.app/v1/scooters/position"
GET_LOCKED_URL = ""
FLASH_LIGHT_URL = ""
SCOOTER_ID = "65ec5acb2e83db0012afafe1"

class Communication:
    def send_data_to_server(latitude, longitude):
        data = {
            "scooter_id": SCOOTER_ID,
            "latitude": latitude,
            "longitude": longitude,
            "api_key": Config.API_KEY
        }
        try:
            response = requests.put(POSITION_UPDATE_URL, json=data)
            if response.status_code != 204 and response.status_code != 200 and response.status_code != 201:
                print(f"Failed to upload GPS data. Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error uploading GPS data: {e}")
            
    def read_is_locked():
        try:
            # to add query parameter to the URL
            GET_LOCKED_URL = f"https://quadsmartapi-production.up.railway.app/v1/scooters/islocked/{SCOOTER_ID}?api_key={Config.API_KEY}"
            response = requests.get(GET_LOCKED_URL)
            if response.status_code != 204 and response.status_code != 200 and response.status_code != 201:
                print(f"Failed to get locked status. Status Code: {response.status_code}")
            else:
                print("islocked http response: ", response.json())
                return response.json()
        except Exception as e:
            print(f"Error getting locked status: {e}")
    
    def GET_FLASH_LIGHT():
        try:
            FLASH_LIGHT_URL = f"https://quadsmartapi-production.up.railway.app/v1/scooters/isflashlighton/{SCOOTER_ID}?api_key={Config.API_KEY}"
            response = requests.get(FLASH_LIGHT_URL)
            if response.status_code != 204 and response.status_code != 200 and response.status_code != 201:
                print(f"Failed to get flash light status. Status Code: {response.status_code}")
            else:
                print("flashLight http response: ", response.json())
                return response.json()
        except Exception as e:
            print(f"Error getting flash light status: {e}")
    
    def check_internet():
        url = "http://www.google.com"
        timeout = 5
        try:
            _ = requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            return False