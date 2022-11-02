odoo.define('le_form_disable_quick_edit.ListRenderer', function (require) {
	'use strict';

	let ListRenderer = require('web.ListRenderer');

	ListRenderer.include({
		/**
		 * Override to remove all 'creates' and the trash icon when not in edit mode
		 * @override
		 * @param {*} parent
		 * @param {*} state
		 * @param {*} params
		 */
		init: function (parent, state, params) {
			this._super.apply(this, arguments);
			if (this.getParent() && this.getParent().mode !== 'edit') {
				this.creates = [];
				this.addCreateLine = false;
				this.addTrashIcon = false;
			}
		},

		/**
		 * @override
		 * @param {*} state
		 * @param {*} params
		 * @returns
		 */
		updateState: function (state, params) {
			if (this.getParent() && this.getParent().mode !== 'edit') {
				params.addCreateLine = false;
				params.addTrashIcon = false;
			}
			return this._super.apply(this, arguments);
		},
	});
});
