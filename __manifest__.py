# -*- coding: utf-8 -*-
{
    "name": "hr_civiltec_reports",
    "version": "1.0",
    "summary": "Module Summary",
    "sequence": -100,
    "description": """Module Description""",
    "category": "Human Resources",
    "website": "https://www.yourcompany.com",
    "depends": ["hr_contract"],
    "data": [
        "views/hr_contract_report.xml",
        "views/hr_contract_report_template.xml",
        "views/hr_contract_views.xml",
    ],
    "demo": [
        # 'demo/demo.xml',
    ],
    "qweb": [],
    "installable": True,
    "application": True,
    "auto_install": False,
}
