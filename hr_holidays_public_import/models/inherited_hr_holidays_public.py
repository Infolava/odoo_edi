# -*- encoding: utf-8 -*-
# --------------------------------------------------------------------------------
# Project:               TransALM
# Copyright:           © 2017 Infolava GmbH. All rights reserved.
# License:
# --------------------------------------------------------------------------------
#    This file is part of TransALM
#
#    TransALM is free software: you can redistribute it and/or modify
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------
# Created:               Aug 7, 2017 3:52:34 PM by atrabelsi
# Last modified:      2017-08-07 15:52
#
# Last Author:           $LastChangedBy$
# Last Checkin:          $LastChangedDate$
# Checked out Version:   $LastChangedRevision$
# HeadURL:               $HeadURL$
# --------------------------------------------------------------------------------
from datetime import datetime , date
from openerp import fields, models, api, _
from openerp.exceptions import ValidationError, Warning

from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
import logging

_logger =  logging.getLogger(__name__)

class HrPublicHolidays(models.Model):
    _name = 'hr.holidays.public'
    _inherit = 'hr.holidays.public'


    
    @api.model
    def import_public_holidays_by_country(self, provider, country, start_year, end_year):
        def _get_state_ids_from_name(state_names, country_id) :
            st_ids = []
            for st_name in state_names :
                st_ids.append(self.env['res.country.state'].get_state_id_from_name(st_name, country_id))
            return st_ids
        
        def _check_translation(resource_name, lang, hol, resource_id):
            tr = self.env['ir.translation'].is_translation_exist(resource_name, 
                                                                 hol['name'], 
                                                                 lang, 
                                                                 resource_id)
            if tr:
                tr.write({'value':hol[lang] if hol.has_key(lang) else hol['name']})
            else:
                self.env['ir.translation'].create({'name' : 'hr.holidays.public.line,name', \
                                                   'lang' : lang, \
                                                   'src' : hol['name'], \
                                                   'value' : hol[lang] if hol.has_key(lang) else hol['name'], \
                                                   'res_id' : resource_id, \
                                                   'type':'model'
                                                   })
        # get list of loaded languages
        lang_codes = [lang.code for lang in self.env['res.lang'].search([])]
        # Ensure English is on loaded language list 
        if 'en_US' not in lang_codes :
            lang_codes.insert('en_US', 0)
        country_code = provider.get_country_code_from_provider(country)
        holidays_list = provider.request_handler(country_code, lang_codes, start_year, end_year)
        lang_codes.remove('en_US')
        for year in holidays_list :
            year_rec = self.search([('year', '=', year['year']), ('country_id', '=', country.id)])
            year_id = year_rec[0].id if year_rec else self.create({'year':year['year'], \
                                                                   'country_id':country.id}).id
            for hol in year['holidays_list']:
                hol.update({'year_id':year_id})
                hol.update({'state_ids' : False})
                if hol.has_key('states') :
                    hol.update({'state_ids' : [[6, False, _get_state_ids_from_name(hol['states'], country.id)]]})
                    del hol['states']
                else :
                    hol.update({'state_ids' : [[6, False, []]]})
                lines = self.env['hr.holidays.public.line'].search([('year_id', '=', year_id), \
                                                                   ('date', '=', datetime.strftime(hol['date'], DF)),\
                                                                   ])
                line = False
                for cpt in lines :
                    if sorted(cpt.state_ids.ids) == sorted(hol['state_ids'][0][2]) :
                        line = cpt
                        line.name = hol['name']
                        break
                if not line :
                    line = self.env['hr.holidays.public.line'].create(hol)
                for lang in lang_codes :
                    _check_translation('hr.holidays.public.line,name', lang, hol, line.id)
                    _check_translation('calendar.event,name', lang, hol, line.event_id.id)

    def automate_import_public_holidays(self, cr, uid, context = None):
        provider_ids = self.pool.get('calendar.provider').search(cr, uid, [])
        providers = self.pool.get('calendar.provider').browse(cr, uid, provider_ids)
        start_year = date.today().year
        end_year = date.today().year + 10
        employee_ids = self.pool.get('hr.employee').search(cr, uid, [])
        for country in self.pool.get('hr.employee')._get_employees_countries(cr, uid, employee_ids, context) :
            for provider in providers :
                try :
                    self.import_public_holidays_by_country(cr, uid, provider[0], country, start_year, end_year, context)
                    break
                except Exception, e:
                    _logger.warning('Could not import public holidays with provider %s.\n %s' %(provider.provider_name, e.message))
                    
class HrPublicHolidaysLine(models.Model):
    _inherit = 'hr.holidays.public.line'

    name = fields.Char('Name', required=True,  translate = True)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
#eof $Id$
