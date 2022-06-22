{
    'name': 'Hostel System',
    'version': '15.0.1.0.0',
    'author': 'Abdullah',
    'website': 'http://www.edu.pk',
    'category': 'Hostel Management System',
    'license': "AGPL-3",
    'Summary': 'A Module For Hostel Management System',
    'depends': ['base'],
    'data': [
    #'views/housekeeping.xml',
    'views/hms_hostel.xml',
    'report/report_1_view.xml',
     'report/report.xml',
         ],

    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'post_init_hook': '_method_run_before_installation',
}

