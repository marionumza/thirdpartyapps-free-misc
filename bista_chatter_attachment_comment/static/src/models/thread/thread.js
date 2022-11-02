/** @odoo-module **/
/**
 * @author Rahul Malve <rahul.malve@bistasolutions.com>
 */
import {
    registerFieldPatchModel,
    registerInstancePatchModel
} from '@mail/model/model_core';
import { attr } from '@mail/model/model_field';
import { insertAndReplace } from '@mail/model/model_field_command';

registerInstancePatchModel('mail.thread', 'bista_chatter_attachment_comment/static/src/thread/thread.js', {

    //----------------------------------------------------------------------
    // Public
    //----------------------------------------------------------------------
    /**
     * @override
     */
    async fetchAttachments() {
        let attachmentsData = await this.async(() => this.env.services.rpc({
            model: 'ir.attachment',
            method: 'search_read',
            domain: [
                ['res_id', '=', this.id],
                ['res_model', '=', this.model],
            ],
            fields: ['id', 'name', 'mimetype', 'description'],
            orderBy: [{name: 'id', asc: false}],
        }, {shadow: true}));
        this.update({
            originThreadAttachments: insertAndReplace(attachmentsData),
        });
        this.update({ areAttachmentsLoaded: true });
    }
});

//registerFieldPatchModel('mail.thread', 'bista_astro_onedrive_integration/static/src/js/thread/thread.js', {});

