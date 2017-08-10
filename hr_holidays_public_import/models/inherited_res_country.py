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
# Created:               Aug 10, 2017 1:43:06 PM by atrabelsi
# Last modified:      2017-08-10 13:43
#
# Last Author:           $LastChangedBy$
# Last Checkin:          $LastChangedDate$
# Checked out Version:   $LastChangedRevision$
# HeadURL:               $HeadURL$
# --------------------------------------------------------------------------------
from openerp import  models

class res_state(models.Model):
    _name = 'res.country.state'
    _inherit = 'res.country.state'
    
    
    def get_state_id_from_name(self, state_name, country_id) :
        st_code = state_name[0:3].upper()
        state= self.search([('name', 'ilike', state_name), \
                                                      ('country_id', '=', country_id)])
        return state[0].id if state else self.create({'name' : state_name, \
                                                   'country_id': country_id,
                                                   'code' : st_code}).id
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
#eof $Id$