odoo.define('l10n_ar_pos_eticket.pos_model', function (require) {
    var models = require('point_of_sale.models');
    var pos_model = require("point_of_sale.models");
    var rpc = require('web.rpc');
    var core = require('web.core');
    var qweb = core.qweb;

    var SuperPosModel = pos_model.PosModel.prototype;
    var SuperOrder = pos_model.Order.prototype;

    

    var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({

         renderElement: function() {
            var self = this;
            this._super();            
          
            if (this.pos.config.pos_auto_invoice) {
               this.$('.js_invoice').addClass('oe_hidden');
            }
        },


        initialize: function (attributes, options) {
            _super_Order.initialize.apply(this, arguments);
            if (this.pos.config.pos_auto_invoice) {
                this.to_invoice = true;
                
            }

            //agrega cliente por defecto agregado jm 02-03-2021
            var partner_default =  this.pos.config.partner_default;
            if (partner_default){         
            var client = this.pos.db.get_partner_by_id(partner_default[0]);         
            this.set_client(client);
            //this.set_to_invoice(true);
             console.log('cargando jm1');
        } 
        },
        init_from_JSON: function (json) {
            var res = _super_Order.init_from_JSON.apply(this, arguments);
            if (json.to_invoice) {
                this.to_invoice = json.to_invoice;
            
            }
        }
    });




    
});
