> 某物 `newSign` 参数分析

# charles 抓包

[![img](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_af832bbabf5d96202f9810340db6b00a.jpg)](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_af832bbabf5d96202f9810340db6b00a.jpg)

就是这个 `newSign`, 一个 `hash` 值

# 反编译分析

[![img](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_089d0fc5bd56b9fdac333b084c2e15d2.jpg)](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_089d0fc5bd56b9fdac333b084c2e15d2.jpg)

全局搜索一下，

[![img](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_337394a848bde42a63db78afd638cebc.jpg)](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_337394a848bde42a63db78afd638cebc.jpg)

打开 `jeb` 搜索一下这个类，`jeb` 分析比较方便一点，进入 `RequestUtils.c` 函数

[![img](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_7700f7e91d686dd88daa539e9a14cd75.jpg)](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_7700f7e91d686dd88daa539e9a14cd75.jpg)

这里调用了 `RequestUtils.f, AESEncrypt.encode` 函数

[![img](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_20a99d59c51589b275183f886c22ca5f.jpg)](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_20a99d59c51589b275183f886c22ca5f.jpg)

`RequestUtils.f` 函数是标准的 `md5`

[![img](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_35fd00a8c9ba4ffd593cb831225ed426.jpg)](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_35fd00a8c9ba4ffd593cb831225ed426.jpg)

`AESEncrypt.encode` 函数调用了 `NCall.IL` 函数

[![img](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_c81e874b6c33b227bf690f2558b2848f.jpg)](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_c81e874b6c33b227bf690f2558b2848f.jpg)

`NCall.IL` 函数是在 `GameVMP`, `so` 里，实际上真正的加密逻辑是在 `libJNIEncrypt.so` 文件里，也就是上上图的 `encodeByte` 函数，俺也没搞懂里面的逻辑是啥，本想分析下 `GameVMP.so` 的，但是奈何里面对抗 `ida` 手段有点多，没搞定就直接放弃了（哪位老哥了解的，还望不杏赐教）

# so 分析

> **分析下 libJNIEncrypt.so**

[![img](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_68e15929fd374925db0254b3165271f0.jpg)](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_68e15929fd374925db0254b3165271f0.jpg)

在导出窗口里可以看到函数也不多，其中就有 `aes` 函数，符号都没去，加密方式是 `aes-128-ebc-pkcs#5`，因为 `so` 的对抗不好处理，就是用 `frida hook` 看看，输入输出

# frida hook

```
function hook() {
    var javaString = Java.use('java.lang.String');
    var AESEncrypt = Java.use('com.duapp.aesjni.AESEncrypt');

    AESEncrypt.encode.overload('java.lang.String').implementation = function (a) {
        console.log('AESEncrypt.encode.a: ', a);

        var res = this.encode(a);

        console.log('AESEncrypt.encode.res: ', res);

        return res;
    }

    AESEncrypt.encodeByte.implementation = function (a, b) {
        console.log('AESEncrypt.encodeByte.a: ', a);
        console.log('AESEncrypt.encodeByte.a: ', javaString.$new(a));
        console.log('AESEncrypt.encodeByte.b: ', b);

        var res = this.encodeByte(a, b);
        console.log('AESEncrypt.encodeByte.res: ', res);

        return res;
    }
}

function hookSo1() {
    var AESBase = Module.findExportByName('libJNIEncrypt.so', 'AES_128_ECB_PKCS5Padding_Encrypt')

    Interceptor.attach(AESBase, {
        onEnter: function (args) {
            console.log('-------------参数 1-------------');
            console.log(hexdump(args[0]));
            console.log('-------------参数 2-------------');
            console.log(hexdump(args[1]));
        },
        onLeave: function (retValue) {
            console.log('-------------返回-------------');
            console.log(hexdump(retValue));
        }
    })
}

function main() {
    Java.perform(function () {
        hook();
        hookSo1();
    })
}

setImmediate(main);

// frida -UF -l hook.jsCOPY
```

以上是 `hook` 代码，手机开启抓包，启动 `hook` 脚本，随便点点

[![img](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_602965d3d020dcf4cb3563bc27f2451d.jpg)](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_602965d3d020dcf4cb3563bc27f2451d.jpg)

`AESEncrypt.encodeByte` 函数的参数一，是请求的 `params`，参数二目前不知道是啥

[![img](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_66ce1e748f5f66577340e21336c68223.jpg)](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_66ce1e748f5f66577340e21336c68223.jpg)

返回值是 `aes` 的加密结果，前面 `java` 层分析到，最后还有个 `md5` 验证一下

[![img](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_dc86625de2e8a9340f148382033c2da2.jpg)](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_dc86625de2e8a9340f148382033c2da2.jpg)

[![img](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_4fff604213cc5c01a8e72aed602413cb.jpg)](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_4fff604213cc5c01a8e72aed602413cb.jpg)

上面分别是 `charles` 抓的包，跟 `cyberchef` 运算的结果相同，那就确定了标准的 `md5`

[![img](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_e6a2716264d2da17a782561367b2c55f.jpg)](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_e6a2716264d2da17a782561367b2c55f.jpg)

再来看看 `libJNIEncrypt.so -> AES_128_ECB_PKCS5Padding_Encrypt` 函数，参数一是 `url params`，参数二长度是 16 个字节，猜测是 `aes-key`

[![img](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_618c87a4f2a13dd8abbd6220db92b39f.jpg)](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_618c87a4f2a13dd8abbd6220db92b39f.jpg)

返回的结果正是 `aes` 加密的结果，使用 `cyberchef` 验证一下

[![img](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_a5ddba12fe670d590674225d40eef829.jpg)](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_a5ddba12fe670d590674225d40eef829.jpg)

正是标准的 `aes` 解密结果也是相同的