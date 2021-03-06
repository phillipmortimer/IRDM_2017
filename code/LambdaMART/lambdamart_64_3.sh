now=$(date +"%T")
echo "Current time : $now"
java -jar ../../RankLib/RankLib.jar -train ../../data/Fold1/train.txt -validate ../../data/Fold1/vali.txt -test ../../data/Fold1/test.txt -ranker 6 -norm linear -tree 250 -tc 64 -leaf 1 -shrinkage 1 -estop 25 -metric2t NDCG@10 -estop 25 -metric2t NDCG@10 -save ../../model/LambdaMART/lm_tc64_lf1_sh1.txt | tee ../../model/LambdaMART/lm_tc64_lf1_sh1.txt.log
now=$(date +"%T")
echo "Current time : $now"
java -jar ../../RankLib/RankLib.jar -train ../../data/Fold1/train.txt -validate ../../data/Fold1/vali.txt -test ../../data/Fold1/test.txt -ranker 6 -norm linear -tree 250 -tc 64 -leaf 10 -shrinkage 1 -estop 25 -metric2t NDCG@10 -estop 25 -metric2t NDCG@10 -save ../../model/LambdaMART/lm_tc64_lf10_sh1.txt | tee ../../model/LambdaMART/lm_tc64_lf10_sh1.txt.log
now=$(date +"%T")
echo "Current time : $now"
java -jar ../../RankLib/RankLib.jar -train ../../data/Fold1/train.txt -validate ../../data/Fold1/vali.txt -test ../../data/Fold1/test.txt -ranker 6 -norm linear -tree 250 -tc 64 -leaf 100 -shrinkage 1 -estop 25 -metric2t NDCG@10 -estop 25 -metric2t NDCG@10 -save ../../model/LambdaMART/lm_tc64_lf100_sh1.txt | tee ../../model/LambdaMART/lm_tc64_lf100_sh1.txt.log
now=$(date +"%T")
echo "Current time : $now"
java -jar ../../RankLib/RankLib.jar -train ../../data/Fold1/train.txt -validate ../../data/Fold1/vali.txt -test ../../data/Fold1/test.txt -ranker 6 -norm linear -tree 250 -tc 64 -leaf 1000 -shrinkage 1 -estop 25 -metric2t NDCG@10 -estop 25 -metric2t NDCG@10 -save ../../model/LambdaMART/lm_tc64_lf1000_sh1.txt | tee ../../model/LambdaMART/lm_tc64_lf1000_sh1.txt.log

