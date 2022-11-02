/** @odoo-module */

import { AttachmentImage } from '@mail/components/attachment_image/attachment_image';
import { patch } from 'web.utils';
import Dialog from 'web.Dialog';
import core from 'web.core';
const _t = core._t;

patch(AttachmentImage.prototype, 'bista_chatter_attachment_comment/static/src/components/attachment_image/attachment_image.js', {
    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    _GetDescription : function (ev){
        /**
         * Open dialog for update attachment tags
         *
         * @private
         * @param {MouseEvent} ev
         */
        ev.preventDefault();
        ev.stopPropagation(); // prevents from opening viewer
        var self = this;
        this.trigger('o-update-attachment-description', {
            res_id: parseInt(ev.target.dataset.id),
            onSaved: (record, changed) => {
                if (changed) {
                    this.trigger('reload', { keepChanges: true });
                }
            },
        });
    }
});
