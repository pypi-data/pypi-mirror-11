Ext.define('bst.pygasus.demo.Application', {
    extend: 'Ext.app.Application',
    requires: [
        'Ext.data.Request',
        'scaffolding.bufferedstore.Card'
    ],

    name: 'DEMO',

    views: [
        'bst.pygasus.demo.view.MainView',
        'bst.pygasus.demo.view.CardView'
    ],
    
    controllers: [
        'bst.pygasus.demo.controller.Main',
        'bst.pygasus.demo.controller.Card'
    ],

    launch: function() {
        Ext.create('bst.pygasus.demo.view.MainView');
    }
});
