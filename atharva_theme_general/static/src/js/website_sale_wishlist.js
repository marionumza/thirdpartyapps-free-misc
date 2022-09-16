odoo.define('atharva_theme_general.wishlist', function (require) {
"use strict";

var wishlist = require('website_sale_wishlist.wishlist');
var publicWidget = require('web.public.widget');
var wSaleUtils = require('website_sale.utils');
function getNavBarButton(selector) {
    var $afixheader = $('header.o_affix_enabled ' + selector);
    var $affixedHeaderButton = $('header.affixed ' + selector);
    if ( $afixheader.length) {
        return  $afixheader;
    }
    else if ($affixedHeaderButton.length) {
        return $affixedHeaderButton;
    } else {
        return $('header ' + selector).first();
    }
}

var ProductWishlist = publicWidget.registry.ProductWishlist;
return ProductWishlist.include({
    init: function () {
        this._super.apply(this, arguments);
    },
    _addNewProducts: function ($el) {
        var self = this;
        var $nvbutton = getNavBarButton('.o_wish_my_wish');
        if ($nvbutton.length == 0){
            return self._super.apply(self, arguments);
        }
        var productID = $el.data('product-product-id');
        if ($el.hasClass('o_add_wishlist_dyn')) {
            productID = $el.parent().find('.product_id').val();
            if (!productID) { // case List View Variants
                productID = $el.parent().find('input:checked').first().val();
            }
            productID = parseInt(productID, 10);
        }
        var $form = $el.closest('form');
        var templateId = $form.find('.product_template_id').val();
        // when adding from /shop instead of the product page, need another selector
        if (!templateId) {
            templateId = $el.data('product-template-id');
        }
        $el.prop("disabled", true).addClass('disabled');
        var productReady = this.selectOrCreateProduct(
            $el.closest('form'),
            productID,
            templateId,
            false
        );

        productReady.then(function (productId) {
            productId = parseInt(productId, 10);

            if (productId && !_.contains(self.wishlistProductIDs, productId)) {
                return self._rpc({
                    route: '/shop/wishlist/add',
                    params: {
                        product_id: productId,
                    },
                }).then(function () {
                    var $navButton = getNavBarButton('.o_wish_my_wish');
                    $('.o_wish_my_wish').removeAttr('style');
                    self.wishlistProductIDs.push(productId);
                    self._updateWishlistView();
                    wSaleUtils.animateClone($navButton, $el.closest('form'), 25, 40);
                }).guardedCatch(function () {
                    $el.prop("disabled", false).removeClass('disabled');
                });
            }
        }).guardedCatch(function () {
            $el.prop("disabled", false).removeClass('disabled');
        });
    },
    _addOrMoveWish: function (e) {
       var $nvbutton = getNavBarButton('.o_wish_my_wish');
        var self = this;
        if ($nvbutton.length == 0){
            return self._super.apply(self, arguments);
        }
        $('.o_wish_my_wish').removeAttr('style');
        var $navButton = getNavBarButton('.o_wish_my_wish');
        var tr = $(e.currentTarget).parents('tr');
        var product = tr.data('product-id');
        $('.o_wsale_my_cart').removeClass('d-none');
        wSaleUtils.animateClone($navButton, tr, 25, 40);

        if ($('#b2b_wish').is(':checked')) {
            return this._addToCart(product, tr.find('add_qty').val() || 1);
        } else {
            var adding_deffered = this._addToCart(product, tr.find('add_qty').val() || 1);
            this._removeWish(e, adding_deffered);
            return adding_deffered;
        }
    },
    _updateWishlistView: function () {
        if (this.wishlistProductIDs.length > 0) {
            $('.o_wsale_my_wish').show();
            $('.my_wish_quantity').text(this.wishlistProductIDs.length);
        } else {
            $('.o_wsale_my_wish').hide();
            $('.my_wish_quantity').text(this.wishlistProductIDs.length);
        }
    },
})


})
