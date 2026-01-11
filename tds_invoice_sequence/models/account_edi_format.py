from odoo import api, models

class AccountEdiFormat(models.Model):
    _inherit = "account.edi.format"

    @api.model
    def _l10n_eg_eta_prepare_eta_invoice(self, invoice):
        eta_invoice=super(AccountEdiFormat,self.sudo())._l10n_eg_eta_prepare_eta_invoice(invoice)
        eta_invoice["internalID"]=invoice.split('/')[-1]
        return eta_invoice