import pandas as pd
import warnings
warnings.filterwarnings("ignore")
pathDict={"life_expectancy":...}
def regional(dfr,region):
    y_dict={}
    if region=="Africa":
      df=dfr
    else:
      df=dfr[dfr["region"]==region]
    for i in range(len(y_c)):
      df["prod"]=df[y_c[i]]*df[y_p[i]]
      plst=df["prod"].tolist()
      pcol=df[y_p[i]].tolist()
      sn=0
      for el in plst:
         if el>0:
            sn+=el
      y_dict[y_c[i]]=sn/sum(pcol)
      l=pd.DataFrame(y_dict,index=[region])
      l["region"]=region
      l["country"]=region
   return l

def create_dim(dim):
    afr=pd.read_csv("africa.csv")
    path=pathDict[dim]
    dim0=pd.read_csv(path,skiprows=4)
    pop0=pd.read_csv("API_SP.POP.TOTL_DS2_en_csv_v2_85.csv",skiprows=4)
    dim0["land"]=dim0["Country Name"]
    pop0["land"]=pop0["Country Name"]
    cols=["land","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021"]
    pcols=[]
    for el in cols[1:]:
       ex="p"+el
       pcols.append(ex)
       pop0[ex]=pop0[el]
    pcols=["land"]+pcols
    dim=dim0[cols]
    pop=pop0[pcols]
    cntries=afr["land"].tolist()
    mrg=pd.merge(dim,afr,on="land",how="right")
    df=pd.merge(mrg,pop,on="land",how="inner")
    print(df.isnull().sum())
    y_c=cols[1:]
    y_p=pcols[1:]
    print(y_c)
    dfList=[df]
    regions=["Africa"]+df["region"].unique().tolist()
    for el in regions:
      dfList.append(regional(df,el))
    ges=pd.concat(dfList)
    for el in y_p:
      del ges[el]
    del ges["land"]
    del ges["prod"]
    melted=pd.melt(ges,id_vars=["region","country"],value_vars=y_c)
    melted[dim]=round(melted["value"],2)
    melted["year"]=melted["variable"]
    del melted["value"]
    del melted["variable"]
    melted=melted[["region","country","year","lex"]]
    sub=melted[melted["region"]==melted["country"]]
    del sub["country"]
    hlp=dim+"_"
    sub[hlp]=sub[dim]
    del sub[dim]
    melted=pd.merge(melted,sub,on=["region","year"],how="right")
    for i in range(len(melted)):
      if pd.isnull(melted.loc[i,dim]):
         melted.loc[i,dim]=melted.loc[i,hlp]
    del melted[hlp]
    melted=melted.sort_values(by=["region","country","year"])
    # melted.to_csv("lex.csv",index=False)
    return melted


   
  
