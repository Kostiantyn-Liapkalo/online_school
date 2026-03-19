# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolEnrollment(models.Model):
    """
    Enrollment model linking students to courses.
    
    Tracks student enrollment status, progress, and completion.
    """
    _name = 'school.enrollment'
    _description = 'Course Enrollment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'enrollment_date desc'

    # Enrollment Identification
    name = fields.Char(
        string='Enrollment Reference',
        compute='_compute_name',
        store=True
    )
    enrollment_number = fields.Char(
        string='Enrollment Number',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('school.enrollment')
    )
    
    # Relations
    student_id = fields.Many2one(
        'school.student',
        string='Student',
        required=True,
        ondelete='restrict',
        tracking=True
    )
    course_id = fields.Many2one(
        'school.course',
        string='Course',
        required=True,
        ondelete='restrict',
        tracking=True
    )
    teacher_id = fields.Many2one(
        'school.teacher',
        string='Teacher',
        related='course_id.teacher_id',
        store=True,
        readonly=True
    )
    
    # Enrollment Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('suspended', 'Suspended')
    ], string='Status', default='draft', tracking=True)
    
    # Dates
    enrollment_date = fields.Date(
        string='Enrollment Date',
        default=fields.Date.today,
        tracking=True
    )
    start_date = fields.Date(
        string='Start Date'
    )
    completion_date = fields.Date(
        string='Completion Date'
    )
    
    # Progress Tracking
    progress_percentage = fields.Float(
        string='Progress (%)',
        default=0.0,
        help='Completion percentage'
    )
    completed_lessons = fields.Integer(
        string='Completed Lessons',
        default=0
    )
    total_lessons = fields.Integer(
        string='Total Lessons',
        related='course_id.lesson_count',
        store=True,
        readonly=True
    )
    
    # Grading
    final_grade = fields.Selection([
        ('a', 'A - Excellent'),
        ('b', 'B - Good'),
        ('c', 'C - Satisfactory'),
        ('d', 'D - Pass'),
        ('f', 'F - Fail')
    ], string='Final Grade')
    
    # Certificate
    certificate_issued = fields.Boolean(
        string='Certificate Issued',
        default=False
    )
    certificate_number = fields.Char(
        string='Certificate Number'
    )
    
    # Additional Info
    notes = fields.Text(
        string='Notes'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    # Compute Methods
    @api.depends('student_id', 'course_id')
    def _compute_name(self):
        """Generate enrollment reference name."""
        for enrollment in self:
            if enrollment.student_id and enrollment.course_id:
                enrollment.name = f"{enrollment.student_id.name} - {enrollment.course_id.name}"
            else:
                enrollment.name = f"Enrollment #{enrollment.id}"
    
    # Constraints
    @api.constrains('student_id', 'course_id')
    def _check_unique_enrollment(self):
        """Prevent duplicate enrollments."""
        for enrollment in self:
            existing = self.search([
                ('student_id', '=', enrollment.student_id.id),
                ('course_id', '=', enrollment.course_id.id),
                ('id', '!=', enrollment.id),
                ('state', 'not in', ['dropped', 'completed'])
            ])
            if existing:
                raise ValidationError(
                    f'Student is already enrolled in this course.'
                )
    
    # Actions
    def action_activate(self):
        """Activate enrollment."""
        self.write({'state': 'active', 'start_date': fields.Date.today()})
    
    def action_complete(self):
        """Mark enrollment as completed."""
        self.write({
            'state': 'completed',
            'completion_date': fields.Date.today(),
            'progress_percentage': 100.0
        })
    
    def action_drop(self):
        """Drop enrollment."""
        self.write({'state': 'dropped'})
    
    def action_suspend(self):
        """Suspend enrollment."""
        self.write({'state': 'suspended'})
    
    def action_issue_certificate(self):
        """Issue completion certificate."""
        for enrollment in self:
            if enrollment.state == 'completed' and not enrollment.certificate_issued:
                enrollment.write({
                    'certificate_issued': True,
                    'certificate_number': self.env['ir.sequence'].next_by_code('school.certificate')
                })
