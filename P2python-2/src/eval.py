# import package ...
import sys
import time
import math

def calculateGain(ranking):
    XDCG={}
    gain=0
    #print("in")
    DCGForEach=[]
    for item in ranking:
        DCGForEach=[]
        index=1
        for x in ranking[item]:
            if index<2:
                DCGForEach.append(x)
            else:
                gain=x/math.log(index,2) 
                oldRel=DCGForEach[len(DCGForEach)-1]
                newRel=gain+oldRel
                DCGForEach.append(newRel)
            index=index+1
        XDCG[item]=DCGForEach
    return XDCG

def eval(runFile,qrelsFile):
    trecCollection={}
    qrelsCollection={}
    fT=open(runFile,'r')
    trecItems=fT.readlines()
    
    fQ=open(qrelsFile,'r')
    qrelsItems=fQ.readlines()
    #get TREC info
    for tItem in trecItems:
        row=tItem.split()
        qid=row[0]
        docID=row[2]
        rank=row[3]
        score=row[4]
        if row[0] not in trecCollection:
            #print(row[0])
            #print(type(row[0]))
            trecCollection[row[0]]=[]
        trecCollection[row[0]].append(row[2:])
    #get qrels info
    for qitem in qrelsItems:
        row=qitem.split()
        qid=row[0]
        docID=row[2]
        relNum=int(row[3])
        item={row[2]:relNum}
        if qid not in qrelsCollection:
            
            qrelsCollection[qid]=[]
            #print(type(qrelsCollection[qid]))
            qrelsCollection[qid].append(item)
        else:
            qrelsCollection[qid][0].update(item)

   # print(trecCollection['47210'][:20])
    #print(qrelsCollection['67316'][0])

    trecTop20={}#qid:rels
    relDocInTrec={}
    trecDocs={}
    for t in trecCollection:
        #print(t)
        rels=[]
        rels2=[]
        allDocRel=[]
        for docID in trecCollection[t][:20]:
            rel=0
            #print(docID[0])
            #print()
            if docID[0] in qrelsCollection[t][0]:
                rel=int(qrelsCollection[t][0][docID[0]])
            rels.append(rel)    
        trecTop20[t]=rels

        for docID2 in trecCollection[t]:
            #print(docID[0])
            #print()
            if docID2[0] in qrelsCollection[t][0]:
                rel2=int(qrelsCollection[t][0][docID2[0]])
                if rel2!=0:
                   rels2.append(rel2)
                
                allDocRel.append(rel2)
                   
  
        relDocInTrec[t]=rels2
        trecDocs[t]=allDocRel

    #print(trecTop20)
    print(trecDocs)

    perfectRanking={}
    queryRels={}
    for qy in qrelsCollection:
        rels=[]
        s_rels=[]
        sorted_qy=dict(sorted(qrelsCollection[qy][0].items(),key=lambda item:item[1],reverse=True)[:20])
        sorted_qy_rels=dict(sorted(qrelsCollection[qy][0].items(),key=lambda item:item[1],reverse=True))
        #print(sorted_qy)
        rels=list(sorted_qy.values())
        s_rels=list(sorted_qy_rels.values())
        #print(rels)
        perfectRanking[qy]=rels
        queryRels[qy]=s_rels

    dcg=calculateGain(trecTop20)
    idcg=calculateGain(perfectRanking)
   # print(dcg['47210'])
    #print(idcg['47210'])
    #test

    #print(dcg['47210'][19]/idcg['47210'][19])
    NDCG20={}
    finalAm={}
   
    for g in dcg:
        NDCG20[g]=round(dcg[g][19]/idcg[g][19],4)
    #print(NDCG20)
    #print(sum(NDCG20.values())/len(NDCG20.keys()))
    finalAm['all']=sum(NDCG20.values())/len(NDCG20.keys())
    
    #numRel
    #print(sorted_qy_rels)
    relDocNum={}
    #print(queryRels['1108729'])
    for q in trecCollection:
        rels=queryRels[q].index(0)
        relDocNum[q]=rels
    #print(relDocNum)

    totalRelDoc=sum(relDocNum.values())
    print(totalRelDoc)
    for qid in relDocInTrec:
        #print(len(relDocInTrec[qid]))
        relDocNum[qid]=len(relDocInTrec[qid])
    print(relDocNum)

    totalRelFound=sum(relDocNum.values())
    print(totalRelFound)


    #RR
    RR={}
    for qid in trecDocs:
        rel1=100
        rel2=100
        rel3=100
        if 1 in trecDocs[qid]:
            rel1=trecDocs[qid].index(1)
        if 2 in trecDocs[qid]:
            rel2=trecDocs[qid].index(2)
        if 3 in trecDocs[qid]:
            rel3=trecDocs[qid].index(3)

        firstR=min(rel1,rel2,rel3)+1
        rR=round(1/firstR,4)
        RR[qid]=rR

    #print(RR)

    #P@10
    P10={}
    for qid in trecDocs:
        TenDocsR=trecDocs[qid][:10]
        #print(TenDocsR)
        numOfNonRelDocs=TenDocsR.count(0)
        #print(numOfRelDocs)
        p=round((len(TenDocsR)-numOfNonRelDocs)/len(TenDocsR),4)
        P10[qid]=p

    print(P10)


    #F1




    #MPA



    #MRR













    #Recall@10





        
    


      

            











