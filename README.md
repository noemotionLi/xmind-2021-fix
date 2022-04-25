# xmind-2021-fix
似乎新版2021xmind以及之后的版本都不兼容python xmind包，可以用这个代码进行修复

xmind-fix.py实质上可以称作为 a tool for creating manifest.xml  automatically

## 1. 背景

xmind新版本无法兼容xmind包生成的文件，并抛出not a valid file错误

![xmind 报错](https://github.com/noemotionLi/xmind-2021-fix/blob/main/images/%E6%8A%A5%E9%94%99.png)

## 2. 原因

新版的xmind文件内（可以用zip压缩软件直接打开），可以看到有META-INF文件夹，而xmind包似乎不会生成这个目录文件。

![目录文件](https://github.com/noemotionLi/xmind-2021-fix/blob/main/images/xmind%E7%9B%AE%E5%BD%95.png)

# 3. 解决方案

思路：创建一个文件不就行了。ps. META-INF/manifest.xml就是个目录文件。比如 

```xml
<file-entry media-type="text/xml" full-path="content.xml"/>
```

其实很简单的，就是打开xmind文件，把原有的目录保存下来,生成一个xml文件。

放回原来的xmind中，就大功告成了。

详细内容请参考代码xmind_update.py。







