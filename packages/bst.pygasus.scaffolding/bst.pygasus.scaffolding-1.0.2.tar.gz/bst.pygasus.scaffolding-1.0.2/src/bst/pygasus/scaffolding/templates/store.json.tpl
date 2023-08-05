Ext.define('${view.cname}', {
    "extend": "Ext.data.Store",
    "alias": "${view.name}",
    "requires": "${view.model}",
    "autoLoad": true,
    "autoSync": {% choose %}{% when view.autoSync %}true{% end %}{% otherwise %}false{% end %}{% end %},
    "storeId": "${view.name}",
    "model": "${view.model}",
    "batchMode": false,
    "pageSize": 100,
    "remoteSort": true,
    "buffered": {% choose %}{% when view.buffered %}true{% end %}{% otherwise %}false{% end %}{% end %},
    "proxy": {
        "url": "${view.url}",
        "reader": {
            "type": "json",
            "root": "data"
        },
        "type": "rest",
        "writer": {
            "type": "json",
            "root": "data"
        },
        "pageParam": null,
        "batchActions": true
    }
});