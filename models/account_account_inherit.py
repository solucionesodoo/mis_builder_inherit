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
			vals = {
				'type': 'num', 
				'compare_method': 'pct', 
				'accumulation_method': 'sum', 
				'report_id': report_id, 
				'sequence': 3, 
				'description': str(code) + '_' + str(self.normalize_word(name)), 
				'name': str(self.normalize_word(name)).replace(' ', '_') + '_' + str(code), 
				'style_id': False, 
				'style_expression': False, 
				'multi': True, 
				'expression_ids': [[0, 0, {'name': 'bali[1%]', 'kpi_id': x.id, 'subkpi_id': saldo_inicial}], [0, 0, {'name': 'debp[1%]', 'kpi_id': x.id, 'subkpi_id': debito}], [0, 0, {'name': 'crdp[1%]', 'kpi_id': x.id, 'subkpi_id': credito}], [0, 0, {'name': 'bale[1%]', 'kpi_id': x.id, 'subkpi_id': saldo_final}]], 
		
				
					}
			pass

				#x.write({'kpi_ids': [(0,0, vals)]})



AccountAccountInherit()