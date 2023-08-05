Ext.define('extjs.security.LoginPageApplication', {
    extend: 'Ext.app.Application',
    requires: [
    ],

    name: 'Login',

    views: [
        'extjs.security.LoginView'
    ],
    
    controllers: [
        'extjs.security.Controller',
    ],
    
    launch: function() {
        Ext.create('extjs.security.LoginView');
    }
});
