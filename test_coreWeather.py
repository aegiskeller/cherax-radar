from coreWeather import download_radar, transform_radar


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
