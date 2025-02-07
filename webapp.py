from flask import Flask
from datetime import datetime
import os
from flask import url_for

app = Flask(__name__)

def get_cloud_model():
    from datetime import datetime, timedelta
    from coreWeather import download_radar, transform_radar, count_rain_pixels, store_rain_pixels
    from plot import plot_rain_pixels
    """
    Fetches the cloud coverage model from an external source.
    
    :return: The cloud coverage model as a NumPy array.
    """
    now_utc = datetime.utcnow()
    
    # Calculate the last midnight in UTC
    last_midnight_utc = datetime(now_utc.year, now_utc.month, now_utc.day)
    # Calculate the difference in hours
    hours_until_midnight = int((now_utc - last_midnight_utc).total_seconds() / 3600)
    # https://cloudfreenight.au/images/map/GFS_seaus_012_cct.png
    hrs = format(hours_until_midnight, '03')
    return (f'https://cloudfreenight.au/images/map/GFS_seaus_{hrs}_cct.png')

@app.route("/")
def hello() -> str:
    """
    Generates the web page
    """
    cloud_model = get_cloud_model()
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <link rel="apple-touch-icon" sizes="180x180" href="{url_for('static', filename='apple-touch-icon.png')}">
        <link rel="icon" type="image/png" sizes="32x32" href="{url_for('static', filename='favicon-32x32.png')}">
        <link rel="icon" type="image/png" sizes="16x16" href="{url_for('static', filename='favicon-16x16.png')}">
        <link rel="manifest" href="/site.webmanifest">
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
                <img src="{url_for('static', filename='rain_px_plot_IDR403.png')}" alt="Rain Pixel Plot">
            </div>
            <div class="panel">
                <h2>Rain Radar Map</h2>
                <img src="{url_for('static', filename='radarIDR403.gif')}" alt="Rain Radar Map">
            </div>
            <div class="panel">
                <h2>Cloud Coverage Model</h2>
                <img src="{cloud_model}" alt="Cloud Coverage Model">
            </div>
            <div class="panel">
                <h2>Wind Speed Map</h2>
                <img src="https://example.com/wind_speed_map.png" alt="Wind Speed Map">
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host="127.0.0.1", port=8080, debug=True)
# [END gae_flex_quickstart]
