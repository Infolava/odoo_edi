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
# Created:               Sep 8, 2017 12:03:01 PM by atrabelsi
# Last modified:      2017-09-08 12:03
#
# Last Author:           $LastChangedBy$
# Last Checkin:          $LastChangedDate$
# Checked out Version:   $LastChangedRevision$
# HeadURL:               $HeadURL$
# --------------------------------------------------------------------------------
from openerp import fields, models, api

class calendar_provider_wizard(models.TransientModel):
    _name = 'api.config'
    _inherit = 'res.config.installer' #needed to launch config wizard
    _description = 'Transient model to set up API Key for calendar providers'
    
    provider_ids = fields.Many2many('calendar.provider')

    @api.model
    def default_get(self, fields_list):
        defaults = super(calendar_provider_wizard, self).default_get(fields_list)
        defaults['provider_ids'] = self.env['calendar.provider'].search([]).ids
        return defaults
    
    @api.multi
    def action_next(self):
        cron = self.env['ir.model.data'].get_object_reference( 'hr_holidays_public_import', 'automate_public_holidays_import')
        self.env['ir.cron'].browse(cron[1]).active = True
        return super(calendar_provider_wizard, self).action_next()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
#eof $Id$