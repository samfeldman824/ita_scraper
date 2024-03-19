# ita_scraper
web scraper that gets match scores from the ITA website

## Setup

```
# creating env with conda
conda env create -f environment.yml
conda activate scraper
```

Both the Chrome browser and Chrome WebDriver will need to be installed and be found
[here](https://googlechromelabs.github.io/chrome-for-testing/)

The full path of your Chrome WebDriver will need to be added to scrape.py at line 16.