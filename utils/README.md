### For Env Install Problem

关于`pip`的install，可以选用国内源,参考如下的格式就行

```
 pip install scrapy -i https://pypi.tuna.tsinghua.edu.cn/simple
```

关于conda的install，可以选择换源.

windows用户如果无法创建`.condarc`文件可以先执行`conda config --set show_channel_urls yes`,之后可以修改成如下

```
channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
ssl_verify: true
```

如果需要pytorch的镜像可以考虑

```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
```

如果要换回conda的默认源、

```
conda config --remove-key channels
```

