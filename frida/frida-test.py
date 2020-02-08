#coding=utf-8
import frida
import sys

# device = frida.get_device_manager().enumerate_devices()[-1]
device = frida.get_remote_device()
# pid = device.spawn(["com.android.chrome"])
session = device.attach("jp.naver.line.android")
# device.resume(pid)
# ,Memory.readByteArray(args[1],256)
# var ptr_data = args[1];
#         var length = args[2];    

#         var data = Memory.readByteArray(ptr_data, length);
#         console.log(data);
#Java_com_linecorp_andromeda_audio_AudioController_nAudioOpen(_JNIEnv *,_jobject *,long long,long long,_jobject *)	00097224	
# sendmsg recvmsg j_ear_str_snprintf BB94DACC recvmsg
src = """
var encArray = new Array(255);
for(var i = 0; i<encArray.length; i++){
    encArray[i] = i;
}

Interceptor.attach(Module.findExportByName("libandromeda.so" , "sendmsg"),
    {   onEnter: function(args){ 
            send("sendmsg args[0]:"+args[0]);
            send("sendmsg args[1]:"+args[1]);
            send("send:")
            for (var i = 0; i < 4; i++) {
                //send(args[0].add(i * Process.pointerSize))
                var pClassName = Memory.readPointer(args[1].add(i * Process.pointerSize));
                send(i+" msg:"+pClassName)
                if(i==2){
                    var iov = Memory.readPointer(pClassName);
                    var leng = Memory.readPointer(pClassName.add(Process.pointerSize));
                    send("    iov:"+iov);
                    
                    send("    length:"+leng);
                    var sendbuffer = iov.readByteArray(leng.toInt32());
                    var sendView = new Uint8Array(sendbuffer,0,leng.toInt32());
                    send("view length:"+sendView.length)
                    var myArray = new Array(sendView.length);
                    if(sendView[0]==0x80 && sendView[1]==0x60){
                        send("send strings:",iov.readByteArray(leng.toInt32()));
                        send("find match pattern")
                        for(var j = 2;j < sendView.length; j++){
                            myArray[j] = sendView[j]^encArray[j];
                        }
                        myArray[0] = sendView[0]
                        myArray[1] = sendView[1]
                        iov.writeByteArray(myArray)
                        send("send strings after:",iov.readByteArray(leng.toInt32()));
                    }
                    
                }
                
            }
            //send("ear_log args[3]:"+args[3].readCString());
            //send("ear_log args[5]:"+args[5].readCString());
            //send("ear_log args[6]:"+args[6].readCString());
            // console.log(Thread.backtrace(this.context,Backtracer.FUZZY).map(DebugSymbol.fromAddress).join("\\n"));
        }
    }
);

Interceptor.attach(Module.findExportByName("libandromeda.so" , "recvmsg"),
    {   onEnter: function(args){ 
            this.iov = args[1];
            //send("ear_log args[3]:"+args[3].readCString());
            //send("ear_log args[5]:"+args[5].readCString());
            //send("ear_log args[6]:"+args[6].readCString());
            // console.log(Thread.backtrace(this.context,Backtracer.FUZZY).map(DebugSymbol.fromAddress).join("\\n"));
        },
        onLeave: function (retval){
            send("recv:")
            for (var i = 0; i < 4; i++) {
                //send(this.iov.add(i * Process.pointerSize))
                var pClassName = Memory.readPointer(this.iov.add(i * Process.pointerSize));
                send(i+" msg:"+pClassName)
                
                if(i==2){
                    var iov = Memory.readPointer(pClassName);
                    var leng = Memory.readPointer(pClassName.add(4));
                    send("    iov:"+iov);
                    
                    send("    length:"+leng);
                    send("    return length:"+retval.toInt32());
                    var sendbuffer = iov.readByteArray(retval.toInt32());
                    var sendView = new Uint8Array(sendbuffer,0,retval.toInt32());
                    send("view length:"+sendView.length)
                    var myArray = new Array(sendView.length);
                    
                    if(sendView[0]==0x80 && sendView[1]==0x60){
                        send("recv strings:",iov.readByteArray(retval.toInt32()));
                        send("find match pattern")
                        for(var j = 2;j < encArray.length; j++){
                            myArray[j] = sendView[j]^encArray[j];
                        }
                        myArray[0] = sendView[0]
                        myArray[1] = sendView[1]
                        iov.writeByteArray(myArray)
                        send("recv strings after:",iov.readByteArray(retval.toInt32()));
                    }
                    

                    
                }
                
            }
        }
    }
);
/*
send("audio")
Interceptor.attach(Module.findExportByName("libandromeda.so" , "ear_sock_send_sync"),
    {   onEnter: function(args){ 
            send("ear_sock_send_sync args[0]:"+args[0]);
            send("ear_sock_send_sync args[1]:"+args[1]);
            send("ear_sock_send_sync args[2]:"+args[2]);
            
                    //var iov = Memory.readPointer(args[1].add(32));
                    //var leng = Memory.readPointer(args[1].add(32).add(4));
                    //send("    iov:"+iov);
                    //send("strings:",iov.readByteArray(0x44c));
                    //send("    length:"+leng);
                
                
            
            //send("vns_unit_send_audio_data args[2]:"+args[2]);
            //send("vns_unit_send_audio_data args[3]:"+args[3]);
            //send("vns_unit_send_audio_data args[5]:"+args[5]);
            //send("ear_log args[6]:"+args[6].readCString());
            // console.log(Thread.backtrace(this.context,Backtracer.FUZZY).map(DebugSymbol.fromAddress).join("\\n"));
        }
    }
);*/
/*
Interceptor.attach(Module.findExportByName("libandromeda.so" , "ear_sock_recv_async"),
    {   onEnter: function(args){ 
            send("ear_sock_recv_async args[0]:"+args[0]);
            send("ear_sock_recv_async args[1]:"+args[1]);
            var iov = Memory.readPointer(args[1].add(32));
            var leng = Memory.readPointer(args[1].add(32).add(4));
            //send("    iov:"+iov);
            //send("strings:",iov.readByteArray(leng.toInt32()));
            //send("    length:"+leng);
            //send("vns_unit_send_audio_data args[2]:"+args[2]);
            //send("vns_unit_send_audio_data args[3]:"+args[3]);
            //send("vns_unit_send_audio_data args[5]:"+args[5]);
            //send("ear_log args[6]:"+args[6].readCString());
            // console.log(Thread.backtrace(this.context,Backtracer.FUZZY).map(DebugSymbol.fromAddress).join("\\n"));
        }
    }
);*/
"""
#导出所有的so导出函数
src2 = """
Java.perform(function(){
    send("Running Script");
    var securityCheck = undefined;
    var exports = Module.enumerateExportsSync("libandromeda.so");
    var i = 0;
    for(i=0; i<exports.length; i++){
        send("hook function name:"+exports[i].name);
        send("hook function addr:"+exports[i].address);
    }
    console.log("hook all end!");

});
"""
#遍历加载的so文件，获取其内存地址
src3 = """
Java.perform(function(){
    Process.enumerateModules({
        onMatch: function(exp){
            if(exp.name == 'libandromeda.so'){
                send(exp.name + "|" + exp.base + "|" + exp.size + "|" + exp.path);
                send(exp);
                return 'stop';
            }
            
        }
        
    });
    var soAddr = Module.findBaseAddress("libandromeda.so");
    send(soAddr);
});
"""

