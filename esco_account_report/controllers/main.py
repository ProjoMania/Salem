# -*- coding: utf-8 -*-

from odoo import fields, http, tools, _
from odoo.exceptions import UserError

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.http import request
from datetime import datetime
from pathlib import Path
from dateutil.relativedelta import relativedelta
import json
import os
from os import path
import base64
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect
from PIL import Image
import math
import io
import base64
from odoo.http import content_disposition, request
from odoo.tools import html_escape
from odoo.addons.web.controllers.main import _serialize_exception


class XLSXReportController(http.Controller):

	@http.route('/xlsx_reports', type='http', auth='user', methods=['POST'], csrf=False)
	def get_report_xlsx(self, model, options, output_format, token, report_name, **kw):
		uid = request.session.uid
		report_obj = request.env[model].with_user(uid)
		options = json.loads(options)
		try:
			if output_format == 'xlsx':
				response = request.make_response(
					None,
					headers=[
						('Content-Type', 'application/vnd.ms-excel'),
						('Content-Disposition', content_disposition(report_name + '.xlsx'))
					]
				)
				report_obj.get_xlsx_report(options, response)
			response.set_cookie('fileToken', token)
			return response
		except Exception as e:
			se = _serialize_exception(e)
			error = {
				'code': 200,
				'message': 'Odoo Server Error',
				'data': se
			}
			return request.make_response(html_escape(json.dumps(error)))
