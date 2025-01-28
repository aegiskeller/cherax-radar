from ftplib import FTP
from PIL import Image
import math

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

def transform_radar(radar_image):
    """
    Here we transform the image so that we have isolated the pixels that are 'rain' related
    These are defined by the colours shon on the bottom legend of the image
    Some colours are worse than others - so we preserve that infomation here
    """
    rain_index = [(180,180,255), (120,120,255), (20,20,255), (0, 216, 195), (0, 150, 144), (0, 102, 102), (255, 255, 0), (255,200,0), (255,150,0), (255,100,0), (255,0,0), (200,0,0), (120,0,0), (40,0,0)]
    image = Image.open(radar_image).convert("RGB")
    pixels = image.load()
    masked_image = Image.new("RGB", image.size, (0, 0, 0))
    masked_pixels = masked_image.load()
    for ri in range(len(rain_index)):
        for y in range(image.height-100):
            for x in range(image.width):
                if pixels[x,y] == rain_index[ri]:
                    masked_pixels[x, y] = pixels[x, y]
    masked_image.save('masked.gif')
    print('generated masked image')
    return()

def count_rain_pixels(xc,yc,radius):
    rain_index = [(180,180,255), (120,120,255), (20,20,255), (0, 216, 195), (0, 150, 144), (0, 102, 102), (255, 255, 0), (255,200,0), (255,150,0), (255,100,0), (255,0,0), (200,0,0), (120,0,0), (40,0,0)]
    count_in_radius = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    numpx_in_radius = 0 
    image = Image.open('masked.gif').convert("RGB")
    pixels = image.load()# how much of the full image is within the radius? 
    for y in range(image.height-100):
        for x in range(image.width):
         if math.sqrt((x - xc) ** 2 + (y - yc) ** 2) <=radius:
                numpx_in_radius +=1
    print(numpx_in_radius)
    for ri in range(len(rain_index)):
        for y in range(image.height-100):
            for x in range(image.width):
                if  pixels[x,y] == rain_index[ri] and math.sqrt((x - xc) ** 2 + (y - yc) ** 2) <=radius:
                    count_in_radius[ri]+=1
        count_in_radius[ri]/=numpx_in_radius
    print(count_in_radius)

# Example usage
#image_url = "http://www.bom.gov.au/radar/IDR403.gif"
#download_radar(image_url, "downloaded_image.jpg")

# from PIL import Image
# from collections import Counter
# def get_rgb_frequencies():
#     image = Image.open('IDR403.gif').convert("RGB")
#     pixels = list(image.getdata())
#     frequency = Counter(pixels)
#     return(frequency)

# rgb_frequencies = get_rgb_frequencies()
# #Print the frequencies
# for rgb, count in rgb_frequencies.items():
#     print(f'RGB: {rgb}, Frequency: {count}')
