def GenCallers(packageDict,androidCallerDict):
    #遍历每一个方法，根据这个方法再计算对其的交叉引用，这个计算过程是巨大的假设有10 0000个方法，每个方
    #法需要遍历10 0000次，所以时间复杂度 是 10^10， 而我的电脑是2.5GHz 每秒2.5*10^9时钟周期，一次遍历需要5s，
    #那么一共需要多少秒呢？5*10^5 = 500000s = 13h 不可能缓存的好吧 只能用服务器的机器来跑，但是可以这样来减少
    #计算时间，那就是在每次正向计算的时候存下调用自己的方法不久行了吗，可以的，就这样算
    #所以遍历每个方法的invoke函数，每个invoke函数记录下自己的caller，问题来了，需要记录安卓函数的父类吗
    #感觉是可以的，相当于我自己在计算callgraph，java中有多态的invoke吗
    #那么对象也存在交叉引用啊，这涉及到数据流怎么构建的问题了，总之 这个dict需要不断地更新，所以按道理只要遍历一次
    #那么是否需要用额外的数据结构来存储callgraph，有必要,需要标记这个调用的属性，即direct / virtual
    #那么这个数据结构怎么表示呢？ classname:{methodnameA:{direct:[{classname:methodname},pb],virtual:[va,vb]},methodnameB:{}}
    #想了一下，还是觉得没有必要新建数据结构，直接增加到原来的字典中
    #新的问题出现了 
    exceptInfoList = []
    notfoundList = []
    foundcount = 0
    notfoundcount = 0
    notfoundSet = {}
    methodCount = 0
    androidapiCallcount=0
    foundinChild = 0
    #取出每一个类
    for clazz in packageDict:
        classDict = packageDict[clazz]
        cPath = classDict['clsPath']
        methodDictList = classDict['methods']
        methodCount += len(methodDictList)
        for methodIdentifer in methodDictList:
            #取出这个类中的所有方法
            methodDict = methodDictList[methodIdentifer]
            modifier = methodDict['modifier']
            methodName = methodDict['methodName']
            params = methodDict['methodParams']
            retType = methodDict['retType']
            invokeList = methodDict['invoke']
            callerKey = '{}{}'.format(methodName,list2Str(params))
            #对这个方法中的所有函数调用进行遍历
            for invokeDict in invokeList:
                invokeType = invokeDict['invokeType']
                iclassName = invokeDict['className'][0]
                # 如果调用的是java/android方法，那么跳过
                # 获取这个方法的指纹信息
                imethodName = invokeDict['methodName']
                iparams = invokeDict['methodParams']
                invokeKey = '{}{}'.format(imethodName,list2Str(iparams))
                #开始找caller
                # try: 
                if iclassName.startswith('java.') or iclassName.startswith('android.') \
                    or iclassName.startswith('androidx.') \
                        or iclassName.startswith('javax.') or 'dalvik' in iclassName:#'dalvik.system.DexClassLoader com.linecorp.linepay.biz.googlepay.a' 'com.samsung.android.sep.camera.SemCameraCaptureProcessor$CaptureParameter'
                    androidapiCallcount+=1
                    #这个点的调用占用到了一半以上，这是图的sink，所以很重要可以从这里开始分析
                    # print("{}.{}".format(iclassName,invokeKey))
                    # input() #这里需要对android/java api进行caller字典生成，暂时生成一个新的字典存放
                    # {classname:{methods:{methodkey:{caller:{cclazzname:{cmethod:invoketype}}}}}}
                    if iclassName not in androidCallerDict:
                        androidCallerDict[iclassName]= {'methods':{invokeKey:{'caller':{clazz:{callerKey:invokeType}}}}}
                    else:
                        if 'methods' not in androidCallerDict[iclassName]:
                            androidCallerDict[iclassName]['methods']= {invokeKey:{'caller':{clazz:{callerKey:invokeType}}}}
                        else:
                            if invokeKey not in androidCallerDict[iclassName]['methods']:
                                androidCallerDict[iclassName]['methods'][invokeKey] = {'caller':{clazz:{callerKey:invokeType}}}
                            else:
                                if clazz not in androidCallerDict[iclassName]['methods'][invokeKey]['caller']:
                                    androidCallerDict[iclassName]['methods'][invokeKey]['caller'][clazz] = {callerKey:invokeType}
                                else:
                                    androidCallerDict[iclassName]['methods'][invokeKey]['caller'][clazz].update({callerKey:invokeType})
                    
                    continue
                if iclassName not in packageDict: # 包含[] 数组方法
                    continue                 
                # 获取invoke方法的类，尝试找到这个invoke方法
                callerclassDict = packageDict[iclassName]
                #这个类找不到的原因有： 这个类是数组
                cclassmethodDictList = callerclassDict['methods']
                #获取这个类的父类，接口等
                foundFlag = False
                if invokeKey in cclassmethodDictList:
                    foundcount += 1
                    foundFlag = True
                    cmethodDict = cclassmethodDictList[invokeKey]
                    callerDict = cmethodDict['caller']
                    #添加caller信息
                    if clazz in callerDict:
                        cclazzDict = callerDict[clazz]
                        cclazzDict.update({callerKey:invokeType})
                    else:
                        callerDict[clazz] = {callerKey:invokeType}
                        #这里我们找到了直接调用的方法，为了构建callgraph，并且便于索引，需要在目标方法中添加caller字段
                        # caller字段是一个dict {invoke-type:类名，现在最恶心的是，方法是一个list，不能够直接索引}
                        # 明天要重构字典，修改所有方法为字典访问，键是什么呢？方法名+参数 可行！
                        # 重构完成后需要抛出一个dict大概需要1个小时
                        # 跑完后需要重新修改所有方法的访问，改成以字典访问
                        # 最后构建每个方法字典的caller字段
                        # caller字段构建后，应该可以完成大部分callgraph的生成，
                        # 打印某些方法的callgraph进行验证，注意需要处理android/java方法的callgraph
                        # 然后是匹配，匹配是最难处理的一步，callgraph上每个节点都是一个方法，匹配需要方法的指纹，然后再说整个图的匹配
                        # 这里需要用到图的匹配算法，所以需要进行调研
                        # 调用完成后实现算法的匹配，说实话，这里不能保证可用
                        # 完成这些需要大概一周的时间
                        # break
                if not foundFlag:
                    #由于invoke-virtual 的关系，导致无法确定具体的对象类，所以需要在父类或者子类中找
                    #首先在子类中找，但是子类可能很多，导致无法确定具体的子类，怎么办？
                    #总之尝试在子类中找吧，但是遍历所有来来找子类是不可能的，只能生成
                    #super 和 implement字段找到父类或者接口，然后在父类或者接口中添加字段
                    #一直super回溯搜索好了 如果这个方法死活找不到，有两种可能性
                    #
                    superClass = callerclassDict['super']
                    implementList = callerclassDict['implements']
                    impList = []
                    impList.extend(implementList)
                    if superClass:
                    #将接口和父类合在一起
                        impList.append(superClass)
                    notfoundList.append("{} {} {} {} {} {}".format(iclassName,imethodName,iparams,clazz,methodName,cPath))
                    print("current cls not found:\n\tclassName:{} methodName:{}({}) location: {}.{} {}".format(iclassName,imethodName,iparams,clazz,methodName,cPath))
                    #遍历父类，在父类方法中匹配
                    # print(implementList)
                    foundFlag = False
                    for sup in impList:
                        print("try super:{}".format(sup))
                        if sup not in packageDict:
                            continue
                        tmp, retClazz, retKey = traverseMethod(packageDict, sup, imethodName, iparams)
                        if tmp:
                            foundcount+=1
                            foundFlag = True
                            foundinChild +=1
                            callerDict = packageDict[retClazz]['methods'][retKey]['caller']
                            #添加caller信息
                            if clazz in callerDict:
                                cclazzDict = callerDict[clazz]
                                cclazzDict.update({callerKey:invokeType+'-child'})
                            else:
                                callerDict[clazz] = {callerKey:invokeType+'-child'}
                            break
                    if not foundFlag:
                        notfoundcount+=1
                        # notfoundSet.add(imethodName)
                        if imethodName in notfoundSet:
                            notfoundSet[imethodName] += 1
                        else:
                            notfoundSet[imethodName] = 0
                        print("not found method")
                        # input()
                    else:
                        ## todo 这里我们找到了invoke的父类方法，这里的方法是父类方法
                        pass
                # input()
                # except KeyError as err:
                #     exceptInfoList.append('{}'.format(err))
                #     pass
                        # input()
    # print("error:{}".format(exceptInfoList))
    FileUtils.writeList(exceptInfoList,"C:\\Users\\limin\\Desktop\\tmp\\error.txt")
    # print("notfound:{}".format(notfoundList))
    FileUtils.writeList(notfoundList,"C:\\Users\\limin\\Desktop\\tmp\\notfound.txt")
    print("{}".format(notfoundSet))
    print("foundcount:{} notfoundcount:{} foundinChild:{}".format(foundcount,notfoundcount,foundinChild))
    print("classcount:{}".format(len(packageDict)))
    print("methodcount:{}".format(methodCount))
    print("androidapiCallcount:{}".format(androidapiCallcount))
    FileUtils.writeDict(androidCallerDict,"C:\\Users\\limin\\Desktop\\tmp\\testAndroid.json")
