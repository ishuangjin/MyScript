> 使用 `frida` 辅助分析 so 加密，并使用 unidbg 完成 黑盒调用, apk 版本 5.7.1

# 分析请求包

[![1-charles-01](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_b4dfb32bd7877651b13b023312f27689.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_b4dfb32bd7877651b13b023312f27689.jpg)

这里请求参数里包含 `sig`，很明显是个 hash 值啊，直接去反编译 apk 分析

# 分析 java

[![2-jeb-01](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_22a45885b3fd12ce79c0f3055674ec22.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_22a45885b3fd12ce79c0f3055674ec22.jpg)

通过全局搜索关键词 `sig` 最终定位到 `com.akc.im.akc.api.sign.Sign` 这个类的 `addHttpUrlParams` 方法，里面会去调用 `MXSecurity.signV1` 函数获取 `sig` 的加密结果

[![3-jeb-02](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_a3971166f7eb1188e8fe5daec6953aab.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_a3971166f7eb1188e8fe5daec6953aab.jpg)

点进去发现这里是个 `native` 函数，函数的实现在 `libmx.so` 文件里，调用 `signV1` 函数需要传递三个`String` 参数，这里我们静态分析，不能确定传递的是什么，使用 `frida hook` 这个函数来查看

# frida hook java function

```
function main() {
    Java.perform(function () {
        var MXSecurity = Java.use('com.mengxiang.arch.security.MXSecurity')

        MXSecurity.signV1.implementation = function (a, b, c) {
            console.log('a: ', a);
            console.log('b: ', b);
            console.log('c: ', c);

            var res = this.signV1(a, b, c);
            console.log('res: ', res);

            return res
        }
    })
}

setImmediate(main);COPY
```

我们直接 `hook` 这个函数，打印参数，跟返回值

[![4-frida-01](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_497d5257bcd1c8b51b7f5d9ed9856bc6.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_497d5257bcd1c8b51b7f5d9ed9856bc6.jpg)

可以看到，这三个分数分别对应的请求的 `url` 跟 `url` 参数里的 `noncestr, timestamp`，加密结果是 `5b47f95d89ef4e29f8a96cb6897049b705de848c`
这里我们记录下这些参数，便于后面主动调用时验证参数。
现在我们直接去使用 `ida` 查看 so 文件逻辑

# ida so 分析

[![5-ida-01](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_2879935c17e4ffd4a3f478dc70bf60e0.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_2879935c17e4ffd4a3f478dc70bf60e0.jpg)

这里可以直接看到 `signV1` 是个静态注册的函数，双进去查看逻辑

[![6-ida-02](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_72ffecb25c2b9a4b4267c46e07a021cc.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_72ffecb25c2b9a4b4267c46e07a021cc.jpg)

这里前面拼接了一些参数，然后调用 `digest` 函数，进行加密，传了三个参数，分别是 `JNIEnv, 加密方式 (sha1), 要加密的内容 bytearray`，双击点击去看看逻辑

[![7-ida-03](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_5e2c465223dadec4d5b045bbce42ae54.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_5e2c465223dadec4d5b045bbce42ae54.jpg)

进来之后就是直接反射调用 `java` 层的 `hash` 加密算法，到这里分析算是结束了
已知使用的是 `sha1` 加密，参数前面已经分析出来了，不过在 `so` 文件里加了个 `secrer` 参数。这个目测应该是盐值，只要获取到这个参数就可以直接还原算法，获取的方式有很多 `jnitrace, frida hook native` 都可以，我们这里不去还原算法，直接使用 `unidbg` 进行黑盒调用

# unidbg 黑盒调用

### 环境搭建

[unidbg github](https://github.com/zhkl0228/unidbg) 这里放个网址，直接 clone 下来，使用 idea 加载就完事了
具体使用就不说了，直接开干

[![8-idea-01](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_ac1ecc87e301acd037e7af92e12b53b5.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_ac1ecc87e301acd037e7af92e12b53b5.jpg)

先在 `unidbg-android/src/test/java/com` 下创建文件夹，我这里创建了 `xiayu`，在创建个一个 `Java Class` 文件.
下面 `resources` 下创建文件夹用来存放 so 文件

### 代码编写

先来个简单的 demo

```
package com.xiayu;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.LibraryResolver;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.AbstractJni;
import com.github.unidbg.linux.android.dvm.DalvikModule;
import com.github.unidbg.linux.android.dvm.DvmClass;
import com.github.unidbg.linux.android.dvm.VM;
import com.github.unidbg.memory.Memory;

import java.io.File;
import java.io.IOException;

public class AkuMx1 extends AbstractJni {
    // 初始化一些 apk 常量
    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;
    private final DvmClass mxSecurity;

    // APK 路径
    public String apkPath = "/Users/admin/Desktop/android/file/aikucun-5.7.1.apk";
    // so 文件路径
    public String soPath = "unidbg-android/src/test/resources/test_so/libmx.so";

    // 加载指定版本的系统库
    private static LibraryResolver createLibraryResolver() {
        return new AndroidResolver(23);
    }

    // 创建 android 模拟器，这里是 32 位的
    private static AndroidEmulator createARMEmulator() {
        return AndroidEmulatorBuilder.for32Bit().build();
    }

    AkuMx1() {
        emulator = createARMEmulator();
        final Memory memory = emulator.getMemory();
        // 设置 sdk版本 23
        memory.setLibraryResolver(createLibraryResolver());

        //创建DalvikVM，可以载入apk，也可以为null
        vm = emulator.createDalvikVM(new File(apkPath));
        // 设置可以调用 jni 函数
        vm.setJni(this);
        // 打印 jni 函数调用具体的 log
        vm.setVerbose(true);

        // 加载 so 文件
        DalvikModule dm = vm.loadLibrary(new File(soPath), true);
        module = dm.getModule();
        // 加载 java 加密函数所在 类
        mxSecurity = vm.resolveClass("com/mengxiang/arch/security/MXSecurity");
    }

    public void run() {}

    // 关闭模拟器
    private void destroy() throws IOException {
        emulator.close();
        System.out.println("destroy");
    }

    public static void main(String[] args) throws IOException {
        AkuMx1 aku = new AkuMx1();
        aku.run();
        aku.destroy();
    }
}COPY
```

[![9-idea-unidbg-01](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_38208152eb0b37a3295ef0b4a587905a.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_38208152eb0b37a3295ef0b4a587905a.jpg)

这里代码写好后跑起来，发现没有任何问题，继续往下写.
上面的分析发现，加密函数是 `signV1` 我们这里直接去调用这个函数，参数是三个 `String` 返回值也是个 `String`

```
public void run() {
        String a = "https://zuul.aikucun.com/aggregation-center-facade/api/app/index/left/brandlist/v1.0?appid=38741001&did=740a8c1c7b0d6dda519d3ae1ec813689&noncestr=a2a0d0&subuserid=316cb4a4af56818d2cffc5cf3147137a×tamp=1623998117&token=460f6160e6a0478eb6583609c2afd774&userId=316cb4a4af56818d2cffc5cf3147137a&userid=316cb4a4af56818d2cffc5cf3147137a&zuul=1";
        String b = "a2a0d0";
        String c = "1623998117";

        DvmObject<?> strRc = mxSecurity.callStaticJniMethodObject(
                emulator,
                "signV1(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;",
                vm.addLocalObject(new StringObject(vm, a)),
                vm.addLocalObject(new StringObject(vm, b)),
                vm.addLocalObject(new StringObject(vm, c))
        );
        System.out.println("strRc: " + strRc.getValue());
    }COPY
```

我们直接在 `run` 函数里编写代码，先构建那三个参数，就是我们刚 `frida hook` 出来的，然后去调用 `mxSecurity.callStaticJniMethodObject`(`mxSecurity` 是函数所在的类，构造函数里已初始化好了)

[![10-idea-unidbg-02](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_c08b2562fbecccac08778d32afe7b1db.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_c08b2562fbecccac08778d32afe7b1db.jpg)

我们再次运行，这里成功调用了`JNIEnv->NewStringUTF`但是返回值是空，这里我们再去分析下 so 文件这个函数

[![11-ida-04](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_db9a6188912e4de042f0111647ac78f8.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_db9a6188912e4de042f0111647ac78f8.jpg)

这里可以看到 `so` 文件进来之后，会先有个 `if` 判断，条件如果不成立会执行 `else` 会返回一个空值，这里可以猜测，是 `if` 判断为成立，什么原因现在还不知道，我们使用 `frida` 主动调用 `signV1` 函数试一下

[![12-pycharm-frida-01](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_39bb5cd88d1706c1e70026a47ed9d6a2.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_39bb5cd88d1706c1e70026a47ed9d6a2.jpg)

这里可以看到，使用 `frida` 一切正常，那我们这里是问题呢，有N多种可能，不过最常见的还是上下文缺失，缺少环境问题，这里我们使用 `jnitrace` 打印下 `libmx.so`的执行流，具体使用就不说了，自行查看 [github](https://github.com/chame1eon/jnitrace) 文档

### 环境依赖

[![13-ida-05](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_9e806323ab581c7a80a9d492fbda8449.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_9e806323ab581c7a80a9d492fbda8449.jpg)

经过 `jnitrace` 的打印，才发现，调用 `signV1` 函数之前还需要调用 `init` 函数也就是上图的函数.
那我们就先调用这个函数

[![14-jeb-03](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_154f59feb5fdebb35c0f27523a4f0745.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_154f59feb5fdebb35c0f27523a4f0745.jpg)

有两个参数，分别是 `context, boolean`，返回值是 `int` ，我们直接来构建，这里的 `boolean` 经过 `frida hook` 发现是个 `null`

```
public void run() {
        // 加载 context 上下文对象
        DvmClass Context = vm.resolveClass("android/content/Context");
        DvmObject<?> strRc1 = mxSecurity.callStaticJniMethodObject(
                emulator, "init(Landroid/content/Context;Z;)I;",
                // Context.newObject(null) 初始化对象，参数直接 null
                vm.addLocalObject(Context.newObject(null)),
                // 这里也是 null
                vm.addLocalObject(null)
        );
        System.out.println("strRc1: " + strRc1);

        String a = "https://zuul.aikucun.com/aggregation-center-facade/api/app/index/left/brandlist/v1.0?appid=38741001&did=740a8c1c7b0d6dda519d3ae1ec813689&noncestr=a2a0d0&subuserid=316cb4a4af56818d2cffc5cf3147137a×tamp=1623998117&token=460f6160e6a0478eb6583609c2afd774&userId=316cb4a4af56818d2cffc5cf3147137a&userid=316cb4a4af56818d2cffc5cf3147137a&zuul=1";
        String b = "a2a0d0";
        String c = "1623998117";

        DvmObject<?> strRc2 = mxSecurity.callStaticJniMethodObject(
                emulator,
                "signV1(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;",
                vm.addLocalObject(new StringObject(vm, a)),
                vm.addLocalObject(new StringObject(vm, b)),
                vm.addLocalObject(new StringObject(vm, c))
        );
        System.out.println("strRc2: " + strRc2.getValue());
    }COPY
```

[![15-idea-unidbg-03](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_fbdf9c48a8e3af10e9f8922446f7f429.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_fbdf9c48a8e3af10e9f8922446f7f429.jpg)

修改后的 `run` 函数，启动又报错，说是找不到 `MessageDigest SHA256`，最后经过百度知道，`SHA256` 是 `android`里的，`java` 里是 `SHA-256`，我们直接重写这个函数，处理这个逻辑

```
@Override
    public DvmObject<?> callStaticObjectMethodV(BaseVM vm, DvmClass dvmClass, String signature, VaList vaList) {
        switch (signature) {
            case "java/security/MessageDigest->getInstance(Ljava/lang/String;)Ljava/security/MessageDigest;":
                StringObject type = vaList.getObjectArg(0);

                String name = "";
                if ("\"SHA256\"".equals(type.toString())) {
                    name = "SHA-256";
                } else {
                    name = type.toString();
                    System.out.println("else name: " + name);
                }

                try {
                    return vm.resolveClass("java/security/MessageDigest").newObject(MessageDigest.getInstance(name));
                } catch (NoSuchAlgorithmException e) {
                    throw new IllegalStateException(e);
                }
        }

        return super.callStaticObjectMethodV(vm, dvmClass, signature, vaList);
    }COPY
```

[![16-idea-unidbg-04](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_4d6e1a284af22bb61880e385496faaa7.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_4d6e1a284af22bb61880e385496faaa7.jpg)

添加这个函数，继续运行，同样的问题继续添加一个 `else if` 分支

```
String name = "";
if ("\"SHA256\"".equals(type.toString())) {
    name = "SHA-256";
} else if ("\"SHA1\"".equals(type.toString())) {
    name = "SHA-1";
} else {
    name = type.toString();
    System.out.println("else name: " + name);
}COPY
```

[![17-idea-unidbg-05](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_e21265b42dc4ca7f7474d6d4d27dee15.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_e21265b42dc4ca7f7474d6d4d27dee15.jpg)

继续运行，现在结果出来了，跟前面 `hook` 到的值进行对比，发现是一样的

# 最后

> 像这种比较简单的 hash 算法，可以直接还原，但是如果遇到比较负责的，这时候 unidbg 的优势就体现出来了，直接模拟 android 环境黑盒调用 so 文件函数，还可以使用 sprintboot 启动服务直接通过接口获取加密结果