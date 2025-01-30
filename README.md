# cherax-radar
An application to check if there is rain in the vicinity of a location from Australian BOM radar coverage. Return a rain status for further action.

## Usage:
o test_harness.py will process a single instance of the radar map for a location
o collect_radar.py will process repeated images for a location and save the results for visualisation
o plot.py visualises the change in rain intensity for a location from the details saved from collect_radar

## Notes

Perhaps best to obtain the predicted cloud cover rather than the observed cloud cover since this is very hard to establish with the dirunal temperature change

e.g. https://www.skippysky.com.au/SE_Australia/transparency/seaus_006_tran.png

Creating a web page to hold the pertainent information:
generate_web_page('rain_px_plot_IDR403.png', 'erty.html')