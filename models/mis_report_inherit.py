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

		return account_ids

	def normalize_word(self, value):
		"""
			Funcion que permite normalizar los caracteres especiales
		"""
		result = ''.join((c for c in unicodedata.normalize('NFD',value) if unicodedata.category(c) != 'Mn'))
		
		return result
		


	def return_vals_sub_kpis(self, value, report_id):
		vals={

			'sequence': 1,
			'report_id': report_id, 
			'name': str(value).lower().replace(' ', '_') if ' ' in value else str(value).lower(), 
			'description': value, 
		}

		return vals





	@api.model
	def load_template_mis_report(self):

		model_mis_report = self.env['mis.report']
		model_mis_report_subkpi = self.env['mis.report.subkpi']
		model_mis_report_kpi = self.env['mis.report.kpi']
		model_mis_report_kpi_expression = self.env['mis.report.kpi.expression']


		#creando reporte
		create_mis_report_template_one = model_mis_report.sudo().create({'name':'Plantilla 1'})
		create_mis_report_template_two = model_mis_report.sudo().create({'name':'Plantilla 2'})


		#creando sub kpis
		create_sub_kpi_saldo_incial = model_mis_report_subkpi.sudo().create(self.return_vals_sub_kpis('Saldo Inicial', create_mis_report_template_one.id))
		create_sub_kpi_debito = model_mis_report_subkpi.sudo().create(self.return_vals_sub_kpis('Debito', create_mis_report_template_one.id))
		create_sub_kpi_credito = model_mis_report_subkpi.sudo().create(self.return_vals_sub_kpis('Credito', create_mis_report_template_one.id))
		create_sub_kpi_saldo_final = model_mis_report_subkpi.sudo().create(self.return_vals_sub_kpis('Saldo Final', create_mis_report_template_one.id))

		create_sub_kpi_saldo_final_ = model_mis_report_subkpi.sudo().create(self.return_vals_sub_kpis('Saldo Final', create_mis_report_template_two.id))


		#agregando sub kpi al reporte
		create_mis_report_template_one.sudo().write({'subkpi_ids': [(6, _, [create_sub_kpi_saldo_incial.id, create_sub_kpi_debito.id, create_sub_kpi_credito.id, create_sub_kpi_saldo_final.id])]})
		create_mis_report_template_two.sudo().write({'subkpi_ids': [(6, _, [create_sub_kpi_saldo_final_.id])]})


		#cargando el plan contable actual
		account_ids = self.return_account_account()

		flag = 0
		sql = """
		INSERT INTO mis_report_kpi (description, name, type, compare_method, accumulation_method, report_id, multi) VALUES
		"""
		values_sql = ""
		for x in account_ids:
			if flag < 10:

				values_sql += '(' + "'" + (str(x.code)  + ' ' + str(self.normalize_word(x.name))) + "'" + ',' + "'" + (str(self.normalize_word(x.name)).replace(' ', '_') + '_' + str(x.code)) + "'" +',' + "'" + 'num' + "'" +',' + "'" + 'pct' + "'" + ',' + "'" + 'sum' + "'" + ','  + (str(create_mis_report_template_one.id)) + ',' +  'True'  '),'

			flag+=1


		sql = sql + values_sql[:len(values_sql)-1]

		print(sql)

		self.env.cr.execute( sql )

		sql_kpi = """INSERT INTO mis_report_kpi_expression (name, kpi_id, subkpi_id) VALUES"""
		value_kpi = ""
		for x in model_mis_report_kpi.search([('report_id', '=', create_mis_report_template_one.id)]):
			value_kpi += "('bali[1%]', " + str(x.id) + "," + str(create_sub_kpi_saldo_incial.id) + "),"
			value_kpi += "('debp[1%]', " + str(x.id) + "," + str(create_sub_kpi_debito.id) + "),"
			value_kpi += "('crdp[1%]', " + str(x.id) + "," + str(create_sub_kpi_credito.id) + "),"
			value_kpi += "('bale[1%]', " + str(x.id) + "," + str(create_sub_kpi_saldo_final.id) + "),"




		sql_kpi = sql_kpi + value_kpi[:len(value_kpi)-1]
		self.env.cr.execute( sql_kpi )
				


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
			'description': str(code) + '_' + str(self.normalize_word(name)), 
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
			'description': str(code) + '_' + str(self.normalize_word(name)), 
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
		
		flag = 0
		for x in account_ids:
			if flag < 10:

				vals = self.return_vals(report_id, x.name, x.code, None)
					
				data.append((0, 0, vals))
			flag+=1
		
		

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


		flag = 0
		for x in account_ids:
			if flag < 10:
			
				vals = self.return_vals_second(report_id, x.name, x.code, None)
				
				data.append((0, 0, vals))
			flag+=1

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

		

MisReportInherit()