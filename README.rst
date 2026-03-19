Online School
=============

.. image:: https://img.shields.io/badge/Odoo-19.0-blue.svg
    :target: https://www.odoo.com/
    :alt: Odoo Version

.. image:: https://img.shields.io/badge/license-LGPL--3-green.svg
    :target: https://www.gnu.org/licenses/lgpl-3.0.en.html
    :alt: License: LGPL-3

A comprehensive Learning Management System (LMS) for Odoo 19.0.

Overview
--------

Online School is a complete learning management system that enables
organizations to create and manage online courses, enroll students,
track progress, and issue completion certificates.

Features
--------

**Courses**
    * Create and manage courses with lessons
    * Set difficulty levels (Beginner, Intermediate, Advanced)
    * Schedule start and end dates
    * Track enrollment statistics

**Students**
    * Student registration linked to partners
    * Enrollment management
    * Progress tracking
    * Completion certificates

**Teachers**
    * Teacher profiles with specializations
    * Qualification tracking
    * Course assignments
    * Student count per teacher

**Lessons**
    * Multi-format content support (Video, Text, Quiz, Assignment)
    * Sequenced lesson ordering
    * Free preview options
    * Required vs optional lessons

**Enrollments**
    * Student-course linking
    * Progress percentage tracking
    * Grade management
    * Certificate issuance

Installation
------------

1. Download the module and place it in your Odoo addons directory
2. Update the apps list in Odoo
3. Install the ``Online School`` module
4. Demo data will be automatically loaded

Configuration
-------------

### User Groups

* **School Administrator**: Full access to all features
* **School Teacher**: Manage courses, students, and content
* **School Student**: View courses and track own progress

No additional configuration required. The module is ready to use after installation.

Usage
-----

1. **Create Teachers**: Register teachers with their specializations
2. **Create Courses**: Define courses with lessons and assign teachers
3. **Register Students**: Add students to the system
4. **Create Enrollments**: Enroll students in courses
5. **Track Progress**: Monitor student completion and grades

Technical Specifications
------------------------

* **Dependencies**: base, mail, contacts
* **Models**: school.course, school.student, school.teacher, school.enrollment, school.lesson
* **Odoo Version**: 19.0
* **License**: LGPL-3

Supported Versions
------------------

* Odoo 19.0

Demo Data
---------

The module includes demo data with:

* 2 demo teachers
* 2 demo students
* 2 published courses with lessons
* 2 sample enrollments

Credits
-------

Author
~~~~~~

* **Kostiantyn Liapkalo** - *Initial work*

License
-------

This module is licensed under the LGPL-3 License.
See https://www.gnu.org/licenses/lgpl-3.0.en.html for details.
