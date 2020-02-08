#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
import frida,sys

native_hook_code = """ Java.perform(function(){ 
    send("Running Script"); 
    var securityCheck = undefined; 
    exports = Module.enumerateExportsSync("libcrackme.so"); 
    for(i=0; i<exports.length; i++){ 
        if(exports[i].name == "Java_com_yaotong_crackme_MainActivity_securityCheck"){ 
            securityCheck = exports[i].address; 
            send("securityCheck is at " + securityCheck); break; 
        }
    } 
    Interceptor.attach(securityCheck,
        { onEnter: function(args)
            { 
                send("key is: " + Memory.readUtf8String(Memory.readPointer(securityCheck.sub(0x11a8).add(0x628c)))); 
            } 
        }
    ); 
}); """

check_hook_code = """ send("Running Script"); Java.perform(function(){ MainActivity = Java.use("com.yaotong.crackme.MainActivity"); MainActivity.securityCheck.implementation = function(v){ send("securityCheck hooked"); return true; } }); """

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)

process = frida.get_device_manager().enumerate_devices()[-1].attach("com.yaotong.crackme")
script = process.create_script(native_hook_code)
script.on('message', on_message)
script.load()
sys.stdin.read()


# -*- coding: UTF-8 -*-
import frida, sys
 
jsCode = """
Java.perform(function(){
    var nativePointer = Module.findExportByName("libhello.so", "Java_com_xiaojianbang_app_NativeHelper_add");
    send("native: " + nativePointer);
    Interceptor.attach(nativePointer, {
        onEnter: function(args){
            send(args[0]);
            send(args[1]);
            send(args[2].toInt32());
            send(args[3].toInt32());
            send(args[4].toInt32());
            args[4] = ptr(1000);   //new NativePointer
            send(args[4].toInt32());
        },
        onLeave: function(retval){
            send(retval.toInt32());
            retval.replace(10000);
            send(retval.toInt32());
        }
    });
});
""";
 
def message(message, data):
    if message["type"] == 'send':
        print(u"[*] {0}".format(message['payload']))
    else:
        print(message)
 
process = frida.get_remote_device().attach("com.xiaojianbang.app")
script= process.create_script(jsCode)
script.on("message", message)
script.load()
sys.stdin.read()

