odoo.define('le_form_disable_quick_edit.FormController', function (require) {
	'use strict';

	let FormController = require('web.FormController');

	FormController.include({
		/**
		 * Override to disable quick editing, but still allow list/kanban fields to bubble (pop) up in readonly mode
		 * @override
		 * @private
		 * @param {OdooEvent} ev
		 */
		_onQuickEdit: function (ev) {
			ev.stopPropagation();
			clearTimeout(this.quickEditTimeout);
			if (this.activeActions.edit && !window.getSelection().toString()) {
				//if a list/kanban record has been selected then it will be possible to open the record
				const openRecord = async () => {
					let extraInfo = ev.data.extraInfo;

					if (extraInfo.type === 'remove') {
						this._removeRecord(extraInfo.recordId);
					} else if (extraInfo.type === 'edit') {
						const parts = [];
						if (extraInfo.row) {
							parts.push(`.o_data_row[data-id="${extraInfo.row}"]`);
						}
						if (extraInfo.subFieldName) {
							parts.push(`[name="${extraInfo.subFieldName}"]`);
						}

						if (parts.length) {
							const el = this.el.querySelector(parts.join(' '));
							if (el) {
								el.click();
							}
						}
					}
				};
				if (this.multiClickTime > 0) {
					this.quickEditTimeout = setTimeout(openRecord, this.multiClickTime);
				} else {
					openRecord();
				}
			}
		},
	});
});
