# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError, ValidationError

class HMSDepartment(models.Model):
    _name = 'hms.department'
    _description = 'Department Information'

    name = fields.Char('Department Name', required=True)
    student_ids = fields.One2many('hms.student', 'department_id', string='Students')

class HMSStudent(models.Model):
    _name = 'hms.student'
    _description = 'Student Information'

    name = fields.Char('Student Name', required=True)
    father_name = fields.Char('Father Name', required=True)
    registration_no = fields.Char(string='Registration No.', required=True)
    cnic = fields.Char(string='Student CNIC')
    contact_phone = fields.Char('Phone no.')
    department_id = fields.Many2one('cms.department', string='Department')

    contact_mobile = fields.Char('Mobile no')
    image = fields.Binary('image')
    admission_date = fields.Date('Admission Date', default=date.today())
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender', states={'done': [('readonly', True)]}, required=True)

    user_id = fields.Many2one('res.users', string='Responsible', readonly=True, default=lambda self: self.env.user)
    date_of_birth = fields.Date('Date of Birth')
    age = fields.Integer(compute='_compute_student_age', string='Age', readonly=True)
    admission_no = fields.Char(string='Admission No.', readonly=True)

    remark = fields.Text('Remark', states={'done': [('readonly', True)]})

    state = fields.Selection([('draft', 'Draft'), ('verified', 'Verified'), ('approved', 'Approved'),
                              ('cancelled', 'Cancelled')], 'Status', readonly=True, default="draft")

    active = fields.Boolean(default=True)


    @api.depends('date_of_birth')
    def _compute_student_age(self):
        '''Method to calculate student age'''
        current_date = date.today()
        for rec in self:
            if rec.date_of_birth:
                start = rec.date_of_birth
                age = (current_date - start).days / 365
                # Age should be greater than 0
                if age > 0.0:
                    rec.age = age
                else:
                    rec.age = 0
            else:
                rec.age = 0

    def set_to_draft(self):
        '''Method to change state to draft'''
        self.state = 'draft'

    def set_to_verified(self):
        '''Method to change state to verified'''
        self.state = 'verified'

    def set_to_approved(self):
        '''Method to change state to approved'''

        if self.admission_date:
            year = self.admission_date.year
            self.admission_no  = str(year) + "-" + self.env['ir.sequence'].next_by_code('hms.student.code')
        else:
            raise ValidationError(_('Please enter admission date for student %s)', self.name))

        self.state = 'approved'

    def set_to_cancelled(self):
        '''Set the state to cancelled'''
        self.state = 'cancelled'


class HMSEmployee(models.Model):
    _name = 'hms.employee'
    _description = 'Employee Information'

    name = fields.Char('Teacher Name', required=True)
    father_name = fields.Char('Father Name', required=True)
    employee_no = fields.Char('Employee No.', required=True)
    cnic = fields.Char(string='Employee CNIC')
    is_teacher = fields.Boolean("Is Teacher", default=True)
    active = fields.Boolean(default=True)

class HMSHostel(models.Model):
    _name = 'hms.hostel'
    _description = 'Hostel Information'

    name  = fields.Char('Hostel Name', required=True)
    hostel_address = fields.Char('Hostel Address', required=True)
    #cnic = fields.Char(string='Student CNIC')
    contact_phone = fields.Char('Hostel Phone no.')
    contact_mobile = fields.Char('Hostel Mobile no')
    image = fields.Binary(string = 'image')
    remark = fields.Text('Remark', states={'done': [('readonly', True)]})

    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancelled', 'Cancelled')],
                             'Status', readonly=True, default="draft")

    active = fields.Boolean(default=True)

    maximum_capacity = fields.Char(string='max_capacity', required=True)
    short_name = fields.Char('Short Title')
    notes = fields.Text('Internal Notes')
    state = fields.Selection([('draft','Not Available'),
                              ('approved', 'Approved')
                              ],
                             'State')
    description = fields.Html("Description",sanitize=True,strip_style=False)
    #admission_date = fields.Date('Admission Date', default=date.today())
    #gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender', states={'done': [('readonly', True)]})
    #user_id = fields.Many2one('res.users', string='Responsible', readonly=True, default=lambda self: self.env.user)
    date_started = fields.Date('Date Started', required=True)
    #age = fields.Integer(compute='_compute_student_age', string='Age', readonly=True)

#    hostel_ids = fields.Many2many(
 #       'res.partner',
  #      string= 'Hostels'
   # )
class HmsHouseKeeping(models.Model):
    _name = "hms.housekeeping"
    _description = "Hostel HouseKeeping"


    date = fields.Datetime(string = "Todays date",required = True)
    room_no = fields.Many2one("hms.hostel_rooms",string = "Room No",required = True)
    Inspect_Date = fields.Datetime("Inspect Date time",required = True)
    clean_type = fields.Selection([('monthly','Monthly'),
                              ('weekly', 'Weekly'),
                              ('daily', 'Daily')],
                             'Clean Type',default = "available")
    Inspector = fields.Selection([('administrator','Administrator'),
                              ('warden', 'Warden'),
                              ('secretary', 'Secretary')],
                             'Inspector' ,default = "available")

    Condition = fields.Selection([('excellent','Excellent'),
                              ('good', 'Good'),
                                ('poor', 'Poor')],
                             'Condition')

    active = fields.Boolean(default=True)
    state = fields.Selection([('draft', 'Draft'), ('verified', 'Verified'), ('approved', 'Approved'),
                              ('cancelled', 'Cancelled')], 'Status', readonly=True, default="draft")


    def set_to_draft(self):
            '''Method to change state to draft'''
            self.state = 'draft'

    def set_to_verified(self):
        '''Method to change state to verified'''
        self.state = 'verified'


    def set_to_cancelled(self):
        '''Set the state to cancelled'''
        self.state = 'cancelled'





