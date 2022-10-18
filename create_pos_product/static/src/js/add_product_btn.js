odoo.define('create_pos_product.CustomRewardButtons', function(require) {
'use strict';
   const { Gui } = require('point_of_sale.Gui');
   const PosComponent = require('point_of_sale.PosComponent');
   const { posbus } = require('point_of_sale.utils');
   const ProductScreen = require('point_of_sale.ProductScreen');
   const { useListener } = require('web.custom_hooks');
   const Registries = require('point_of_sale.Registries');
   const PaymentScreen = require('point_of_sale.PaymentScreen');
   const ajax = require('web.ajax');
   class CustomRewardButtons extends PosComponent {
       constructor() {
           super(...arguments);
           useListener('click', this.onClick);
       }
       is_available() {
           const order = this.env.pos.get_order();
           return order
       }
       async onClick() {
            await this.showTempScreen('CustomListScreen');
        }
   }
   CustomRewardButtons.template = 'CustomRewardButtons';
   ProductScreen.addControlButton({
       component: CustomRewardButtons,
       condition: function() {
           return this.env.pos;
       },
   });
   Registries.Component.add(CustomRewardButtons);
   return CustomRewardButtons;
});