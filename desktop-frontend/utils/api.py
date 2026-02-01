import requests

BASE_URL = 'http://127.0.0.1:8000/api'

def upload_dataset(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f'{BASE_URL}/upload/', files=files)
        return response

def get_history():
    try:
        response = requests.get(f'{BASE_URL}/history/')
        response.raise_for_status()
        return response.json()
    except:
        return []

def get_analysis(id):
    try:
        response = requests.get(f'{BASE_URL}/analysis/{id}/')
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(e)
        return None

def download_report(id, save_path):
    response = requests.get(f'{BASE_URL}/report/{id}/', stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return True
    return False
