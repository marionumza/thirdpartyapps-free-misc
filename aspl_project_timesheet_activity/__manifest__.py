{
    "name": "Project Timesheet Activity",
    "summary": "Project Timesheet Activity",
    "author": "Aspire Softserv Pvt. Ltd",
    "website": "https://aspiresoftware.in/",
    "category": "Timesheet",
    "version": "0.0.9",
    "license": "AGPL-3",
    "depends": ['hr_timesheet','project'],
    "data": [
        "security/ir.model.access.csv",
        "views/project_timesheet_activity_configuration.xml",
        "views/inherit_project_task.xml"
    ],
    "application": False,
    "development_status": "Beta",
    "maintainer": "Aspire Softserv Pvt. Ltd",
    "installable": True,
    "support":"odoo@aspiresoftserv.com",
    "summary": "his module adds a new field 'Activity' in timesheet line. User can analyze the time spent in different type of activities. This analysis helps in better planning.",
    'images': ['images/timesheetontask.png'
                ],
}