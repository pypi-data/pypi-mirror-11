Ext.define('extjs.security.Controller', {
    extend: 'Ext.app.Controller',
    
    requires: [
        'scaffolding.model.Credentials'
    ],
    
    refs: [{
        ref: 'loginWindow',
        selector: '#loginwindow'
    }, {
        ref: 'form',
        selector: 'FormCredentials'
    }],

    stores: ['scaffolding.store.Credentials'],


    init: function(){
        this.control({
            'button[name=submit]': {
                click: this.onSubmit
            },
            'FormCredentials': {
                render: this.onContentRendered,
            },
        });
        
        new Ext.KeyMap(Ext.getBody(), {
            key: Ext.EventObject.ENTER,
            fn: this.onSubmit,
            scope: this,
        });
    },


    onContentRendered: function(){
        var form = this.getForm();
        // just hide success and redirect field because it was autocreated
        form.getForm().findField('success').hide();
        form.getForm().findField('defaultredirect').hide();
        var store = this.getScaffoldingStoreCredentialsStore();
        store.on('write', this.onStoreUpdate, this);
        store.on({
            scope:this,
            load: function(){
                var creds = store.getAt(0);
                this.getForm().loadRecord(creds);
                this.getForm().getForm().findField('login').focus();
            }
        });
    },


    onStoreUpdate: function(store, operator){
        var model = operator.records[0];
        if (model.get('success')){
            var camefrom = this.camefromurl();
            if (camefrom === false)
                window.location = model.get('defaultredirect');
            else
                window.location = camefrom;
        } else {
            this.shake();
            Ext.each(this.getForm().items.items, function(item){
                item.setValue('');
            });
        }
    },


    onSubmit: function(){
        var form = this.getForm();
        if (!form.isValid()){
            this.shake();
            return;
        }
        form.updateRecord(form.getRecord());
    },


    camefromurl: function(){
        var rawparams = document.URL.split("?");
        if (rawparams < 2)
            return false;
        var params = Ext.urlDecode(rawparams[rawparams.length - 1]);
        if ('camefrom' in params)
            return params['camefrom'];
        return false;
    },


    shake: function(){
        var win = this.getLoginWindow();
        var pos = win.getPosition()[0];
        var move = function(p){
            win.el.animate({duration:30, to:{x:p}});
        };
        
        for (var i=0; i < 10; i++) {
            if (i%2 == 0)
                move(pos-15);
            else
                move(pos+15);
        };
        move(pos);
    }


});
