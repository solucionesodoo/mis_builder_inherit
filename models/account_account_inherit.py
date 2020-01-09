# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    Autor: Brayhan Andres Jaramillo Castaño
#    Correo: brayhanjaramillo@hotmail.com
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

from odoo import api, fields, models, _
import time
from datetime import datetime, timedelta, date
import logging
_logger = logging.getLogger(__name__)
from odoo import modules
from odoo.addons import decimal_precision as dp

class AccountAccountInherit(models.Model):

	_inherit = "account.account"


	@api.multi
	def update_report_mis(self):

		print('estamos creando en account')

		model_mis_report = self.env['mis.report']

		for x in model_mis_report.sudo().search([]):

			report_ids = self.env['mis.report.kpi'].search([('report_id', '=', x.id)])
			
			if report_ids:
				for value in report_ids:
					
					value.unlink()

		for x in model_mis_report.sudo().search([]):
			if x.default_code:
				if x.type_report == 'first':
					print('listo')
					x.kpi_ids = model_mis_report.create_data(x.id)
				if x.type_report == 'second':
					print('listooooo')
					x.kpi_ids = model_mis_report.create_data_second(x.id)



AccountAccountInherit()