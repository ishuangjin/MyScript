**自行抓包，下面直接分析 java**

# java 层分析

[![img](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_88a70adb9b9b8c6c831604c14fe269f4.jpg)](https://www.qinless.com/wp-content/uploads/2021/11/wp_editor_md_88a70adb9b9b8c6c831604c14fe269f4.jpg)

先全局搜索 `siua` 关键词，定位到这里在搜索，`API_KEY_siua`

[![img](https://www.qinless.com/wp-content/uploads/2021/11/619fb00c22627.png)](https://www.qinless.com/wp-content/uploads/2021/11/619fb00c22627.png)

点进这里看一下

[![img](https://www.qinless.com/wp-content/uploads/2021/11/619fb0ddb25c1.png)](https://www.qinless.com/wp-content/uploads/2021/11/619fb0ddb25c1.png)

跟进 `MTGuard.userIdentification` 函数， 在跟进 `MTGuard.siua` 函数

[![img](https://www.qinless.com/wp-content/uploads/2021/11/619fb1309a866.png)](https://www.qinless.com/wp-content/uploads/2021/11/619fb1309a866.png)

[![img](https://www.qinless.com/wp-content/uploads/2021/11/619fb17089b30.png)](https://www.qinless.com/wp-content/uploads/2021/11/619fb17089b30.png)

[![img](https://www.qinless.com/wp-content/uploads/2021/11/619fb17c2831e.png)](https://www.qinless.com/wp-content/uploads/2021/11/619fb17c2831e.png)

继续跟下去最终是来到了 `startCollection native` 函数，该函数是个实例函数，不是 `static`

# unidbg

[![img](https://www.qinless.com/wp-content/uploads/2021/11/619fb2276ea61.png)](https://www.qinless.com/wp-content/uploads/2021/11/619fb2276ea61.png)

因为是实例方法，所以在调用的时候需要先初始化一下 `SIUACollector` 这个类，当然如果你是根据 函数地址调用，完全不需要这一步操作

- 跑起来之后就开始补环境，过程是十分的漫长，需要补很多
- siua 获取了很多设备指纹，比如电量电池之屏幕亮度啥的

[![img](https://www.qinless.com/wp-content/uploads/2021/11/619fb30b9c19d.png)](https://www.qinless.com/wp-content/uploads/2021/11/619fb30b9c19d.png)

最终补完 630 行代码左右，最后结果也是成功运行出来，环境总体来说，不难，就是需要花时间