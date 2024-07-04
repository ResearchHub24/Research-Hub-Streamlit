import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from utils.Secrates import json_data

credentials = service_account.Credentials.from_service_account_info(
    json_data,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# Refresh the token
credentials.refresh(Request())

# Get the access token
access_token = credentials.token

print(access_token)
