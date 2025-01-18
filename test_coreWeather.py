from coreWeather import download_radar


def test_download_radar():
    assert "Radar obtained" in download_radar("http://www.bom.gov.au/radar/IDR403.gif", "erty.gif")

def test_fail_radar():
    assert "Radar obtained" in download_radar("http://www.rabbits.com/fridge.jpg", "erty.gif")


#def test_get_text_blob():
#    assert "farrk" == get_text_blob("farrk")


#def test_get_phrases():
#    assert "francophonie" in get_phrases("Franco")