odoo.define('pos_l10n_ar_identification.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models');

    models.load_fields('res.partner', ['l10n_ar_afip_responsibility_type_id',
                                          'l10n_latam_identification_type_id']);


    

   models.load_models({
            model: 'l10n_ar.afip.responsibility.type',
            fields: [],
            loaded: function (self, responsability_type) {
            self.responsability_type=responsability_type;
                
            },
        });

    models.load_models([
        {
            model: 'l10n_latam.identification.type',
            fields: [],
            loaded: function (self, identification_type) {
                self.identification_type = identification_type;
            }
        }
    ]);






   

}); 
