odoo.define('pos_expenses_pay.SaleOrderScreen', function (require) {
    'use strict';

    const { useState } = owl.hooks;
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('web.custom_hooks');

    class SaleOrderScreen extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('close-screen', this.back);
            useListener('click-sale-order', this._onClickSaleOrder);
            this.state = useState({
                orders: []
            });
        }
        async mounted(){
            super.mounted;
            this.state.orders = await this.orders();
        }
        back() {
            this.showScreen('ProductScreen');
        }
        get date() {
            return moment(this.order.date_order).format('YYYY-MM-DD hh:mm A');
        }

        async orders() {
            var result = Promise.resolve()
            result = await this.rpc({
                model: 'sale.order',
                method: 'search_read',
                kwargs: {
                    domain: [['is_pos_created', '=', true]],
                    fields: ['id', 'name', 'partner_id', 'date_order', 'state', 'amount_total', 'user_id'],
                }
            });
            return result;
        }

        async _onClickSaleOrder(event) {
            const clickedOrder = event.detail;
            const { confirmed, payload: selectedOption } = await this.showPopup('SalesSelectionPopup',
                {
                    title: this.env._t('Sale Order')  + '  ' + clickedOrder.name,
                    list: [
                            {
                                id:1, 
                                label: this.env._t("Confirm Sales Order"), 
                                item: true,
                                icon: 'fa fa-check-circle',
                            }, 
                        {
                            id:2, 
                            label: this.env._t("Cancel Sales Order"), 
                            item: false,
                            icon: 'fa fa-close',
                        }
                    ],
                });
            if (confirmed){
                if(selectedOption){
                    if (clickedOrder.state !== 'sale') {
                        var result = await this.rpc({
                            model: 'sale.order',
                            method: 'action_confirm',
                            args: [clickedOrder.id]
                        });
                    }
                    else {
                        await this.showPopup('ConfirmPopup', {
                            title: this.env._t('Already Confirmed'),
                            body: this.env._t(
                                'This Sales Order is Already in confirmed state!!!!'
                            ),
                        });
                    }
                }
                if (!selectedOption){
                    if (clickedOrder.state !== 'cancel') {
                        var result = await this.rpc({
                            model: 'sale.order',
                            method: 'action_cancel',
                            args: [clickedOrder.id]
                        });
                    }
                    else {
                        await this.showPopup('ConfirmPopup', {
                            title: this.env._t('Already Cancelled'),
                            body: this.env._t(
                                'This Sales Order is Already in Cancel State!!!!'
                            ),
                        });
                    }
                }
            }
        }
    }
    SaleOrderScreen.template = 'SaleOrderScreenWidget';
    SaleOrderScreen.defaultProps = {
    };

    Registries.Component.add(SaleOrderScreen);

    return SaleOrderScreen;
});