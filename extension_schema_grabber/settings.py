from email.encoders import encode_quopri
import yaml

with open("config/config.yaml", "r", encoding="UTF-8") as file:
    config_file = yaml.safe_load(file)

token = config_file['token']
schema_path = config_file['schema_path']
tenant = config_file['tenant']
print(token)