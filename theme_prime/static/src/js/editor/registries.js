/** @odoo-module alias=theme_prime.all_registries */
import { registry } from '@web/core/registry';

let PRODUCTS_ACTIONS = ['rating', 'quick_view', 'add_to_cart', 'comparison', 'wishlist', 'category_info', 'label'];
registry.category('theme_prime_card_registry')
    .add('s_card_style_1', {supportedActions: PRODUCTS_ACTIONS})
    .add('s_card_style_2', {supportedActions: PRODUCTS_ACTIONS})
    .add('s_card_style_3', {supportedActions: _.union(PRODUCTS_ACTIONS, ['show_similar'])})
    .add('s_card_style_4', {supportedActions: PRODUCTS_ACTIONS})
    .add('s_card_style_5', {supportedActions: _.union(PRODUCTS_ACTIONS, ['images'])})
    .add('s_card_style_6', { supportedActions: _.union(PRODUCTS_ACTIONS, ['show_similar', 'colors']) })
    .add('s_card_style_7', { supportedActions: _.union(PRODUCTS_ACTIONS, ['show_similar', 'colors'])})

registry.category('theme_prime_small_card_registry')
    .add('tp_category_product_card_style_1', { supportedActions: ['add_to_cart', 'rating', 'category_info']})
    .add('tp_category_product_card_style_2', { supportedActions: ['add_to_cart', 'category_info']})
    .add('tp_category_product_card_style_3', { supportedActions: ['add_to_cart']})

registry.category('theme_prime_top_category_card_registry')
    .add('tp_category_category_card_style_1', {})
    .add('tp_category_category_card_style_2', {})

registry.category('theme_prime_two_column_card_registry')
    .add('tp_two_column_card_style_1', { supportedActions: ['rating', 'category_info', 'add_to_cart', 'wishlist', 'comparison', 'description_sale', 'label']})
    .add('tp_two_column_card_style_2', { supportedActions: ['rating', 'category_info', 'add_to_cart', 'wishlist', 'comparison', 'description_sale', 'label', 'colors']})
    .add('tp_two_column_card_style_3', { supportedActions: ['rating', 'category_info', 'add_to_cart', 'wishlist', 'comparison', 'description_sale', 'label', 'colors']});

registry.category('theme_prime_snippet_registry')
    .add('d_products_snippet', { widgets: { SelectionComponent: { model: 'product.template' }, UiComponent: { cardRegistry: 'theme_prime_card_registry', subComponents: ['style', 'mode', 'ppr'] } } })
    .add('s_two_column_card', { widgets: { SelectionComponent: { model: 'product.template' }, UiComponent: { cardRegistry: 'theme_prime_two_column_card_registry', subComponents: ['style', 'mode'] } } })
    .add('s_d_single_product_count_down', { widgets: { SelectionComponent: { model: 'product.template' } }, defaultValue: { recordsLimit: 5, noConfirmBtn: true, noSwicher: true } })
    .add('s_d_products_grid', { widgets: { SelectionComponent: { model: 'product.template' } }, defaultValue: { recordsLimit: 9, noConfirmBtn: true, noSwicher: true } })
    .add('d_category_snippet', { widgets: { SelectionComponent: { model: 'product.public.category', subModel: 'product.template' }, UiComponent: { cardRegistry: 'theme_prime_card_registry', subComponents: ['style', 'mode', 'ppr', 'tabStyle', 'sortBy', 'limit', 'includesChild'] } } })
    .add('s_products_by_brands_tabs', { widgets: { SelectionComponent: { model: 'product.attribute.value', subModel: 'product.template' }, UiComponent: { cardRegistry: 'theme_prime_card_registry', subComponents: ['style', 'mode', 'ppr', 'tabStyle', 'sortBy', 'limit'] } } })
    .add('d_single_category_snippet', { widgets: { SelectionComponent: { model: 'product.public.category', subModel: 'product.template' }, UiComponent: { cardRegistry: 'theme_prime_small_card_registry', subComponents: ['style', 'sortBy', 'includesChild'] } }, defaultValue: { recordsLimit: 1, noSwicher: true } })
    .add('d_single_product_snippet', { widgets: { SelectionComponent: { model: 'product.template' } }, defaultValue: { recordsLimit: 1, noConfirmBtn: true, noSwicher: true } })
    .add('s_d_single_product_cover_snippet', { widgets: { SelectionComponent: { model: 'product.template' } }, defaultValue: { recordsLimit: 1, noConfirmBtn: true, noSwicher: true } })
    .add('s_d_product_count_down', { widgets: { SelectionComponent: { model: 'product.template' } }, defaultValue: { noConfirmBtn: true } })
    .add('s_d_product_small_block', { widgets: { SelectionComponent: { model: 'product.template' } }, defaultValue: { noConfirmBtn: true } })
    .add('s_d_image_products_block', { widgets: { SelectionComponent: { model: 'product.template' } }, defaultValue: { noConfirmBtn: true } })
    .add('d_top_categories', { widgets: { SelectionComponent: { model: 'product.public.category', subModel: 'product.template' }, UiComponent: { cardRegistry: 'theme_prime_top_category_card_registry', subComponents: ['style', 'sortBy', 'includesChild'] } }, defaultValue: { recordsLimit: 3, noSwicher: true } })
    .add('s_category_snippet', { widgets: { SelectionComponent: { model: 'product.public.category', subModel: 'product.template' }, UiComponent: { cardRegistry: 'theme_prime_category_card_registry', subComponents: ['style'] } }, defaultValue: { noSwicher: true } })
    .add('s_product_listing_cards', { widgets: { UiComponent: { noSelection: true, cardRegistry: 'theme_prime_product_list_cards', headerRegistry: 'theme_prime_product_list_cards_headers', subComponents: ['style', 'limit', 'header', 'bestseller', 'newArrived', 'discount'] } }})
    // .add('s_product_listing_tabs', { widgets: { UiComponent: { noSelection: true, cardRegistry: 'theme_prime_card_registry', subComponents: ['style', 'mode', 'ppr', 'tabStyle', 'limit', 'bestseller', 'newArrived', 'discount'] } }})
    .add('s_product_listing_tabs', { widgets: { SelectionComponent: { model: 'product.public.category', subModel: 'product.template' }, UiComponent: { cardRegistry: 'theme_prime_card_registry', subComponents: ['style', 'mode', 'ppr', 'tabStyle', 'limit', 'bestseller', 'newArrived', 'discount'] } }, defaultValue: { recordsLimit: 1, noSwicher: true } })
    .add('s_tp_mega_menu_category_snippet', { widgets: { SelectionComponent: { model: 'product.public.category', subModel: 'product.template' }, UiComponent: { cardRegistry: 'theme_prime_mega_menu_cards', maxValue: 10, minValue: 2, subComponents: ['style', 'productListing', 'limit', 'childOrder'] } }, defaultValue: { noSwicher: true } })
    .add('s_category_tabs_snippet', { widgets: { SelectionComponent: { model: 'product.public.category', subModel: 'product.template' }, UiComponent: { cardRegistry: 'theme_prime_mega_menu_tabs_styles', maxValue: 12, minValue: 2, subComponents: ['style', 'limit', 'categoryTabsConfig', 'menuLabel', 'childOrder'] } }, defaultValue: { noSwicher: true } });

