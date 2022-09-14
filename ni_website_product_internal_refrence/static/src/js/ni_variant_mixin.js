odoo.define('ni_website_product_internal_refrence.ni_variant_mixin', function (require) {
"use strict";

var VariantMixin = require('sale.VariantMixin');
var publicWidget = require('web.public.widget');
var ajax = require('web.ajax');
var core = require('web.core');
var QWeb = core.qweb;

publicWidget.registry.WebsiteSale.include(_.extend({}, {
    _onChangeCombination: function (ev, $parent, combination) {
    var res = this._super.apply(this, arguments);
    var ni_default_code = document.getElementById("ni_default_code");
    if(ni_default_code != null){
        ni_default_code.innerHTML = combination.ni_default_code;
    }
    var ni_product_description = document.getElementById("ni_product_description");
        if(ni_product_description != null){
            if(combination.ni_product_description != false){
               ni_product_description.innerHTML = combination.ni_product_description;
            }else{
               ni_product_description.innerHTML = '';
                }
        }

    },
}));
});
