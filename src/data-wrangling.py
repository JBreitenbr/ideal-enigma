import pandas as pd
import warnings
warnings.filterwarnings("ignore")
afr=pd.read_csv("africa.csv")
path="API_SP.DYN.LE00.IN_DS2_en_csv_v2_107.csv"
lex0=pd.read_csv(path,skiprows=4)
pop0=pd.read_csv("API_SP.POP.TOTL_DS2_en_csv_v2_85.csv",skiprows=4)
lex0["land"]=lex0["Country Name"]
pop0["land"]=pop0["Country Name"]
cols=["land","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021"]
pcols=[]
for el in cols[1:]:
   ex="p"+el
   pcols.append(ex)
   pop0[ex]=pop0[el]
pcols=["land"]+pcols
lex=lex0[cols]
pop=pop0[pcols]
cntries=afr["land"].tolist()
mrg=pd.merge(lex,afr,on="land",how="right")
df=pd.merge(mrg,pop,on="land",how="inner")
print(df.isnull().sum())
y_c=cols[1:]
y_p=pcols[1:]
print(y_c)

def afri(dfr,region):
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
dfList=[df]
regions=["Africa"]+df["region"].unique().tolist()
for el in regions:
  dfList.append(afri(df,el))

ges=pd.concat(dfList)
for el in y_p:
  del ges[el]
del ges["land"]
del ges["prod"]
melted=pd.melt(ges,id_vars=["region","country"],value_vars=y_c)
melted["lex"]=round(melted["value"],2)
melted["year"]=melted["variable"]
del melted["value"]
del melted["variable"]

melted=melted[["region","country","year","lex"]]
sub=melted[melted["region"]==melted["country"]]
del sub["country"]
sub["lex_"]=sub["lex"]
del sub["lex"]
melted=pd.merge(melted,sub,on=["region","year"],how="right")
for i in range(len(melted)):
  if pd.isnull(melted.loc[i,"lex"]):
      melted.loc[i,"lex"]=melted.loc[i,"lex_"]
del melted["lex_"]
melted=melted.sort_values(by=["region","country","year"])
melted.to_csv("lex.csv",index=False)


   
  
