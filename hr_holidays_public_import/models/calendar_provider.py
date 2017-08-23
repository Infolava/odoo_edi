from openerp import models, fields, api, _ 
from openerp.exceptions import AccessError, ValidationError, Warning
import json
import urllib2
import logging

_logger =  logging.getLogger(__name__)

class calendar_provider(models.Model):
    """Class defining the configuration values of a Calendar provider"""

    _name = 'calendar.provider'
    _description = 'Model to handle calendar provider parameters'
    _rec_name = "provider_name"

    provider_name = fields.Char('Provider Name')
    provider_url = fields.Char('Provider URL')
    provider_api_key = fields.Char('Provider API key')
    description = fields.Text('Description')
   
    def get_country_code_from_provider(self, country):
        return country.code
    
    def provider_response_parser(self, json_request_response):
        return []
   
    @api.multi
    def request_handler(self, country_code, lang_codes, start_year, end_year):
        self.ensure_one()
        headers = {
                   'Content-Type': 'application/json',
                   }
        json_response = {}
        if self.provider_name == "Google Calendar" :
            # only one url request for google calendar will return 3 years
            # [previous_year, current_year, next_year]
            end_year = start_year
        for year in range(start_year, end_year + 1) :
            json_response[year] = {}
            for lang_code in lang_codes :
                url = self.provider_url.format(country = country_code, lang = lang_code.split('_')[0], api_key = self.provider_api_key, year = year)
                request = urllib2.Request(url, headers = headers)
                try :
                    res = urllib2.urlopen(request)
                    response = res.read()
                    json_response[year][lang_code] = json.loads(response)
                    res.close()
                except urllib2.HTTPError as e:
                    if e.code == 404 :
                        if lang_code != 'en':
                            raise ValidationError(_('Unsupported country'))
                        else :
                            #TODO fix HTTPError for unsupported language 
                            _logger.warning('Not supported language %s for provider %s' %(lang_code, self.provider_name))
                    elif e.code == 400 :
                        raise AccessError(_('Please contact your administration to verify API key configuration'))
                    else :
                        #TODO Test other HTTPError
                        raise ValidationError(_('Unknown error'))
        return self.provider_response_parser(json_response)


class goolglecalendar_provider(models.Model):
    """Class defining the response parser of Google Calendar provider"""

    _inherit = 'calendar.provider'
    _description = 'Google Calendar Provider Parameters'

#     provider_name = "Google Calendar"
#     provider_url = "https://www.googleapis.com/calendar/v3/calendars/{country}__{lang}%40holiday.calendar.google.com/events?key={api_key}"
#     provider_api_key = "admin"
   
    country_list = {'Australia': 'australian',
                    'Austria': 'austrian',
                    'Brazil' : 'canadian',
                    'China' : 'china',
                    'Denmark' : 'danish',
                    'Netherlands': 'dutch',
                    'Finland' : 'finnish',
                    'France' : 'french',
                    'Germany': 'german',
                    'Greece' : 'greek',
                    'Hong Kong' : 'hong_kong',
                    'India' : 'indian',
                    'Indonesia' : 'indonesian',
                    'Iran' : 'iranian',
                    'Ireland' : 'irish',
                    'Italia' : 'italian',
                    'Japan' : 'japanese',
                    'Malaysia' : 'malaysia',
                    'Mexico' : 'mexican',
                    'New Zealand' : 'new_zealand',
                    'Norwegia' : 'norwegian',
                    'Philippines' : 'philippines',
                    'Poland' : 'polish',
                    'Portuguese' : 'portuguese',
                    'Russia' : 'russian',
                    'Singapore' : 'singapore',
                    'South Africa' : 'sa',
                    'South Korean' : 'south_korea',
                    'Spain' : 'spain',
                    'Sweden' : 'swedish',
                    'Taiwan' : 'taiwan',
                    'Thai' : 'thai',
                    'United Kingdom' : 'uk',
                    'United States' : 'usa',
                    'Vietnam' : 'vietnamese'}
             
    def get_country_code_from_provider(self, country):
        if country.name in self.country_list :
            return self.country_list[country.name]
        return super(goolglecalendar_provider, self).get_country_code_from_provider(country)
    
    def provider_response_parser(self, json_request_responses, date_format = "%Y-%m-%d"):
        from datetime import datetime, timedelta
        json_request_response = json_request_responses[json_request_responses.keys()[0]]
        if not json_request_response['en_US']['items'] :
            raise Warning(_('No Data Provided for selected country'))
        # sort holidays list by start date
        holidays_items = {}
        langs = json_request_response.keys()
        for lang in langs :
            holidays_items[lang] = sorted(json_request_response[lang]['items'], \
                                    key=lambda hol_items: datetime.strptime(hol_items['start']['date'], date_format))
        holidays_by_year = [] 
        # default value, to be update with first holiday year
        year =  0000
        langs.remove('en_US')
        for item in holidays_items['en_US'] :
            holidays_list = []
            hol = {}
            hol['name'] = item['summary']
            for lang in langs :
                hol[lang] = holidays_items[lang][holidays_items['en_US'].index(item)]['summary']
            if item.has_key('description') :
                hol['states'] = item['description'].split(': ')[1].split(', ')
            date_end = datetime.strptime(item['end']['date'], date_format) 
            date_start = datetime.strptime(item['start']['date'], date_format)
            while date_start < date_end :
                if date_start.year != year :
                    year = date_start.year
                    holidays_by_year.append({'year' : year, 'holidays_list' : []})
                hol['date'] = date_start
                holidays_list.append(hol)
                date_start += timedelta(days = 1)
            holidays_by_year[-1]['holidays_list'] += holidays_list
        return holidays_by_year
