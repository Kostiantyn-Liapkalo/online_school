# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolLesson(models.Model):
    """
    Lesson model representing a single unit of course content.
    
    Lessons are ordered within a course and can contain
    various content types: video, text, quiz, etc.
    """
    _name = 'school.lesson'
    _description = 'Course Lesson'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'

    # Lesson Identification
    name = fields.Char(
        string='Lesson Name',
        required=True,
        tracking=True
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Order within the course'
    )
    
    # Relations
    course_id = fields.Many2one(
        'school.course',
        string='Course',
        required=True,
        ondelete='cascade',
        tracking=True
    )
    teacher_id = fields.Many2one(
        'school.teacher',
        string='Teacher',
        related='course_id.teacher_id',
        store=True,
        readonly=True
    )
    
    # Content
    content_type = fields.Selection([
        ('video', 'Video'),
        ('text', 'Text Article'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('mixed', 'Mixed Content')
    ], string='Content Type', default='text', required=True)
    
    description = fields.Text(
        string='Short Description'
    )
    content = fields.Html(
        string='Lesson Content',
        help='Main lesson content in HTML format'
    )
    
    # Video Fields
    video_url = fields.Char(
        string='Video URL',
        help='External video link (YouTube, Vimeo, etc.)'
    )
    video_duration = fields.Integer(
        string='Video Duration (minutes)',
        help='Video length in minutes'
    )
    
    # Lesson Settings
    duration_minutes = fields.Integer(
        string='Estimated Duration (minutes)',
        default=30,
        help='Estimated time to complete this lesson'
    )
    is_preview = fields.Boolean(
        string='Free Preview',
        default=False,
        help='Allow non-enrolled students to view this lesson'
    )
    is_required = fields.Boolean(
        string='Required',
        default=True,
        help='Must be completed to finish the course'
    )
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ], string='Status', default='draft', tracking=True)
    
    # Additional Resources
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'lesson_attachment_rel',
        'lesson_id',
        'attachment_id',
        string='Attachments'
    )
    
    # Computed Fields
    attachment_count = fields.Integer(
        string='Attachments Count',
        compute='_compute_attachment_count'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    # Compute Methods
    @api.depends('attachment_ids')
    def _compute_attachment_count(self):
        """Count attached files."""
        for lesson in self:
            lesson.attachment_count = len(lesson.attachment_ids)
    
    # Actions
    def action_publish(self):
        """Publish the lesson."""
        self.write({'state': 'published'})
    
    def action_archive(self):
        """Archive the lesson."""
        self.write({'state': 'archived'})
    
    def action_draft(self):
        """Set lesson to draft."""
        self.write({'state': 'draft'})
    
    # Constraints
    @api.constrains('video_url')
    def _check_video_url(self):
        """Validate video URL format if provided."""
        for lesson in self:
            if lesson.video_url and lesson.content_type == 'video':
                if not lesson.video_url.startswith(('http://', 'https://')):
                    raise ValidationError(
                        'Video URL must start with http:// or https://'
                    )
