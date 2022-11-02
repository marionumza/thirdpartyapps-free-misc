odoo.define('omar_new_audio', function (require) {
    // "use strict";
    // version 15 
    var core = require('web.core');
    var FieldBinaryFile = require("web.basic_fields").FieldBinaryFile
    var session = require('web.session');
    var _t = core._t;


    var fieldRegistry = require('web.field_registry');

    
    var AudioWidget = FieldBinaryFile.extend({

        supportedFieldTypes: ['binary'],
        accepted_file_extensions:'audio/*,application/ogg',


        _getAudioUrl: function (model, res_id, field, unique) {
            // every 
            return session.url('/web/content', {
                model: model,
                id: JSON.stringify(res_id),
                field: field,
            });
        },
    
    
        _renderReadonly: function () {
            // This function will run if we are not in "edit" mode
            self = this

           if (this.value) {
                url = this._getAudioUrl(this.model, this.res_id, this.name);
                console.log(url)
                $audio = $('<audio>', {
                    'src': url,
                    'controls': true,
                    'preload':"metadata"
                })
                s = this.$el.append($audio);

                $audio.on("error",function(){
                    //  this checks if there is an error on Media element  (DOM refrence)
                    // self.displayNotification(_t("Wrong File Extension!"), _t("the field "+self.name+" must be an audio"));
                    self.displayNotification({ title: _t('Wrong File Extension'), message: _t("the field "+self.name+" must be an audio"), type: 'danger' });

                })

                s[0].childNodes[0].onloadedmetadata =function() {
                        // there is an event in media Elements called "onloadedmetadata"
                        //  here we run a function with this element (Just to only logging the two message on console)
                        console.log('metadata loaded!');
                        console.log(this.duration);//this refers to my audio
                }

            }



       },
       on_file_change: function (ev) {
        // This is a function from FieldBinaryFile: we just overrided it after calling the main function as super 
        // we here check if the file extension is audio or not , if not we just send a Warning error

        this._super.apply(this, arguments);
        var f_input = $(ev.target)

        var files = ev.target.files
        console.log(f_input.val())
        if (!files || files.length === 0) {
            return;
        }
        console.log(files)
        var valid_ext = ['wav', 'ogg', 'mp3','oga','ogx']

        // var file = ev.target.files;

        var msg = _t("the file type must be An audio");
        var file = files[0];
        var name_arr = file.name.split(".")
        var ext = name_arr[name_arr.length - 1]
        // var msg = _t("The selected file exceed the maximum file size of %s.");

        console.log(file.name)
        console.log(ext)
        if(!valid_ext.includes(ext)){
            this.displayNotification({ title: _t('Wrong File Extension'), message: _t("the field "+this.name+" this field for Audio files only"), type: 'danger' });

            // this.displayNotification(_t("Wrong File Extension!"), _t("this field for Audio files only ."));

        }
    }

 


    })

    fieldRegistry.add('audio_omar_widget', AudioWidget);
    
    return {
        AudioWidget: AudioWidget,
    };

    
})

