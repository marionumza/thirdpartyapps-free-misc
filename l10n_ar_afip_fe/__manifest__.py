##############################################################################
#
#    Copyright (C) 2007  pronexo.com  (https://www.pronexo.com)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Factura Electrónica Argentina",
    'version': "15.0.1.0.0",
    'category': 'Accounting/Localizations',
    'sequence': 14,
    'author': 'Pronexo',
    'website': 'https://www.pronexo.com',
    'description': """

Funcional
----------

Con este módulo se puede ser capaz de crear diarios en Odoo para crear facturas electrónicas de clientes e informar luego a AFIP (a través de servicios web).
Las opciones disponibles son:

 
Configuración:

1. Vaya a la sección Configuración de contabilidad> Localización para Argentina.


    
1.1. Configure el modo de servicios web AFIP:

    * Entorno de prueba para usar certificados de demostración que se usarán para probar la instancia y para hacer NOT
      Facturas reales a AFIP. es solo para probar. Para las instancias de demostración ya está predefinido, no necesitará configurar
      it (comúnmente denominado en AFIP como entorno de homologación).
    * Ambiente de producción a fin de generar certificados reales y facturas legales a AFIP,

    
1.2. Configure su Certificado AFIP: Si se encuentra en una instancia de demostración, esta se habrá configurado de forma predeterminada. Si tu
         están en una instancia de producción, solo tiene que ir a cargar su certificado AFIP

   
1.3. Opcionalmente, puede definir si desea poder verificar las facturas de los proveedores en AFIP.

2. Cree diarios de ventas que representen cada uno de sus POS AFIP (Disponible en el Portal AFIP) que desea utilizar en Odoo.

    2.1. El campo Usar documentos está configurado de forma predeterminada, no lo cambie
    2.2. Configure AFIP POS System para uno de los electrónicos.

        * Electronic Invoice - Web Service'
        * Electronic Fiscal Bond - Web Service'
        * Export Voucher - Web Service'

   
2.3. Configure el Número POS AFIP y la Dirección POS AFIP teniendo en cuenta lo que ha configurado en su Portal AFIP.

    NOTA: Puede usar el botón "Verificar POS AFIP disponible" en el formulario de Revistas para corroborar el uso que se usará para crear las revistas.

Para obtener más información sobre la facturación electrónica en Argentina, puede visitar http://www.afip.gob.ar/fe/ayuda.asp

Técnico
---------

Los servicios web que se implementan son los que son los más habituales:

* wsfev1 - "Factura Electrónica" (Electronic Invoice)
* wsbfev1 - "Bono Fiscal Electrónico" (Electronic Fiscal Bond)
* wsfexv1 - "Factura de Exportación Electrónica" (Electronic Exportation Invoice - same as Export Voucher)
* wscdc - "Constatación de Comprobantes" (Invoices Verification)


Para obtener imayor nformación sobre este desarrollo, puede visitar  http://www.afip.gob.ar/fe/documentos/WSBFEv1%20-%20Manual%20para%20el%20desarrollador.pdf

""",
    'depends': [
        'l10n_ar',
    ],
    'external_dependencies': {
        'python': ['pyOpenSSL', 'zeep']
    },
    'data': [
        'wizards/l10n_ar_afip_fe_consult_view.xml',
        'views/l10n_ar_afip_fe_connection_view.xml',
        'views/res_config_settings_view.xml',
        'views/account_move_view.xml',
        'views/account_journal_view.xml',
        'views/uom_uom_view.xml',
        'views/res_currency_view.xml',
        'views/product_template_view.xml',
        'views/report_invoice.xml',
        'security/ir.model.access.csv',
        'data/ir_actions_act_url_data.xml',
    ],
    'demo': [
        'demo/res_company_demo.xml',
        'demo/res_config_settings_demo_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
