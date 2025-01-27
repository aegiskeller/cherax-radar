from ftplib import FTP

def download_radar(src_filename, dst_filename):
    """
    Australian BOM has the lovely ftp repo of radar images
    The radar of interest to us is IDR403 for the Canberra region
    """
    try:
        ftp = FTP('ftp.bom.gov.au')
        ftp.login()
        ftp.cwd('anon/gen/radar')
        with open(dst_filename, "wb") as file: 
            ftp.retrbinary(f"RETR {src_filename}", file.write)
        ftp.quit()
        print(f"Image successfully downloaded: {src_filename}")
        return('Radar obtained')
    except Exception as e:
        print(f"Failed to download image: {e}")
        return('Radar failed')

# Example usage
#image_url = "http://www.bom.gov.au/radar/IDR403.gif"
#download_radar(image_url, "downloaded_image.jpg")
