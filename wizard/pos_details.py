# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import time
from datetime import datetime
import psycopg2
# from pytz import timezone, UTC

# import pytz
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class PosDetails(models.TransientModel):
    _name = 'pos.details.wizard'
    _description = 'Point of Sale Details Report'

    '''def _default_start_date(self):

        today = datetime.now()
        today.strftime('%Y-%m-%d %H:%M:%S')
        ff = datetime.strftime(today, '%Y-%m-%d %H:%M:%S')
        # print(' equis2 ', result_utc_datetime.strftime(fmt))
        dt = ff
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'MST')
        date_tz = pytz.UTC.localize(datetime.strptime(dt, DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(user_tz)
        print(date_tz, fields.Datetime.to_string(date_tz))
        print(' equis ', ff)
        return fields.Datetime.to_string(date_tz)

    def _default_end_date(self):
        fecha_hoy = time.strftime("%Y-%m-%d", time.localtime())
        dt = datetime.strptime(str(fecha_hoy), '%Y-%m-%d')
        old_tz = pytz.timezone('UTC')
        new_tz = pytz.timezone('MST')
        fecha_hoy = old_tz.localize(dt).astimezone(new_tz)
        ff = datetime.strftime(fecha_hoy, '%Y-%m-%d')

        fecha_dma3 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dt = datetime.strptime(str(fecha_dma3), '%Y-%m-%d %H:%M:%S')
        fecha_dma3 = datetime.strftime(dt, '%Y-%m-%d')
        hora = datetime.strftime(dt, '%H:%M:%S')
        if hora >= '07:00:00' and hora <= '14:59:59':
            fecha_dma3 = fecha_dma3 + ' 14:59:00'
        if hora >= '15:00:00' and hora <= '22:59:59':
            fecha_dma3 = fecha_dma3 + ' 22:59:59'
        if hora >= '23:00:00' and hora <= '23:59:59' or hora >= '00:00:00' and hora <= '06:59:59':
            ff = fecha_dma3 + ' 07:00:00'
            fecha_dma3 = ''
        print(ff, 'fecha', hora)
        return fecha_dma3 or ff'''

    start_date = fields.Datetime(required=True, default=fields.Datetime.now)
    end_date = fields.Datetime(required=True, default=fields.Datetime.now)

    pos_config_ids = fields.Many2many('pos.config', 'pos_detail_configs',
        default=lambda s: s.env['pos.config'].search([]))

    '''@api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.end_date and self.end_date < self.start_date:
            self.start_date = self.end_date'''

    def generate_report(self):
        data = {'date_start': self.start_date, 'date_stop': self.end_date, 'config_ids': self.pos_config_ids.ids}
        return self.env.ref('point_of_sale.sale_details_report').report_action([], data=data)
