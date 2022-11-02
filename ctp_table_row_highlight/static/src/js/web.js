odoo.define("ctp_table_row_highlight.web", function (require) {
  "use strict";

  var ListRenderer = require("web.ListRenderer");
  var session = require("web.session");
  var rpc = require("web.rpc");

  ListRenderer.include({
    init: function (parent, model, renderer, params) {
      this._super.apply(this, arguments);
      this.model = model;
      this.renderer = renderer;
    },

    _findRecordById: function (id) {
      return _.find(this.state.data, function (record) {
        return record.id === id;
      });
    },

    _onSelectRecord: function (event) {
      var self = this;
      this._super.apply(this, arguments);
      var checkbox = $(event.currentTarget).find("input");
      var $selectedRow = $(checkbox).closest("tr");
      if ($(checkbox).prop("checked")) {
        $selectedRow.addClass("row_selected");
      } else {
        $selectedRow.removeClass("row_selected");
      }
    },
    
    _onToggleSelection: function (event) {
      this._super.apply(this, arguments);
      var checked = $(event.currentTarget).prop("checked") || false;
      if (checked) {
        this.$("tbody .o_list_record_selector")
          .closest("tr")
          .addClass("row_selected");
      } else {
        this.$("tbody .o_list_record_selector")
          .closest("tr")
          .removeClass("row_selected");
      }
    },
  });
});
