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
        'data/sequence_data.xml',
    ],
    'installable':
        True,
    'application':
        True,
    'auto_install':
        False,
    'license':
        'LGPL-3',
}
