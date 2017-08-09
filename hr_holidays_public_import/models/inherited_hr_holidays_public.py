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
from datetime import date, datetime
from openerp import fields, models, api, _
from openerp.exceptions import ValidationError, Warning

from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class HrPublicHolidays(models.Model):
    _name = 'hr.holidays.public'
    _inherit = 'hr.holidays.public'
        
    def import_public_holidays_by_country(self, country, lang, year):
        provider = self.env['calendar.provider'].browse(1)
        holidays_list = provider.request_handler(country.code, lang, year)
        for year in holidays_list:
            year_rec = self.search([('year', '=', year['year']), ('country_id', '=', country.id)])
            year_id = year_rec[0].id if year_rec else self.create({'year':year['year'], 'country_id':country.id}).id
            for hol in year['holidays_list']:
                hol.update({'year_id':year_id})
                line = self.env['hr.holidays.public.line'].search([('year_id', '=', year_id), ('date', '=', datetime.strftime(hol['date'], DF))])
                if line :
                    line[0].name = hol['name']
                else :
                    self.env['hr.holidays.public.line'].create(hol)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
#eof $Id$