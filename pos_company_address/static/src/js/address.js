odoo.define('pos_company_address.address', function (require) {
"use strict";

    var models = require('point_of_sale.models');
    models.load_fields('res.company', ['street', 'street2', 'city', ]);

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        export_for_printing: function(){
            var receipt = _super_order.export_for_printing.apply(this,arguments);
            var company = this.pos.company;
            receipt.company.street = company.street;
            receipt.company.street2 = company.street2;
            receipt.company.city = company.city;
            return receipt;
        },
    });

});


