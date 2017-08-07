# -*- encoding: utf-8 -*-
# --------------------------------------------------------------------------------
# Project:               TransALM
# Copyright:           © 2017 All rights reserved.
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
# Created:               Aug 7, 2017 11:16:49 AM by hbouzidi
# Last modified:      2017-08-07 11:16
#
# Last Author:           $LastChangedBy$
# Last Checkin:          $LastChangedDate$
# Checked out Version:   $LastChangedRevision$
# HeadURL:               $HeadURL$
# --------------------------------------------------------------------------------

from openerp import models, fields, api, _ 
from openerp.exceptions import except_orm

class hr_contract(models.Model):
    _name = 'hr.contract'
    _inherit = 'hr.contract'
    _descripton = 'Manage contract by state'
    
    state_id = fields.Many2one('res.country.state', string= 'State', ondelete = 'restrict', required = True)
    
    @api.multi
    def write(self, values):
        if values.has_key('state_id'):
            raise except_orm(_("You cannot modify the state of the current contract"), self.state_id.name)
        return super(hr_contract,self).write(values)
    

    

