from ftplib import FTP
from PIL import Image
import math
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt



def download_radar(src_filename, dst_filename):
    """
    Australian BOM has the lovely ftp repo of radar images
    The radar of interest to us is IDR403 for the Canberra region
    """
    ftp = FTP("ftp.bom.gov.au")
    ftp.login()
    ftp.cwd("anon/gen/radar")
    with open(dst_filename, "wb") as file:
        ftp.retrbinary(f"RETR {src_filename}", file.write)
    ftp.quit()
    print(f"Image successfully downloaded: {src_filename}")
    return "Radar obtained"


def transform_radar(radar_image):
    """
    Here we transform the image so that we have isolated the pixels that are 'rain' related
    These are defined by the colours shon on the bottom legend of the image
    Some colours are worse than others - so we preserve that infomation here
    """
    rain_index = [
        (180, 180, 255),
        (120, 120, 255),
        (20, 20, 255),
        (0, 216, 195),
        (0, 150, 144),
        (0, 102, 102),
        (255, 255, 0),
        (255, 200, 0),
        (255, 150, 0),
        (255, 100, 0),
        (255, 0, 0),
        (200, 0, 0),
        (120, 0, 0),
        (40, 0, 0),
    ]
    try:
        image = Image.open(radar_image).convert("RGB")
        pixels = image.load()
        masked_image = Image.new("RGB", image.size, (0, 0, 0))
        masked_pixels = masked_image.load()
        for ri in range(len(rain_index)):
            for y in range(image.height - 100):
                for x in range(image.width):
                    if pixels[x, y] == rain_index[ri]:
                        masked_pixels[x, y] = pixels[x, y]
        masked_image.save("static/masked.gif")
        print("generated masked image")
        return "generated masked image"
    except FileNotFoundError:
        return "masked image failed"


def count_rain_pixels(xc, yc, radius):
    """
    We select the colours of interest and count the number in each category within a radius about a given
    centre and then express this as a fraction of the total number of pixels in the radius
    """
    rain_index = [
        (180, 180, 255),
        (120, 120, 255),
        (20, 20, 255),
        (0, 216, 195),
        (0, 150, 144),
        (0, 102, 102),
        (255, 255, 0),
        (255, 200, 0),
        (255, 150, 0),
        (255, 100, 0),
        (255, 0, 0),
        (200, 0, 0),
        (120, 0, 0),
        (40, 0, 0),
    ]
    count_in_radius = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    numpx_in_radius = 0
    image = Image.open("static/masked.gif").convert("RGB")
    pixels = image.load()
    # how much of the full image is within the radius?
    for y in range(image.height - 100):
        for x in range(image.width):
            if math.sqrt((x - xc) ** 2 + (y - yc) ** 2) <= radius:
                numpx_in_radius += 1
    # print(numpx_in_radius)
    for ri in range(len(rain_index)):
        for y in range(image.height - 100):
            for x in range(image.width):
                if (
                    pixels[x, y] == rain_index[ri]
                    and math.sqrt((x - xc) ** 2 + (y - yc) ** 2) <= radius
                ):
                    count_in_radius[ri] += 1
        count_in_radius[ri] /= numpx_in_radius
    return [radius] + count_in_radius

def plot_rain_pixels(site):
    """
    This function reads the rain pixel results from the file and plots time vs. columns.
    The RGB values rain_index are used in tahe plot to be consistent with the original radar image
    The plot is saved as a PNG file.
    """
    rain_index = [
        (180, 180, 255),
        (120, 120, 255),
        (20, 20, 255),
        (0, 216, 195),
        (0, 150, 144),
        (0, 102, 102),
        (255, 255, 0),
        (255, 200, 0),
        (255, 150, 0),
        (255, 100, 0),
        (255, 0, 0),
        (200, 0, 0),
        (120, 0, 0),
        (40, 0, 0),
    ]
    # Read the data from the file
    file_path = f"static/rain_px_results_{site}.txt"
    data = pd.read_csv(
        file_path,
        header=None,
        names=["timestamp"] + ["radius"] + [f"int_{i}" for i in range(1, 15)],
    )

    # Convert the timestamp column to datetime
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    # print(data.head())
    # Calculate the sum of rain pixel columns
    data["sum"] = data.iloc[:, 2:].sum(axis=1)

    # Calculate the moving average (5 time steps)
    data["moving_avg"] = data["sum"].rolling(window=5).mean()
    # Plot the data
    plt.figure(figsize=(8, 6))
    for i, col in enumerate(data.columns[2:15]):
        plt.plot(
            data["timestamp"],
            data[col],
            label=col,
            color=[c / 255 for c in rain_index[i]],
        )

    # Plot the moving average
    plt.plot(
        data["timestamp"],
        data["moving_avg"],
        label="Mv Avg",
        color="black",
        linewidth=2,
    )

    plt.xlabel("Time")
    plt.ylabel("Fraction of Region with Rain Pixels")
    plt.title(f"Rain Pixel Count Over Time for {site}")
    plt.legend(bbox_to_anchor=(0.90, 1), loc="upper left")
    plt.grid(True)

    # Save the plot as a PNG file
    output_file = f"static/rain_px_plot_{site}.png"
    plt.savefig(output_file)
    return f"Plot saved as {output_file}"


