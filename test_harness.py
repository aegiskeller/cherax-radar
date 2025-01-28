from coreWeather import download_radar, transform_radar, count_rain_pixels, store_rain_pixels

download_radar('IDR403.gif', 'radar.gif')

transform_radar('radar.gif')

pixel_cnt = count_rain_pixels(256,256,100)

store_rain_pixels(pixel_cnt)