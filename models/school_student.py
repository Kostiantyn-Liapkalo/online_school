# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolStudent(models.Model):
    """
    Student model for online school.
    
    Links to res.partner for contact information.
    Tracks student enrollments and progress.
    """
    _name = 'school.student'
    _description = 'School Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'partner_id'

    # Student Identification
    student_number = fields.Char(
        string='Student Number',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('school.student')
    )
    
    # Link to Partner
    user_id = fields.Many2one(
        'res.users',
        string='User',
        related='partner_id.user_id',
        store=True,
        readonly=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Contact',
        required=True,
        ondelete='restrict',
        help='Linked contact record'
    )
    name = fields.Char(
        string='Name',
        related='partner_id.name',
        store=True,
        readonly=True
    )
    email = fields.Char(
        string='Email',
        related='partner_id.email',
        store=True,
        readonly=True
    )
    phone = fields.Char(
        string='Phone',
        related='partner_id.phone',
        store=True,
        readonly=True
    )
    
    # Academic Information
    registration_date = fields.Date(
        string='Registration Date',
        default=fields.Date.today
    )
    status = fields.Selection([
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('graduated', 'Graduated'),
        ('inactive', 'Inactive')
    ], string='Student Status', default='active', tracking=True)
    
    # Relations
    enrollment_ids = fields.One2many(
        'school.enrollment',
        'student_id',
        string='Enrollments'
    )
    
    # Computed Fields
    enrollment_count = fields.Integer(
        string='Course Enrollments',
        compute='_compute_enrollment_count'
    )
    completed_courses = fields.Integer(
        string='Completed Courses',
        compute='_compute_completed_courses'
    )
    
    # Additional Info
    date_of_birth = fields.Date(
        string='Date of Birth'
    )
    notes = fields.Text(
        string='Notes'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    # Compute Methods
    @api.depends('enrollment_ids')
    def _compute_enrollment_count(self):
        """Count total enrollments."""
        for student in self:
            student.enrollment_count = len(student.enrollment_ids)
    
    @api.depends('enrollment_ids.state')
    def _compute_completed_courses(self):
        """Count completed courses."""
        for student in self:
            student.completed_courses = len(student.enrollment_ids.filtered(
                lambda e: e.state == 'completed'
            ))
    
    # Constraints
    @api.constrains('partner_id')
    def _check_unique_partner(self):
        """Ensure one partner can only be one student."""
        for student in self:
            existing = self.search([
                ('partner_id', '=', student.partner_id.id),
                ('id', '!=', student.id)
            ])
            if existing:
                raise ValidationError(
                    f'This contact is already registered as a student.'
                )
