odoo.define('pos_l10n_ar_identification.screens', function(require) {
    'use strict';

    const ClientListScreen = require('point_of_sale.ClientListScreen');
    const Registries = require('point_of_sale.Registries');
    var { Gui } = require('point_of_sale.Gui');
    var models = require('point_of_sale.models');

    

    const POSSaveClientOverride = ClientListScreen =>
        class extends ClientListScreen {
            /**
             * @override
             */

         

            async saveChanges(event) {



                try {


                var jm_l10n_ar_afip_responsibility_type_id=$('.l10n_ar_afip_responsibility_type_id').val();
                var jm_l10n_latam_identification_type_id=$('.l10n_latam_identification_type_id').val();
                var jm_identification_number=$('.identification_number').val();

             
                if (jm_l10n_ar_afip_responsibility_type_id == '0' ) {


                         await this.showPopup('ErrorPopup', {
                        title: this.env._t('Resp. AFIP debe completarse'),
                        body: this.env._t('Debe completar el campo Resp. AFIP'),
                    });
                         return;
                    }else if (jm_l10n_latam_identification_type_id == '0' ) {


                         await this.showPopup('ErrorPopup', {
                        title: this.env._t('Tipo Doc debe completarse'),
                        body: this.env._t('Debe completar el campo Tipo Doc'),
                    });
                         return;
                    }else if (jm_identification_number == '' ) {


                         await this.showPopup('ErrorPopup', {
                        title: this.env._t('Numero debe completarse'),
                        body: this.env._t('Debe completarse el campo Número de Identificación'),
                    });
                         return;
                    }


                    if (!jm_identification_number &&  jm_l10n_ar_afip_responsibility_type_id=='1' ) {


                         await this.showPopup('ErrorPopup', {
                        title: this.env._t('El campo CUIT (NIF) es requerido.'),
                        body: this.env._t('El Campo CUIT es requerido'),
                    });
                         return;
                    }

                    
                let partnerId = await this.rpc({
                    model: 'res.partner',
                    method: 'create_from_ui',
                    args: [event.detail.processedChanges],
                });
                await this.env.pos.load_new_partners();
                this.state.selectedClient = this.env.pos.db.get_partner_by_id(partnerId);
                this.state.detailIsShown = false;
                this.render();
            } catch (error) {
                if (error.message.code < 0) {
                    await this.showPopup('OfflineErrorPopup', {
                        title: this.env._t('Offline'),
                        body: this.env._t('Unable to save changes.'),
                    });
                } else {
                    throw error;
                }
            }
        


            }


               
        };

    Registries.Component.extend(ClientListScreen, POSSaveClientOverride);

    return ClientListScreen;
});
