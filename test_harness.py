from coreWeather import download_radar, transform_radar, count_rain_pixels

download_radar('IDR403.gif', 'radar.gif')

masked_pixels = transform_radar('radar.gif')

count_rain_pixels(256,256,100)