# 打印native调用栈
console.log("begin====");
var libavmp = Module.findBaseAddress("libsgavmpso-6.4.20.so");
var func = ptr(parseInt(libavmp)+0x1ea);
console.log("libavmp base: "+libavmp);
console.log("function base: "+func);
Interceptor.attach(func, {
	    onEnter: function(args) {
  console.log(Thread.backtrace(this.context,Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join(" "));
			

	    },
	    onLeave:function(retval){
	    	console.log("retval: "+retval);
	    }
	});

Interceptor.attach(Module.findExportByName("libnative-lib.so", 'Java_cn_hluwa_fridasamples_MainActivity_stringFromJNI'),
{
    onEnter: function (args) {
        console.log(Thread.backtrace(this.context, Backtracer.FUZZY)
        .map(DebugSymbol.fromAddress).join("\\n"))
    },
    onLeave: function (retval) {
    }
});

#打印 java层堆栈
Java.perform(
	function(){
		var ToastCls = Java.use('android.widget.Toast');
		var ThrowableCls = Java.use('java.lang.Throwable');
		ToastCls.makeText.overload('android.content.Context', 'java.lang.CharSequence', 'int').implementation = function (a1,a2,a3) {
			console.log("toast makeText: " + a2);
			var StackTrace = ThrowableCls.$new().getStackTrace()
			for(var stack in StackTrace)
			{
				console.log(StackTrace[stack]);
			}
			return this.makeText(a1,a2,a3);
		}
		console.log("hooked");
	}
);

#socket 活动
Process
  .getModuleByName({ linux: 'libc.so', darwin: 'libSystem.B.dylib', windows: 'ws2_32.dll' }[Process.platform])
  .enumerateExports().filter(ex => ex.type === 'function' && ['connect', 'recv', 'send', 'read', 'write'].some(prefix => ex.name.indexOf(prefix) === 0))
  .forEach(ex => {
    Interceptor.attach(ex.address, {
      onEnter: function (args) {
        var fd = args[0].toInt32();
        if (Socket.type(fd) !== 'tcp')
          return;
        var address = Socket.peerAddress(fd);
        if (address === null)
          return;
        console.log(fd, ex.name, address.ip + ':' + address.port);
      }
    })
  })


  function print_dump(addr,size){
    buf = Memory.readByteArray(addr,size)
    console.log("[function] send@ " + addr.toString() + "  "+ "length: " + size.toString() + "\n[data]")
    console.log(hexdump(buf, {
      offset: 0,
      length: size,
          header: false,
          ansi: false
    }));
    console.log("")
}

# -*- coding: UTF-8 -*-
import frida, sys
 
jsCode = """
Java.perform(function(){
    var soAddr = Module.findBaseAddress("libhello.so");
    send('soAddr: ' + soAddr);
    var MD5FinalAddr = soAddr.add(0x1768 + 1);
    send('MD5FinalAddr: ' + MD5FinalAddr);
    Interceptor.attach(MD5FinalAddr, {
        onEnter: function(args){
            send(args[0]);
            send(args[1]);
        },
        onLeave: function(retval){
            send(retval);
        }
    });
});
""";
 //console.log(Thread.backtrace(this.context,Backtracer.FUZZY).map(DebugSymbol.fromAddress).join("\\n"));
 //console.log(Thread.backtrace(this.context,Backtracer.FUZZY).map(DebugSymbol.fromAddress).join("\\n"));
def message(message, data):
    if message["type"] == 'send':
        print(u"[*] {0}".format(message['payload']))
    else:
        print(message)
 
process = frida.get_remote_device().attach("com.xiaojianbang.app")
script= process.create_script(jsCode)
script.on("message", message)
script.load()
sys.stdin.read()


function frida_Module() {
    Java.perform(function () {
        Module.getExportByName('libhello.so', 'c_getStr')
        console.log("Java_com_roysue_roysueapplication_hellojni_getStr address:",Module.findExportByName('libhello.so', 'Java_com_roysue_roysueapplication_hellojni_getStr'));
        console.log("Java_com_roysue_roysueapplication_hellojni_getStr address:",Module.getExportByName('libhello.so', 'Java_com_roysue_roysueapplication_hellojni_getStr'));
    });
}



//hook native未导出得函数
var moduleName = "libfoo.so"; 
var nativeFuncAddr = 0x1234; // $ nm --demangle --dynamic libfoo.so | grep "Class::method("

Interceptor.attach(Module.findExportByName(null, "dlopen"), {
    onEnter: function(args) {
        this.lib = Memory.readUtf8String(args[0]);
        console.log("dlopen called with: " + this.lib);
    },
    onLeave: function(retval) {
        if (this.lib.endsWith(moduleName)) {
            console.log("ret: " + retval);
            var baseAddr = Module.findBaseAddress(moduleName);
            Interceptor.attach(baseAddr.add(nativeFuncAddr), {
                onEnter: function(args) {
                    console.log("[-] hook invoked");
                    console.log(JSON.stringify({
                        a1: args[1].toInt32(),
                        a2: Memory.readUtf8String(Memory.readPointer(args[2])),
                        a3: Boolean(args[3])
                    }, null, '\t'));
                }
            });
        }
    }
});

console.log(hexdump(args[1], {
                offset: 0,
                length: args[1].length,
                header: true,
                ansi: false
            }));

/*
Interceptor.attach(Module.findExportByName("libandromeda.so" , "ear_str_snprintf"),
    { onEnter: function(args)
        { 
            console.log("ear_str_snprintf called!");
            
            console.log(hexdump(args[2], {
                offset: 0,
                length: args[2].length,
                header: true,
                ansi: false
            }));
            var i =0;
            for(i = 0;i<args.length;i++){
                if(i>1){
                    //console.log(Memory.readUtf8String(args[i]));
                    //print_dump(args[i],100);
                }
            }
            
            
            //console.log(Thread.backtrace(this.context,Backtracer.FUZZY).map(DebugSymbol.fromAddress).join("\\n"));
        },
        onLeave:function(retval){
            
        
        }
    }
    

);

Interceptor.attach(Module.findExportByName("libandromeda.so" , "vns_repacketizer_get_packet"),
    {   onEnter: function(args){ 
            send("vns_repacketizer_get_packet");
            console.log(Thread.backtrace(this.context,Backtracer.FUZZY).map(DebugSymbol.fromAddress).join("\\n"));
        }
    }
);
Interceptor.attach(Module.findExportByName("libandromeda.so" , "ear_iov_get_iov"),
    {   onEnter: function(args){ 
            send("ear_iov_get_iov");
        },
        onLeave:function(retval){
	    	console.log("retval: "+retval);
            var pSize = Process.pointerSize;
            var basebuffer = Memory.readPointer(retval);
            
            var basesize = Memory.readUInt(retval.add(pSize));
            
            console.log("basebuffer:"+basebuffer);
            console.log("basesize:"+basesize);
            send("data:",Memory.readByteArray(basebuffer,basesize))
	    }
    }
);
Interceptor.attach(Module.findExportByName("libandromeda.so" , "ear_iov_get_count"),
    {   onEnter: function(args){ 
            send("ear_iov_get_count");
        },
        onLeave:function(retval){
	    	console.log("retval: "+retval);
	    }
    }
);*/


//访问字段
Java.perform(function () {
    var utils = Java.use(‘com.xiaojianbang.app.Utils‘);
    var money = Java.use(‘com.xiaojianbang.app.Money‘);
    var clazz = Java.use(‘java.lang.Class‘);
    utils.test.overload(‘com.xiaojianbang.app.Money‘).implementation = function (obj) {
        send("Hook Start...");
        var mon = money.$new(4000,‘test‘);
        send(mon.getInfo());
        send(mon.name.value);
        mon.name.value="haidragon";
         send(mon);
        send(mon.name.value);
        var numid = Java.cast(mon.getClass(),clazz).getDeclaredField(‘num‘);
        numid.setAccessible(true);
        var value = numid.get(mon);
        console.log(value);
        send(value);
        numid.setInt(mon, 3000);
        var valueNew= numid.get(mon);
        send(numid.getInt(mon));
        return this.test(mon);
    }
});


var StringBuilder = Java.use('java.lang.StringBuilder');
  // We need to replace .$init() instead of .$new(), since .$new() = .alloc() + .init()
  var ctor = StringBuilder.$init.overload('java.lang.String');
  ctor.implementation = function (arg) {
    var partial = '';
    var result = ctor.call(this, arg);
    if (arg !== null) {
      partial = arg.toString().replace('\n', '').slice(0, 10);
    }