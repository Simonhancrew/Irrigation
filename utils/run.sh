# for cvmart yolov5
project_root_dir=/project/train/src_repo
dataset_dir=/home/data
log_file=/project/train/log/log.txt

echo "remove pre" 
rm -rf /project/train/models/result-graphs && rm -rf /project/train/log && rm -rf /project/train/src_repo/trainval
rm -rf /project/train/models/exp* && rm -rf /project/train/tensorboard

echo "create new folder"
mkdir -p /project/train/result-graphs && mkdir -p /project/train/log && mkdir -p ./trainval && mkdir -p /project/train/tensorboard

# 进入代码文件
cd /project/train/src_repo

# 复制数据集到当前目论文件下
echo "复制数据集"
cp -r /home/data/664 ./trainval
echo "复制完成"
echo "切分"
python split.py && python path.py
echo "切分完成"

# 开始训练
cd yolov5
python train.py --batch 16 --epoch 100 --data ./data/my.yaml --hyp ./data/hyps/hyp.scratch-med.yaml --weights /project/train/src_repo/yolov5/ --img 480 --project /project/train/models/ --cfg ./models/yolov5s.yaml |  tee -a ${log_file}

echo "图片放到result" 
cp /project/train/models/exp/*.jpg /project/train/models/exp/*.png /project/train/tensorboard/results.png /project/train/result-graphs | tee -a ${log_file} 
