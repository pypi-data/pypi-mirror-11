{
    "xtype": "combobox",
    "name": "${view.name}",
    "fieldLabel": "${view.fieldLabel}",
    "emptyText": "${view.emptyText}",
    "allowBlank": {% choose %}{% when view.allowBlank %}true{% end %}{% otherwise %}false{% end %}{% end %},
    "valueField": "${view.valueField}",
    "displayField": "${view.displayField}",
    "queryMode": "${view.queryMode}",
    "store": ${view.store}
}