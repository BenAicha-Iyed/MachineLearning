import pandas as pd
from math import log2

class valueInfo:
    def __init__(self,key):
        self.info={}
        self.card=0
        self.value=key
        self.entropie=0
    def increment(self,key):
        if key in self.info:
            self.info[key] +=1
        else :
            self.info[key]=1
        self.card +=1
    def __eq__(self, other):
        if isinstance(other,valueInfo):
            return self.value==other.value
        return False
    def calculEntropie(self):
        self.entropie= -sum([(v/self.card)*log2(v/self.card) for v in self.info.values()])
    def __repr__(self):
        return self.value

class itemInfo:
    def __init__(self,key=""):
        self.item=key
        self.info=[]
        self.entropie=0
    def __eq__(self, other):
        if isinstance(other,itemInfo):
            return self.item==other.item
        return False
    def __len__(self):
        return len(self.info)
    def update(self,val,out):
        value=valueInfo(val)
        idValue=len(self)
        try:
            idValue=self.info.index(value)
        except:
            self.info.append(value)
        self.info[idValue].increment(out)
    def calculEntropie(self):
        n=0
        for v in self.info:
            n+=v.card
            v.calculEntropie()
            self.entropie+=v.entropie * v.card
        self.entropie/=n
        # return self.entropie
    def __lt__(self, other):
        if isinstance(other,itemInfo):
            return self.entropie<=other.entropie
        return False
    def createInfo(self,X,output):
        for i in range(len(X)):
            self.update(X[i],output[i])
    def __str__(self):
        return self.item
    def __contains__(self, item):
        return valueInfo(item) in self.info

class decision:
    def __init__(self, df):
        print("Choose the alternative output:")
        while(True):
            self.output=input(list(df.columns))
            if self.output in df.columns:
                break
        self.items=[]
    def createItems(self,df):
        for col in df.columns:
            if col !=self.output:
                item=itemInfo(col)
                item.createInfo(df[col],df[self.output])
                item.calculEntropie()
                self.items.append(item)
    def root(self):
        return min(self.items)
    def getChoise(self,root):
        while (True):
            print(root, "\nPrint the alternative answer: ")
            ans = input(' | '.join([str(v) for v in root.info])+': ')
            if ans in root:
                return ans
    def newDataFrame(self,df,root,ans):
        mask = (df[root.item]!=ans)
        data = df[~mask]
        data.index=range(len(data))
        return data.drop([root.item], axis=1)
    def makeDecision(self,df):
        TTL=0
        while(len(set(df[self.output]))>1):
            TTL+=1
            self.createItems(df)
            root=self.root()
            ans=self.getChoise(root)
            df=self.newDataFrame(df,root,ans)

        return df[self.output][0]

df = pd.read_csv('TD_Machine_R/Bank.csv')
dec = decision(df)
print(dec.makeDecision(df))
