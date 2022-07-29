# 工作准备

> apk 版本：7.45.6
> 工具：jadx-gui, jeb, ida, frida.

# 分析数据包

> 发现headers里有个hash值，OAuth api_sign，直接去反编译 apk 静态分析
> 前面 java 层的分析就不贴图了，直接贴关键点

# 分析java层

[![1-jeb-01](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_85d1560e61f13f0928373c06028da32e.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_85d1560e61f13f0928373c06028da32e.jpg)

通过全局搜索关键词，最终定位到 `com.vip.vcsp.security.sign.VCSPSecurityConfig` 这个类

[![2-jeb-02](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_bc95d5b9ef018f9dee2882edbe492f05.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_bc95d5b9ef018f9dee2882edbe492f05.jpg)

主要看 `getMapParamsSign` 函数, 会先处理请求 `params` 然后调用 `VCSPSecurityConfig.getSignHash`

[![3-jeb-03](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_b17ea112fcd4f633a5690da22e2a6d38.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_b17ea112fcd4f633a5690da22e2a6d38.jpg)

这里是 `getSignHash` 函数，直接调用 `VCSPSecurityConfig.gs` 函数

[![4-jeb-04](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_d18a86a7f496fb4e62d8187c06d91e20.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_d18a86a7f496fb4e62d8187c06d91e20.jpg)
[![5-jeb-05](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_41538fd87202466ffc8dcde567f3a2b0.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_41538fd87202466ffc8dcde567f3a2b0.jpg)

`VCSPSecurityConfig.gs` 函数里主要做了两件事情，第一件是调用 `initInstance` 函数初始化, 第二件是 通过 `clazz.getMethod` 函数获取到 `gs` 函数并调用

[![6-jeb-06](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_dbcd859dbc7ef5af05d4db0406a03052.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_dbcd859dbc7ef5af05d4db0406a03052.jpg)

`gs` 里 调用了 native 函数 `gsNav`，此函数在 `libkeyinfo.so` 文件里，使用 ida 静态分析

# ida 静态分析

[![7-ida-01](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_ef13b3bf1cd81d74397974fa2a44f59b.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_ef13b3bf1cd81d74397974fa2a44f59b.jpg)

这里直接在 `exports` 导出窗口里搜索 `Java` 关键词，发现 `gsNav` 这个函数是静态注册的直接双击进去

[![8-ida-02](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_e0ab79f30ee23f3243255ff535bb025e.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_e0ab79f30ee23f3243255ff535bb025e.jpg)

这里通过分析主要加密逻辑在 `j_Functions_gs` 函数里，其他的就不看了，点进去看看逻辑

[![9-ida-03](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_15a12d7d387fe3efeaf0be51bec37942.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_15a12d7d387fe3efeaf0be51bec37942.jpg)

这里是对 `params` map 处理，往下走

[![10-ida-04](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_c33f09e04f1d31470c4f1184986b16da.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_c33f09e04f1d31470c4f1184986b16da.jpg)

这里调用了 `j_getByteHash` 函数，跟进去看看, 会有个 `getByteHash` 函数在跟进去

[![11-ida-05](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_25bef0cd47dc8a1c915f35dd90b5adc7.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_25bef0cd47dc8a1c915f35dd90b5adc7.jpg)

发现使用的是 `sha1` 加密，直接使用 `frida` hook `getByteHash` 函数看看传递的是哪些参数

# frida hook native function

```
function main() {
  Java.perform(function () {
        var native_func = Module.findExportByName(
            "libkeyinfo.so", "getByteHash"
        );

        Interceptor.attach(native_func, {
            onEnter: function (args) {
                console.log('args[2]: ', Memory.readCString(args[2]));
            },
            onLeave: function (return_val) {
                console.log('return_val: ', Memory.readCString(return_val));
            }
        });
    });
}

setImmediate(main)COPY
```

[![12-charles-01](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_a3026ff0d5f1ce7bf576c2c105f7f716.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_a3026ff0d5f1ce7bf576c2c105f7f716.jpg)

抓包查看到 hash值是 `8d8ca93ad1a79b08f9f324db15f6b7d0cd898ae3`

[![13-frida-01](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_15b7d0f1fa26df0011ffbde502831078.jpg)](https://www.qinless.com/wp-content/uploads/2021/09/wp_editor_md_15b7d0f1fa26df0011ffbde502831078.jpg)

`frida hook 结果` 也是对的，中间调用了两次 sha1 加密, 每次前面都会加上一个 盐值 `a84c5883206309ad076deea939e850dc`