# -*- coding: utf-8 -*-
{
    'name': 'Product Log',
    'version': '15.0.0.1',
    'summary': 'Create a log of Sale price and Cost price Change',
    'description': '''Create log,Create log of Sale price,Create log of Cost price,create log sale and cost price,
                    create sale price log,create log cost price log,create sale price log,manufacturing, mrp, create log, 
		    create accounting log, create accounting journal log, create journal log, create account journal log,
		    create log for account, create log for accounting, create log for accounting journal, create log for accounts journal,
		    create log for Inventory, create log for Inventory operation type, create Inventory log, create log for operation type,
		    create Operation type log, create Inventory's operation type log, create log for Inventory's Warehouse, create log for  Warehouse, create Inventory's warehouse log, create warehouse log, create log for manufacturing's product bill of material, create log for  product bill of material, create log for bill of material, create log for manufacturing's bill of material, create manufacturing's product bill of material log, create bill of material log, create manufacturing's product log, create manufacturing's log, create product bill of material log,  create log for Inventory's product,  create log for product,
		CREATE LOG,CREATE LOG OF SALE PRICE,CREATE LOG OF COST PRICE,CREATE LOG SALE AND COST PRICE,
                CREATE SALE PRICE LOG,CREATE LOG COST PRICE LOG,CREATE SALE PRICE LOG,MANUFACTURING, MRP, CREATE LOG, 
		CREATE ACCOUNTING LOG, CREATE ACCOUNTING JOURNAL LOG, CREATE JOURNAL LOG, CREATE ACCOUNT JOURNAL LOG,
		CREATE LOG FOR ACCOUNT, CREATE LOG FOR ACCOUNTING, CREATE LOG FOR ACCOUNTING JOURNAL, CREATE LOG FOR ACCOUNTS JOURNAL,
		CREATE LOG FOR INVENTORY, CREATE LOG FOR INVENTORY OPERATION TYPE, CREATE INVENTORY LOG, CREATE LOG FOR OPERATION TYPE,
		CREATE OPERATION TYPE LOG, CREATE INVENTORY'S OPERATION TYPE LOG, CREATE LOG FOR INVENTORY'S WAREHOUSE, CREATE LOG FOR  WAREHOUSE, CREATE INVENTORY'S WAREHOUSE LOG, CREATE WAREHOUSE LOG, CREATE LOG FOR MANUFACTURING'S PRODUCT BILL OF MATERIAL, CREATE LOG FOR  PRODUCT BILL OF MATERIAL, CREATE LOG FOR BILL OF MATERIAL, CREATE LOG FOR MANUFACTURING'S BILL OF MATERIAL, CREATE MANUFACTURING'S PRODUCT BILL OF MATERIAL LOG, CREATE BILL OF MATERIAL LOG, CREATE MANUFACTURING'S PRODUCT LOG, CREATE MANUFACTURING'S LOG, CREATE PRODUCT BILL OF MATERIAL LOG,  CREATE LOG FOR INVENTORY'S PRODUCT,  CREATE LOG FOR PRODUCT,

		    ''',
    'category': 'Sales',
    'author': 'Geo TechnoSoft',
    'website': 'https://www.geotechnosoft.com/',
    'sequence': 1,
    'images': [],
    'depends': ['base', 'stock', 'sale_management', 'mrp', 'account', 'account_accountant'],
    'data': [
        'views/log.xml'
    ],
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
