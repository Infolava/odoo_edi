from openerp import models, fields, api, _ 
from openerp.exceptions import AccessError, ValidationError, Warning
import json
import urllib2

class calendar_provider(models.Model):
    """Class defining the configuration values of a Calendar provider"""

    _name = 'calendar.provider'
    _description = 'Model to handle calendar provider parameters'

    provider_name = fields.Char('Provider Name')
    provider_url = fields.Char('Provider URL')
    provider_api_key = fields.Char('Provider API key')
   
    def provider_response_parser(self, json_request_response):
        return []
   
    @api.multi
    def request_handler(self, country_code, lang_code, year):
        headers = {
                   'Content-Type': 'application/json',
                   }
        url = self.provider_url.format(country = country_code, lang = lang_code, api_key = self.provider_api_key, year = year)
        request = urllib2.Request(url, headers = headers)
        try :
            res = urllib2.urlopen(request)
            response = res.read()
            json_response = json.loads(response)
            res.close()
        except urllib2.HTTPError as e:
            if e.code == 404 :
                #TODO fix HTTPError for unsupported language 
                #TODO fix HTTPError for unsupported country
                raise ValidationError(_('Unsupported language or country'))
            elif e.code == 400 :
                raise AccessError(_('Please contact your administration to verify API key configuration'))
            else :
                #TODO Test other HTTPError
                raise ValidationError(_('Unknown error'))
        return self.provider_response_parser(json_response)


class goolglecalendar_provider(models.Model):
    """Class defining the response parser of Gogle Calendar provider"""

    _inherit = 'calendar.provider'
    _description = 'Google Calendar Provider Parameters'

#     provider_name = "Google Calendar"
#     provider_url = "https://www.googleapis.com/calendar/v3/calendars/{country}__{lang}%40holiday.calendar.google.com/events?key={api_key}"
#     provider_api_key = "admin"
   
    def provider_response_parser(self, json_request_response, date_format = "%Y-%m-%d"):
        from datetime import datetime, timedelta
        if not json_request_response['items'] :
            raise Warning(_('No Data Provided for selected country'))
        # sort holidays list by start date
        holidays_items = sorted(json_request_response['items'], \
                                key=lambda hol_items: datetime.strptime(hol_items['start']['date'], date_format))
        holidays_by_year = [] 
        # default value, to be update with first holiday year
        year =  0000
        for item in holidays_items :
            holidays_list = []
            hol = {}
            hol['name'] = item['summary']
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