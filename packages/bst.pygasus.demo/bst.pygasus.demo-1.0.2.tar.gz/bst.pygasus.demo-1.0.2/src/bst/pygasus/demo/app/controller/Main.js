Ext.define('bst.pygasus.demo.controller.Main', {
    extend: 'Ext.app.Controller',
    
    requires: [
        'scaffolding.bufferedstore.Card'
    ],    

    refs: [{
        ref: 'form',
        selector: 'FormCard'
    }, {
        ref: 'idform',
        selector: 'FormCard field[name=id]'
    }, {
        ref: 'grid',
        selector: 'GridCard'
    }],

    init: function(){
        this.control({
            'FormCard button[action=save]': {
                click: this.onFormSave
            },
            'FormCard button[action=cancel]': {
                click: function() { this.getForm().getForm().reset(); }
            },
            '#mainView': {
                afterrender: this.onContentRendered
            },
            'GridCard': {
                cellclick: function(ele, td, cellIndex, record) {
                    this.application.controllers.get('bst.pygasus.demo.controller.Card').addContent(record);
                }
            },
            'EditGridCard': {
                validateedit: function(editor, context) {
                    var store = this.getStore('scaffolding.store.Card');
                    store.loadRecords([context.record]);
                }
            }
        });
        
    },


    onContentRendered: function(){
        this.getIdform().hide();
    },



    onFormSave: function(button, event){
        var form = this.getForm();
        if(form.isValid()){
            var store = this.getStore('scaffolding.store.Card');
            var record = Ext.create('scaffolding.model.Card');
            form.updateRecord(record);
            record.set('id', 0);
            record.phantom = true;
            store.add(record);
            alert('Record stored successfully');
            form.getForm().reset();
        }
    },

    deleteRecord: function(record){
        var grid = this.getGrid();
        var store = this.getStore('scaffolding.store.Card');
        store.loadRecords([record]);
        store.remove(record);
        var sel = grid.getSelectionModel();
        sel.deselect(sel.getSelection());
        //store = this.getStore('scaffolding.bufferedstore.Card');
        store.load();
        grid.reconfigure(store);
    }
});
