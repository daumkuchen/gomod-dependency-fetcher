import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_license(repository_url, repository_type):
    try:
        if repository_url == '-':
            return '-', '-'
        
        parts = repository_url.rstrip('/').split('/')
        repo_owner = parts[-2]
        repo_name = parts[-1]

        # githubのみ対応
        if repository_type == 'github':
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
            headers = {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                license_info = data.get("license")
                if license_info:
                    url = license_info.get("url")
                    info = license_info.get("spdx_id")
                    return url, info
            elif response.status_code == 403 or response.status_code == 404:
                return 'ERROR', 'ERROR'
            return '-', '-'

        return '-', '-' 

    except requests.exceptions.RequestException:
        return '-', '-'