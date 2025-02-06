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

## GCP deploy

# Idea 1: deploy all the machinary to GCP App Runner
sudo apt-get update
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get update && sudo apt-get install google-cloud-cli
gcloud init

gcloud app deploy

# Idea 2: Deploy a static html that is updated from remote compute

After struggling with the App Runner environment and scheduling of remote regeneration of the web page, I am thinking that it might be best to perform the updates remotely and push the html to a portal
