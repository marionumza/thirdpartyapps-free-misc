/** @odoo-module **/

import { UserMenu } from "@web/webclient/user_menu/user_menu";
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";

const userMenuRegistry = registry.category("user_menuitems");

patch(UserMenu.prototype, "anita_pwa_user_menu_patch", {
    setup() {
        this._super();
        
        this.deferredInstallPrompt = undefined;
        if ("serviceWorker" in navigator) {
            navigator.serviceWorker.register("/anita-service-worker.js").then(function(reg) {
                console.log("pwa service worker registered.", reg);
            })
            window.addEventListener(
                "beforeinstallprompt", 
                this.before_install_prompt_call_back.bind(this));
        }
    },

    before_install_prompt_call_back(evt) {
        this.deferredInstallPrompt = evt;
        // check install_pwa are not already installed
        if (!userMenuRegistry.contains("install_pwa")) {
            // add to the menu items
            userMenuRegistry.add("install_pwa", (env) => {
                return {
                    type: "item",
                    id: "PWA_install",
                    description: env._t("Install PWA"),
                    callback: () => {
                        this._onMenuInstallPwa();
                    },
                    sequence: 20,
                }
            }, false, {sequence: 10,});
            this.render();
        }
    },

    /*
    * install pwa 
    */
    _onMenuInstallPwa(env) {
        var self = this
        this.deferredInstallPrompt.prompt();
        this.deferredInstallPrompt.userChoice.then(function (choice) {
            if (choice.outcome === "accepted") {
                self.deferredInstallPrompt = null;
                console.log("User accepted the \"Add To Home Screen (A2HS)\"  prompt", choice);
                userMenuRegistry.remove("install_pwa");
            } else {
                console.log("User dismissed the \"Add To Home Screen (A2HS)\"  prompt", choice);
            }
        });
    }
});