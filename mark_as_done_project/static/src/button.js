odoo.define('new_project_field.menukanban', function(require) {
    "use strict";

    var KanbanController = require("web.KanbanController");

    KanbanController.include({
    events: {
        "click .my-contacts-button": "return_customer",
        "click .my-overview-button": "return_overview",
    },
    return_customer: function () {
    var self = this;
        var yy = this._rpc({
           model: 'project.project',
            method: 'get_partner_id',
            args: [this.initialState['context']['active_id']],
        }).then(function(result){
            if(result==false){
                alert('Customer does not exist against this project')
                return
            }
             self.do_action({
                    type: 'ir.actions.act_window',
                    name: 'res.partner',
                    res_model:  'res.partner',
                    res_id: result,
                    views: [[false, 'form']],
                });
            });

    },
    return_overview: function () {
    var self = this;
    this._rpc({
               model: 'project.project',
                method: 'action_view_timesheet',
                args: [this.initialState['context']['active_id']],
            }).then(function(result){
            self.do_action (result);
            });

    },

    });

});