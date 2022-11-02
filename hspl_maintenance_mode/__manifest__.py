{
    "name": "HSPL Maintenance Mode",
    "summary": """
        HSPL Maintenance Mode
        """,
    "description": """
        HSPL Maintenance Mode
    """,
    "author": "Heliconia Solutions Pvt. Ltd.",
    "website": "https://heliconia.io/",
    "category": "web",
    "version": "15.0.0.1.0",
    "license": "OPL-1",
    "depends": ["base_setup", "web", "website"],
    "data": [
        "views/res_config_settings.xml",
        "views/templates.xml",
    ],
    "images": ["static/description/icon.jpg"],
    "installable": True,
    "auto_install": False,
    "application": True,
    "assets": {
        "web.assets_frontend": [
            "hspl_maintenance_mode/static/src/css/main.css",
            "hspl_maintenance_mode/static/src/css/util.css",
        ],
    },
}
