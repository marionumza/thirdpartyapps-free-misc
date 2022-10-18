odoo.define('easyerps_pos_menu.CashMoveButton', function(require) {
	'use strict';

	const Registries = require('point_of_sale.Registries');
	const CashMoveButton = require('point_of_sale.CashMoveButton');
	const { _t } = require('web.core');

	const TRANSLATED_CASH_MOVE_TYPE = {
		in: _t('in'),
		out: _t('out'),
	};

	const myCashMoveButton = (CashMoveButton) =>
		class extends CashMoveButton {
			async onClick() {
				super.onClick();
				this.trigger('toggle-posMenu');
			}

		}

	Registries.Component.extend(CashMoveButton, myCashMoveButton);

	return CashMoveButton;
});