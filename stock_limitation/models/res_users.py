# -*- coding: utf-8 -*-

from odoo import fields, models


class ResUsers(models.Model):
    """
    Override to let assign allowed locations on a user form
    """
    _inherit = "res.users"

    def _inverse_location_ids(self):
        """
        Inverse method for location_ids.
        The goal is to make sure location users are re-computed recursively

        Methods:
         * _compute_user_ids of stock.location
        """
        for user in self.sudo():
            user.location_ids._compute_user_ids()

    location_ids = fields.Many2many(
        comodel_name="stock.location",
        relation="res_users_stock_location_own_rel_table",
        column1="res_users_own_id",        # user id
        column2="stock_location_own_id",   # location id
        string="Available Locations",
        inverse="_inverse_location_ids",
        help="User would have access to these locations and their child locations.",
    )