def traverseMethod(packageDict, iclassName, imethodName, iparams):
    ## invoke的函数如果在整个包中找到则返回其函数签名
    callerclassDict = packageDict[iclassName]
    cclassmethodDictList = callerclassDict['methods']
    superClass = callerclassDict['super']
    implementList = callerclassDict['implements']
    impList = []
    impList.extend(implementList)
    if superClass:
    #将接口和父类合在一起
        impList.append(superClass)
    
    foundFlag = False
    invokeKey = '{}{}'.format(imethodName,list2Str(iparams))
    
    if invokeKey in cclassmethodDictList:
        foundFlag = True
        print("found in super class:{} {}".format(iclassName,invokeKey))
        return (foundFlag, iclassName, invokeKey)

    if not foundFlag:
        #由于invoke-virtual 的关系，导致无法确定具体的对象类，所以需要在父类或者子类中找
        #首先在子类中找，但是子类可能很多，导致无法确定具体的子类，怎么办？
        #总之尝试在子类中找吧，但是遍历所有来来找子类是不可能的，只能生成
        #super 和 implement字段找到父类或者接口，然后在父类或者接口中添加字段
        #一直super回溯搜索好了
        for sup in impList:
            if sup not in packageDict:
                #这里需要筛选出java/android api
                continue
            tmp,retClazz, retKey = traverseMethod(packageDict, sup, imethodName, iparams)
            if tmp:
                return (tmp, retClazz, retKey)
    return (False,"","")
    # input()