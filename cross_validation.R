# Template for generic cross validation with AUC output

library(pROC)
library(gbm)

k = 3 # Number of k-folds
id = sample(1:k,nrow(data),replace=TRUE)
list = 1:k
aucs=c()
for (i in 1:k){
  trainingset = data[id %in% list[-i],]
  testset = data[id %in% c(i),]
  
  # Training GBM
  fit.gbm = gbm(target ~ .,
                data=trainingset, distribution="adaboost", 
                n.trees=500, shrinkage=0.7, interaction.depth=1)
  pred = predict(fit.gbm, testset, type="response", n.trees=500) 
  
  # # Training GLM
  # fit.glm = glm(target ~ ., 
  #               data=trainingset, family=binomial)
  # pred = predict(fit.glm, testset, type="response")
  
  # Testing
  real = testset$target
  aucs = c(aucs,auc(real, pred))
  cat("auc:",auc(real, pred),"\n")
}
cat("mean auc:", mean(aucs),"sd:",sd(aucs),"\n")