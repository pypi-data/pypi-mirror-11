(function (root) {

    var I18nMessageObject = function(msgid, defaultmsg, mapping){

        var private = { 
                        msgid: undefined,
                        defaultmsg: undefined,
                        mapping: undefined,
                        message: undefined
                      };


        this.getMapping = function(){
            return private.mapping;
        };

        this.getMsgId = function(){
            return private.msgid;
        };

        this.getDefaultMsg = function(){
            return private.defaultmsg;
        };

        this.setMapping = function(new_mapping){
            private.mapping = new_mapping;
        };

        this.setTranslation = function(new_message){
            if (new_message) {
                private.message = new_message;
            } else {
                if (private.defaultmsg)
                    private.message = defaultmsg;
                else
                    private.message = msgid;
            }
        };

        var _string = function(){
            re = private.message;
            for(var key in private.mapping) {
                re = re.replace('${' + key + '}', private.mapping[key]);
            }
            return re;
        };
        this.toString = _string;
        this.valueOf = _string;


        if (!private.mapping)
            private.mapping = {};

        private.msgid = msgid;
        private.message = null;
        private.defaultmsg = defaultmsg;
        this.setMapping(mapping);
        this.setTranslation(null);
    };
    I18nMessageObject.prototype.__proto__ = String.prototype;


    var retrieve_url = function() {
        filename = 'bst.pygasus.i18n';
        pathname = 'fanstatic/i18n/';
        var scripts = document.getElementsByTagName('script');
        if (scripts && scripts.length > 0) {
            for (var i in scripts) {
                if (scripts[i].src && scripts[i].src.match(new RegExp(filename+'\\.js$'))) {
                    return scripts[i].src.replace(new RegExp('(.*)'+pathname+filename+'\\.js$'), '$1');
                }
            }
        }
    };


    var data = {};
    var msgobjects = {};
    i18n = function(domain) {
        if (!(domain in msgobjects))
            msgobjects[domain] = new Array();

        var filldata = function(){
            if (!data[domain])
                return;
            while( msgobj = msgobjects[domain].pop() ) {
                if ( msgobj.getMsgId() in data[domain]['messages'])
                    msgobj.setTranslation(data[domain]['messages'][msgobj.getMsgId()]);
                else
                    msgobj.setTranslation(null);
            }
        };
        
        var i18nMessageFactory = function(msgid, defaultmsg, mapping){
            var msgobj = new I18nMessageObject(msgid, defaultmsg, mapping);
            msgobjects[domain].push(msgobj);
            filldata();
            return msgobj;
        };

        if (domain in data){
            filldata();
        } else {
            data[domain] = null;

            var xhr = new XMLHttpRequest();
            xhr.open('get', retrieve_url() + 'i18n/' + domain, true);
            xhr.responseType = ''; // load as text and IE9 will be happy!
            xhr.onload = function() {
                var status = xhr.status;
                if (status == 200) {
                    data[domain] = JSON.parse(xhr.responseText);
                    filldata();
                } else {
                    console.log('server-side failure with status code ' + status);
                }
            };
            xhr.send();
        }
        
        return i18nMessageFactory;
    };



})(this);
