
// $new()用来创建对象，$init用来进行hook，是一个类字段，首先得有对象才能调用$init函数
// We need to replace .$init() instead of .$new(), since .$new() = .alloc() + .init()

//hook java函数File类的构造函数，观察读写文件的路径
//java方法：new File(String)
var fileConstr = JFile.$init.overload("java.lang.String");
fileConstr.implementation = function(argments){
    var filePath = argments.toString();
    var stackinfo = Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new())
    send(filePath)
    return fileConstr.call(this,argments); 
}

//java堆栈打印到logcat
//对应java方法： Log.i(TAG,Log.getStackTraceString(new Exception())); new Throwable()也行
var LogClazz = Java.use("android.util.Log")
var ExceptionClazz = Java.use("java.lang.Exception")
var exceptInstance = ExceptionClazz.$new() //创建类的一个对象，为什么不用$init，因为$init在没有对象的时候调用
console.log(LogClazz.getStackTraceString(exceptInstance))//转成string输出到控制台
//或者连起来一句话
console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()))

//调用Log输出日志
var LogClazz = Java.use("android.util.Log")
LogClazz.v("MyTag","this is test");
LogClazz.e("MyTag","this is error message");

//java层函数hook, 拓展hook所有重载函数
var className = "";
var methodName = "";
var targetClazz = Java.use(className)
//如果函数没有重载
targetClazz[methodName].implementation = function(argments){
    //函数重写的逻辑
    this //关键字this在函数内部代表函数所在的对象
    arguments[0],arguments[1]//关键字arguments代表参数数组，可以通过索引访问
    this.m.value = 0; //修改对象成员变量值
    this.otherfunc(); //调用对象其他方法
};
//java层函数hook, 拓展hook所有重载函数
var className = "";
var methodName = "";
var targetClazz = Java.use(className)
//如果函数有重载，则要指定参数类型
var paramTypes = ['int','int']
targetClazz[methodName].overload(paramTypes).implementation = function(arguments){
    this //关键字this在函数内部代表函数所在的对象
    arguments[0],arguments[1]//关键字arguments代表参数数组，可以通过索引访问
    this.mAge.value = 0; //修改对象成员变量值
    this.otherfunc(); //调用对象其他方法
};
//或者
targetClazz[methodName].overload('int','int').implementation = function(argments){
    //函数重写的逻辑
};
//重载参数写法：基本类型同java写法，基本类型的数组需要用 [+缩写，例如int[] -> [I
//非基本类型，类的全名即可，系统类与自定义类都是全名

//todo 类型转换：将对象转换成目标类的对象 
var NewTypeClass=Java.cast(variable,targetClass);

//遍历对象字段,修改对象字段值
/* java代码
Class cls = o.getClass();
Field[] fields = cls.getDeclaredFields();
for(int i = 0;i < fields.length; i ++){
    Field f = fields[i];
    f.setAccessible(true);
    try {
        //f.getName()得到对应字段的属性名，f.get(o)得到对应字段属性值,f.getGenericType()得到对应字段的类型
        System.out.println("属性名："+f.getName()+"；属性值："+f.get(o)+";字段类型：" + f.getGenericType());
    } catch (IllegalArgumentException | IllegalAccessException e) {
        // TODO Auto-generated catch block
        e.printStackTrace();
    }
}
*/
function enumerateFields(obj){
    var clazz = Java.use('java.lang.Class');
    var fields = Java.cast(obj.getClass(),clazz).getDeclaredFields();
    for(var i in fields){
        var field = fields[i];
        // send("item:"+i)
        field.setAccessible(true);
        var name = field.getName();
        var type = field.getGenericType();
        var value = field.get(obj);
        //修改当前字段的值
        field.set(obj, 1);
        console.log(name,type,value)
    }
}
//不用反射来获取并修改字段的值
obj.m.value = xxx


//获取Application Context
var currentApplication = Java.use('android.app.ActivityThread').currentApplication();
var context = currentApplication.getApplicationContext();

//创建一个实例对象
var stringClass = Java.use("java.lang.String");
var stringInstance = stringClass.$new("Hello World");



//hook 所有重写的方法，这里的hook方式不太能够理解
function hookOverloads(className, func) {
    var clazz = Java.use(className);
    var overloads = clazz[func].overloads;
    for (var i in overloads) {
      if (overloads[i].hasOwnProperty('argumentTypes')) {
        var parameters = [];
  
        var curArgumentTypes = overloads[i].argumentTypes, args = [], argLog = '[';
        for (var j in curArgumentTypes) {
          var cName = curArgumentTypes[j].className;
          parameters.push(cName);
          argLog += "'(" + cName + ") ' + v" + j + ",";
          args.push('v' + j);
        }
        argLog += ']';
  
        var script = "var ret = this." + func + '(' + args.join(',') + ") || '';\n"
          + "console.log(JSON.stringify(" + argLog + "));\n"
          + "return ret;"
  
        args.push(script);
        clazz[func].overload.apply(this, parameters).implementation = Function.apply(null, args);
      }
    }
}
Java.perform(function() {
    //调用全局函数
    hookOverloads('java.lang.StringBuilder', '$init');
})




//target method
var className = "com.example.test.Hello";
var methodName = "testFunc";
var targetClazz = Java.use(className)
targetClazz[methodName].overload("int","java.lang.String").implementation = function(v0,v1){
    this //this Object
    arguments[0],arguments[1]//get access to arguments
    this.mAge.value = 0; //modify variable in this object
    this.otherfunc(); //invoke other function in this object
};

//hook sendmsg()
var nativePointer = Module.findExportByName("libc.so", "sendmsg");
//absolute address of sendmsg
Interceptor.attach(nativePointer, {
    onEnter: function(args){// before the execution of this function
        send(args[0]); //print first arg
        send(args[1]);
        args[0] = ptr(1000); //modify arg0
    },
    onLeave: function(retval){//after the execution of this function
        send(retval.toInt32()); //get the return value 
        retval.replace(10000); //modify the return value
    }
});