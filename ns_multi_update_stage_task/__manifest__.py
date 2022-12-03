# -*- coding: utf-8 -*-
{
    'name': "Multi-update of stage of task",
    'summary': """
        Module that add functionality Multi-update of stage of task""",
    'description': """
        Module that add functionality Multi-update of stage of task
    """,
    'author': "Noarison Léonce",
    'website': "lrazafimiandrisoa@gmail.com",
    'category': 'Services/Project',
    'version': '15.0.1.0',
    'depends': [
        'base',
        'project'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'wizard/multi_update_task_stage_wizard.xml',
        'views/project_task_views.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
    'license': 'LGPL-3',
}
