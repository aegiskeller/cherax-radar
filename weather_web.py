def get_cloud_model():
    from datetime import datetime, timedelta
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
    hrs = format(hours_until_midnight, '03')
    return (f'https://cloudfreenight.au/images/map/GFS_seaus_{hrs}_cct.png')

def generate_web_page(image_path, output_html_path):
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
                <img src="rain_px_plot_IDR403.png" alt="Rain Pixel Plot">
            </div>
            <div class="panel">
                <h2>Rain Radar Map</h2>
                <img src="radarIDR403.gif" alt="Rain Radar Map">
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

    # Write the HTML content to the output file
    with open(output_html_path, 'w') as html_file:
        html_file.write(html_content)
    print(f'Web page generated successfully at {output_html_path}')

# Example usage
# generate_web_page('rain_px_plot_IDR403.png', 'weather_watch.html')
if __name__ == "__main__":
    generate_web_page('rain_px_plot_IDR403.png', 'weather_watch.html')
