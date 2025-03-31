from coreWeather import (
    download_radar,
    transform_radar,
    count_rain_pixels,
    store_rain_pixels,
    get_cloud_model,
    examine_cloud_model,
)

# site = "IDR403"  # Captain's Flat NSW
# # site = 'IDR163' # Pt Headland WA

# download_radar(site + ".gif", "static/radar" + site + ".gif")

# transform_radar("radar" + site + ".gif")

# pixel_cnt = count_rain_pixels(256, 256, 100)

# store_rain_pixels(pixel_cnt, site)

site = "IDR403"  # Captain's Flat NSW
url = get_cloud_model('twilight')
examine_cloud_model(site, url)