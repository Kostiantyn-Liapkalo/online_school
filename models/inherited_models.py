# -*- coding: utf-8 -*-
"""
Inheritance models for extending standard Odoo functionality.
"""

from odoo import models, fields, api


class ResPartner(models.Model):
    """Extend res.partner to add school-related fields."""

    _inherit = 'res.partner'

    is_student = fields.Boolean(
        default=False,
        help='Mark if this partner is a school student'
    )
    is_teacher = fields.Boolean(
        default=False,
        help='Mark if this partner is a school teacher'
    )
    student_id = fields.Many2one(
        'school.student',
        string='Related Student',
        compute='_compute_student_id',
        store=True,
        help='Related student record'
    )
    teacher_id = fields.Many2one(
        'school.teacher',
        string='Related Teacher',
        compute='_compute_teacher_id',
        store=True,
        help='Related teacher record'
    )

    @api.depends('is_student')
    def _compute_student_id(self):
        """Compute related student record."""
        student_obj = self.env['school.student']
        for partner in self:
            if partner.is_student:
                student = student_obj.search([('partner_id', '=', partner.id)], limit=1)
                partner.student_id = student.id if student else False
            else:
                partner.student_id = False

    @api.depends('is_teacher')
    def _compute_teacher_id(self):
        """Compute related teacher record."""
        teacher_obj = self.env['school.teacher']
        for partner in self:
            if partner.is_teacher:
                teacher = teacher_obj.search([('partner_id', '=', partner.id)], limit=1)
                partner.teacher_id = teacher.id if teacher else False
            else:
                partner.teacher_id = False


class MailActivity(models.Model):
    """Extend mail.activity for school-specific activities."""

    _inherit = 'mail.activity'

    school_course_id = fields.Many2one(
        'school.course',
        string='Related Course',
        help='Course related to this activity'
    )
    school_lesson_id = fields.Many2one(
        'school.lesson',
        string='Related Lesson',
        help='Lesson related to this activity'
    )

    def action_mark_done(self):
        """Override to add school-specific logic when marking done."""
        # Call parent method
        result = super(MailActivity, self).action_mark_done()

        # If this is a lesson activity, update lesson completion
        for activity in self:
            if activity.school_lesson_id and activity.res_model == 'school.enrollment':
                enrollment = self.env['school.enrollment'].browse(activity.res_id)
                if enrollment.exists():
                    enrollment._compute_progress()

        return result
