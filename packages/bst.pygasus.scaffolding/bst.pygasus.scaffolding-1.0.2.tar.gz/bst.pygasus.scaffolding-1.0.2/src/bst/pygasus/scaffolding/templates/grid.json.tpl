Ext.define('${view.name}', {
    "extend": "Ext.grid.Panel",
    "requires": "${view.requires}",
    "alias": "${view.alias}",
    "title": "${view.title}",
    "store": ${view.store},
    "columns": [
        ${','.join(view.columns)}
    ]
});