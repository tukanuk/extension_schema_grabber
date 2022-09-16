import json
import requests
import settings as settings
import os

token = settings.token
schemea_path = settings.schema_path
tenant = settings.tenant


def get_latest_schema_version():
    """ find the lastest version and a complete list of versions of the schema """

    url = f"{tenant}/api/v2/extensions/schemas"

    payload={}
    headers = {
    'Authorization': f'Api-Token {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.json())

    latest = response.json()['versions'][-1]
    
    return latest, response.json()['versions']

def get_file_list_for_schema(version: str):
    """ get the list of files for the specified version """

    url = f"{tenant}/api/v2/extensions/schemas/{version}"

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
        
    url = f"{tenant}/api/v2/extensions/schemas/{schema_version}/{filename}"

    payload={}
    headers = {
    'Authorization': f'Api-Token {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)

    return response.json()

def save_schema_file(path: str, name: str, contents: str):
    """ save the schema file in a directory"""

    # print(f"Writing to {path}{name}")
    with open(path + "/" + name, "w", encoding="UTF-8") as file:
        json.dump(contents, file, indent=4, default=str)

def main():
    latest, version_list = get_latest_schema_version()

    for version in version_list:
        schema_list = get_file_list_for_schema(version)
        # print(schema_list)

        print(f"Schema for version: {version}")
        newdir = os.path.join(schemea_path, version)
        if not os.path.exists(newdir):
            os.makedirs(newdir)
            # print(f"Creating path: {newdir}")
            if os.path.exists(newdir):
                # print("The path is now present")
                pass
        # else:
        #     print(f"{newdir} exists")

        print(f"Gettings schema for {version}")
        for schema_file in schema_list:
            # print(f"Getting: {schema_file}")
            
            file_contents = get_schema_file(version, schema_file)

            # path = f"~/.schemas/{version}/"        
            save_schema_file(newdir, schema_file, file_contents)


if __name__ == '__main__':
    main()