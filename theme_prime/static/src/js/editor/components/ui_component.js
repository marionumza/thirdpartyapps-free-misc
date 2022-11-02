/** @odoo-module alias=theme_prime.ui_component */
import AbstractComponent from '@theme_prime/js/editor/components/abstract_component';
import { registry } from '@web/core/registry';
import { _t, qweb } from 'web.core';
import { DroggolUtils } from 'theme_prime.mixins';
let UiComponent = AbstractComponent.extend(DroggolUtils, {
    template: 'theme_prime.ui_component',
    xmlDependencies: AbstractComponent.prototype.xmlDependencies.concat(['/theme_prime/static/src/xml/editor/components/ui_component.xml']),
    events: {
        'click .tp-switch-to-selector': '_onClickSwitchToSelector',
        'click .tp-action:not(.tp-action-disabled)': '_onClickAction',
        'click .tp-preview-container a': '_onClickLink',
    },
    componentAttrName: 'data-ui-config-info',
    /**
     * @constructor
     */
    init: function (parent, options) {
        this._super.apply(this, arguments);
        this.stylesRegistry = registry.category(options.cardRegistry);
        this.headerRegistry = registry.category(options.headerRegistry);
        this.$relatedTarget = options.$target.clone();
        this.styles = _.keys(this.stylesRegistry.content);
        this.style = options.style || this.styles[0];
        this.headers = _.keys(this.headerRegistry.content);
        this.header = options.header || this.headers[0];
        this.mode = options.mode || 'slider';
        this.ppr = options.ppr || 4;
        this.activeActions = options.activeActions || this._getSupportedAction();
        this.subModel = options.subModel || false;
        this.model = options.model || false;
        this.tabStyle = options.tabStyle || 'tp-dynamic-snippet-tab-1';
        this.sortBy = options.sortBy || 'list_price asc';
        this.includesChild = _.contains(_.keys(options), 'includesChild') ? options.includesChild : true;
        this.bestseller = options.bestseller;
        this.newArrived = options.newArrived;
        this.discount = options.discount;
        this.subComponents = options.subComponents || [];
        this.limit = options.limit || 5;
        this.maxValue = options.maxValue || 20;
        this.minValue = options.minValue || 4;
        this.noSelection = options.noSelection || false;
        this.menuLabel = options.menuLabel || false;
        this.childOrder = options.childOrder || 'count';
        this.categoryTabsConfig = options.categoryTabsConfig || {};
        this.productListing = options.productListing || 'bestseller';
    },
    /**
     * @override
     */
    willStart: async function () {
        const res = this._super(...arguments);
        this.shopConfig = await this._getShopConfig() || {};
        return res;
    },
    /**
     * @override
     */
    start: function () {
        this._super.apply(this, arguments);
        if (this._isSelectionConfigSet()) {
            this._appendPreview();
            this._refreshPreview(this.$relatedTarget);
        }
        this._refreshActions();
    },

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------
    /**
     * @public
     * @param operation {String} node attribute
     * @param value {Object}
     */
    setAttrsNode: function (attr, value) {
        this.$relatedTarget.attr(attr, JSON.stringify(value));
        if (this._isSelectionConfigSet()) {
            this._appendPreview()
        }
        this._refreshPreview(this.$relatedTarget);
    },
    /**
     * @public
     * @override
     */
    ComponentCurrentState: function () {
        // auto call _getComponentState method for subComponents list
        let allResult = {
            style: this._getComponentState('style'),
            header: this._getComponentState('header'),
            mode: this._getComponentState('mode'),
            tabStyle: this._getComponentState('tabStyle'),
            productListing: this._getComponentState('productListing'),
            sortBy: this._getComponentState('sortBy'),
            ppr: parseInt(this._getComponentState('ppr')),
            includesChild: this._getComponentState('includesChild'),
            bestseller: this._getComponentState('bestseller'),
            newArrived: this._getComponentState('newArrived'),
            discount: this._getComponentState('discount'),
            limit: parseInt(this._getComponentState('limit')),
            categoryTabsConfig: this._getComponentState('categoryTabsConfig'),
            menuLabel: this._getComponentState('menuLabel'),
            childOrder: this._getComponentState('childOrder'),
        };
        let result = this._filterResult(allResult);
        _.extend(result, {activeActions: this.activeActions, model:this.model});
        return result;
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     * Append Preview
     */
    _appendPreview: function () {
        this.$('.tp-preview-container').empty().append(this.$relatedTarget);
    },
    /**
     * @private
     * @returns {object}
     */
    _fillUpDefaults: function (records, state) {
        _.each(records, record => {
            let matchedRecord = _.findWhere(state, { id: record.id });
            if (matchedRecord) {
                record = _.defaults(record, matchedRecord);
            }
        });
        return { records: records };
    },
    /**
     * @private
     * @returns {object}
     */
    _getAction: function (action) {
        let allActions = { colors: {icon: 'fa fa-paint-brush', label: _t('Colors')}, count: { icon: 'fa fa-hashtag', label: _t("Count") }, brand: { icon: 'dri dri-tag-l', label: _t("Brands") }, quick_view: { icon: 'dri dri-eye', label: _t('QUICK VIEW') }, add_to_cart: { icon: 'dri dri-cart', label: _t('ADD TO CART') }, category_info: { icon: 'fa fa-font', label: _t('CATEGORY') }, wishlist: { icon: 'fa fa-heart-o', label: _t('WISHLIST') }, comparison: { icon: 'dri dri-compare', label: _t('COMPARE') }, rating: { icon: 'fa fa-star', label: _t('RATING') }, description_sale: { icon: 'fa fa-align-left', label: _t('DESCRIPTION') }, label: { icon: 'fa fa-bookmark-o', label: _t('LABEL') }, images: { icon: 'fa fa-photo', label: _t('MULTI-IMAGES') }, show_similar: { icon: 'fa fa-clone', label: _t('SIMILAR') }};
        let selectedAction = _.contains(_.keys(allActions), action) ? allActions[action] : false;
        if (_.contains(['rating', 'wishlist', 'comparison'], action) && !this.shopConfig[`is_${action}_active`]) {
            selectedAction['disabled'] = true;
            selectedAction['title'] = `${action} is disabled from the shop if you want to use it please enable it from the shop`;
        }
        return selectedAction;
    },
    /**
     * @private
     * @returns {object}
     */
    _getDefaultFieldValue: function () {
        // TO-DO only call those methods which component is used must be done in Abstract not here
        return {
            style: this._getStyles(),
            header: this._getHeaders(),
            mode: this._getMode(),
            ppr: { value: this.ppr },
            tabStyle: this._getTabStyles(),
            sortBy: this._getSortBy(),
            productListing: this._getProductListing(),
            limit: { value: this.limit, maxValue: this.maxValue, minValue: this.minValue },
            includesChild: {value: this.includesChild},
            bestseller: {value: this.bestseller},
            newArrived: {value: this.newArrived},
            discount: {value: this.discount},
            menuLabel: { value: this.menuLabel },
            childOrder: this._getChildOrder(),
            categoryTabsConfig: this._getCategoryTabsConfig(),
        };
    },
    /**
     * @private
     * @returns {object}
     */
    _getCategoryTabsConfig: function () {
        let resComponent = this.parentComponent._getComponentByName("productSelection");
        let recordsIDs = resComponent.ComponentCurrentState();
        let records = resComponent.getRecordsData(recordsIDs);
        if (_.contains(_.keys(this.destroyedComponents), 'categoryTabsConfig')) {
            return this._fillUpDefaults(records, this.destroyedComponents.categoryTabsConfig.records)
        } else if (_.contains(_.keys(this.categoryTabsConfig), 'records')) {
            return this._fillUpDefaults(records, this.categoryTabsConfig.records);
        }
        return { records: records };
    },
    /**
     * @private
     * @returns {object}
     */
    _getMode: function () {
        return {
            recordID: this.mode || 'grid',
            records: [{ id: 'grid', iconClass: 'dri dri-category pr-2', title: _t('Grid') }, { iconClass: 'fa pr-2 fa-arrows-h', id: 'slider', title: _t('Slider') }]
        }
    },
    /**
     * @private
     * @returns {object}
     */
    _getHeaders: function () {
        return {
            recordID: this.header,
            records: _.map(this.headers, function (style, index) { return { id: style, title: _t(`Style - ${index + 1}`) }; })
        };
    },
    /**
     * @private
     * @returns {object}
     */
    _getStyles: function () {
        return {
            recordID: this.style,
            records: _.map(this.styles, function (style, index) { return { id: style, title: _t(`Style - ${index + 1}`) }; })
        };
    },
    /**
     * @private
     * @returns {Array}
     */
    _getSupportedAction: function () {
        return this.stylesRegistry.get(this.style).supportedActions || [];
    },
    /**
     * @private
     * @returns {Array}
     */
    _getSortBy: function () {
        return {
            recordID: this.sortBy,
            records: [{ id: 'list_price asc', iconClass: 'fa fa-sort-numeric-asc', title: _t("Price: Low to High") }, { id: 'list_price desc', iconClass: 'fa fa-sort-numeric-desc', title: _t("Price: High to Low") }, { id: 'name asc', iconClass: 'fa fa-sort-alpha-asc', title: _t("Name: A to Z") }, { id: 'name desc', iconClass: 'fa fa-sort-alpha-desc', title: _t("Name: Z to A") }, { iconClass: 'fa fa-clock-o', id: 'create_date desc', title: _t("Newly Arrived") }, { id: 'bestseller', iconClass: 'dri dri-bolt', title: _t("Bestseller")}]
        };
    },
    /**
     * @private
     * @returns {Array}
     */
    _getChildOrder: function () {
        return {
            recordID: this.childOrder,
            records: [{ id: 'count', title: _t("No. of Products") }, { id: 'sequence', title: _t("Sequence") }]
        };
    },
    /**
     * @private
     * @returns {Array}
     */
    _getProductListing: function () {
        return {
            recordID: this.productListing,
            records: [{ iconClass: 'fa fa-percent', id: 'discount', title: _t("On Sale") }, { iconClass: 'fa fa-clock-o', id: 'newArrived', title: _t("Newly Arrived") }, { id: 'bestseller', iconClass: 'dri dri-bolt', title: _t("Bestseller")}]
        };
    },
    /**
     * @private
     * @returns {Array}
     */
    _getTabStyles: function () {
        return {
            recordID: this.tabStyle,
            records: _.map([1, 2, 3, 4, 5, 6], function (style, index) { return { id: `tp-dynamic-snippet-tab-${index+1}`, title: _t(`Style - ${index + 1}`) }; })
        };
    },
    /**
     * @private
     * @returns {Boolean}
     */
    _isSelectionConfigSet: function () {
        return this.noSelection ? this.noSelection : this.$relatedTarget[0].hasAttribute('data-selection-info');
    },
    /**
     * @private
     * @returns {Boolean}
     */
    _isUiConfigSet: function () {
        return this.$relatedTarget[0].hasAttribute(this.componentAttrName);
    },
    /**
     * @private
     * @returns {Boolean}
     */
    _isVisible: function (component) {
        return _.contains(this.subComponents, component);
    },
    /**
     * @private
     * @param operation {String} possible values (add/delete)
     * @param recordID {Integer} ID of record
     * Update widget state accordingly
     */
    _notifyActionChanges: async function (operation, actionID) {
        switch (operation) {
            case 'add':
                if (!_.contains(this.activeActions, actionID)) {
                    this.activeActions.push(actionID);
                }
                break;
            case 'delete':
                this.activeActions = _.without(this.activeActions, actionID);
                break;
        }
        this._refreshActions();
        this.setAttrsNode(this.componentAttrName, this.ComponentCurrentState());
    },
    /**
     * @private
     */
    _refreshActions: function () {
        let $actions = $(qweb.render('theme_prime.tp_ui_actions', { widget: this }));
        this.$('.tp-actions-container').empty().append($actions);
    },
    /**
     * @private
     */
    _refreshPreview: function ($target) {
        if (this._isSelectionConfigSet() && this._isUiConfigSet()) {
            this.trigger_up('widgets_start_request', {
                editableMode: true,
                $target: $target,
                onSuccess: this._onSuccess.bind(this),
            });
            this.$('.tp-preview-container').removeClass('d-none');
        }
    },
    _resetActions: function () {
        this.activeActions = this._getSupportedAction();
        this._refreshActions();
    },
    _notifyParentComponentStateChange: function () {
        this._forceRefreshComponent('categoryTabsConfig');
        this.categoryTabsConfig = {};
        this.setAttrsNode(this.componentAttrName, this.ComponentCurrentState());
        this.setAttrsNode(this.parentComponent.componentAttrName, this.parentComponent.ComponentCurrentState());
    },
    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _onClickSwitchToSelector: function () {
        this.trigger_up('tp_change_visibility', { hideField: this.fieldName, displayField: 'SelectionComponent'});
    },
    /**
     * @private
     * @param {MouseEvent} ev
     */
    _onClickAction: function (ev) {
        let $target = $(ev.currentTarget);
        let actionName = $target.attr('data-action-name');
        if ($target.hasClass('tp-action-active')) {
            this._notifyActionChanges('delete', actionName)
        } else {
            this._notifyActionChanges('add', actionName)
        }
    },
    /**
     * @override
     */
    _onChangeComponentValue: function (ev) {
        this._super.apply(this, arguments);
        let { fieldName, value } = ev.data;
        if (_.contains(this.subComponents, fieldName)) {
            this[fieldName] = value;
            if (fieldName === 'style') {
                this._resetActions()
            }
        }
        this.setAttrsNode(this.componentAttrName, this.ComponentCurrentState());
    },
    /**
     * @private
     * @param {MouseEvent} ev
     */
    _onSuccess: function () {
        this.$('.tp-no-data-template').remove();
        _.delay(() => {
            let height = this.$('.tp-preview-container > [data-tp-snippet-id]').height() + 16;
            this.$('.tp-preview-container').css("min-height", height + 'px');
        }, 1500);
    },
    /**
     * @private
     * @param {MouseEvent} ev
     */
    _onClickLink: function (ev) {
        ev.preventDefault();
    }
});

registry.category("theme_prime_components").add("UiComponent", UiComponent);
export default UiComponent;