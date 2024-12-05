import requests
from bs4 import BeautifulSoup


def get_repository_url(module_url):
    try:
        response = requests.get(module_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        unit_meta_repo_div = soup.find('div', class_='UnitMeta-repo')

        github_link = unit_meta_repo_div.find('a', href=lambda href: href and 'github.com' in href)
        if github_link:
            return github_link.get('href'), "github"
        
        gitlab_link = unit_meta_repo_div.find('a', href=lambda href: href and 'gitlab.com' in href)
        if gitlab_link:
            return gitlab_link.get('href'), "gitlab"

        opensource_google_link = unit_meta_repo_div.find('a', href=lambda href: href and 'cs.opensource.google' in href)
        if opensource_google_link:
            return opensource_google_link.get('href'), "opensource_google"
        
        googlesource_link = unit_meta_repo_div.find('a', href=lambda href: href and 'go.googlesource.com' in href)
        if googlesource_link:
            return googlesource_link.get('href'), "googlesource"
        
        return "-", "-"
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repository URL from {module_url}: {e}")
        return "-", "-"
    

def get_license_url_and_info(module_url):
    try:
        response = requests.get(module_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        result = soup.find("span", {
            "class": "go-Main-headerDetailItem",
            "data-test-id": "UnitHeader-licenses"
        })

        if result:
            a_tag = result.find("a")
            if a_tag:
                url = f"https://pkg.go.dev{a_tag['href']}"
                info = a_tag.text
                return url, info

        return "-", "-"
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repository URL from {module_url}: {e}")
        return "-", "-"