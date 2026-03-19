# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolCourse(models.Model):
    """
    Online Course model.
    
    Represents a course in the online learning system.
    Contains lessons, enrolled students, and assigned teachers.
    """
    _name = 'school.course'
    _description = 'Online Course'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # Course Information
    name = fields.Char(
        string='Course Name',
        required=True,
        tracking=True
    )
    code = fields.Char(
        string='Course Code',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('school.course')
    )
    description = fields.Html(
        string='Description',
        help='Detailed course description'
    )
    short_description = fields.Text(
        string='Short Description',
        help='Brief summary for course listings'
    )
    
    # Status and Dates
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ], string='Status', default='draft', tracking=True)
    
    start_date = fields.Date(
        string='Start Date',
        tracking=True
    )
    end_date = fields.Date(
        string='End Date',
        tracking=True
    )
    
    # Relations
    teacher_id = fields.Many2one(
        'school.teacher',
        string='Main Teacher',
        required=True,
        tracking=True
    )
    lesson_ids = fields.One2many(
        'school.lesson',
        'course_id',
        string='Lessons'
    )
    enrollment_ids = fields.One2many(
        'school.enrollment',
        'course_id',
        string='Enrollments'
    )
    
    # Computed Fields
    lesson_count = fields.Integer(
        string='Number of Lessons',
        compute='_compute_lesson_count'
    )
    student_count = fields.Integer(
        string='Enrolled Students',
        compute='_compute_student_count'
    )
    
    # Course Settings
    duration_hours = fields.Integer(
        string='Duration (Hours)',
        help='Estimated course duration'
    )
    difficulty = fields.Selection([
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], string='Difficulty Level', default='beginner')
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    # Constraints
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """Ensure end date is after start date."""
        for course in self:
            if course.start_date and course.end_date:
                if course.end_date < course.start_date:
                    raise ValidationError('End date must be after start date.')
    
    # Compute Methods
    @api.depends('lesson_ids')
    def _compute_lesson_count(self):
        """Count number of lessons in course."""
        for course in self:
            course.lesson_count = len(course.lesson_ids)
    
    @api.depends('enrollment_ids')
    def _compute_student_count(self):
        """Count enrolled students."""
        for course in self:
            course.student_count = len(course.enrollment_ids.filtered(
                lambda e: e.state == 'active'
            ))
    
    # Actions
    def action_publish(self):
        """Publish the course."""
        self.write({'state': 'published'})
    
    def action_archive(self):
        """Archive the course."""
        self.write({'state': 'archived'})
    
    def action_draft(self):
        """Set course to draft."""
        self.write({'state': 'draft'})
