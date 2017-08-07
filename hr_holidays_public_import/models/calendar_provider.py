from openerp import models, fields, api, _ 

class calendar_provider(models.Model):
    """Class defining the configuration values of a Calendar provider"""

    _name = 'calendar.provider'
    _description = 'Model to handle calendar provider parametres'

    provider_name = fields.Char('Provider Name')
    provider_url = fields.Char('Provider URL')
    provider_api_key = fields.Char('Provider API key')
    provider_response_parser = fields.Text('Provider response parser')
   
