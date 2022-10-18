odoo.define('wt_create_so_from_pos.SaleOrderButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class SaleOrderButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        async onClick() {
            var self = this;
            const oderdetails = {};
            if (this.env.pos.get_client()){
                if (this.env.pos.get_order().get_orderlines().length > 0){
                    this.env.pos.get_order().get_orderlines().forEach(function(orderLine) {
                        oderdetails[orderLine.id] = { 
                            product: orderLine.get_product().id, 
                            quantity: orderLine.quantity,
                            price: orderLine.price,
                            discount: orderLine.discount,
                            };
                    });
                    if (this.env.pos.get_order().get_total_tax() > 0){
                        oderdetails['tax_amount'] = this.env.pos.get_order().get_total_tax()
                    }
                    oderdetails['partner_id'] = this.env.pos.get_client().id;
                    const result = await this.rpc({
                        model: 'sale.order',
                        method: 'craete_saleorder_from_pos',
                        args: [oderdetails],
                    });
                    if(result){
                        this.showScreen('ProductScreen');
                        await this.showPopup('ConfirmPopup', {
                            title: this.env._t('Successfully!'),
                            body: this.env._t(
                                'Sales Order ' + result.name +' Created Successfully!!!!'
                            ),
                        });
                    }

                }
                else if(this.env.pos.get_order().get_orderlines().length <= 0){
                    await this.showPopup('ErrorPopup', {
                        title: this.env._t('No Product'),
                        body: this.env._t("There are no Product for SaleOrder."),
                    });
                }
            }
            else{
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Unknown Customer'),
                    body: this.env._t("Select Customer."),
                });
            }
            
        }
    }
    SaleOrderButton.template = 'SaleOrderButton';

    ProductScreen.addControlButton({
        component: SaleOrderButton,
        condition: function() {
            return this.env.pos.config.create_so;
        },
    });

    Registries.Component.add(SaleOrderButton);

    return SaleOrderButton;
});
