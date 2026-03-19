# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolTeacher(models.Model):
    """
    Teacher model for online school.
    
    Links to res.partner for contact information.
    Teachers can be assigned to multiple courses.
    """
    _name = 'school.teacher'
    _description = 'School Teacher'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'partner_id'

    # Teacher Identification
    teacher_number = fields.Char(
        string='Teacher Number',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('school.teacher')
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
    
    # Professional Information
    specialization = fields.Char(
        string='Specialization',
        help='Subject area or teaching specialty'
    )
    qualification = fields.Text(
        string='Qualifications',
        help='Education and professional qualifications'
    )
    experience_years = fields.Integer(
        string='Years of Experience',
        default=0
    )
    
    # Employment
    hire_date = fields.Date(
        string='Hire Date',
        default=fields.Date.today
    )
    status = fields.Selection([
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('inactive', 'Inactive')
    ], string='Teacher Status', default='active', tracking=True)
    
    # Relations
    course_ids = fields.One2many(
        'school.course',
        'teacher_id',
        string='Teaching Courses'
    )
    
    # Computed Fields
    course_count = fields.Integer(
        string='Number of Courses',
        compute='_compute_course_count'
    )
    total_students = fields.Integer(
        string='Total Students',
        compute='_compute_total_students'
    )
    
    # Additional Info
    bio = fields.Html(
        string='Biography',
        help='Teacher bio for course pages'
    )
    website = fields.Char(
        string='Personal Website'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    # Compute Methods
    @api.depends('course_ids')
    def _compute_course_count(self):
        """Count assigned courses."""
        for teacher in self:
            teacher.course_count = len(teacher.course_ids)
    
    @api.depends('course_ids.enrollment_ids')
    def _compute_total_students(self):
        """Count total students across all courses."""
        for teacher in self:
            total = 0
            for course in teacher.course_ids:
                total += len(course.enrollment_ids.filtered(
                    lambda e: e.state == 'active'
                ))
            teacher.total_students = total
    
    # Constraints
    @api.constrains('partner_id')
    def _check_unique_partner(self):
        """Ensure one partner can only be one teacher."""
        for teacher in self:
            existing = self.search([
                ('partner_id', '=', teacher.partner_id.id),
                ('id', '!=', teacher.id)
            ])
            if existing:
                raise ValidationError(
                    f'This contact is already registered as a teacher.'
                )
