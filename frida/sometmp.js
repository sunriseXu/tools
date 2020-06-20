var voipNoti= Java.use("j.a.a.a.VoipNotificationCommand");
voipNoti.onStartCommand.overload("android.content.Intent","int","int").implementation = function(arg0,arg1,arg2){
    send("this is voip start command:"+arg1);
    var bundle = arg0.getBundleExtra("callConnectionInfo_bundle");
    if(bundle){
        var callConnectionInfo = bundle.getParcelable("callConnectionInfo");
        //go though all fields
        var fields = Java.cast(callConnectionInfo.getClass(),clazz).getDeclaredFields();
        for(var i in fields){
            var field = fields[i];
            // send("item:"+i)
            field.setAccessible(true);
            var tmpValue = field.get(callConnectionInfo);
            if(!tmpValue){
                continue;
            }
            var fieldValue = tmpValue.toString();
            //uid  is uxxxx length 33
            if(fieldValue.startsWith("u") && fieldValue.length==33){
                uidStr = fieldValue;
                break;
            }
        }
        Log.v(TAG_L, "[*] start audio call with "+uidStr);
        
    }
    return this.onStartCommand.overload("android.content.Intent","int","int").call(this,arg0,arg1,arg2);
}
var JFile = Java.use('java.io.File');
JFile.exists.implementation = function(argments){
    var filePath = this.getAbsolutePath();
        Log.v(TAG_L, "found file:"+filePath);
    return this.exists.call(argments);
    
}



var fileConstr = JFile.$init.overload("java.lang.String");
fileConstr.implementation = function(argments){
    var filePath = argments.toString();
    Log.v(TAG_L, "found file:"+filePath);
    if(filePath.indexOf(".jpg")!=-1|| filePath.indexOf(".aac")!=-1){
        Log.v(TAG_L, "start to print stack trace");
        var stackinfo = Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new())
        Log.v(TAG_L,"stackinfo:"+stackinfo);
        Log.v(TAG_L,"modify filepath:"+stackinfo);
        return fileConstr.call(this,"/sdcard/Android/data/13_20200106_004253.jpg");
    }
        return fileConstr.call(this,argments); 
}

var someClass = Java.use("j.a.a.a.b2.e.o");
someClass.a.overload("java.lang.String","boolean").implementation=function(v0,v1){
    Log.v(TAG_L, "arg0: "+v0+" arg1:"+v1);
    this.a.overload("java.lang.String","boolean").call(this,v0,v1);
}
var someClass2 = Java.use("k.a.l0.c.g");
someClass2.b.overload("java.lang.String").implementation=function(v0){
    Log.v(TAG_L, "b's arg0: "+v0);
    var res = this.b.overload("java.lang.String").call(this,v0);
    Log.v(TAG_L, "b's ress: "+res);
    return res;
}