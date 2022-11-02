# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import models, fields, api
from datetime import date, timedelta


class Patients(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(string="Patient Name")
    dob = fields.Date(string="Date of Birth", required=True)
    status = fields.Selection([('married', 'Married'),
                               ('unmarried', 'Unmarried')],
                              string="Marital Status", required=True)
    gender = fields.Selection([('female', 'Female'),
                               ('male', 'Male'),
                               ('others', 'Other')],
                              string="Gender", required=True)
    profession = fields.Char(string="Profession")
    patient_seq = fields.Char(string='Patient No.', required=True,
                              copy=False,
                              readonly=True,
                              index=True,
                              default=lambda self: 'New')
    notes = fields.Html('Note', sanitize_style=True)
    patient_profession = fields.Char(string="Profession", help="Profession of patient")
    patient_age = fields.Integer(string="Age", compute='_compute_age')
    blood_grp = fields.Many2one('hospital.blood', string="Blood Group")
    doctor_id = fields.Many2one('hr.employee', string="Family Doctor",
                                domain="[('is_doctor','=','doctor')]")
    place = fields.Char(string="Place")
    group = fields.Selection([('hindu', 'Hindu'), ('muslim', 'Muslim'),
                              ('christian',
                               'Christian')], string="Ethnic Group", help="can specify your religion")
    risk_id = fields.Many2one('genetic.risks', "Genetic Risks")
    insurance = fields.Char(string="Insurance", help="patient insurance")
    family_ids = fields.One2many('hospital.family', 'family_id', "Family ID")
    prescription_ids = fields.One2many('hospital.prescription', 'patient_id')
    evaluation_ids = fields.One2many('hospital.evaluation', 'patient_id',
                                     string="Evaluation ID")

    hos_lab_ids = fields.One2many('lab.test.result', 'patient_id',
                                  string="Lab ID")

    hospital_vaccine_id = fields.One2many('hospital.vaccination', 'patient_id')
    economic_level = fields.Selection([('low', 'Lower Class'),
                                       ('middle', 'Middle Class'),
                                       ('upper', 'Upper Class')],
                                      string="Socioeconomic", help="Specify your economic status ")
    education_level = fields.Selection([('post', 'Post Graduation'),
                                        ('graduation', 'Graduation'),
                                        ('pre', 'Pre Graduation')],
                                       string="Education Level", help="Education status of patient")

    house_level = fields.Selection([('good', 'Good'),
                                    ('bad', 'Bad'),
                                    ('poor', 'Poor')],
                                   string="House Condition", help="Specify your house's condition")
    occupation = fields.Char('Occupation')
    work_home = fields.Boolean('Work At Home')
    hours_outside = fields.Integer('Hours Stay Outside Home', help="Specify how many hours you stay away from home ")
    hostile = fields.Boolean('Hostile Area', help="Specify your house in a friendly neighbourhood ")
    income = fields.Monetary('Income', help="The in come of patient")
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id
                                  .currency_id.id,
                                  required=True)

    sanitary = fields.Boolean('Sanitary Sewers',
        help="A sewer or sewer system for carrying off wastewater and waste matter from a residence, business, etc")
    running = fields.Boolean('Running Water',
                    help="water that comes into a building through pipes. a cabin with hot and cold running water.")
    electricity = fields.Boolean('Electricity')
    gass = fields.Boolean('Gas Supply')
    trash = fields.Boolean('Trash Collection')
    home_phone = fields.Boolean('Telephone')
    tv = fields.Boolean('Television')
    internet = fields.Boolean('Internet')

    help = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                            string="Family Help", help="Specify your family is willing to help or not")
    discussion = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                  string="Family Discussion ",
                                  help="Specify your family have a good discussion at home ")
    ability = fields.Selection([('very', 'Very good'), ('good', 'Good'),
                                ('bad', 'Bad'), ('poor', 'Poor')],
                               string="Family Ability" ,help="family status of the patient")
    time_sharing = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                    string=" Family Time Sharing ",
                                    help="Specify your family share time at home ")
    affection = fields.Selection([('very', 'Very good'), ('good', 'Good'),
                                  ('bad', 'Bad'), ('poor', 'Poor')],
                                 string="Family Affection ", help="Specify your family's affection ")
    single = fields.Boolean('Single Parent Family')
    violence = fields.Boolean('Domestic Violence')
    children = fields.Boolean('Working Children')
    abuse = fields.Boolean('Sexual Abuse')
    drug = fields.Boolean('Drug Addiction')
    withdrawal = fields.Boolean('School Withdrawal')
    in_prison = fields.Boolean('Has Been In Prison')
    current_prison = fields.Boolean('Currently In Prison')
    relative_prison = fields.Boolean('Relative In Prison')

    fertile = fields.Boolean('Fertile', help="Capable of developing into a complete organism; fertilized. Capable of "
                                             "supporting plant life; favorable to the growth of crops and plants.")
    menarche_age = fields.Integer('Menarche Age', help="The first menstrual period in a female adolescent")
    pause = fields.Boolean('Menopause',
                           help="Menopause is a point in time 12 months after a woman's last period")
    pause_age = fields.Integer('Menopause Age')
    pap = fields.Boolean('PAP Test', help="A procedure in which a small brush is used to gently remove cells from the "
                                          "surface of the cervix and the area around it so they can be checked under "
                                          "a microscope for cervical cancer or cell changes that may lead to cervical "
                                          "cancer.")
    colposcopy = fields.Boolean('Colposcopy', help=" test to take a closer look at your cervix")
    self = fields.Boolean('Self breast examination', help="A breast self-exam for breast awareness is an inspection "
                                                          "of your breasts that women do on your own")
    mommography = fields.Boolean('Mommography', help="Mammograms can be used to look for breast cancer")
    last_pap = fields.Date("Last PAP Test")
    last_col = fields.Date("Last Colposcopy")

    gpa = fields.Char('Occupation')
    deceased = fields.Integer('Deceased during 1st week')
    grandiva = fields.Integer('Grandiva')
    alive = fields.Integer('Born Alive')
    premature = fields.Integer('Premature', help="Premature birth is birth that happens too soon, before 37 weeks of pregnancy")
    abortions = fields.Integer('No Of Abortions')
    perinatal_ids = fields.One2many('hospital.perinatal', 'patient_id', )

    exercise = fields.Boolean('Exercise')
    minute = fields.Integer('Minute/Day')

    day_sleep = fields.Boolean('Sleeps At Daytime')
    sleep_hrs = fields.Integer('Sleep Hours')

    meals = fields.Integer('Meals/Day')
    alone = fields.Boolean('Eat Alone')
    coffee = fields.Boolean('Coffee')
    cup = fields.Integer('Cups/Day')
    drink = fields.Boolean('Soft Drink')
    salt = fields.Boolean('Salt')
    diet = fields.Boolean('Currently On Diet')
    notes = fields.Text("Notes")

    smoke = fields.Boolean('Smoker')
    ex_smoke = fields.Boolean('Ex-Smoker')
    age_start = fields.Integer('Age to Start Smoking')
    cigarettes = fields.Integer('Cigarettes/Day')
    passive = fields.Boolean('Passive Smoker')
    age_quit = fields.Integer('Age of Quitting')

    alcoholic = fields.Boolean('Alcoholic')
    ex_alcoholic = fields.Boolean('Ex-Smoker')
    age_start_alco = fields.Integer('Age to Start Drinking')
    beer = fields.Integer('Beer/Day')
    liquor = fields.Integer('Liquor/Day')
    wine = fields.Integer('Wine/Day')
    age_quit_alcoholic = fields.Integer('Age Of Quitting')

    drugs = fields.Boolean('Drug User')
    ex_drugs = fields.Boolean('Ex-Drug User')
    iv_user = fields.Boolean('IV Drug User')
    age_start_drug = fields.Integer('Age to Start Using Drugs')
    age_quit_drug = fields.Integer('Age Of Quitting')

    orientation = fields.Selection([('straight', 'Straight'),
                                    ('homo', 'Homosexual'),
                                    ('trans', 'Trans-Gender')], "Orientation")
    age_sex = fields.Integer("Age of First Encounter")
    partners = fields.Integer("No of Partners")
    anti = fields.Selection(
        [('pills', 'Anticonceptive Pills'), ('ring', 'Contraceptive Ring'),
         ('injection', 'Contraceptive Injection')],
        string="Anticonceptive Methods")
    oral = fields.Boolean('Oral Sex', help="uttered by the mouth or in words")
    anal = fields.Boolean('Anal Sex', help="")
    prostitute = fields.Boolean('Prostitute')
    prostitute_sex = fields.Boolean(' Sex With Prostitute')
    sex_notes = fields.Text('Notes')

    rider = fields.Boolean('Motorcycle Rider')
    helmet = fields.Boolean('Uses Helmet')
    laws = fields.Boolean('Obey Traffic Laws')
    revision = fields.Boolean('Car Revision')
    belt = fields.Boolean('Seat Belt')
    safety = fields.Boolean('Car Child Safety')
    home = fields.Boolean('Home Safety')

    def _compute_age(self):
        """age calculation of patient"""
        for rec in self:
            rec.patient_age = False
            if rec.dob:
                rec.patient_age = (date.today() - rec.dob) // timedelta(days=365.2425)

    def name_get(self):
        res = []
        for name in self:
            res.append((name.id, ("%s (%s)") % (name.name, name.patient_seq)))
        return res

    @api.model
    def create(self, vals):
        if vals.get('patient_seq', 'New') == 'New':
            vals['patient_seq'] = self.env['ir.sequence'].next_by_code(
                'patients.sequence') or 'New'
        result = super(Patients, self).create(vals)
        return result