'''def calculateGain(ranking):
    XDCG={}
    gain=0
    print("in")
    DCGForEach=[]
    for item in ranking:
        DCGForEach=[]
        index=1
        for x in ranking[item]:
            if index<2:
                DCGForEach.append(x)
            else:
                gain=x/math.log(index,2)
                print(round(gain,3))
                oldRel=DCGForEach[len(DCGForEach)-1]
                newRel=round(gain+oldRel,2)
                DCGForEach.append(newRel)
            index=index+1
        XDCG[item]=DCGForEach
    return XDCG
def convertToIntegerList(array):
    nArr=[]
    for x in array:
        x=int(x)
        nArr.append(x)
    return nArr

def eval(runFile, qrelsFile):
    # Your function start here ...
    qrels=[]
    trec=[]
    trec2={}
    queryIds=[]
    f1=open(runFile,'r')
    f2=open(qrelsFile,'r')
    i=0
    linesInTrec=f1.readlines()
    linesInQ=f2.readlines()
    #print(linesInQ)
    for line in linesInTrec:
        row=[]
        row=line.split()
        qID=int(row[0])
        if qID not in trec2:
           trec2[qID]=[]
        trec2[qID].append(row[2:])
        trec.append(row)
        if int(row[0]) not in queryIds:
            queryIds.append(int(row[0]))
    #print(queryIds)
    #print(trec[:10])
    #print(trec2[47210][:20])
    #print(len(trec2.items()))
    qels={}
    for line in linesInQ:
        row=[]
        row=line.split()
        qID=int(row[0])
        if qID in queryIds:
          if qID not in qels:
            qels[qID]=[]
          item=row[2:]
          qels[qID].append(item)

    #print(qrels)
    #NDCG@20
    #get top20 doc relevance
    rels={}
    i=0
    relNum=[]
    for x in queryIds:
        docID=[]
        top20=trec2[x][:20]
        for y in top20:
            docID.append(y[0])       
                #print(row)
        #print(f'doc:{len(docID)}')
        rels[x]=docID 
    oldRanking={}
   
    #print(len(rels.items()))
    #print(len(qels.items()))
    for qID in rels:
        docIDS=rels[qID]
        top20Rels=[]
        #print(f'qid:{qID}')
        for d in docIDS:
            items=qels[qID]
            count=0
            for e in items:
                if d==e[0]:
                    top20Rels.append(int(e[1]))
                else:
                    count=count+1
                if count==len(items):
                    top20Rels.append(0)
        #print(f'test:{top20Rels[15]}')
        #print(f'in here:{len(top20Rels)}')
        oldRanking[qID]=top20Rels
    
    #print(oldRanking)

    perfectRanking={}

    for e in oldRanking:
        sortedRanking=sorted(oldRanking[e],reverse=True)
        perfectRanking[e]=sortedRanking
    #print(perfectRanking)
    #oldRanking={47210:[3, 2, 3, 0, 0, 1, 2, 2, 3, 0]}
    #perfectRanking={47210:[3, 3, 3, 2, 2, 2, 1, 0, 0, 0]}
    #oldRanking={47210: [3, 1, 2, 0, 0, 1, 1, 0, 3, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0]}
    #perfectRanking={47210: [3, 3, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    DCG=calculateGain(oldRanking)
    IDCG=calculateGain(perfectRanking)
    
    print(f'orginalRanking:{oldRanking}')
    print(f'DCG:{DCG}')
    print('\n')
    print(f'perfectRanking:{perfectRanking}')
    print(f'IDCG:{IDCG}')
    print('\n')
    NDCG_20={}
    print(IDCG[940548])
    for x in DCG:
        itemDCG=DCG[x]
        
        itemIDCG=IDCG[x]
        if itemIDCG[19]==0:
            print("yes")
            print(x)
        itemNDGC=round(itemDCG[19]/itemIDCG[19],3)
        print(f'NDCG@20=DCG@20/IDCG@20={itemNDGC}')'''
        
    
        

                
                








        
                    
                    
                   
        
    
            
            





    




if __name__ == '__main__':
    argv_len = len(sys.argv)
    #runFile = sys.argv[1] if argv_len >= 2 else "msmarcosmall-bm25.trecrun"
    #qrelsFile = sys.argv[2] if argv_len >= 3 else "msmarco.qrels"
    #outputFile = sys.argv[3] if argv_len >= 4 else "my-msmarcosmall-bm25.eval"
    runFile='msmarcosmall-ql.trecrun'
    qrelsFile='msmarco.qrels'
    eval(runFile,qrelsFile)
    #eval(runFile, qrelsFile, outputFile)
    # Feel free to change anything here ...
