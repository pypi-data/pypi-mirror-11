var _ = i18n('bst.pygasus.demo');

Ext.define('bst.pygasus.demo.view.MainView', {
    extend: 'Ext.container.Viewport',

    requires: [
        'scaffolding.grid.Card',
        'scaffolding.editgrid.Card',
        'scaffolding.form.Card',
        'scaffolding.display.Card',
        'scaffolding.model.Card'
    ],    

    itemId: 'mainView',
    layout: 'fit',

    initComponent: function() {
        var me = this;

        Ext.applyIf(me, {
            xtype: 'panel',
            items: [{
                xtype: 'tabpanel',
                items: [{
                    xtype: 'GridCard',
                    title: 'Grid',
                },
                {
                    xtype: 'EditGridCard',
                    title: 'EditGrid'
                },
                {
                    xtype: 'FormCard',
                    title: 'Form',
                    margin: '5 5 5 5',
                    dockedItems: [{
                        xtype: 'toolbar',
                        docked: 'top',
                        items: [{
                            xtype: 'button',
                            action: 'save',
                            text: _('tr_save', 'Save'),
                        },{
                            text: 'Cancel',
                            action: 'cancel'
                        }]
                    }]
                }]
            }]
        });

        me.callParent(arguments);
    }

});
