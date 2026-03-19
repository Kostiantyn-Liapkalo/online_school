# -*- coding: utf-8 -*-
"""
Wizard for enrolling multiple students to a course.
"""

from odoo import models, fields, api


class SchoolEnrollmentWizard(models.TransientModel):
    """Wizard for enrolling multiple students to a course."""

    _name = 'school.enrollment.wizard'
    _description = 'Enroll Students Wizard'

    course_id = fields.Many2one(
        'school.course',
        string='Course',
        required=True,
        help='The course to enroll students in'
    )
    student_ids = fields.Many2many(
        'school.student',
        string='Students',
        required=True,
        help='Students to enroll in the course'
    )
    teacher_id = fields.Many2one(
        'school.teacher',
        string='Teacher',
        help='Teacher assigned to the enrollments'
    )
    enrollment_date = fields.Date(
        string='Enrollment Date',
        default=fields.Date.today,
        required=True,
        help='Date of enrollment'
    )
    notes = fields.Text(
        string='Notes',
        help='Additional notes for the enrollment'
    )

    def action_enroll_students(self):
        """Create enrollments for selected students.

        Returns:
            dict: Action to display created enrollments
        """
        self.ensure_one()
        enrollment_obj = self.env['school.enrollment']
        enrollment_ids = []

        for student in self.student_ids:
            enrollment = enrollment_obj.create({
                'student_id': student.id,
                'course_id': self.course_id.id,
                'teacher_id': self.teacher_id.id or self.course_id.teacher_id.id,
                'enrollment_date': self.enrollment_date,
                'notes': self.notes,
                'state': 'draft',
            })
            enrollment_ids.append(enrollment.id)

        if enrollment_ids:
            return {
                'name': 'Enrollments',
                'type': 'ir.actions.act_window',
                'res_model': 'school.enrollment',
                'view_mode': 'list,form',
                'domain': [('id', 'in', enrollment_ids)],
                'target': 'current',
            }
        return {'type': 'ir.actions.act_window_close'}
