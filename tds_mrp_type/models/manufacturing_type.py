from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ManufacturingType(models.Model):
    _name = "manufacturing.type"
    _description = "Manufacturing Type"

    name = fields.Char(string="Description", required=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("unique_mrp_type_name", "unique (name, active)", "Description must be unique."),
    ]


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    mrp_type_id = fields.Many2one(
        "manufacturing.type",
        string="Manufacturing Type",
        required=True,
        index=True,
    )


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    # User selects this first (like your old behavior).
    mrp_type_id = fields.Many2one(
        "manufacturing.type",
        string="Manufacturing Type",
        tracking=True,
    )

    # Filter BoMs by selected manufacturing type + keep Odoo standard conditions.
    bom_id = fields.Many2one(
        "mrp.bom",
        string="Bill of Material",
        readonly=False,
        compute="_compute_bom_id",
        store=True,
        precompute=True,
        check_company=True,
        domain="""
            [
                '&',
                    '|', ('company_id', '=', False), ('company_id', '=', company_id),
                '&',
                    '|',
                        ('product_id', '=', product_id),
                        '&',
                            ('product_tmpl_id.product_variant_ids', '=', product_id),
                            ('product_id', '=', False),
                '&',
                    ('type', '=', 'normal'),
                    ('mrp_type_id', '=', mrp_type_id)
            ]
        """,
        help="Bill of Materials allow you to define the list of required components to make a finished product.",
    )

    @api.onchange("mrp_type_id")
    def _onchange_mrp_type_id(self):
        # If user changes manufacturing type, clear BoM if it no longer matches.
        for mo in self:
            if mo.bom_id and mo.mrp_type_id and mo.bom_id.mrp_type_id != mo.mrp_type_id:
                mo.bom_id = False

    @api.onchange("bom_id")
    def _onchange_bom_id_set_mrp_type(self):
        # If user picks a BoM, enforce manufacturing type from BoM (keeps them consistent).
        for mo in self:
            if mo.bom_id and mo.bom_id.mrp_type_id:
                mo.mrp_type_id = mo.bom_id.mrp_type_id

    @api.constrains("mrp_type_id", "bom_id")
    def _check_mrp_type_matches_bom(self):
        for mo in self:
            if mo.bom_id and mo.mrp_type_id and mo.bom_id.mrp_type_id != mo.mrp_type_id:
                raise ValidationError(
                    _("Manufacturing Type must match the Manufacturing Type on the selected BoM.")
                )


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _prepare_mo_vals(
        self, product_id, product_qty, product_uom, location_dest_id,
        name, origin, company_id, values, bom
    ):
        # Must use super() for Odoo 18 compatibility.
        mo_vals = super()._prepare_mo_vals(
            product_id, product_qty, product_uom, location_dest_id,
            name, origin, company_id, values, bom
        )

        # When MO is created from procurement with a BoM, force manufacturing type from that BoM.
        if bom and bom.mrp_type_id:
            mo_vals["mrp_type_id"] = bom.mrp_type_id.id

        return mo_vals
