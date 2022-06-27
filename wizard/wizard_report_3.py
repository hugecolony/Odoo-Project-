'''
Created on Aug 6, 2021

@author: abdullah
'''
from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError, Warning as UserError


class CMSWizardStudentReport(models.TransientModel):
    _name = 'hms.wizard.student.report'
    _description = 'Hostel Student Report Wizard'

    from_date = fields.Date('From Date', default=lambda * a: date.today())
    to_date = fields.Date('To Date', default=lambda * a: date.today())
    
    def print_report3(self):
        data = self.read()[0]
        print("------------------------")
        ids = self.env['hms.student'].search([('date_of_birth','>=',self.from_date),('date_of_birth','<=',self.to_date)]).ids
        return self.env.ref('hms_student.report_qweb_3_id').report_action(ids, data=data)
