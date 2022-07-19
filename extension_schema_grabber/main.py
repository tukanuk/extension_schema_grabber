import json
import requests
import settings as settings

token = settings.token


def get_latest_schema_version():
    """ find the lastest version of the schema """

    url = "https://kqw28951.dev.dynatracelabs.com/api/v2/extensions/schemas"

    payload={}
    headers = {
    'Authorization': f'Api-Token {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.json())

    latest = response.json()['versions'][-1]
    
    return latest

def get_file_list_for_schema(version: str):
    """ get the list of files for the specified version """

    url = f"https://kqw28951.dev.dynatracelabs.com/api/v2/extensions/schemas/{version}"

    payload={}
    headers = {
    'Authorization': f'Api-Token {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)

    schema_list = dict(response.json())

    return schema_list['files']

def get_schema_file(schema_version:str, filename: str):
    """ Get the requested schema file"""
        
    url = f"https://kqw28951.dev.dynatracelabs.com/api/v2/extensions/schemas/{schema_version}/{filename}"

    payload={}
    headers = {
    'Authorization': f'Api-Token {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)

    return response.json()

def save_schema_file(path: str, name: str, contents: str):
    """ save the schema file in a directory"""

    with open(path + name, "w", encoding="UTF-8") as file:
        json.dump(contents, file, indent=4, default=str)

def main():
    latest = get_latest_schema_version()
    schema_list = get_file_list_for_schema(latest)
    # print(schema_list)

    for schema_file in schema_list:
        print(f"Getting: {schema_file}")
        
        file_contents = get_schema_file(latest, schema_file)

        path = f"~/.schemas/{latest}/"        
        save_schema_file(path, schema_file, file_contents)


if __name__ == '__main__':
    main()