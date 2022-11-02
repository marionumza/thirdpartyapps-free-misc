odoo.define('le_form_disable_quick_edit.relational_fields', function (require) {
	let FieldX2Many = require('web.relational_fields').FieldX2Many;

	FieldX2Many.include({
		/**
		 * Override to set _canQuickEdit to false on list views where editable is also false
		 * This will enable records to bubble (pop) up in readonly mode
		 * @override
		 * @param {*} parent
		 * @param {*} name
		 * @param {*} record
		 * @param {*} options
		 */
		init: function (parent, name, record, options) {
			this._super.apply(this, arguments);

			if (!this.editable || this.mode === 'readonly') {
				this._canQuickEdit = false;
			}
		},
	});
});