#hook java层函数 发送消息
src4 = """
Java.perform(function(){
    var l= Java.use("jp.naver.line.android.activity.chathistory.f.l");
    send("start")
    l.a.overload("java.lang.CharSequence","java.lang.Long").implementation = function(arg0,arg1){
        send("Called - test(int,String):"+arg0+"----"+arg1);
        // just return origin
        return this.a.overload("java.lang.CharSequence","java.lang.Long").call(this,"arg0",arg1);
    };
    send("end")
    
});
"""

#hook java层函数 音频采集
src5 = """
Java.perform(function(){
    var l= Java.use("android.media.AudioRecord");
    send("start")
    l.startRecording.overload().implementation = function(){
        send("startrecording...");
        // just return origin
        return this.startRecording.overload().call(this);
    };
    send("end")
    
});
"""
#BB6A0428
jsCode = """
var soAddr = Module.findBaseAddress("libandromeda.so");

var targetAddr = ptr(0xBB69D054);
var audioopenAddr = ptr(0xBB69D224);

var real_audioOpen = ptr(Module.findExportByName('libandromeda.so', '_Z60Java_com_linecorp_andromeda_audio_AudioController_nAudioOpenP7_JNIEnvP8_jobjectxxS2_'));
var real_targetAddr = real_audioOpen.add(targetAddr).sub(audioopenAddr)
send(real_targetAddr)
 
Interceptor.attach(real_targetAddr, {
    onEnter: function(args) {
        console.log("[-] real_targetAddr hook invoked");
        send(args[0])
        send(args[1])
        send(args[2])
        send(args[3])
        send(args[4])
        args[2]=ptr(0);
        var v16 = Memory.readPointer(args[0].add(8));
        send("v16:"+v16)
        console.log(hexdump(args[0], {
                offset: 0,
                length: args[0].length,
                header: true,
                ansi: false
            }));
        var funcptr=Memory.readPointer(v16).add(8);
        send("funcptr:"+funcptr);
    }
});

targetAddr = ptr(0xBB6A0428);
real_targetAddr = real_audioOpen.add(targetAddr).sub(audioopenAddr)
send(real_targetAddr)
Interceptor.attach(real_targetAddr, {
    onEnter: function(args) {
        console.log("[-] real_targetAddr audiorecord hook invoked");
        //console.log(Thread.backtrace(this.context,Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join("\\n"));
        send("buffer address:"+args[0])
        
        for (var i = 0; i < 12; i++) {
            //send(args[0].add(i * Process.pointerSize))
            var pClassName = Memory.readPointer(args[0].add(i * Process.pointerSize));
            send(i+":"+pClassName)
        }
    }
});

targetAddr = ptr(0xBBA9182E);
real_targetAddr = real_audioOpen.add(targetAddr).sub(audioopenAddr)
send("BBA917F2:"+real_targetAddr)
Interceptor.attach(real_targetAddr, {
    onEnter: function(args) {
        console.log("[-] BBA9182E hook invoked");
        //console.log(Thread.backtrace(this.context,Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join("\\n"));
    }
});

"""
#BB94DACC
def on_message(message ,data):
    # file_object=open("d:\\log.txt",'ab+')
    # file_object.write(message['payload'].encode())
    # file_object.write(data.split(b'\x00')[0])
    # file_object.write('\n'.encode())
    # file_object.close()
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)
    if data:
        print(data)

with open("frida-test.js","r") as file:
    fridaSrc = file.read()
# print(fridaSrc)
script = session.create_script(fridaSrc)
script.on("message" , on_message)
script.load()
sys.stdin.read()