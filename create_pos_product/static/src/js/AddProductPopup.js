odoo.define('create_pos_product.Add_product_popup', function (require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { _t } = require('web.core');
    const { parse } = require('web.field_utils');

    class Add_product_popup extends AbstractAwaitablePopup {
        setup() {
            this.state = owl.hooks.useState({
                inputType: '',
                inputAmount: '',
                inputName: '',
                inputCategory: '',
                unitMeasure: '',
                barcode: '',
            });
            this.inputAmountRef = owl.hooks.useRef('input-amount-ref');
        }
        getPayload() {
            var lis_vals = [];
            var product_category = this.state.inputCategory;
            var product = this.state.inputName;
            var price = this.state.inputAmount;
            var unit = this.state.unitMeasure;
            var product_type = this.state.inputType;
            var barcode = this.state.barcode;
            lis_vals.push(product_category);
            lis_vals.push(product);
            lis_vals.push(price);
            lis_vals.push(product_type);
            lis_vals.push(unit);
            lis_vals.push(barcode);
            return lis_vals
        }
    }
    Add_product_popup.template = 'Add_product_popup';
    Add_product_popup.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
        array: [],
        title: 'Create Product',
        body: '',
        startingValue: '',
        priceValue: 1,
        list: [],
    };

    Registries.Component.add(Add_product_popup);

    return Add_product_popup;
});
