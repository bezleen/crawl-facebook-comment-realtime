# Download the Chrome Driver
Find your chrome driver suit your chrome browser
Follow this link: "https://chromedriver.chromium.org/downloads"
Download and paste it in folder "chrome_drivers" 
# Install the requirements
## Initialize the virtual environment
```
virtualenv .venv -p python3.8
```
## Activate the virtual environment
```
source .venv/bin/activate
```
## Install the requirements
```
pip install -r requirements.txt
```
# Set up Stream URL
go to src/app.py set the stream_url
# Implement output
You can change where the output will be written by put your code in the function "save_content" in class FacebookStreamingCrawl. The path is src/models/base.py 
# Set Login Info
create file .env by copy the sample.env file then type your facebook email and password
if not login -> comment will not load
# Run the crawl realtime
```
python3 src/app.py
```

