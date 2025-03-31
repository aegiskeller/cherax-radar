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


def test_download_radar():
    assert "Radar obtained" in download_radar("IDR403.gif", "radar.gif")


def test_fail_radar():
    try:
        download_radar("fridge.jpg", "radar.gif")
    except Exception as e:
        print(f"raises {e}")


def test_transform_radar():
    download_radar("IDR403.gif", "radar.gif")
    assert "generated masked image" in transform_radar("radar.gif")


def test_fail_transform_radar():
    download_radar("IDR403.gif", "radar.gif")
    assert "masked image failed" in transform_radar("radart.gif")


# test the functions in coreWeather.py
def test_count_rain_pixels():
    download_radar("IDR403.gif", "radar.gif")
    transform_radar("radar.gif")
    assert 100 in count_rain_pixels(256, 256, 100)


def test_store_rain_pixels():
    download_radar("IDR403.gif", "radar.gif")
    transform_radar("radar.gif")
    count = count_rain_pixels(256, 256, 100)
    assert "appended results to static/rain_px_results_" in store_rain_pixels(
        count, "IDR403"
    )


def test_plot_rain_pixels():
    download_radar("IDR403.gif", "radar.gif")
    transform_radar("radar.gif")
    assert "Plot saved as" in plot_rain_pixels("IDR403")
