from odoo import models, fields, api


class TDSBomLine(models.Model):
    _inherit = "mrp.bom.line"

    tds_cost = fields.Float(string="Cost",related="product_id.standard_price",readonly=True)
    tds_avg_cost = fields.Float(string="Total Cost", compute="_calc_avg_cost", store=True)

    @api.depends("tds_cost", "product_qty")
    def _calc_avg_cost(self):
        for line in self:
            line.tds_avg_cost = (line.tds_cost or 0.0) * (line.product_qty or 0.0)


class TDSBom(models.Model):
    _inherit = "mrp.bom"

    total_tds_cost = fields.Float(string="Total Components Cost", compute="_calc_total_tds_cost", store=True)
    tds_avg_cost = fields.Float(string="Avg Cost", compute="_calc_tds_avg_cost", store=True)

    @api.depends("bom_line_ids.tds_avg_cost")
    def _calc_total_tds_cost(self):
        for bom in self:
            bom.total_tds_cost = sum(bom.bom_line_ids.mapped("tds_avg_cost"))

    @api.depends("total_tds_cost", "product_qty")
    def _calc_tds_avg_cost(self):
        for bom in self:
            qty = bom.product_qty or 0.0
            bom.tds_avg_cost = (bom.total_tds_cost / qty) if qty else 0.0
