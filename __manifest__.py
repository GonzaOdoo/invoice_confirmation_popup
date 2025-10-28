# -*- coding: utf-8 -*-
{
    'name': "Pop up al confirmar Facturas",

    'summary': """
        Al confirmar facturas de proveedor, muestra un pop up para confirmar la Empresa.
        """,

    'description': """
        Al confirmar facturas de proveedor, muestra un pop up para confirmar la Empresa. 
    """,

    'author': "GonzaOdoo",
    'website': "https://github.com/GonzaOdoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account','purchase_stock','approvals_purchase','stock'],
    'data':[
        'views/views.xml',
        'security/ir.model.access.csv',
    ]

}