registry.category('theme_prime_category_card_registry')
    .add('s_tp_category_style_1', {})
    .add('s_tp_category_style_2', {})
    .add('s_tp_category_style_3', {})
    .add('s_tp_category_style_4', {})
    .add('s_tp_category_style_5', {});

registry.category('theme_prime_product_list_cards')
    .add('tp_product_list_cards_1', {supportedActions: ['rating']})
    .add('tp_product_list_cards_2', {supportedActions: ['rating']})
    .add('tp_product_list_cards_3', {supportedActions: ['rating', 'add_to_cart']})
    .add('tp_product_list_cards_4', {supportedActions: ['rating', 'add_to_cart', 'wishlist', 'quick_view']});

registry.category('theme_prime_product_list_cards_headers')
    .add('tp_product_list_header_1', {})
    .add('tp_product_list_header_2', {})
    .add('tp_product_list_header_3', {});

registry.category('theme_prime_mega_menu_tabs_styles')
    .add('tp_mega_menu_tab_style_1', {})
    .add('tp_mega_menu_tab_style_2', {})

registry.category('theme_prime_mega_menu_cards')
    .add('s_tp_hierarchical_category_style_1', {supportedActions: ['limit', 'brand', 'label', 'count', 'style', 'background']})
    .add('s_tp_hierarchical_category_style_2', {supportedActions: ['limit', 'brand', 'label', 'count', 'style', 'background']})
    .add('s_tp_hierarchical_category_style_3', {supportedActions: ['limit', 'brand', 'label', 'count', 'style', 'background']})
    .add('s_tp_hierarchical_category_style_4', {supportedActions: ['limit', 'brand', 'label', 'count', 'style', 'background']})
    .add('s_tp_hierarchical_category_style_5', {supportedActions: ['productListing', 'limit', 'brand', 'label', 'count', 'style', 'background']})
    .add('s_tp_hierarchical_category_style_6', {supportedActions: ['limit', 'brand', 'label', 'count', 'style', 'background']})
    .add('s_tp_hierarchical_category_style_7', {supportedActions: ['limit', 'brand', 'label', 'count', 'style', 'background']})
    .add('s_tp_hierarchical_category_style_8', {supportedActions: ['limit', 'brand', 'label', 'count', 'style', 'background']})
    .add('s_tp_hierarchical_category_style_9', {supportedActions: ['limit', 'brand', 'label', 'count', 'style', 'background']})
    .add('s_tp_hierarchical_category_style_10', {supportedActions: ['limit', 'brand', 'label', 'count', 'style', 'background']})
    .add('s_tp_hierarchical_category_style_11', {supportedActions: ['limit', 'brand', 'label', 'count', 'style', 'background']});