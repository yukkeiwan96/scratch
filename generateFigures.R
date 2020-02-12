counts=read.table(file="DNMT1-PARP1.csv",sep="\t")
colnames(counts)<-c("combination","G","FC")
df<-counts
df$G<- as.factor(df$G)
head(df)
log2FC<-df$FC
Combinations<-df$G
Type<-df$combination
library(ggplot2)
ggplot(df, aes(x=Combinations, y=log2FC, color=Type)) +
  geom_point(size=4, alpha=0.7, position=position_jitter(w=0.1, h=0)) +
  stat_summary(fun.y=mean, geom="point", shape=23, color="black", size=4) +         
  stat_summary(fun.ymin=function(x)(mean(x)-sd(x)), 
               fun.ymax=function(x)(mean(x)+sd(x)),
               geom="errorbar", width=0.1) +
  theme_bw()

counts=read.table(file="Nick_pairwise_CV1_sgRNA.csv",sep=",")
colnames(counts)<-c("combination","FC")
df<-counts
head(df)
log2FC<-df$FC
Combinations<-df$combination
ggplot(df, aes(x=df$combination, y=df$FC)) + 
  geom_point(col="tomato2", size=3) 

counts=read.table(file="Book1.csv",sep=",")
colnames(counts)<-c("model","type","MSE")
df<-counts
df$model<- as.factor(df$model)
head(df)
Model<-df$model
MSE<-df$MSE
Type<-df$type
library(ggplot2)
ggplot(df, aes(x=model, y=MSE, color=Type)) +
  geom_point(size=4, alpha=0.7, position=position_jitter(w=0.1, h=0)) +
  stat_summary(fun.y=mean, geom="point", shape=23, color="black", size=4) +         
  stat_summary(fun.ymin=function(x)(mean(x)-sd(x)), 
               fun.ymax=function(x)(mean(x)+sd(x)),
               geom="errorbar", width=0.1) +
  theme_bw()
