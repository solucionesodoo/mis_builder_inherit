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

class MisReportKpiInherit(models.Model):

	_inherit = "mis.report.kpi"

	name = fields.Char(size=255, required=True, string="Name")

	@api.onchange("multi")
	def _onchange_multi(self):
		for kpi in self:
			if not kpi.multi:
				if kpi.expression_ids:
					kpi.expression = kpi.expression_ids[0].name
				else:
					kpi.expression = None
			else:
				expressions = []
				for subkpi in kpi.report_id.subkpi_ids:
					expressions.append(
						(0, 0, {"name": kpi.expression, "subkpi_id": subkpi.id})
					)
				kpi.expression_ids = None   
				kpi.expression_ids = expressions


MisReportKpiInherit()