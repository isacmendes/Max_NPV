dggenER<-function(nNodes=8,nLayers=3,maxFan=3,edgeProb=99,nodeMult=16){
  library(igraph)
  Ns=nNodes*nodeMult
  maxFanIn=maxFan
  maxFanOut=maxFan
  nMax<-nLayers*(nLayers-1)/2
  pairs<-matrix(nrow=nMax,ncol=2)
  suc<-list()
  pre<-list()
  
  #second version based on Erdos-Reminyi
  #TODO: 1-quando parar

  iniNode<-1
  endNode<-nNodes+2
  aM<-matrix(0,nrow=endNode,ncol = endNode)
  edges<-vector(mode="numeric")
  nEdges=0
  
  combOrder<-function(n=3){
    nMax<-n*(n-1)/2
    ind<-0
    pairs<-matrix(nrow=nMax,ncol=2)
    for(i in 1:(n-1)){
      for(j in (i+1):n){
        ind<-ind+1
        pairs[ind,1]<-i
        pairs[ind,2]<-j
      }
    }
    pairs
  }
  
  fanOut<-function(){
    s<-apply(aM,1,sum)
    s
  }
  fanIn<-function(){
    p<-apply(aM,2,sum)
    p
  }
  
  fanOutNode<-function(node){
    s<-sum(aM[node,])
    s
  }
  
  fanInNode<-function(node){
    p<-sum(aM[,node])
    p
  }
  noSucs<-function(){
    s<-apply(aM,1,sum)
    noSuc<-which(s==0)
    last<-which(noSuc==endNode)
    noSuc<-noSuc[-c(1,last)]
    noSuc
  }
  
  noPreds<-function(){
    p<-apply(aM,2,sum)
    noPred<-which(p==0)
    noPred<-noPred[-1]
  }
  
  dfs<-function(nStart,nEnd){
    found<-FALSE
    if (sum(aM[nStart,])!=0){ # successors
      if (nEnd %in% which(aM[nStart,]==1)){
        found=TRUE
      } else
        for (i in which(aM[nStart,]==1)){
          if( found<-dfs(i,nEnd))
            break
        }	
    }
    found
  }
  
  partition<-function(nNodes,nLayers){
    layerComposition<-vector('list',length = nLayers)
    numberNodesLayer<-rep(1,nLayers)
    #sample nodes into layers
    for (i in 1:(nNodes-nLayers)){
      sampleLayer<-sample(1:nLayers,1,replace = T)
      numberNodesLayer[sampleLayer]<-numberNodesLayer[sampleLayer]+1
    }
    #print(numberNodesLayer)
    nodeIni=2
    for(i in 1:nLayers){
      layerComposition[[i]]<-nodeIni:(nodeIni+numberNodesLayer[i]-1)
      nodeIni<-nodeIni+numberNodesLayer[i]
    }
    r<-layerComposition
    r
  }
  
  #1-sample a partition of nNodes into nLayers
  nodesPerLayer<-partition(nNodes,nLayers)
  pairs<-combOrder(nLayers)
  #print(nodesPerLayer)
                           
  for (ns in 1:Ns){
  #-sample origin and destination layer
   s<-sample(1:nMax,1)
   oL<-pairs[s,1]
   dL<-pairs[s,2]

  #-sample Ns nodes in oL and dL
   if(length(nodesPerLayer[[oL]])>1){
      oN<-sample(nodesPerLayer[[oL]],1)
   }else{
     oN<-nodesPerLayer[[oL]]
   }
   if(length(nodesPerLayer[[dL]])>1){
      dN<-sample(nodesPerLayer[[dL]],1)
   }else{
     dN<-nodesPerLayer[[dL]]
    }
      
    if (runif (1)*100 < edgeProb){
      if((!dfs(oN,dN))&&
        (fanOutNode(oN)<maxFanOut)&&
        (fanInNode(dN)<maxFanIn)) #accept
        {
      aM[oN,dN]<-1
      edges<-c(edges,c(oN,dN))
      nEdges<-nEdges+1
    }
    }
  }
  
  #6-connect noSucs to end
  noSuc<-noSucs()
  for (i in noSuc){
    aM[i,endNode]<-1
    edges<-c(edges,c(i,endNode))
  }

  #7-connect noPreds to init
  noPred<-noPreds()
  for (i in noPred){
    aM[1,i]<-1
    edges<-c(edges,c(1,i))
  }

  #generating successor list
  for (i in 1:endNode){
    s<-which(aM[i,]==1)
    suc[[i]]<-s
  }
  suc[[endNode]]<-0
  #generating predecessor list
  for (i in 1:endNode){
    p<-which(aM[,i]==1)
    pre[[i]]<-p
  }
  pre[[1]]<-0
  
  #return
  fI<-fanIn()
  fO<-fanOut()
  #g<-make_graph(edges=edges)
  #tkplot(g,vertex.color='white')
  #r<-list(Layers=nodesPerLayer,FanIn=fI,FanOut=fO,Edges=nEdges)
  r<-list(aM=aM,edges=edges,suc=suc,pre=pre)
}  
