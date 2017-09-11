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
from openerp import fields, models, api
from datetime import date

class HrPublicHolidaysWizard(models.TransientModel):
    _name = 'hr.holidays.public.wizard'
    _description = 'Transient model to import public holidays'
    
    country_id = fields.Many2one('res.country', 'Country')
    provider_id = fields.Many2one('calendar.provider', 'Calendar Provider')
    provider_name = fields.Char('Provider Name', related = 'provider_id.provider_name')
    year_start = fields.Integer('Starting Year', size = 4 , default=date.today().year)
    year_end = fields.Integer('Ending Year', size = 4, default=date.today().year + 1)
    
    @api.model
    def default_get(self, fields_list):
        defaults = super(HrPublicHolidaysWizard, self).default_get(fields_list)
        if self._context.has_key('active_ids') and self._context['active_ids'] :
            pub_hol = self.env['hr.holidays.public'].browse(self._context['active_ids'])[0]
            defaults['country_id'] = pub_hol['country_id'].id
            defaults['year_start'] = pub_hol['year']
            defaults['year_end'] = pub_hol['year'] + 1
        return defaults
    
    @api.multi
    def import_public_holidays(self):
        return self.env['hr.holidays.public'].import_public_holidays_by_country(self.provider_id, self.country_id, self.year_start, self.year_end)
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
#eof $Id$