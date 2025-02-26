from coreWeather import (
    download_radar,
    transform_radar,
    count_rain_pixels,
    store_rain_pixels,
)
from plot import plot_rain_pixels
import os

site = "IDR403"  # Captain's Flat NSW
# site = 'IDR163' # Pt Headland WA
destination_folder = "static"

# this is to be called by a cron job
# Check if the 'static' directory exists, if not create it
if not os.path.exists("static"):
    os.makedirs("static")

download_radar(site + ".gif", "static/radar" + site + ".gif")

transform_radar("static/radar" + site + ".gif")

# 100 pixel radius about the centre of the image equates to 50km
pixel_cnt = count_rain_pixels(256, 256, 100)

store_rain_pixels(pixel_cnt, site)

plot_rain_pixels(site)
