import random
import datetime
import time
import pandas as pd
from dataclasses import dataclass
import math

@dataclass
class Passport:
    surname:str
    name: str
    patronymic:str
    series:str|int
    number:str|int
    birthday:datetime.date
    issueDate: datetime.date
    gender: str
    codeDep: str
    birthplace: str| None =None
    dep: str|None = None
    def __str__(self) -> str:
        tem=self.surname+" "+self.name+" "+self.patronymic+" Серия:"+str(self.series)+" Номер:"+str(self.number)+" Дата рождения: "+\
            str(self.birthday)+" дата выпуска:"+str(self.issueDate)+" пол:" +self.gender+" код:"+self.codeDep+" выдан:"+str(self.dep)+\
            " место рождения:"+str(self.birthplace)
        return tem

digits =["0","1","2","3","4","5","6","7","8","9"]

def genIssueDate():
    start = datetime.date(2011, 7, 1)
    end = datetime.date.today()
    return start + (end - start) * random.random()

def genBirthday(issueDate):
    start = datetime.date(1943, 1, 1)
    end = issueDate-datetime.timedelta(days=14*365)
    return start + (end - start) * random.random()

def genSeries(issueDate:datetime.date,dep):
    res=""
    if issueDate.month<4:
        res=f"{dep['ОКАТО']}{issueDate.year%100-1}"
    else:
        res=f"{dep['ОКАТО']}{issueDate.year%100}"
    return res

def genNumber():
    number=""
    for _ in range(6):
        number+=random.choice(digits)
    return number


def generateData(n=None,batch=False)->Passport|list[Passport]:
    ''''''
    surnames = pd.read_json("data/surnames.json")
    surnamesMale=surnames.loc[surnames['gender'].isin(["m","u"])]
    surnamesFemale=surnames.loc[surnames['gender'].isin(["f","u"])]
    surnamesMale["count"] = surnamesMale["count"]/surnamesMale["count"].sum()
    surnamesFemale["count"] = surnamesFemale["count"]/surnamesFemale["count"].sum()
    mSurnameProb = surnamesMale["count"].to_list()
    fSurnameProb = surnamesFemale["count"].to_list()
    maleSurnames=surnamesMale["text"].to_list()
    femaleSurnames=surnamesFemale["text"].to_list()

    midnames = pd.read_json("data/midnames.json")
    midnamesMale=midnames.loc[midnames['gender'].isin(["m","u"])]
    midnamesFemale=midnames.loc[midnames['gender'].isin(["f","u"])]
    midnamesMale["count"] = midnamesMale["count"]/midnamesMale["count"].sum()
    midnamesFemale["count"] = midnamesFemale["count"]/midnamesFemale["count"].sum()
    mMidnameProb = midnamesMale["count"].to_list()
    fMidnameProb = midnamesFemale["count"].to_list()
    maleMidnames=midnamesMale["text"].to_list()
    femaleMidnames=midnamesFemale["text"].to_list()

    names = pd.read_json("data/names.json")
    namesMale=names.loc[names['gender'].isin(["m","u"])]
    namesFemale=names.loc[names['gender'].isin(["f","u"])]
    namesMale["count"] = namesMale["count"]/(namesMale["count"].sum())
    namesFemale["count"] = namesFemale["count"]/(namesFemale["count"].sum())
    mNameProb = namesMale["count"].to_list()
    fNameProb = namesFemale["count"].to_list()
    maleNames=namesMale["text"].to_list()
    femaleNames=namesFemale["text"].to_list()
    deps = pd.read_csv("fmsData/regions.csv",sep=";", dtype=str)
    codes = pd.read_csv("fmsData/fms_unit_normalized.csv", dtype=str)
    if n ==None:
        gender = random.choice(["M","F"])
        if gender =="F":
            surname = random.choices(femaleSurnames,fSurnameProb)[0]
            name = random.choices(femaleNames,fNameProb)[0]
            midname = random.choices(femaleMidnames,fMidnameProb)[0]
        else:
            surname = random.choices(maleSurnames,mSurnameProb)[0]
            name = random.choices(maleNames,mNameProb)[0]
            midname = random.choices(maleMidnames,mMidnameProb)[0]
        issueDate = genIssueDate()
        birthday = genBirthday(issueDate)
        dep = deps.sample(1).to_dict(orient="records")[0] # Выбранный
        series= genSeries(issueDate,dep)
        dfNeededCode = codes[codes["code"].str.match(f'{str(dep["ГИБДД"])}')]
        neededCode = dfNeededCode.code.to_list()
        selCode = random.choice(neededCode)
        number = genNumber()
        return Passport(surname,name,midname, series, number,birthday,issueDate,gender,selCode)
    else:
        res=[]
        start=time.time()
        batchSize = 1000
        if n>batchSize and batch==True:
            batchNum = math.ceil(n/batchSize)
            dep=dep = deps.sample(n,replace=True).to_dict(orient="records")
            for i in range(batchNum):
                print(f"Batch № {i+1} started")
                gender = random.choice(["M","F"])
                if gender =="F":
                    surname = random.choices(femaleSurnames,fSurnameProb,k=batchSize)
                    name = random.choices(femaleNames,fNameProb,k=batchSize)
                    midname = random.choices(femaleMidnames,fMidnameProb,k=batchSize)
                else:
                    surname = random.choices(maleSurnames,mSurnameProb,k=batchSize)
                    name = random.choices(maleNames,mNameProb,k=batchSize)
                    midname = random.choices(maleMidnames,mMidnameProb,k=batchSize)
                for j in range(batchSize):
                    issueDate = genIssueDate()
                    birthday = genBirthday(issueDate)
                    # dep = deps.sample(1).to_dict(orient="records")[0]
                    series= genSeries(issueDate,dep[i*batchSize+j])
                    dfNeededCode = codes[codes["code"].str.match(f'{str(dep[i*batchSize+j]["ГИБДД"])}')]
                    neededCode = dfNeededCode.code.to_list()
                    selCode = random.choice(neededCode)
                    number = genNumber()
                    passport= Passport(surname[j],name[j],midname[j], series, number,birthday,issueDate,gender,selCode)
                    res.append(passport)
                    print(f"{i} out of {n},elapsed time={time.time()-start}",flush=True,end="\r")
                    if i*batchSize+j+1==n:
                        print("broken")
                        break
        else:
            for i in range(n):
                gender = random.choice(["M","F"])
                if gender =="F":
                    surname = random.choices(femaleSurnames,fSurnameProb)[0]
                    name = random.choices(femaleNames,fNameProb)[0]
                    midname = random.choices(femaleMidnames,fMidnameProb)[0]
                else:
                    surname = random.choices(maleSurnames,mSurnameProb)[0]
                    name = random.choices(maleNames,mNameProb)[0]
                    midname = random.choices(maleMidnames,mMidnameProb)[0]
                issueDate = genIssueDate()
                birthday = genBirthday(issueDate)
                dep = deps.sample(1).to_dict(orient="records")[0]
                series= genSeries(issueDate,dep)
                dfNeededCode = codes[codes["code"].str.match(f'{str(dep["ГИБДД"])}')]
                neededCode = dfNeededCode.code.to_list()
                selCode = random.choice(neededCode)
                number = genNumber()
                passport= Passport(surname,name,midname, series, number,birthday,issueDate,gender,selCode)
                res.append(passport)
                
                print(f"{i} out of {n},elapsed time={time.time()-start}",flush=True,end="\r")
        return res