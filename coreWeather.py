import subprocess

def download_radar(url, file_name):
    try:
        result = subprocess.run(['curl', '-o', file_name, url], check=True, text=True, capture_output=True)
        print(f"Image successfully downloaded: {file_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to download image: {e}")

# Example usage
#image_url = "http://www.bom.gov.au/radar/IDR403.gif"
#download_radar(image_url, "downloaded_image.jpg")
