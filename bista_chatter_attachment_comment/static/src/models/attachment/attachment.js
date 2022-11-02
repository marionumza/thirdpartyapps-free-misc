/** @odoo-module **/
/**
 * @author Rahul Malve <rahul.malve@bistasolutions.com>
 */
import {
    registerClassPatchModel,
    registerInstancePatchModel,
    registerFieldPatchModel
} from'@mail/model/model_core';
import { attr } from '@mail/model/model_field';
import { clear, insert } from '@mail/model/model_field_command';
import { useAutofocus, useService } from "@web/core/utils/hooks";

registerFieldPatchModel('mail.attachment', 'bista_chatter_attachment_comment/static/src/models/attachment/attachment.js', {
    description: attr({
        compute: '_computeDescription',
    }),
});

registerClassPatchModel('mail.attachment', 'bista_chatter_attachment_comment/static/src/models/attachment/attachment.js', {
    /**
     * @override
     */
    convertData(data) {
        const res = this._super(data);
        if ('description' in data) {
            res.description = data.description;
        }
        return res;
    },
});

registerInstancePatchModel('mail.attachment', 'bista_chatter_attachment_comment/static/src/models/attachment/attachment.js', {
    _computeDescription() {
        const description = this.description;
        if (description) {
            return description;
        }
        return clear();
    },

});