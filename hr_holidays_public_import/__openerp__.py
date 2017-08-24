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
# Created:               Jul 24, 2017 11:42:46 AM by atrabelsi
# Last modified:      2017-07-24 11:42
#
# Last Author:           $LastChangedBy$
# Last Checkin:          $LastChangedDate$
# Checked out Version:   $LastChangedRevision$
# HeadURL:               $HeadURL$
# --------------------------------------------------------------------------------
{
    'name' : 'Import HR Public Holidays',
    'version' : '8.0.1.0.0',
    'category' : 'Human Resources',
    'author' : 'Infolava',
    'website' : 'http://www.infolava.ch',
    'summary' : "Import Public Holidays From External Provider",
    'depends' : [
                 'hr_public_holidays',
                 'hr_contract',
                ],
    'data': [
             'views/inherited_res_config.xml',
             'views/calendar_provider_view.xml',
             'views/public_holidays_import_wizard_view.xml',
             'views/templates.xml',
             'data/calendar_provider.xml',
             'security/calendar_provider_access.xml'
            ],
    'qweb': ['static/src/xml/import.xml'],
    'installable': True,
    'application' : True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
#eof $Id$