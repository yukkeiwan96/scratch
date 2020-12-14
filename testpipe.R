# test
dat <- read.table("IBD.txt",header=T,na.strings="NA",blank.lines.skip=F,row.names=1)
col_names <- paste(names(dat)[1:13], "normal", sep=" ")
colnames(dat)[1:13] <- col_names
col_names <- paste(names(dat)[14:21], "remission", sep=" ")
colnames(dat)[14:21] <- col_names
col_names <- paste(names(dat)[36:43], "mucosa", sep=" ")
colnames(dat)[36:43] <- col_names
col_names <- paste(names(dat)[34], "mucosa", sep=" ")
colnames(dat)[34] <- col_names
col_names <- paste(names(dat)[32], "mucosa", sep=" ")
colnames(dat)[32] <- col_names
col_names <- paste(names(dat)[30], "mucosa", sep=" ")
colnames(dat)[30] <- col_names
col_names <- paste(names(dat)[29], "mucosa", sep=" ")
colnames(dat)[29] <- col_names
col_names <- paste(names(dat)[27], "mucosa", sep=" ")
colnames(dat)[27] <- col_names
col_names <- paste(names(dat)[25], "mucosa", sep=" ")
colnames(dat)[25] <- col_names
col_names <- paste(names(dat)[23], "mucosa", sep=" ")
colnames(dat)[23] <- col_names
col_names <- paste(names(dat)[22], "non", sep=" ")
colnames(dat)[22] <- col_names
col_names <- paste(names(dat)[24], "non", sep=" ")
colnames(dat)[24] <- col_names
col_names <- paste(names(dat)[26], "non", sep=" ")
colnames(dat)[26] <- col_names
col_names <- paste(names(dat)[28], "non", sep=" ")
colnames(dat)[28] <- col_names
col_names <- paste(names(dat)[31], "non", sep=" ")
colnames(dat)[31] <- col_names
col_names <- paste(names(dat)[33], "non", sep=" ")
colnames(dat)[33] <- col_names
col_names <- paste(names(dat)[35], "non", sep=" ")
colnames(dat)[35] <- col_names
##outlier(s) identification##
#Average correlation plot
library(gplots)
dat.cor <- cor(dat,use="pairwise.complete.obs", method="pearson")
dat.avg <- apply(dat.cor,1,mean)
par(oma=c(3,0.1,0.1,0.1))
plot(c(1,length(dat.avg)),range(dat.avg),type="n",xlab="",ylab="Avg r",main="Average correlation of Normal/IBD samples",axes=F)
points(dat.avg,bg="red",col=1,pch=21,cex=1.25)
axis(1,at=c(1:length(dat.avg)),labels=dimnames(dat)[[2]],las=2,cex.lab=0.4,cex.axis=0.6)
axis(2)
abline(v=seq(0.5,62.5,1),col="grey")
##Remove Outliers (avg r below 0.95)##
dat$`GSM948591 mucosa`<- NULL
##filter genes with low expression values avg gene expression < 10##
av<- rowMeans(dat, na.rm = FALSE, dims = 1)
filt <- function(X) {X[ ifelse(X>14, TRUE,FALSE)]}
avf<-filt(av)
avf<-filt(av)[1:128]  #this removes the last NA
avf<- as.data.frame(avf)
fdat <- subset(dat, rownames(dat) %in% rownames(avf))
##two-sample t-test##
fdat<- fdat[,c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,19,20,21,22,24,26,28,31,33,35,23,25,27,29,30,32,34,36,37,38,39,40,41,42)]
normal<-names(dat[1:13])
remission<-names(dat[14:21])
nonmucosa<-names(dat[22:28])
mucosa<-names(dat[29:42])
aov.all.genes <- function(x,s1,s2,s3,s4) {
  x1 <- as.numeric(x[s1])
  x2 <- as.numeric(x[s2])
  x3 <- as.numeric(x[s3])
  x4 <- as.numeric(x[s4])
  fac <- c(rep("A",length(x1)), rep("B",length(x2)), rep("C",length(x3)), rep("D",length(x4)))
  a.dat <- data.frame(as.factor(fac),c(x1,x2,x3,x4))
  names(a.dat) <- c("factor","express")
  p.out <- summary(aov(express~factor, a.dat))[[1]][1,5]
  return(p.out)
}
aov.run <- apply(fdat,1, aov.all.genes,s1=normal,s2=remission,s3=nonmucosa, s4=mucosa)
##genes retains with a p-value < 0.05##
length(which(aov.run < 0.01))
##histogram##
hist(aov.run,breaks=100,col="lightblue",xlab="p-values",main="P-value dist’n between\nNormal and IBD samples",cex.main=0.9)
abline(v=.01,col=2,lwd=2)
##hieracal clustering##
pv<-as.data.frame(aov.run)
pvf<- subset(pv, pv < 0.01)
fdat <- subset(fdat, rownames(fdat) %in% rownames(pvf))
dat.selected<-fdat[,sample(ncol(fdat), replace= FALSE) ]
plot(hclust(dist(dat.selected, method="manhattan"), method="median"),main="hierarchical clustering of IBD/Normal samples \n using manhattan distance metric and median linkage method")
heatmap(t(dat.selected), main="hierarchical clustering of IBD dataset")
##PCA##
dat.pca <- prcomp(t(fdat),cor=F)
dat.loadings <- dat.pca$x[,1:3]
plot(range(dat.loadings[,2]),range(dat.loadings[,2]),type="n",xlab='p1',ylab='p2',main='PCA plot of IBD data\np2 vs. p1')
points(dat.loadings[,1][grep('normal', rownames(dat.loadings))], dat.loadings[,2][grep('normal', rownames(dat.loadings))],col=1,bg='black',pch=21,cex=1.5)
points(dat.loadings[,1][grep('remission', rownames(dat.loadings))], dat.loadings[,2][grep('remission', rownames(dat.loadings))],col=1,bg='blue',pch=21,cex=1.5)
points(dat.loadings[,1][grep('non', rownames(dat.loadings))], dat.loadings[,2][grep('non', rownames(dat.loadings))],col=1,bg='orange',pch=21,cex=1.5)
points(dat.loadings[,1][grep('mucosa', rownames(dat.loadings))], dat.loadings[,2][grep('mucosa', rownames(dat.loadings))],col=1,bg='red',pch=21,cex=1.5)
legend(-2, -1.5, legend=c("normal","remission","non-mucosal","mucosal"),col=c("black","blue", "orange", "red"), lty=1:2, cex=0.7)
##classification##
library(MASS)
clas <- names(fdat)
clas[grep("normal",clas)]<-rep("normal",length(clas[grep("normal",clas)]))
clas[grep("remission",clas)]<-rep("remission",length(clas[grep("remission",clas)]))
clas[grep("mucosa",clas)]<-rep("mucosa",length(clas[grep("mucosa",clas)]))
clas[grep("non",clas)]<-rep("non",length(clas[grep("non",clas)]))
clasdx<- as.matrix(fdat)
dx <- as.data.frame(t(fdat))
dx <- data.frame(clas,dx)
trainl<-c(1:6, 14:19, 22:25, 29:32)
train <- as.data.frame(dx[trainl,])
testl<-c(1:13, 14:21, 22:28, 29:42)
test <- dx[testl,]
trainclas<- as.vector(train[,1])
sampclas<- as.vector(test[,1])
test<- test[,2:42]
all.train.lda<-lda(trainclas~.,train[2:20])
all.test.pre <- predict(all.train.lda,test)
all.tg<- table(all.test.pre$class,sampclas)
plot(all.test.pre$x,bg=as.numeric(factor(all.test.pre$class)),pch=c(21,22,23,24)[all.test.pre$class],col=1,ylab="Discriminant function",xlab="Score",axes= F,main="Discriminant function for IBD dataset\n based on all genes in the dataset")
axis(1, all.test.pre$x[,1] ,labels=sampclas,las=2,cex.axis=0.7)
axis(2)
legend(-11,6.5,legend=levels(all.test.pre$class),pch=c(21,22,23,24),title="Predicted class")
##upregulated vs. downregulated genes##
##12/16, I need to head to work tmr. Will deal with this later##
##get F-statistic
aov.all.genes <- function(x,s1,s2,s3,s4) {
  x1 <- as.numeric(x[s1])
  x2 <- as.numeric(x[s2])
  x3 <- as.numeric(x[s3])
  x4 <- as.numeric(x[s4])
  fac <- c(rep("A",length(x1)), rep("B",length(x2)), rep("C",length(x3)), rep("D",length(x4)))
  a.dat <- data.frame(as.factor(fac),c(x1,x2,x3,x4))
  names(a.dat) <- c("factor","express")
  p.out <- summary(aov(express~factor, a.dat))[[1]][1,4]
  return(p.out)
}
aov.run <- apply(fdat,1, aov.all.genes,s1=normal,s2=remission,s3=nonmucosa, s4=mucosa)
A<- as.numeric(aov.run) 
tstat<- t.test(A)
tstat95<- tstat$conf.int[1]
aov<- as.data.frame(aov.run)
daov<- subset(aov, aov$aov.run < tstat95)
uaov<- subset(aov, aov$aov.run > tstat95)
library(limma)
fit<- lmFit(fdat)
ebaye<- eBayes(fit)
evpv<- ebaye$p.value 
evpv<- as.table(ebaye$p.value)
sevpv<- evpv[order(evpv),]
d<- length(daov[[1]])
u<- length(uaov[[1]])
fed<- as.data.frame(sevpv[1:d])
feu<- as.data.frame(sevpv[1:u])
ind<- intersect(rownames(daov), rownames(fed))
inu<- intersect(rownames(uaov), rownames(feu))
ug<- subset(aov, rownames(aov) %in% inu)
dg<- subset(aov, rownames(aov) %in% ind)
