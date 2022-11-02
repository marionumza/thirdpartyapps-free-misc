/** @odoo-module **/
/**
 * @author Rahul Malve <rahul.malve@bistasolutions.com>
 */
import core from 'web.core';
import FormRenderer from 'web.FormRenderer';
import ViewDialogs from 'web.view_dialogs';

const _t = core._t;

FormRenderer.include({

    /**
     * @private
     */
    init() {
        this._super(...arguments);
        this.on('o_update_attachment_description', this, ev => this._onOpenUpdateDescriptionDialog(ev));
    },

    /**
     * @override
     */
    destroy() {
        this._super(...arguments);
        this.off('o_update_attachment_description', this);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Open dialog for update attachment description
     *
     * @private
     * @param {OdooEvent} ev
     */
    _onOpenUpdateDescriptionDialog(ev) {
        ev.stopPropagation();
        let res_id = ev.data.res_id;
        if (res_id) {
            let context = _.extend({}, this.state.context, {
                'form_view_ref': 'bista_chatter_attachment_comment.view_ir_attachment_description_form',
            });
            let onSaved = ev.data.onSaved || function () {};
            new ViewDialogs.FormViewDialog(this, {
                res_model: 'ir.attachment',
                res_id: res_id,
                title: _t("Add Comment "),
                context: context,
                readonly: false,
                size: 'small',
                on_saved: onSaved,
            }).open();
        }
    },
});
