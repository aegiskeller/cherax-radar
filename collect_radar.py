from coreWeather import download_radar, transform_radar, count_rain_pixels, store_rain_pixels
from time import sleep

site = 'IDR403' # Captain's Flat NSW
#site = 'IDR163' # Pt Headland WA


while True:
    download_radar(site+'.gif', 'radar'+site+'.gif')

    transform_radar('radar'+site+'.gif')

    pixel_cnt = count_rain_pixels(256,256,100)

    store_rain_pixels(pixel_cnt, site)
    sleep(300)