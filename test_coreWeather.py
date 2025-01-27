from coreWeather import download_radar


def test_download_radar():
    assert "Radar obtained" in download_radar("IDR403.gif", "radar.gif")

def test_fail_radar():
    assert "Radar failed" in download_radar("fridge.jpg", "radar.gif")


#def test_get_text_blob():
#    assert "farrk" == get_text_blob("farrk")


#def test_get_phrases():
#    assert "francophonie" in get_phrases("Franco")