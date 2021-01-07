batchGraphGen<-function(batchSize=10){
#uses dggen to generate batches of digraphs 
  source('dggenER.r')
# Factor parameters 
  # nodeFactorSet<-c(16,32,64,128)
  # LayerFactorSet<-c(4,6,8)
  # maxFanFactorSet<-c(3,4,5)
  # # orderSt<-c(25,50,75)
  # discRateFactorSet<-c(25,50,75,100)
  # percNegFactorSet<-c(0,25,50,75)
  # cpMultFactorSet<-c(1,1.5,2)
  
  nodeFactorSet<-c(16,64,128)
  LayerFactorSet<-c(4,6,8)
  maxFanFactorSet<-c(3,4)
  # orderSt<-c(25,50,75)
  discRateFactorSet<-c(25)
  percNegFactorSet<-c(25,50)
  cpMultFactorSet<-c(1)
  
  
  minDur=5
  maxDur=10
  minCf=-50
  maxCf=100
  cpMult=1
  maxCfPos=100
  minCfNeg=-50
  cfPos=1:maxCfPos
  cfNeg=minCfNeg:(-1)
  
  

# dggen graph parameters
  nNodes =8
  nLayers =2
  maxFan  =3
  edgeProb =33
  plotGraph=FALSE

  
  cpmf<-function(s,est){
    #find early start and early finish times
    eft[s]<-est[s]+d[s]
    if ((suc[[s]][1]!=0)){
      for (i in suc[[s]]){
        if (est[i] < eft[s]){
          est[i]<-eft[s]
        }
        est<-cpmf(i,est)
      }
    }
    est
  }

  actDur<-function(n){
    #returns activity duration vector
    d<-sample(minDur:maxDur,n,replace = T)
    d[1]=0
    d[n]=0
    d
  }
  
 
  
  cFVal<-function(n,negFactor){
    #returns CF vector
    negFactor<-negFactor/100
    r<-vector(length=n)
    r[1]<-0
    r[n]<-0
    for ( i in 2:(n-1)){
      if (rbinom(1,1,negFactor)){
        r[i]<-sample(cfPos,1)}
      else{
        r[i]<-sample(cfNeg,1)
      }
    }
    r  
  }    
  
  
  cpDur<-function(suc){
    #return cp duration
    #aux function
    cpmf<-function(s,est){
      #find early start and early finish times
      eft[s]<-est[s]+d[s]
      if ((suc[[s]][1]!=0)){
        for (i in suc[[s]]){
          if (est[i] < eft[s]){
            est[i]<-eft[s]
          }
          est<-cpmf(i,est)
        }
      }
      est
    }
    
    #returns cp duration
    n<-length(suc)
    est<-vector (mode="numeric",length=n)
    eft<-vector (mode="numeric",length=n)
    
    est<-cpmf(1,est)
    r<-est[n]
    r
  }
  
    
printToFile<-function(namedir,fLabel,fIndex,suc,d,cF){
  nl<-length(suc)
  
  #file name
  outFile<-paste(namedir,'/',fLabel,fIndex,'.tpf',sep="",collapse = "")
  outcon<-file(outFile,open="wt")
  
  #print first line
  est<-cpDur(suc)
  r<-c(nl,est*(1+cpMult))
  write(r,file=outcon,append=TRUE, sep = " ")
  
  #read writeand suc
  for (i in 1:nl){
    r<-c(i,length(suc[[i]]),suc[[i]])
    #print(r)
    write(r,file=outcon,append=TRUE, sep = " ",ncolumns = length(r))
  }
 
  
  for (i in 1:nl){
     r<-(c(i,d[i],cF[i]))
     write(r,file=outcon,append=TRUE, sep = "  ")
  }
  close(outcon)
}
  
#main
  tini<-proc.time()
  for (nNodes in nodeFactorSet){
    for (nlayers in LayerFactorSet){
      for(fan in maxFanFactorSet){
        for (dr in discRateFactorSet){
          for (percNeg in percNegFactorSet){
            for (cpMult in cpMultFactorSet){
              date.time <- format(Sys.time(), "%m-%d-%H-%M")
              namedir<-paste('Lotes/',date.time,'-',nNodes,'-',nlayers,'-',fan,'-',dr,'-',percNeg,'-',cpMult,sep="",collapse = "")
              print(namedir)              
              #1-create folder for batch
              dir.create(namedir,recursive = TRUE)
              
              #2-generate batch samples
              for (i in 1:batchSize){
                  g<-dggenER(nNodes=nNodes,nLayers=nlayers,maxFan=fan,edgeProb=99,nodeMult=16)
                  n<-length(g$suc)
                  d<-actDur(n)
                  cF<-cFVal(n,percNeg)
                  printToFile(namedir,fLabel='dg',fIndex=i,suc=g$suc,d,cF)
              }
          }
        }
          
      }
    }
  }
  }  
  tproc<-proc.time()-tini
  tproc
}