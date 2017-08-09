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
        
class HrPublicHolidaysWizard(models.TransientModel):
    _name = 'hr.holidays.public.wizard'
    _description = 'Transient model to import public holidays'
    
    country_id = fields.Many2one('res.country', 'Country')
    lang_id = fields.Many2one('res.lang', 'Language')
    
    @api.multi
    def import_public_holidays(self):
        lang = self.lang_id.code.split('_')[0]
        year = "2017"
        return self.env['hr.holidays.public'].import_public_holidays_by_country(self.country_id, lang, year)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
#eof $Id$