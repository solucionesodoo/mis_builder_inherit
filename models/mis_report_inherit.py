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

import unicodedata

from odoo import api, fields, models, _
import time
from datetime import datetime, timedelta, date
import logging
_logger = logging.getLogger(__name__)
from odoo import modules
from odoo.addons import decimal_precision as dp


class MisReportInherit(models.Model):

	_inherit = "mis.report"

	TYPE_REPORT = [ ('first', 'Primero'),
					('second', 'Segundo')]

	type_report = fields.Selection(TYPE_REPORT, string="Tipo Reporte")
	default_code = fields.Char(string="Code")

	def return_account_account(self):
		"""
			Funcion que permite retornar todo el plan contable
		"""

		account_ids = self.env['account.account'].search([])


		data_account = []
		aux = []



		#for x in account_ids:
			#print(x.code + ' ' + x.name)

		return account_ids

	def normalize_word(self, value):
		result = ''.join((c for c in unicodedata.normalize('NFD',value) if unicodedata.category(c) != 'Mn'))
		return result
		
	def return_subkpi_ids(self):

		"""
			Funcion que permite retornar los subkpis disponibles
		"""
		expressions = []

		for subkpi in self.subkpi_ids:
			name = ''
			if subkpi.name == 'saldo_inicial':
				name= 'bali[1%]'
			if subkpi.name == 'debito':
				name= 'debp[1%]'
			if subkpi.name == 'credito':
				name= 'crdp[1%]'
			if subkpi.name == 'saldo_final':
				name= 'bale[1%]'

			expressions.append((0, 0, {"name": subkpi.expression_ids[0].name or '', "subkpi_id": subkpi.id}))


		return expressions


	def return_vals(self, report_id, name, code, expression_ids):

		"""
		{'type': 'num', 
		'compare_method': 'pct', 
		'accumulation_method': 'sum', 
		'report_id': 3, 
		'sequence': 3, 
		'description': 'aaaaa', 
		'name': 'aaaaa', 
		'style_id': False, 
		'style_expression': False, 
		'multi': True, 
		'expression_ids': [[0, 'virtual_342', {'name': False, 'subkpi_id': 10}], [0, 'virtual_345', {'name': False, 'subkpi_id': 11}], [0, 'virtual_348', {'name': False, 'subkpi_id': 12}], [0, 'virtual_351', {'name': False, 'subkpi_id': 13}]], 'auto_expand_accounts': False, 'auto_expand_accounts_style_id': False}
				
		"""
		"""
		saldo_inicial = self.env.ref('mis_builder_inherit.data_saldo_inicial')
		debito = self.env.ref('mis_builder_inherit.data_debito')
		credito = self.env.ref('mis_builder_inherit.data_credito')
		saldo_final = self.env.ref('mis_builder_inherit.data_saldo_final')
		"""
		model_mis_report_subkpi = self.env['mis.report.subkpi']
		saldo_inicial = model_mis_report_subkpi.search([('name', '=', 'saldo_inicial')], limit=1).id
		debito = model_mis_report_subkpi.search([('name', '=', 'debito')], limit=1).id
		credito = model_mis_report_subkpi.search([('name', '=', 'credito')], limit=1).id
		saldo_final = model_mis_report_subkpi.search([('name', '=', 'saldo_final')], limit=1).id


		#name = str(name.encode('utf-8'))
		vals = {
			'type': 'num', 
			'compare_method': 'pct', 
			'accumulation_method': 'sum', 
			'report_id': report_id, 
			'sequence': 3, 
			'description': str(code) + ' ' + str(self.normalize_word(name)), 
			'name': str(self.normalize_word(name)).replace(' ', '_') + '_' + str(code), 
			'style_id': False, 
			'style_expression': False, 
			'multi': True, 
			'expression_ids': [[0, 0, {'name': 'bali[1%]', 'subkpi_id': saldo_inicial}], [0, 0, {'name': 'debp[1%]', 'subkpi_id': debito}], [0, 0, {'name': 'crdp[1%]', 'subkpi_id': credito}], [0, 0, {'name': 'bale[1%]', 'subkpi_id': saldo_final}]], 
			#'auto_expand_accounts': False, 
			#'auto_expand_accounts_style_id': False
			
				}

		return vals




	def return_vals_second(self, report_id, name, code, expression_ids):

		model_mis_report_subkpi = self.env['mis.report.subkpi']
		saldo_final = model_mis_report_subkpi.search([('name', '=', 'saldo_final')], limit=1).id

		#name = str(name.encode('utf-8'))

		vals = {
			'type': 'num', 
			'compare_method': 'pct', 
			'accumulation_method': 'sum', 
			'report_id': report_id, 
			'sequence': 3, 
			'description': str(code) + ' ' + str(self.normalize_word(name)), 
			'name': str(self.normalize_word(name)).replace(' ', '_') + '_' + str(code), 
			'style_id': False, 
			'style_expression': False, 
			'multi': True, 
			'expression_ids': [[0, 0, {'name': 'bale[1%]', 'subkpi_id': saldo_final}]], 
			#'auto_expand_accounts': False, 
			#'auto_expand_accounts_style_id': False
			
				}

		return vals

	def create_data(self, report_id):
		"""
			Funcion que permite crear la data para armar el reporte
		"""
		account_ids = self.return_account_account()

		data = []
		
		#expressions = self.return_subkpi_ids()
		#report_id = self.subkpi_ids[0].report_id.id
		

		for x in account_ids:
			

			vals = self.return_vals(report_id, x.name, x.code, None)
				
			data.append((0, 0, vals))
		
		

		#vals['kpi_ids'] = None
		#vals['kpi_ids'] = data
		#self.kpi_ids = None
		#self.kpi_ids = data

		return data



	def create_data_second(self, report_id):
		"""
			Funcion que permite crear la data para armar el reporte
		"""
		account_ids = self.return_account_account()

		flag = 0

		data = []
		
		#expressions = self.return_subkpi_ids()
		#report_id = self.subkpi_ids[0].report_id.id


		for x in account_ids:
			
			vals = self.return_vals_second(report_id, x.name, x.code, None)
			
			data.append((0, 0, vals))
			

		#vals['kpi_ids'] = None
		#vals['kpi_ids'] = data
		#self.kpi_ids = None
		#self.kpi_ids = data

		return data



		#for x in self:

		#	for value in self.kpi_ids:
		#		pass
				#value.write({'multi': True})
				#value.multi = True
				#value._onchange_multi()
				
			
	@api.depends('type_report')
	@api.onchange('type_report')
	def onchange_type_report(self):
		"""
			Funcion que permite cargar todo el plan contable de acuerdo al tipo de reporte
			type report -> 	first
						-> 	Saldo Inicial
							Debito
							Credito
							Saldo Final

			type report -> 	second
						-> 	Saldo Final
							
		"""

		
		#self.create_data(self)


		self.kpi_ids = None

		


	@api.model
	def create(self, vals):


		if 'type_report' in vals:
			print('mira que si')

			if vals['type_report'] == 'first':
				if 'default_code' in vals:
					if vals['default_code'] == 'first':
						vals['kpi_ids'] = None
						vals['kpi_ids'] = self.create_data(self.id)

			if vals['type_report'] == 'second':
				if 'default_code' in vals:
					if vals['default_code'] == 'second':	
						vals['kpi_ids'] = None
						vals['kpi_ids'] = self.create_data_second(self.id)

		res = super(MisReportInherit, self).create(vals)

		return res

	@api.multi
	def write(self, vals):

		#print(self.create_data(self.id))
		report_ids= self.env['mis.report.kpi'].search([('report_id', '=', self.id)])
		
		if report_ids:
			for x in report_ids:
				x.unlink()

		for x in self.kpi_ids:
			for value in x.expression_ids:
				value.multi = True

		if 'type_report' in vals:
			print('mira que si')

			if vals['type_report'] == 'first':
			
				if self.default_code == 'first':

					print('solamente editando el primero')
					vals['kpi_ids'] = None
					vals['kpi_ids'] = self.create_data(self.id)

			if vals['type_report'] == 'second':
				
				if self.default_code == 'second':	
					print('solamente editando el segundo')	
					vals['kpi_ids'] = None
					vals['kpi_ids'] = self.create_data_second(self.id)

		res = super(MisReportInherit, self).write(vals)

		return res







MisReportInherit()