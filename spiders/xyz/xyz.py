import scrapy
from app.settings import SPIDER_SETTINGS
from scrapy.exceptions import CloseSpider
from scrapy.utils.markup import remove_tags, replace_entities

BASE_URL = 'https://www.clippersync.com'


class ClipItem(scrapy.Item):
    date = scrapy.Field()
    raw_note = scrapy.Field()


class xyz(scrapy.Spider):
    @classmethod
    def spider_details(cls):
        for item in SPIDER_SETTINGS:
            if item['spider'] == cls.__name__:
                return item

    name = 'xyz'
    start_urls = [BASE_URL]

    def parse(self, response):
        credentials = self.spider_details()
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
            time_stamp = clip.xpath('.//div[3]/span/text()').extract_first()
            note = clip.xpath('.//div[2]/a')

            if len(note) == 0:
                continue

            note_text = note.extract_first()
            note_text = remove_tags(note_text)
            note_text = replace_entities(note_text)

            if note_text.endswith('...'):
                note_url = note.xpath('@href').extract_first()
                yield scrapy.Request(BASE_URL + note_url, callback=self.extended_notes, meta={'time_stamp': time_stamp})
            else:
                item = ClipItem()
                item['date'] = time_stamp
                item['raw_note'] = note_text
                yield item

    @staticmethod
    def extended_notes(response):
        time_stamp = response.meta.get('time_stamp')
        note = response.selector.xpath('//*[@id="clipping-box"]/div[2]/div[2]').extract_first()

        note = remove_tags(note)
        note = replace_entities(note)
        note = note.strip('\n\t\t\t\t\t')
        item = ClipItem()
        item['date'] = time_stamp
        item['raw_note'] = note

        yield item
