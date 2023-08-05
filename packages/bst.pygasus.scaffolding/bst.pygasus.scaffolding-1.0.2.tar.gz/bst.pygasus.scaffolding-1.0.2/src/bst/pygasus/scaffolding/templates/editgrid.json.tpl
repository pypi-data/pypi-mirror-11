var rowEditing = Ext.create("Ext.grid.plugin.RowEditing");
Ext.define('${view.name}', {
    "extend": "Ext.grid.Panel",
    "requires": "${view.requires}",
    "alias": "${view.alias}",
    "title": "${view.title}",
    "store": ${view.store},
    "plugins": [rowEditing],
    "columns": [
        ${','.join(view.columns)}
    ]
});