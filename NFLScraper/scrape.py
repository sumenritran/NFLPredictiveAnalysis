# Execute the below command to scrape data from pro-football-reference.com:
from scrapy import cmdline
cmdline.execute('scrapy crawl nfl_games -o nfl_scraped.csv'.split())