from odoo import models, fields

class CustomJournalReportHandler(models.AbstractModel):
    _inherit = 'account.journal.report.handler'

    def _query_journal_with_cuit(self, options):
        """
        Consulta personalizada para incluir el campo CUIT del partner.
        """
        query = """
            SELECT
                aml.id,
                aml.date,
                aml.name,
                aml.partner_id,
                partner.vat AS partner_cuit,
                -- Otros campos que puedas necesitar
            FROM
                account_move_line aml
            LEFT JOIN
                res_partner partner ON aml.partner_id = partner.id
            WHERE
                -- Aquí puedes agregar condiciones adicionales según tus necesidades
        """
        # Ejecutar la consulta y procesar los resultados
        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        return result

    def _dynamic_lines_generator(self, report, options, all_column_groups_expression_totals, warnings=None):
        # Obtener las líneas del reporte original
        lines = super()._dynamic_lines_generator(report, options, all_column_groups_expression_totals, warnings)

        cuit_lines = self._query_journal_with_cuit(options)

        for line in cuit_lines:
            lines.append({
                'id': line['id'],
                'name': line['name'],
                'columns': [
                    {'name': line.get('partner_cuit', '')},  # Agrega el CUIT aquí
                ],
            })

        return lines