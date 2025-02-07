from coreWeather import download_radar, transform_radar, count_rain_pixels, store_rain_pixels
from time import sleep
import shutil
import os

site = 'IDR403' # Captain's Flat NSW
#site = 'IDR163' # Pt Headland WA


while True:
    download_radar(site+'.gif', 'static/radar'+site+'.gif')

    transform_radar('static/radar'+site+'.gif')

    pixel_cnt = count_rain_pixels(256,256,100)

    store_rain_pixels(pixel_cnt, site)

    source_folder = '/home/aegiskeller/cherax-radar/static'
    destination_folder = '/var/www/html/static'

    # Copy the entire folder to the destination
# Check if the destination folder exists and remove it
    if os.path.exists(destination_folder):
        shutil.rmtree(destination_folder)
    shutil.copytree(source_folder, destination_folder)    
    sleep(300)
