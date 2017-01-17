test.py 负责训练
run.py 预测1000张结果

1000张预测的名称、landmarks、ratings
imagename.txt
new_landmarks.txt
new_ratings.txt

训练集
landmarks.txt
ratings.txt

上述文件已部署好，只需运行python test.py得到降维模型pcaModel.model和训练模型trainModel.model
若想查看预测结果，则运行python run.py, 查看predict_ratings.txt

最后麻烦把pcaModel.model和trainModel.model发给我谢谢