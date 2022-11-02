// -*- coding: utf-8 -*-
// Copyright 2018, 2020 Heliconia Solutions Pvt Ltd (https://heliconia.io)

odoo.define("hspl_menu_category", function (require) {
    "use strict";

    var AppsMenu = require("web.AppsMenu");
    var Menu = require("web.Menu");
    var webClient = require("web.WebClient");
    var SystrayMenu = require("web.SystrayMenu");
    var dom = require("web.dom");

    webClient.include({
        _loadMenuCtg: function () {
            return this._rpc({
                model: "ir.ui.menu.category",
                method: "get_category",
            }).then(function (ctgData) {
                return ctgData;
            });
        },

        instanciate_menu_widgets: function () {
            var self = this;
            var defs = [];
            var loadmenu = this.load_menus();
            var loadctgs = this._loadMenuCtg();

            return $.when(loadmenu, loadctgs).done(function (menuData, ctgData) {
                self.menu_data = menuData;
                self.ctg_data = ctgData;
                // Here, we instanciate every menu widgets and we immediately append them into dummy
                // document fragments, so that their `start` method are executed before inserting them
                // into the DOM.
                if (self.menu) {
                    self.menu.destroy();
                }
                self.menu = new Menu(self, menuData, ctgData);
                defs.push(self.menu.prependTo(self.$el));
                return $.when.apply($, defs);
            });
        },
    });

    AppsMenu.include({
        init: function (parent, menuData, ctg_data) {
            this._super.apply(this, arguments);

            for (var c in this._apps) {
                this._apps[c].category_id = menuData.children[c].category_id;
            }
            this.ctg_data = ctg_data;
            setTimeout(this.appendAppsCategorywise, 1000);
            this._ctgs = _.map(ctg_data, function (appCtgData) {
                return {
                    ctgID: appCtgData.id,
                    name: appCtgData.name,
                };
            });
        },

        get_category: function () {
            return this._ctgs;
        },
        appendAppsCategorywise: function () {
            $(".categ_ind").each(function () {
                var ctg_ind = $(this);
                var ctg_id = ctg_ind.find("input").attr("data-value");

                $(".dropdown-item.o_app").each(function () {
                    var menu_ind = $(this);
                    var menu_id = menu_ind.find("input").attr("data-value");
                    if (ctg_id === menu_id) {
                        ctg_ind.append(menu_ind);
                    }
                });
            });
        },
    });

    Menu.include({
        init: function (parent, menu_data, ctg_data) {
            this._super.apply(this, arguments);
            this.ctg_data = ctg_data;
        },

        start: function () {
            var self = this;
            this.$menu_toggle = this.$(".o-menu-toggle");
            this.$menu_apps = this.$(".o_menu_apps");
            this.$menu_brand_placeholder = this.$(".o_menu_brand");
            this.$section_placeholder = this.$(".o_menu_sections");

            // Navbar's menus event handlers
            var on_secondary_menu_click = function (ev) {
                ev.preventDefault();
                var menu_id = $(ev.currentTarget).data("menu");
                var action_id = $(ev.currentTarget).data("action-id");
                self._on_secondary_menu_click(menu_id, action_id);
            };
            var menu_ids = _.keys(this.$menu_sections);
            var primary_menu_id = false;
            var $section = false;
            for (var i = 0; i < menu_ids.length; i++) {
                primary_menu_id = menu_ids[i];
                $section = this.$menu_sections[primary_menu_id];
                $section.on(
                    "click",
                    "a[data-menu]",
                    self,
                    on_secondary_menu_click.bind(this)
                );
            }

            // Systray Menu
            this.systray_menu = new SystrayMenu(this);
            this.systray_menu.attachTo(this.$(".o_menu_systray")).then(function () {
                dom.initAutoMoreMenu(self.$section_placeholder, {
                    maxWidth: function () {
                        return (
                            self.$el.width() -
                            (self.$menu_apps.outerWidth(true) +
                                self.$menu_brand_placeholder.outerWidth(true) +
                                self.systray_menu.$el.outerWidth(true))
                        );
                    },
                    sizeClass: "SM",
                });
            });
            // Return Promise.all([this._super.apply(this, arguments), appsMenuProm, systrayMenuProm]);
        },
    });
});
