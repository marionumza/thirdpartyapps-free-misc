odoo.define('easyerps_pos_menu.TicketButton', function(require) {
	'use strict';

	const Registries = require('point_of_sale.Registries');
	const TicketButton = require('point_of_sale.TicketButton');
	const { _t } = require('web.core');


	const myTicketButton = (TicketButton) =>
		class extends TicketButton {
			onClick() {
				super.onClick();
				this.trigger('toggle-posMenu');
			}

		}

	Registries.Component.extend(TicketButton, myTicketButton);

	return TicketButton;
});