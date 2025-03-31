from coreWeather import (
    download_radar,
    transform_radar,
    count_rain_pixels,
    store_rain_pixels,
    plot_rain_pixels,
    recommended_action,
    get_cloud_model,
    generate_web_page,
)
import os

# the site is Captain's Flat NSW IDR403
site = "IDR403"
path = os.getcwd()
# run the functions in order
download_radar(site + ".gif", path + "/static/radar" + site + ".gif")
transform_radar(path + "/static/radar" + site + ".gif")
count = count_rain_pixels(256, 256, 100)
store_rain_pixels(count, site)
plot_rain_pixels(site)
rec_str = recommended_action(site)
generate_web_page(rec_str, path)
