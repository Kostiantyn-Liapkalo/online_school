# -*- coding: utf-8 -*-
{
    'name': 'Online School',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'Online Learning Management System',
    'description': """
Online School Module
====================

A comprehensive online learning management system for Odoo 19.0.

Features:
---------
* **Courses**: Create and manage online courses with lessons
* **Students**: Student registration and profile management
* **Teachers**: Teacher assignment and management
* **Enrollments**: Course enrollment with status tracking
* **Lessons**: Structured lesson content with video/text support
* **Progress Tracking**: Student progress and completion tracking
* **Certificates**: Generate completion certificates

Technical Details:
------------------
* Fully integrated with Odoo partner model
* Responsive web interface
* Multi-language support ready
* Access control and security rules

Usage:
------
Install the module and configure courses, teachers, and enrollments
through the dedicated menu.
    """,
    'author': 'Kostiantyn Liapkalo',
    'website': 'https://github.com/kostiantyn-liapkalo',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/school_security.xml',
        'security/ir.model.access.csv',
        'data/school_sequence.xml',
        'views/school_course_views.xml',
        'views/school_student_views.xml',
        'views/school_teacher_views.xml',
        'views/school_enrollment_views.xml',
        'views/school_lesson_views.xml',
        'views/school_menus.xml',
        'wizards/school_enrollment_wizard_views.xml',
        'report/school_enrollment_report.xml',
    ],
    'demo': [
        'demo/school_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
