# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from openerp import models, fields, tools, api

class base_config_settings(models.TransientModel):
    
    _name = 'base.config.settings'
    _inherit = 'base.config.settings'

    provider_name = fields.Char('Calendar Provider Name')
    provider_api_key = fields.Char('Calendar Provider API key')
    provider_url = fields.Char('Calendar Provider URL')

    def default_get(self, cr, uid, fields, context=None):
        res = super(base_config_settings, self).default_get(cr, uid, fields, context=context)
        res.update(self.get_calendar_providers(cr, uid, fields, context=context))
        return res

    def get_calendar_providers(self, cr, uid, fields, context=None):
#         googlecalendar_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'hr_holidays_public_import', 'provider_googlecalendar')[1]
#         googlecalendar= self.pool.get('calendar.provider').read(cr, uid, [googlecalendar_id], context = context)[0]
        return {
            'provider_name': tools.config.options['provider_name'] or 'Google Calendar',
            'provider_api_key': tools.config.options['provider_api_key'] or 'admin',
            'provider_url': tools.config.options['provider_url'] or "https://www.googleapis.com/calendar/v3/calendars/{country}__{lang}%40holiday.calendar.google.com/events?key={api_key}",
        }
        
    @api.multi
    def set_calendar_providers(self):
        self.ensure_one()
        calendar_param = {
            'provider_name' : self.provider_name,
            'provider_api_key' : self.provider_api_key,
            'provider_url' : self.provider_url,
        }

        self.pool.get('calendar.provider').write(self._cr, self._uid, [1], calendar_param)

base_config_settings()