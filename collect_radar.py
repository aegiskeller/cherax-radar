from coreWeather import download_radar, transform_radar, count_rain_pixels, store_rain_pixels
from plot import plot_rain_pixels
import os

site = 'IDR403' # Captain's Flat NSW
#site = 'IDR163' # Pt Headland WA
destination_folder = 'static'

<<<<<<< HEAD

while True:
    # Check if the 'static' directory exists, if not create it
    if not os.path.exists('static'):
        os.makedirs('static')

    download_radar(site+'.gif', 'static/radar'+site+'.gif')

    transform_radar('static/radar'+site+'.gif')

    pixel_cnt = count_rain_pixels(256,256,100)

    store_rain_pixels(pixel_cnt, site)

    plot_rain_pixels(site)

    source_folder = '/home/aegiskeller/cherax-radar/static'
    destination_folder = '/var/www/html/static'

    sleep(300)
=======
# Check if the destination folder exists and remove it
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

download_radar(site+'.gif', 'static/radar'+site+'.gif')

transform_radar('static/radar'+site+'.gif')

# a radius of 100px is 50km
pixel_cnt = count_rain_pixels(256,256,100)

store_rain_pixels(pixel_cnt, site)

plot_rain_pixels(site)

>>>>>>> 66a09f7 (added simple recommendation)
