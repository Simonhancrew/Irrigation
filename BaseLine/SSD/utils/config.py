Config = {
    #-----------------------------------------------------------------#
    #   训练前一定要修改num_classes，不然会出现shape不匹配！
    #-----------------------------------------------------------------#
    'num_classes': 21,
    #-----------------------------------------------------------------#
    #   min_dim有两个选择。
    #   一个是300、一个是512。
    #   这里的SSD512不是原版的SSD512。
    #   原版的SSD512的比SSD300多一个预测层；
    #   修改起来比较麻烦，所以我只是修改了输入大小
    #   这样也可以用比较大的图片训练，对于小目标有好处
    #   当min_dim = 512时，'feature_maps': [64, 32, 16, 8, 6, 4]
    #   当min_dim = 300时，'feature_maps': [38, 19, 10, 5, 3, 1]
    #-----------------------------------------------------------------#
    'min_dim': 300,
    'feature_maps': {
        'vgg'       : [38, 19, 10, 5, 3, 1],
        'mobilenet' : [19, 10, 5, 3, 2, 1],
    },
    # 'min_dim': 512,
    # 'feature_maps': {
    #     'vgg'       : [64, 32, 16, 8, 6, 4],
    #     'mobilenet' : [32, 16, 8, 4, 2, 1],
    # },

    #----------------------------------------------------#
    #   min_sizes、max_sizes可用于设定先验框的大小
    #   默认的是根据voc数据集设定的，大多数情况下都是通用的！
    #   如果想要检测小物体，可以修改
    #   一般调小浅层先验框的大小就行了！因为浅层负责小物体检测！
    #   比如min_sizes = [21,45,99,153,207,261]
    #       max_sizes = [45,99,153,207,261,315]
    #----------------------------------------------------#
    'min_sizes': [30, 60, 111, 162, 213, 264],
    'max_sizes': [60, 111, 162, 213, 264, 315],
    
    'aspect_ratios': {
        'vgg'       : [[2], [2, 3], [2, 3], [2, 3], [2], [2]],
        'mobilenet' : [[2, 3], [2, 3], [2, 3], [2, 3], [2, 3], [2, 3]]
    },
    'variance': [0.1, 0.2],
    'clip': True,
}
