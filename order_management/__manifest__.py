{
    'name':
        'Order Management System',
    'version':
        '17.0.1.0.0',
    'category':
        'Sales',
    'summary':
        'Complete Order Management with Workflow and Reporting',
    'description':
        """
        Order Management System
        =======================
        * Manage orders and order items
        * Workflow states with business rules
        * Role-based permissions
        * Comprehensive reporting
    """,
    'author':
        'Code Zone',
    'website':
        'https://www.codezone-eg.com',
    'depends': ['base', 'mail', 'product'],
    'data': [
        'security/order_security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/paperformat_data.xml',
        'reports/order_report.xml',
        'views/order_management_views.xml',
        'views/order_management_item_views.xml',
        'views/order_menu.xml',
        'reports/order_report_template.xml',
    ],
    'demo': ['demo/demo_data.xml',],
    'assets': {
        'web.report_assets_pdf': ['order_management/static/src/css/order_report.css',],
    },
    'installable':
        True,
    'application':
        True,
    'auto_install':
        False,
    'license':
        'LGPL-3',
}