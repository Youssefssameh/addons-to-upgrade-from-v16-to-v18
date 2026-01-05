# -*- coding: utf-8 -*-

from odoo import api, models


class StockQuant(models.Model):
    """
    Override to avoid security bugs when walking up location hierarchy.
    """
    _inherit = "stock.quant"

    @api.model
    def _get_removal_strategy(self, product_id, location_id):
        """
        Return removal strategy method.
        - If product category has a forced removal strategy: use it.
        - Else walk up the location hierarchy (under sudo) to find a strategy.
        """
        # Product category strategy first (same logic as your code)
        if product_id.categ_id.removal_strategy_id:
            return product_id.categ_id.removal_strategy_id.method

        loc = location_id
        while loc:
            if loc.removal_strategy_id:
                return loc.removal_strategy_id.method
            # move to parent under sudo to avoid access issues
            loc = loc.sudo().location_id

        # Default
        return "fifo"
