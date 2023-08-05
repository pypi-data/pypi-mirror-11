Ext.define('bst.pygasus.demo.view.CardView', {
    extend: 'Ext.window.Window',

    requires: [
        'scaffolding.display.Card'
    ],

    itemId: 'cardView',
    layout: 'vbox',

    initComponent: function() {
        var me = this;
        
        me.items = [{
            xtype: 'DisplayCard',
            itemId: 'displayCard',
            title: '',
            maxWidth: '500'
        },
        {
            xtype: 'button',
            text: 'Delete',
            action: 'delete'
        }];

        me.bodyPadding = '5 5 5 5';

        me.callParent(arguments);
    }

});