class HMSDepositPaymentPolicy(models.Model):
    _name  = "hms.deposit_policy"
    _description = "Hostel Deposit Payment Policy"

    From_date = fields.Datetime("From Date",required=True)
    name = fields.Char(string = "Policy Name" , required= True)
    Percentage =  fields.Float("Percentage")
    Minimum_deposit_Amount = fields.Float("Minimum Deposit Amount",required = True)
    End_date = fields.Datetime("End Date",required=True)
    short_description = fields.Char(string = "Short Description" , required = True)
    Calculation_category_type = fields.Selection([('weekly','Weekly'),
                              ('bitweekly', 'BitWeekly'),
                              ('Monthly', 'Monthly'),
                              ('Yearly', 'Yearly'),],
                             'Calculation Category ')
    taxes =fields.Integer(string = "Taxes",default =0.15)
    fixed_charges = fields.Boolean(string = "Fixed Charges")
    bookable_packages = fields.Boolean(string  = "Bookable Packages")
    inactive = fields.Boolean(default=False , string = "inactive")
    hostel_id = fields.Many2one("hms.hostel",string = "Policy Defined for Hostel ")

class HMSAmenity(models.Model):
    _name = 'hms.amenities'
    _description = 'Hostel amenities Information'

    name  = fields.Char('Name', required=True)

    category_type = fields.Selection([('draft','Normal'),
                              ('cheap', 'Cheap'),
                              ('expensive', 'Expensive')],
                             'Category')

    price = fields.Char('PRODUCT PRICE',required=True)
    date_of_purchase = fields.Date('Date of Purchase', required=True)
    room_id = fields.Many2one("hms.hostel_rooms",string = "Room")

class HMSHostelRooms(models.Model):
    _name  = 'hms.hostel_rooms'
    _description = "Hostel Room Information"

    name  = fields.Char('Name', required=True)
    room_id = fields.Many2one('hms.hostel',string = "Hostel Name")
    Room_number = fields.Char('Rooms Number',required = "True")
    no_of_rooms = fields.Char(string='Capacity in Rooms', required=True)
    no_of_floor = fields.Char(string='Number of floor', required=True)
    things_in_room  = fields.Many2one('hms.amenities',string = "Things in Rooms")
    Rent = fields.Integer(string = "Rent",required = True)
class HMSHostelAdmission(models.Model):
    _name = "hms.hostel_admission"
    _description = "Hostel Admission"

    name = fields.Char("Hostel Admission")
    admission_no  = fields.Integer("Admission Number")
    father_name = fields.Many2one("hms.student",string = "Father Name")
    price_list_policy = fields.Selection([('Public','Public Pricelist PKR'),
                              ('Private', 'Private Pricelist PKR'),
                              ('VIP', 'VIP Pricelist PKR'),
                              ('Foreign', 'Foreign Pricelist $$$'),],
                             'Payment List')
    hostel_name = fields.Many2one("hms.hostel",string = "Hostel Name")
    admission_date = fields.Date('Admission Date', default=date.today())
    Number_of_days = fields.Integer("No of days")
    Deposit_policy  = fields.Many2one("hms.deposit_policy",string = "DepositPolicy")
    Billing_date = fields.Datetime("Billing_date",required = True)
    payment_frequency = fields.Selection([('weekly','Weekly'),
                              ('bitweekly', 'BitWeekly'),
                              ('Monthly', 'Monthly'),
                              ('Yearly', 'Yearly'),],
                             'Payment Frequency')
    leaving_date = fields.Datetime("Leaving_date",required = True)

    state = fields.Selection([('draft', 'Draft'), ('verified', 'Verified'), ('done', 'Done'),
                              ('cancelled', 'Cancelled')], 'Status', readonly=True, default="draft")
    active = fields.Boolean(default=True)
    user_id = fields.Many2one('res.users', string='Responsible', readonly=True, default=lambda self: self.env.user)
    student_name_id =  fields.Many2one("hms.student",string = "Student Name")
    room_id = fields.Many2one("hms.hostel_rooms",string = "Room Assaigned")

    name_seq = fields.Char(string = "Order Reference",required = True ,copy = False,readonly = True,index=True,default = lambda self: _('New'))
    def set_to_cancelled(self):
        self.state = 'cancelled'

    def set_to_draft(self):
            '''Method to change state to draft'''
            self.state = 'draft'

    def set_to_verified(self):
        '''Method to change state to verified'''
        self.state = 'verified'

    def set_to_approved(self):
        self.state = 'approved'

    def set_done(self):
        self.state = 'done'
