import requests
from tqdm import tqdm
import re
import sys
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def extract_headers(disposition, header):
    return re.findall(f"{header}=(.+)", disposition)[0].split(';')[0]


def download_file(url):
    #Create request as a retriable session
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1, allowed_methods=None))
    session.mount('http://', adapter)
    
    while(1):
        try:
            print("\nConnecting to the server...\n")
            response = session.get(url, stream=True, timeout=1)
            
            #Check the response status code
            response.raise_for_status()

            # Extract the disposition headers from the response
            disposition = response.headers.get("Content-Disposition")
            filename = extract_headers(disposition, "filename")
            file_size = int(extract_headers(disposition, "filesize"))
        
            print('\nConnection established')
            #Start downloading the file
            print('\nStart downloading data...')
            with open(filename, "wb") as f, tqdm(
                        total = file_size, 
                        unit = 'B', 
                        unit_scale = True, 
                        unit_divisor = 1024, 
                        dynamic_ncols = True,
                        colour = 'green',
                        file = sys.stderr,
                        ) as bar:
                for chunk in response.iter_content(chunk_size=(1024*1024)):
                    if chunk:
                        size = f.write(chunk)
                        bar.update(size)
            print("\nFile successfully downloaded!\n")
            return filename
        
        except requests.exceptions.ConnectionError as e:
            print("\nError: Connection with the server was not established\n")
            break
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error code: {response.status_code}")
            break
        except requests.exceptions.ChunkedEncodingError as e:
            print("\nError: Connection was aborted while downloading data\n")
            answer = input('Do you want to try downloading again? (y/n): ')
            if answer == 'y':
                continue
            else:
                print("\nFile was not downloaded\n")
                break
    
if __name__ == "__main__":
    download_file("http://localhost:8000/getvideofile")

