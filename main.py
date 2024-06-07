from bs4 import BeautifulSoup, Tag
import concurrent.futures
import json
import requests
from typing import List, Optional, Dict

user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
headers: Dict[str, str] = {'User-Agent': user_agent}
not_taken: List[str] = []

def check_username(username: str) -> None:
    try:
        response: requests.Response = requests.get(f"https://www.tiktok.com/@{username}", headers=headers)
        response.raise_for_status() # Haults execution on current thread if an HTTPError occurs

        soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')

        # Finds the script tag that contains the status code we are looking for
        script_tag: Optional[Tag] = soup.find('script', {'id': '__UNIVERSAL_DATA_FOR_REHYDRATION__'})

        if script_tag and script_tag.string:
            json_data: Dict = json.loads(script_tag.string) # Extract and parse the JSON data

            # Accesses the nested JSON data inside __DEFAULT_SCOPE__
            default_scope_data: Dict = json_data["__DEFAULT_SCOPE__"]

            # Accesses the webapp.user-detail nested JSON data
            user_detail: Dict = default_scope_data["webapp.user-detail"]

            status_code: Optional[int] = user_detail.get("statusCode")

            if status_code is None:
                print(f"There was an error handling your request for: @{username}")
            elif status_code == 0:
                print(f"Username @{username} is taken")
            elif status_code == 10221:
                print(f"Username @{username} is potentially available.")
                not_taken.append(username)
        else:
            print(f"Incorrect response received, unable to check: @{username}")

    except Exception as e:
        print(f"There was an error handling your request for: @{username}, error: {e}")

def read_usernames_from_file(file_path: str) -> List[str]:
    with open(file_path, "r") as f:
        return [username.strip() for username in f.readlines()]

def write_available_usernames(file_path: str, usernames: List[str]) -> None:
    with open(file_path, "a") as f:
        for username in usernames:
            f.write(username + "\n")

if __name__ == "__main__":
    usernames: List[str] = read_usernames_from_file("usernames.txt")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_username, usernames)

    write_available_usernames("available.txt", not_taken)
