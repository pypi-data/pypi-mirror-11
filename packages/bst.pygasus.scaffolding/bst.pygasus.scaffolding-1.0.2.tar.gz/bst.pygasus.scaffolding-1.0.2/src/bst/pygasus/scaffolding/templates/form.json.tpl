Ext.define('${view.name}', {
    "extend": "Ext.form.Panel",
    "alias": "${'widget.%s%s' % (view.aliasprefix, view.descriptive.classname)}",
    "title": "${view.title}",
    "items": [
        ${','.join(view.items)}
    ]
});