/** @odoo-module */
/**
 * @author Rahul Malve <rahul.malve@bistasolutions.com>
 */
import { AttachmentCard } from '@mail/components/attachment_card/attachment_card';
import { patch } from 'web.utils';
import core from 'web.core';
const _t = core._t;

patch(AttachmentCard.prototype, 'bista_chatter_attachment_comment/static/src/components/attachment_card/attachment_card.js', {
    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------
    /**
     * Small override that asks for confirmation in case there is a meeting linked to this activity.
     *
     * @override
     */
    _onClickComment(ev) {
        ev.preventDefault();
        var attachment_id = ev.target.dataset.id;
        this.trigger('o-update-attachment-description', {
            res_id: parseInt(attachment_id),
            onSaved: (record, changed) => {
                if (changed) {
                    this.trigger('reload', { keepChanges: true });
                }
            },
        });
    },

});
