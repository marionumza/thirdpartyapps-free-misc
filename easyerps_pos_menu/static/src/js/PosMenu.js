odoo.define('easyerps_pos_menu.PosMenu', function(require) {
	'use strict';
	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');
	class PosMenu extends PosComponent {
		onClick() {
			this.trigger('toggle-posMenu');
		}
	}
	PosMenu.template = 'PosMenu';
	Registries.Component.add(PosMenu);
	return PosMenu;
});