def store_rain_pixels(px_count, site):
    """
    Here we have a simple stub to store the pixel results
    the site parameter is here to enable logging for multiple sites
    """
    local_timestamp = datetime.now()
    formatted_timestamp = local_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    with open(f"static/rain_px_results_{site}.txt", "a", encoding="utf-8") as file:
        file.write("\n" + formatted_timestamp + ",")
        file.write(",".join(map(str, px_count)))
    return f"appended results to static/rain_px_results_{site}.txt"


def recommended_action(site):
    """
    Here we recommend an action based on the pixel results
    """
    # Read the data from the file
    file_path = f"static/rain_px_results_{site}.txt"
    data = pd.read_csv(
        file_path,
        header=None,
        names=["timestamp"] + ["radius"] + [f"int_{i}" for i in range(1, 15)],
    )

    # Convert the timestamp column to datetime
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    # print(data.head())
    # Calculate the sum of rain pixel columns
    data["sum"] = data.iloc[:, 2:].sum(axis=1)

    # Calculate the moving average (5 time steps)
    data["moving_avg"] = data["sum"].rolling(window=5).mean()
    cloud_trend = "trend not clear"
    try:
        d1 = data["moving_avg"].iloc[-5] - data["moving_avg"].iloc[-10]
        d2 = data["moving_avg"].iloc[-10] - data["moving_avg"].iloc[-15]
        print(d1, d2)
        if d1 > 0.01 and d2 > 0.01:
            print(f"Condition is worsening for {site}")
            cloud_trend = "worsening"
        if d1 < -0.01 and d2 < -0.01:
            print(f"Condition is improving for {site}")
            cloud_trend = "improving"
    except:
        print("Not enough data to determine trend")
    # additonally if there really is not cloud around then show it is clear
    if data["moving_avg"].iloc[-1] < 0.01:
        cloud_trend = "clear"
    obs_status = "close undefined"
    if data["moving_avg"].iloc[-1] > 0.1:
        print(f"Close Action recommended for {site}")
        obs_status = "close"
    else:
        print(f"Open Action recommended for {site}")
        obs_status = "open"
    print(f"{site} - {cloud_trend} - {obs_status}")
    return f"{site} - {cloud_trend} - {obs_status}"

def get_cloud_model():

    """
    Fetches the cloud coverage model from an external source.
    
    :return: The cloud coverage model as a NumPy array.
    """
    # Get the current time in UTC
    now_utc = datetime.utcnow()

    # Calculate the last midnight in UTC
    last_midnight_utc = datetime(now_utc.year, now_utc.month, now_utc.day)
    # Calculate the difference in hours
    hours_until_midnight = int((now_utc - last_midnight_utc).total_seconds() / 3600)
    # https://cloudfreenight.au/images/map/GFS_seaus_012_cct.png
    hrs = format(hours_until_midnight, "03")
    return f"https://cloudfreenight.au/images/map/GFS_seaus_{hrs}_cct.png"

def generate_web_page(recommendation, output_html_path):
    """
    Generates a web page with the title 'Weather Watch' and includes the specified image.

    :param image_path: The path to the image file to include in the web page.
    :param output_html_path: The path to save the generated HTML file.
    """
    cloud_model = get_cloud_model()
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weather Watch</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #121212;
                color: #ffffff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 150vh;
            }}
            .container {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                grid-gap: 20px;
                width: 80%;
                max-width: 1200px;
            }}
            .panel {{
                background-color: #1e1e1e;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
                text-align: center;
            }}
            .panel img {{
                max-width: 100%;
                height: auto;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="panel">
                <h2>Rain Pixel Plot</h2>
                <img src="static/rain_px_plot_IDR403.png" alt="Rain Pixel Plot">
            </div>
            <div class="panel">
                <h2>Rain Radar Map</h2>
                <img src="static/radarIDR403.gif" alt="Rain Radar Map">
            </div>
            <div class="panel">
                <h2>Cloud Coverage Model</h2>
                <img src="{cloud_model}" alt="Cloud Coverage Model">
            </div>
            <div class="panel">
                <h2>Recommended Action</h2>
                <p>{recommendation}</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Write the HTML content to the output file
    with open(output_html_path+"/weather_watch.html", "w") as html_file:
        html_file.write(html_content)
    print(f"Web page generated successfully at {output_html_path}")
