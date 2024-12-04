import requests

branches = [
    "main",
    "master",
    "trunk",
    "v1",
    "v2",
    "5.0",
]

license_files = [
    [
        "LICENSE",
        "LICENSE.md",
        "LICENSE.txt",
    ],
    [
        "License",
        "License.md",
        "License.txt",
    ],
    [
        "LICENSE-APACHE-2.0",
        "LICENSE-APACHE-2.0.md",
        "LICENSE-APACHE-2.0.txt",
    ],
    [
        "COPYING",
        "COPYING.md",
        "COPYING.txt",
    ],
    [
        "Copying",
        "Copying.md",
        "Copying.txt",
    ],
    [
        "UNLICENSE",
        "UNLICENSE.md",
        "UNLICENSE.txt",
    ],
    [
        "Unlicense",
        "Unlicense.md",
        "Unlicense.txt",
    ],
]

license_categories = [
    # Apache 2.0
    {"txt":'apache license', "name": 'Apache 2.0'},
    
    # BSD
    {"txt":'redistribution and use in source and binary forms, with or without', "name": 'BSD'},

    # MIT
    {"txt":'mit license',                                   "name": 'MIT'},
    {"txt":'permission is hereby granted, free of charge,', "name": 'MIT'},
    
    # ISC
    {"txt":'isc license', "name": 'ISC'},

    # MPL
    {"txt":'mozilla public license', "name": 'MPL'},

    # LGPLv3
    {"txt":'this software is licensed under the lgplv3', "name": 'LGPLv3'},

    # GPL
    {"txt":'gnu general public license', "name": 'GPL'},

    # CC
    {"txt":'creative commons', "name": 'Creative Commons'},
]

def get_license_url(repository_url, repository_type):
    try:
        if repository_url == '-':
            return '-'

        parts = repository_url.rstrip('/').split('/')
        repo_owner = parts[-2]
        repo_name = parts[-1]

        # MEMO: パフォーマンス最適化したい
        if repository_type == 'github':
            base = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/refs/heads"
            for branch in branches:
                for license_file in license_files:
                    for file in license_file:
                        license_url = f"{base}/{branch}/{file}"
                        if requests.get(license_url).status_code == 200:
                            return license_url
            return '-'
        elif repository_type == 'gitlab':
            base = f"https://gitlab.com/{repo_owner}/{repo_name}/-/raw"
            for branch in branches:
                license_url = f"{base}/{branch}/LICENSE?ref_type=heads"
                if requests.get(license_url).status_code == 200:
                    return license_url
            return '-'
        elif repository_type == 'opensource_google':
            base = f"https://cs.opensource.google/go/{repo_owner}/{repo_name}/+"
            for branch in branches:
                license_url = f"{base}/{branch}:LICENSE"
                if requests.get(license_url).status_code == 200:
                    return license_url
            return '-'
        elif repository_type == 'googlesource':
            base = f"https://go.googlesource.com/{repo_name}/+/refs/heads"
            for branch in branches:
                license_url = f"{base}/{branch}/LICENSE"
                if requests.get(license_url).status_code == 200:
                    return license_url
            return '-'
        return '-'
    
    except requests.exceptions.RequestException:
        return '-'
    
def get_license_info(license_url):
    try:
        if license_url.lower() in 'Unlicense'.lower():
            return 'Unlicense'

        license_response = requests.get(license_url)
        if license_response.status_code == 200:
            license_text = license_response.text.lower()

            for license_category in license_categories:
                if license_category['txt'].lower() in license_text:
                    return license_category['name']
            else:
                return 'Other License'
        return '-'

    except requests.exceptions.RequestException:
        return '-'