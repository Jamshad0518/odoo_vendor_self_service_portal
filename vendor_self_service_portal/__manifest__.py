{
    'name': 'Vendor Self Service Portal',
    'version': '16.0',
    'depends': ['base','mail','product','sale'],
    'author': 'Jamshad A',
    'category': 'Sales',
    'description': 'This module consists of (i)Vendor Forecast:vendors can view a basic list of upcoming demand forecasts for the next quarter'
                   '                        (ii)Sale Order Adjustment Request Submission with Mail',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/vendor_forecast_views.xml',
        'views/vendor_adjustment_request_views.xml',
        'data/mail_template.xml',

    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
