# -*- coding: utf-8 -*-

from odoo import api, fields, models


class stock_location(models.Model):
    """
    Override to add features of allowed users
    """
    _inherit = "stock.location"

    @api.depends("own_user_ids", "location_id.own_user_ids", "location_id.user_ids")
    def _compute_user_ids(self):
        
        Users = self.env["res.users"]
        for loc in self:
            parent_users = loc.location_id.user_ids if loc.location_id else Users
            loc.user_ids = parent_users | loc.own_user_ids

    def _inverse_own_user_ids(self):
        
        for loc in self.sudo():
            children = self.env["stock.location"].search([("location_id", "child_of", loc.id)])
            children._compute_user_ids()

    own_user_ids = fields.Many2many(
        comodel_name="res.users",
        relation="res_users_stock_location_own_rel_table",
        column1="stock_location_own_id",   # location id
        column2="res_users_own_id",        # user id
        string="Own Accepted Users",
        inverse="_inverse_own_user_ids",
    )

    user_ids = fields.Many2many(
        comodel_name="res.users",
        relation="res_users_stock_location_rel_table",
        column1="stock_location_id",  # location id
        column2="res_users_id",       # user id
        string="Accepted Users",
        compute="_compute_user_ids",
        compute_sudo=True,
        store=True,
    )

