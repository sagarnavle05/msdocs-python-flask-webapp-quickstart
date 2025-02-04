from flask import Flask, render_template, Response
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

app = Flask(__name__)

# ADLS Gen2 Configuration
account_name = "sntrainingstorageaccount"  # Storage Account Name
file_system_name = "azurefiles"  # File System (Container) Name
file_name ="Image1.jpg" # The image file you want to read directly from the container

# Azure AD Authentication
credential = DefaultAzureCredential()
    
# Create DataLakeServiceClient
def get_datalake_service_client():
    return DataLakeServiceClient(
        account_url=f"https://{account_name}.dfs.core.windows.net",
        credential=credential
    )

# Access Image File from ADLS Gen2
def get_image_from_adls():
    try:
        service_client = get_datalake_service_client()
        file_system_client = service_client.get_file_system_client(file_system_name)
        
        # Access the file directly from the container
        file_client = file_system_client.get_file_client(file_name)

        # Download the image
        download = file_client.download_file()
        image_data = download.readall()
        return image_data
    except Exception as e:
        return f"Error retrieving image: {e}"

# Route to display image
@app.route('/image')
def serve_image():
    image_data = get_image_from_adls()  # Retrieve image from ADLS Gen2
    return Response(image_data, content_type='image/jpeg')  # Serve the image as a JPEG

# Home route to display the image in the template
@app.route('/')
def index():
    return render_template('index.html')  # You can add additional content here if necessary

if __name__ == '__main__':
    app.run(debug=True)