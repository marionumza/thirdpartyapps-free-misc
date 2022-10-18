odoo.define('easyerps_pos_menu.Chrome', function(require) {
	'use strict';
	const { useState, useRef, useContext, useExternalListener } = owl.hooks;
	const { useListener } = require('web.custom_hooks');
	const Registries = require('point_of_sale.Registries');
	const Chrome = require('point_of_sale.Chrome');
	const myChrome = (Chrome) =>
		class extends Chrome {
			constructor() {
				super(...arguments);
				useListener('toggle-posMenu', this._ontoggle_easyerps_pos_menu);
				this.PosMenuState = useState({ show: false });
			}
			get isTicketScreenShown() {
				if (this.mainScreenProps.ui && this.mainScreenProps.ui.booking == true) {
					return false;
				}
				return this.mainScreen.name === 'TicketScreen';
			}
			get isPosMenuShown() {
				return this.PosMenuState.show;
			}
			_ontoggle_easyerps_pos_menu() {
				if (this.PosMenuState.show) {
					this.PosMenuState.show = false;
				} else {
					this.PosMenuState.show = true;
				}
			}
		};
	Chrome.template = 'Chrome';

	Registries.Component.extend(Chrome, myChrome);
	return Chrome;
});