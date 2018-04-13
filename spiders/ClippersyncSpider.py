import scrapy
from settings import SPIDER_SETTINGS
from scrapy.exceptions import CloseSpider

BASE_URL = 'https://www.clippersync.com'

class ClipItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    note = scrapy.Field()


class ClippersyncSpider(scrapy.Spider):
    @classmethod
    def get_credentials(cls):
        for item in SPIDER_SETTINGS:
            if item['spider'] == cls.__name__:
                return {'email':item['email'], 'password': item['password']}

    name = 'clippersync'
    start_urls = [BASE_URL]

    def parse(self, response):
        credentials = self.get_credentials()
        yield scrapy.FormRequest.from_response(
            response,
            formxpath='//*[@id="login"]/div/div/form',
            formdata={
                'email': credentials['email'],
                'password': credentials['password']
            },
            callback=self.after_login
        )

    def after_login(self, response):
        if 'Invalid username or password.' in str(response.body):
            raise CloseSpider('Invalid login credentials')
        if response.status != 200:
            raise CloseSpider('Problem Fetching page, try again')

        clippings = response.selector.xpath('//*[@id="clippings"]/div[*]/div')
        for clip in clippings:
            time_stamp = clip.xpath('.//div[3]/span/text()').extract_first()  #  //*[@id="clippings"]/div[6]/div/div[3]
            note = clip.xpath('.//div[2]/a')
            note_text = note.xpath('text()').extract_first()
            if note_text is None:
                continue
            if note_text.endswith('...'):
                note_url = note.xpath('@href').extract_first()
                yield scrapy.Request(BASE_URL + note_url, callback=self.extended_notes, meta={'time_stamp': time_stamp})
            else:
                item = ClipItem()
                item['date'] = time_stamp
                item['note'] = note_text
                yield item
                return

    def extended_notes(self, response):
        time_stamp = response.meta.get('time_stamp')
        note = response.selector.xpath('//*[@id="clipping-box"]/div[2]/div[2]/text()').extract_first()
        note = note.strip('\n\t\t\t\t\t')
        item = ClipItem()
        item['date'] = time_stamp
        item['note'] = note

        yield item
