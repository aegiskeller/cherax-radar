from ftplib import FTP
from datetime import datetime
import os
import argparse
from PIL import Image


def download_most_recent_file(product_id, local_file_path):
    """
    Connects to an FTP site, finds the most recent file in the specified directory, and downloads it.
    
    :param remote_dir: The directory on the FTP server to search for files.
    :param local_file_path: The path to save the file locally.
    """
    # Connect to the FTP server
    ftp = FTP('ftp.bom.gov.au')
    ftp.login()
    
    # Change to the desired directory
    ftp.cwd('anon/gen/gms')
    
    # Get a listing of the current directory
    files = ftp.nlst()

    #filter files for a given prefix to obtain a particular product
    files = [file for file in files if file.startswith(product_id)]
    
    # Get the most recent file based on modification time
    most_recent_file = None
    most_recent_time = None
    for file in files:
        modified_time = ftp.sendcmd(f'MDTM {file}')
        modified_time = datetime.strptime(modified_time[4:], "%Y%m%d%H%M%S")
        if most_recent_time is None or modified_time > most_recent_time:
            most_recent_time = modified_time
            most_recent_file = file
    
    if most_recent_file:
        # Obtain the file extension
        _, file_extension = os.path.splitext(most_recent_file)
         # Download the most recent file
        with open(local_file_path+file_extension, 'wb') as local_file:
            ftp.retrbinary(f'RETR {most_recent_file}', local_file.write)
        print(f'Most recent file "{most_recent_file}" downloaded successfully to {local_file_path}')
    else:
        print('No files found in the directory.')
    
    # Close the connection
    ftp.quit()
    return(local_file_path+file_extension)


def create_subimage(input_image_path, output_image_path, crop_box):
    """
    Creates a subimage from the input image by cropping the specified region.
    
    :param input_image_path: The path to the input image file.
    :param output_image_path: The path to save the cropped subimage.
    :param crop_box: A tuple (left, upper, right, lower) defining the region to crop.
    """
    # Open the input image
    with Image.open(input_image_path) as img:
        # Crop the image
        subimage = img.crop(crop_box)
        
        # Save the subimage
        subimage.save(output_image_path)
        print(f'Subimage saved to {output_image_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download the most recent file with a specific prefix from an FTP site.')
    parser.add_argument('product_id', type=str, help='The identifier for the product to download.')
    parser.add_argument('local_file_path', type=str, help='The path to save the file locally.')
    
    args = parser.parse_args()
    
    raw_image = download_most_recent_file(args.product_id, args.local_file_path)
    create_subimage(raw_image, 'subimage.png', (3000, 2500, 4000, 3500))