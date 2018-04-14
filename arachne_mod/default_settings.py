# This allows scrapy to dynamically assign port to crawler object
TELNETCONSOLE_PORT = None

# Crawl responsibly
USER_AGENT = "ClipperSync /0.0 (+https://github.com/dmkitui/ClipperSync-Scrapper)"

# Export data to JSON or CSV
EXPORT_PATH = 'exports/'
EXPORT_JSON = False
EXPORT_CSV = False

# Logs can be turned on and off. Default directory is logs/
LOGS = False
LOGS_PATH = 'logs/'


# DEBUG setting for spiders always true
DEBUG = True

# common settings for each spider
SCRAPY_SETTINGS = {'ITEM_PIPELINES': {}}
