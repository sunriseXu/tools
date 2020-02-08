

var encArray = new Array(255);
for(var i = 0; i<encArray.length; i++){
    encArray[i] = i;
}
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
                    //send("strings:",iov.readByteArray(leng.toInt32()));
                    send("    length:"+leng);
                    var sendbuffer = iov.readByteArray(leng.toInt32());
                    var sendView = new Uint8Array(sendbuffer,0,leng.toInt32());
                    send("view length:"+sendView.length)
                    var myArray = new Array(sendView.length);
                    if(sendView[0]==0x80 && sendView[1]==0x60){
                        send("find match pattern")
                        for(var j = 2;j < sendView.length; j++){
                            myArray[j] = sendView[j]^encArray[j];
                        }
                        myArray[0] = sendView[0]
                        myArray[1] = sendView[1]
                        iov.writeByteArray(myArray)
                    }
                    //send("strings after:",iov.readByteArray(leng.toInt32()));
                }
                
            }

        }
    }
);

Interceptor.attach(Module.findExportByName("libandromeda.so" , "recvmsg"),
    {   onEnter: function(args){ 
            this.iov = args[1];
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
                    //send("strings:",iov.readByteArray(leng.toInt32()));
                    send("    length:"+leng);
                    var sendbuffer = iov.readByteArray(leng.toInt32());
                    var sendView = new Uint8Array(sendbuffer,0,leng.toInt32());
                    //send("view length:"+sendView.length)
                    var myArray = new Array(sendView.length);
                    
                    if(sendView[0]==0x80 && sendView[1]==0x60){
                        send("find match pattern")
                        for(var j = 2;j < encArray.length; j++){
                            myArray[j] = sendView[j]^encArray[j];
                        }
                        myArray[0] = sendView[0]
                        myArray[1] = sendView[1]
                        iov.writeByteArray(myArray)
                    }
                    //send("strings after:",iov.readByteArray(leng.toInt32()));

                    
                }
                
            }
        }
    }
);