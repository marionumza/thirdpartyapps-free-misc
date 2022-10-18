odoo.define('create_pos_product.CustomListScreen', function(require) {
    'use strict';

    const { debounce } = owl.utils;
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('web.custom_hooks');
    const { isConnectionError } = require('point_of_sale.utils');
    const { useAsyncLockedMethod } = require('point_of_sale.custom_hooks');
    const ajax = require('web.ajax');

    class CustomListScreen extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('update-search', this._updateSearch);
            this.state = owl.hooks.useState({ searchWord: '' });

            this.state = {
                query: null,
                productID: 0,
                prod_lst:[],
                productIds: [],
                detailIsShown: false,
                isEditMode: false,
                editModeProps: {
                    partner: {
                        country_id: this.env.pos.company.country_id,
                        state_id: this.env.pos.company.state_id,
                    }
                },
            };
            this.updateProductList = debounce(this.updateProductList, 70);
        }
        back() {
            if(this.state.detailIsShown) {
                this.state.detailIsShown = false;
                this.render();
            } else {
                this.props.resolve({ confirmed: false, payload: false });
                this.trigger('close-temp-screen');
            }
        }
        async button_click()
        {
            var self = this;
            const {
                confirmed,
                payload
            } = await this.showPopup('Add_product_popup', {
                title: this.env._t(' Add Product'),
                body: this.env._t('Add New Product'),
            });
            if (confirmed) {
                var product_category = payload[0];
                var product_name = payload[1];
                var product_price = payload[2];
                var product_type = payload[3];
                var product_uom = payload[4];
                var product_barcode = payload[5];
                ajax.jsonRpc('/Add_Product', 'call', {
                    'category': product_category,
                    'name': product_name,
                    'price': product_price,
                    'uom': product_uom,
                    'type': product_type,
                    'barcode': product_barcode,
                }).then(function(response) {});
            }
        }

        get searchWord() {
            return this.state.searchWord.trim();
        }
        async _updateSearch(event) {
        this.state.searchWord = event.detail;
       let foundProductIds = [];
        foundProductIds = await this.rpc({
        model: 'product.product',
        method: 'search',
        args: [[['name', 'ilike', this.state.searchWord]]],
        context: this.env.session.user_context,
        });

        if(this.state.searchWord=='')
        {
        this.state.productID = 0;
        this.render_list();
        }

        else
        {
        if(foundProductIds.length<=0)
        {
        $("#table-body").empty();
        alert("No Product Found");
        }
        else
        {
        this.state.productIds=[];
        for(let i=0; i<foundProductIds.length; i++)
        {
        this.state.productIds.push(foundProductIds[i]);
        }
        this.state.productID = foundProductIds[0];
        this.render_list();
        }
        }
        return this.state.productID;
        }

        reload(){
            window.location.reload();
        }
        get productID()
        {
        return this.state.productID;
        }

        get productsToDisplay() {
           let res;
           if(this.state.productID!==0)
           {
           this.state.prod_lst=[];
           for(let i=0; i<this.state.productIds.length; i++)
           {
           res = this.env.pos.db.get_product_by_id(this.state.productIds[i]);
           if(res)
           {
           this.state.prod_lst.push(res);
           }
           }
           }
           else
           {
           this.state.prod_lst=[];
           res = this.env.pos.db.get_product_by_category(0);
           this.state.prod_lst.push(res);
           }
            return res;
            }


        render_list(){

        $("#table-body").empty();
        const products = this.productsToDisplay;
        if(this.state.productID!==0)
        {
        var rows ="";
        for(let i=0; i<this.state.prod_lst.length; i++)
        {
        let prod = this.state.prod_lst[i];
        if(prod.barcode)
        {
        rows = "<tr><td>"+prod.display_name+"</td><td>"+prod.categ_id[1]+"</td><td>"+prod.lst_price+"</td><td>"+prod.barcode+"</td></tr>"
        }
        else
        {
        rows = "<tr><td>"+prod.display_name+"</td><td>"+prod.categ_id[1]+"</td><td>"+prod.lst_price+"</td><td>"+"-"+"</td></tr>"
        }
        $(rows).appendTo("#list tbody");
        var rows = document.getElementById('list').rows;
        for (var row = 0; row < rows.length; row++) {
        var cols = rows[row].cells;
        }
        }
        }
        else
        {
        let all_prod = this.state.prod_lst[0];
        for(let i=0; i<all_prod.length; i++)
        {
        let prod = all_prod[i];
        if(prod.barcode)
        {
        rows = "<tr><td>"+prod.display_name+"</td><td>"+prod.categ_id[1]+"</td><td>"+prod.lst_price+"</td><td>"+prod.barcode+"</td></tr>"
        }
        else
        {
        rows = "<tr><td>"+prod.display_name+"</td><td>"+prod.categ_id[1]+"</td><td>"+prod.lst_price+"</td><td>"+"-"+"</td></tr>"
        }
        $(rows).appendTo("#list tbody");
        var rows = document.getElementById('list').rows;
        for (var row = 0; row < rows.length; row++) {
        var cols = rows[row].cells;
        }
        }
        }
        }

        get currentOrder() {
            return this.env.pos.get_order();
        }
        async updateSearch(event) {
        if(event.code==="Enter")
        {
        console.log();
        }
        else if(event.code==="Backspace" && this.state.searchWord=='')
        {
        console.log();
        }
        else
        {
        this.trigger('update-search', event.target.value);
        }
        }
    }
    CustomListScreen.template = 'CustomListScreen';

    Registries.Component.add(CustomListScreen);

    return CustomListScreen;
});
