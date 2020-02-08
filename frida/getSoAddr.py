# -*- coding: UTF-8 -*-
import frida, sys
 
jsCode = """
Java.perform(function(){
    Process.enumerateModules({
        onMatch: function(exp){
            if(exp.name == 'libandromeda.so'){
                send(exp.name + "|" + exp.base + "|" + exp.size + "|" + exp.path);
                send(exp);
                return 'stop';
            }
        },
        onComplete: function(){
            send('stop');
        }
    });
    var soAddr = Module.findBaseAddress("libandromeda.so");
    send(soAddr);
});
"""
 
def message(message, data):
    if message["type"] == 'send':
        print(u"[*] {0}".format(message['payload']))
    else:
        print(message)
 
process = frida.get_remote_device().attach("jp.naver.line.android")
script= process.create_script(jsCode)
script.on("message", message)
script.load()
sys.stdin.read()