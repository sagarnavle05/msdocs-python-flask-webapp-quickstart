from flask import Flask, render_template, request
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

app = Flask(__name__)

# ADLS Gen2 Configuration
account_name = "sntrainingstorageaccount"
file_system_name = "azurefiles"
file_name = "Image1.jpg"

# Azure AD Authentication
credential = DefaultAzureCredential()

# Create DataLakeServiceClient
def get_datalake_service_client():
    return DataLakeServiceClient(
        account_url=f"https://{account_name}.dfs.core.windows.net",
        credential=credential
    )

# Access File from ADLS Gen2
def read_file_from_adls():
    try:
        service_client = get_datalake_service_client()
        file_system_client = service_client.get_file_system_client(file_system_name)
        
        file_client = directory_client.get_file_client(file_name)

        download = file_client.download_file()
        content = download.readall().decode('utf-8')
        return content
    except Exception as e:
        return f"Error reading file: {e}"

@app.route('/')
def index():
    content = read_file_from_adls()  # Access file from ADLS Gen2
    return render_template('index.html', content=content)

if __name__ == '__main__':
    app.run(debug=True)
