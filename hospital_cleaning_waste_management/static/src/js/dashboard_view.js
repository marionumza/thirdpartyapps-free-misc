odoo.define('hospital_cleaning_waste_management.Dashboard', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var web_client = require('web.web_client');
    var session = require('web.session');
    var _t = core._t;
    var QWeb = core.qweb;
    var self = this;
    var currency;
    var DashBoard = AbstractAction.extend({
        contentTemplate: 'Dashboard',
        events: {
            'click .employees': 'employees',
            'click .teams': 'teams',
            'click .unassigned_leads': 'unassigned_leads',
            'click .shifts': 'shifts',
            'click .waste': 'waste',
            'change #income_expense_values': function(e) {
                e.stopPropagation();
                var $target = $(e.target);
                var value = $target.val();
                if (value=="this_year"){
                    this.onclick_this_year($target.val());
                }else if (value=="this_month"){
                    this.onclick_this_month($target.val());
                }else if (value=="this_week"){
                    this.onclick_this_week($target.val());
                }
            },

        },

        init: function(parent, context) {
            this._super(parent, context);
            this.dashboards_templates = ['Managercrm','Admincrm'];
            this.login_employee = [];
        },

        willStart: function(){
            var self = this;
            this.login_employee = {};
            return this._super()
            .then(function() {

                var def5 = self._rpc({
                    model: "hr.employee",
                    method: "get_dept_employee",
                })
                .then(function (res) {
                    self.data = res['data'];
                });

                var def4 = self._rpc({
                    model: "employee.shift",
                    method: "get_shift",
                })
                .then(function (res) {
                    self.top_sp_revenue = res['top_revenue'];
                });

                var def8 = self._rpc({
                    model: "employee.shift",
                    method: "get_employee_shift",
                })
                .then(function (res) {
                    self.top_country_wise_ratio = res['final'];
                });
                var def12 = self._rpc({
                    model: "employee.shift",
                    method: "get_count_unassigned",
                })
                .then(function (res) {
                    self.get_count_unassigned = res['count_unassigned'];
                });

                return $.when(def4,def5, def8,def12);
            });
        },


        //employee
        employees: function(e) {
            var self = this;
            e.stopPropagation();
            e.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t("Employees"),
                type: 'ir.actions.act_window',
                res_model: 'hr.employee',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['department_id', '=', 'Cleaning']],
                target: 'current',
            }, options)
        },

         unassigned_leads: function(e) {
            var self = this;
            e.stopPropagation();
            e.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t("My Shifts"),
                type: 'ir.actions.act_window',
                res_model: 'employee.shift',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                domain: [['department_id', '=', 'Cleaning']],
                target: 'current',
            }, options)
        },

        //teams
        teams: function(e) {
            var self = this;
            e.stopPropagation();
            e.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t("Teams"),
                type: 'ir.actions.act_window',
                res_model: 'cleaning.teams',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],

                target: 'current',
            }, options)
        },

        //shifts
        shifts: function(e) {
            var self = this;
            e.stopPropagation();
            e.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t("Employee Shifts"),
                type: 'ir.actions.act_window',
                res_model: 'employee.shift',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                target: 'current',
            }, options)
        },

        //waste
        waste: function(e) {
            var self = this;
            e.stopPropagation();
            e.preventDefault();
            var options = {
                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
            };
            this.do_action({
                name: _t("Waste Type"),
                type: 'ir.actions.act_window',
                res_model: 'waste.types',
                view_mode: 'tree,form,calendar',
                views: [[false, 'list'],[false, 'form']],
                target: 'current',
            }, options)
        },



        start: function() {
            var self = this;
            this.set("title", 'Dashboard');
            return this._super().then(function() {
                self.update_cp();
                self.render_dashboards();
                self.render_graphs();
                self.$el.parent().addClass('oe_background_grey');
            });
        },

        render_graphs: function(){
            console.log('ewzrxtcyvghubijnk')
            var self = this;
            self.render_employee_shifts_count_graph();
             },

        render_employee_shifts_count_graph:function(){
            var self = this
            var ctx = self.$(".shift_count");
            rpc.query({
                model: "employee.shift",
                method: "get_employee_shift_count",
            }).then(function (arrays) {
                var data = {
                    labels : arrays[1],
                    datasets: [{
                        label: "",
                        data: arrays[0],
                        backgroundColor: [
                            "#003f5c",
                            "#2f4b7c",
                            "#f95d6a",
                            "#665191",
                            "#d45087",
                            "#ff7c43",
                            "#ffa600",
                            "#a05195",
                            "#6d5c16"
                        ],
                        borderColor: [
                            "#003f5c",
                            "#2f4b7c",
                            "#f95d6a",
                            "#665191",
                            "#d45087",
                            "#ff7c43",
                            "#ffa600",
                            "#a05195",
                            "#6d5c16"
                        ],
                        borderWidth: 1
                    },]
                };

                //options
                var options = {
                    responsive: true,
                    title: false,
                    legend: {
                        display: true,
                        position: "right",
                        labels: {
                            fontColor: "#333",
                            fontSize: 16
                        }
                    },
                    scales: {
                        yAxes: [{
                            gridLines: {
                                color: "rgba(0, 0, 0, 0)",
                                display: false,
                            },
                            ticks: {
                                min: 0,
                                display: false,
                            }
                        }]
                    }
                };

                //create Chart class object
                var chart = new Chart(ctx, {
                    type: "doughnut",
                    data: data,
                    options: options
                });
            });
        },


        fetch_data: function() {
            var self = this;
            var def8 = self._rpc({
                model: "employee.shift",
                method: "get_employee_shift",
            })
            .then(function (res) {
                self.top_country_wise_ratio = res['final'];
            });


            var def4 = self._rpc({
                    model: "employee.shift",
                    method: "get_shift",
                })
                .then(function (res) {
                    self.top_sp_revenue = res['top_revenue'];
                });

             var def12 = self._rpc({
                            model: "employee.shift",
                            method: "get_count_unassigned",
                        })
                        .then(function (res) {
                            self.get_count_unassigned = res['count_unassigned'];
                        });

            return $.when(def4,def8, def12);
        },

        render_dashboards: function() {
            var self = this;
            if (this.login_employee){
                var templates = []
                if( self.is_manager == true){
                    templates = [ 'Managercrm','Admincrm'];
                }
                else{
                    templates = ['Managercrm','Admincrm'];
                }
                _.each(templates, function(template) {
                    self.$('.o_hr_dashboard').append(QWeb.render(template, {widget: self}));
                });
            }
            else{
                self.$('.o_hr_dashboard').append(QWeb.render('EmployeeWarning', {widget: self}));
            }
        },

        on_reverse_breadcrumb: function() {
            var self = this;
            web_client.do_push_state({});
            this.update_cp();
            this.fetch_data().then(function() {
                self.$('.o_hr_dashboard').reload();
                self.render_dashboards();
            });
        },

         update_cp: function() {
            var self = this;
         },
    });

    core.action_registry.add('shift_dashboard_tag', DashBoard);
    return DashBoard;
});