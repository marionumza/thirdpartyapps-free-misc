/** @odoo-module **/

import KanbanRecord from "web.KanbanRecord";
import {constants} from "./constants";

KanbanRecord.include({
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     * @private
     */
    _openRecord: function () {
        if (
            this.modelName === constants.model_name &&
            this.$(".o_partner_category_kanban_boxes a").length
        ) {
            this.$(".o_partner_category_kanban_boxes a").first().click();
        } else {
            this._super.apply(this, arguments);
        }
    },
});
