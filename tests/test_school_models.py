# -*- coding: utf-8 -*-
"""Tests for the online_school module."""

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestSchoolCourse(TransactionCase):
    """Test cases for the school.course model."""

    def setUp(self):
        """Set up test data."""
        super(TestSchoolCourse, self).setUp()
        self.teacher = self.env['school.teacher'].create({
            'name': 'Test Teacher',
            'email': 'teacher@test.com',
        })
        self.course = self.env['school.course'].create({
            'name': 'Test Course',
            'teacher_id': self.teacher.id,
            'difficulty': 'beginner',
        })

    def test_course_creation(self):
        """Test that a course can be created."""
        self.assertEqual(self.course.name, 'Test Course')
        self.assertEqual(self.course.state, 'draft')
        self.assertEqual(self.course.teacher_id, self.teacher)

    def test_course_publish(self):
        """Test publishing a course."""
        self.course.action_publish()
        self.assertEqual(self.course.state, 'published')

    def test_course_archive(self):
        """Test archiving a course."""
        self.course.action_publish()
        self.course.action_archive()
        self.assertEqual(self.course.state, 'archived')


class TestSchoolStudent(TransactionCase):
    """Test cases for the school.student model."""

    def setUp(self):
        """Set up test data."""
        super(TestSchoolStudent, self).setUp()
        self.student = self.env['school.student'].create({
            'name': 'Test Student',
            'email': 'student@test.com',
            'date_of_birth': '2000-01-01',
        })

    def test_student_creation(self):
        """Test that a student can be created."""
        self.assertEqual(self.student.name, 'Test Student')
        self.assertEqual(self.student.status, 'active')
        self.assertTrue(self.student.student_number)

    def test_student_age_calculation(self):
        """Test that age is calculated correctly."""
        self.assertTrue(self.student.age > 0)

    def test_student_deactivate(self):
        """Test deactivating a student."""
        self.student.action_deactivate()
        self.assertEqual(self.student.status, 'inactive')


class TestSchoolTeacher(TransactionCase):
    """Test cases for the school.teacher model."""

    def setUp(self):
        """Set up test data."""
        super(TestSchoolTeacher, self).setUp()
        self.teacher = self.env['school.teacher'].create({
            'name': 'Test Teacher',
            'email': 'teacher@test.com',
            'specialization': 'Mathematics',
        })

    def test_teacher_creation(self):
        """Test that a teacher can be created."""
        self.assertEqual(self.teacher.name, 'Test Teacher')
        self.assertEqual(self.teacher.status, 'active')
        self.assertTrue(self.teacher.teacher_number)

    def test_teacher_experience_calculation(self):
        """Test that experience years are calculated correctly."""
        self.teacher.write({'hire_date': '2020-01-01'})
        self.assertTrue(self.teacher.experience_years >= 0)


class TestSchoolEnrollment(TransactionCase):
    """Test cases for the school.enrollment model."""

    def setUp(self):
        """Set up test data."""
        super(TestSchoolEnrollment, self).setUp()
        self.teacher = self.env['school.teacher'].create({
            'name': 'Test Teacher',
            'email': 'teacher@test.com',
        })
        self.student = self.env['school.student'].create({
            'name': 'Test Student',
            'email': 'student@test.com',
        })
        self.course = self.env['school.course'].create({
            'name': 'Test Course',
            'teacher_id': self.teacher.id,
        })
        self.enrollment = self.env['school.enrollment'].create({
            'student_id': self.student.id,
            'course_id': self.course.id,
            'teacher_id': self.teacher.id,
        })

    def test_enrollment_creation(self):
        """Test that an enrollment can be created."""
        self.assertEqual(self.enrollment.student_id, self.student)
        self.assertEqual(self.enrollment.course_id, self.course)
        self.assertEqual(self.enrollment.state, 'draft')
        self.assertTrue(self.enrollment.enrollment_number)

    def test_enrollment_activate(self):
        """Test activating an enrollment."""
        self.enrollment.action_activate()
        self.assertEqual(self.enrollment.state, 'active')

    def test_enrollment_complete(self):
        """Test completing an enrollment."""
        self.enrollment.action_activate()
        self.enrollment.action_complete()
        self.assertEqual(self.enrollment.state, 'completed')

    def test_enrollment_drop(self):
        """Test dropping an enrollment."""
        self.enrollment.action_activate()
        self.enrollment.action_drop()
        self.assertEqual(self.enrollment.state, 'dropped')


class TestSchoolLesson(TransactionCase):
    """Test cases for the school.lesson model."""

    def setUp(self):
        """Set up test data."""
        super(TestSchoolLesson, self).setUp()
        self.teacher = self.env['school.teacher'].create({
            'name': 'Test Teacher',
            'email': 'teacher@test.com',
        })
        self.course = self.env['school.course'].create({
            'name': 'Test Course',
            'teacher_id': self.teacher.id,
        })
        self.lesson = self.env['school.lesson'].create({
            'name': 'Test Lesson',
            'course_id': self.course.id,
            'content_type': 'text',
            'sequence': 1,
        })

    def test_lesson_creation(self):
        """Test that a lesson can be created."""
        self.assertEqual(self.lesson.name, 'Test Lesson')
        self.assertEqual(self.lesson.state, 'draft')
        self.assertEqual(self.lesson.course_id, self.course)

    def test_lesson_publish(self):
        """Test publishing a lesson."""
        self.lesson.action_publish()
        self.assertEqual(self.lesson.state, 'published')

    def test_lesson_archive(self):
        """Test archiving a lesson."""
        self.lesson.action_publish()
        self.lesson.action_archive()
        self.assertEqual(self.lesson.state, 'archived')


class TestSchoolEnrollmentWizard(TransactionCase):
    """Test cases for the school.enrollment.wizard model."""

    def setUp(self):
        """Set up test data."""
        super(TestSchoolEnrollmentWizard, self).setUp()
        self.teacher = self.env['school.teacher'].create({
            'name': 'Test Teacher',
            'email': 'teacher@test.com',
        })
        self.course = self.env['school.course'].create({
            'name': 'Test Course',
            'teacher_id': self.teacher.id,
        })
        self.student1 = self.env['school.student'].create({
            'name': 'Student 1',
            'email': 'student1@test.com',
        })
        self.student2 = self.env['school.student'].create({
            'name': 'Student 2',
            'email': 'student2@test.com',
        })

    def test_wizard_enroll_students(self):
        """Test enrolling multiple students via wizard."""
        wizard = self.env['school.enrollment.wizard'].create({
            'course_id': self.course.id,
            'teacher_id': self.teacher.id,
            'student_ids': [(6, 0, [self.student1.id, self.student2.id])],
        })
        result = wizard.action_enroll_students()
        self.assertEqual(result['type'], 'ir.actions.act_window')
        self.assertEqual(result['res_model'], 'school.enrollment')
