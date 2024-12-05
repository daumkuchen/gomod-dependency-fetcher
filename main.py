import json
import subprocess

import repository
import license
import util


def get_go_module_dependencies():
    try:
        result = subprocess.run(
            ["go", "list", "-m", "-json", "all"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        raw_output = result.stdout.strip()
        decoder = json.JSONDecoder()

        dependencies = []
        pos = 0
        i = 0

        while pos < len(raw_output):
            module_data, pos = decoder.raw_decode(raw_output, pos)
            module_name = module_data.get("Path", "")

            print(f"({pos}/{len(raw_output)}): {module_name}")
            
            if "expo2025" in module_name:
                while pos < len(raw_output) and raw_output[pos].isspace():
                    pos += 1
                continue

            module_url = f"https://pkg.go.dev/{module_name}" if module_name else None
            print(f"- module_url: {module_url}")

            repository_url, repository_type = repository.get_repository_url(module_url)
            print(f"- repository_url: {repository_url}")
            print(f"- repository_type: {repository_type}")

            license_url, license_info = license.get_license_url(repository_url, repository_type)
            print(f"- license_url: {license_url}")
            print(f"- license_info: {license_info}")

            if module_name and module_url:
                dependencies.append((module_name, module_url, repository_url, license_url, license_info))

            while pos < len(raw_output) and raw_output[pos].isspace():
                pos += 1

            # if i >= 10 - 1:
            #     break
            # i += 1

        return dependencies

    except subprocess.CalledProcessError as e:
        print(f"Error running 'go list': {e.stderr}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return []


def main():
    print("Fetching Go module dependencies...")
    dependencies = get_go_module_dependencies()

    if dependencies:
        print("Found the following dependencies:")
        util.save_to_csv_for_google_sheets(dependencies, "./output/sheet.csv")
    else:
        print("No dependencies found or failed to fetch dependencies.")


if __name__ == "__main__":
    main()