class Family(models.Model):
    _name = 'hospital.family'
    _description = 'Family'
    name = fields.Char(string="Name")
    relation = fields.Char(string="Relation")
    age = fields.Integer(string="Age")
    deceased = fields.Selection([('yes', 'Yes'), ('no', 'NO')], string="Diseased")
    family_id = fields.Many2one('res.partner',
                                string="Family ID")


class Evaluation(models.Model):
    _name = 'hospital.evaluation'
    _description = 'Evaluation'
    patient_id = fields.Many2one('res.partner', "Family ID")
    name = fields.Char(string="Name")
    indication = fields.Char(string="Indication")
    doctor = fields.Char(string="Doctor")
    appointment = fields.Char(string="Appointment")
    eval_date = fields.Date(string="Date")
    body_mass = fields.Char(string="BMI")
    eval_type = fields.Char(string="Evaluation Type")


class Perinatal(models.Model):
    _name = 'hospital.perinatal'
    _description = 'Family'
    code = fields.Char(string="Code")
    grandiva = fields.Char(string="Grandiva")
    admission_date = fields.Date("Admission Date")
    dismiss = fields.Char(string="Dismiss From Hospital")
    weeks = fields.Char(string="Gestational Weeks")
    abortion = fields.Integer(string="Abortion")
    patient_id = fields.Many2one('res.partner', string="ID")


class LabTest(models.Model):
    _name = 'hospital.lab'
    _description = 'Lab Test'
    lab_test = fields.Char(string="Lab Test")
    lab_type = fields.Char(string="Lab Type")
    date_req = fields.Date(string="Date Requested")
    date_analysis = fields.Date(string="Date of Analysis")
    state = fields.Date(string="State")
    patient_id = fields.Many2one('res.partner', string="ID")


class Medicine(models.Model):
    _name = 'patient.medicine'
    _description = 'Medicine'

    medicine_id = fields.Many2one('hospital.medicine', string="Medicine")
    indication = fields.Char(string="Indication", help="a sign, symptom, or medical condition that leads to the "
                                                       "recommendation of a treatment, test, or procedure")
    prescription = fields.Char(string="Prescription Reference")
    dose = fields.Char(string="Dose")
    dose_unit = fields.Char(string="Dose Unit")
    form = fields.Char(string="Form")
    frequency = fields.Char(string="Frequency")
    duration = fields.Char(string="Treatment Duration")
    period = fields.Char(string="Treatment Period")
    patient_id = fields.Many2one('res.partner', string="ID")
