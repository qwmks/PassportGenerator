import datetime
import re
import pandas as pd
codes = pd.read_csv("fmsData/fms_unit_normalized.csv", dtype=str)

names=pd.read_json(f"data/names.json")["text"].to_list()
surnames=pd.read_json(f"data/surnames.json")["text"].to_list()
patrs=pd.read_json(f"data/midnames.json")["text"].to_list()

ru2En = {
    "А": "A",
    "Б": "B",
    "В": "V",
    "Г": "G",
    "Д": "D",
    "Е": "E",
    "Ё": "2",
    "Ж": "J",
    "З": "Z",
    "И": "I",
    "Й": "Q",
    "К": "K",
    "Л": "L",
    "М": "M",
    "Н": "N",
    "О": "O",
    "П": "P",
    "Р": "R",
    "С": "S",
    "Т": "T",
    "У": "U",
    "Ф": "F",
    "Х": "H",
    "Ц": "C",
    "Ч": "3",
    "Ш": "4",
    "Щ": "W",
    "Ъ": "X",
    "Ы": "Y",
    "Ь": "9",
    "Э": "6",
    "Ю": "7",
    "Я": "8",
    " ": " ",
    "-": "-",
    "<": "<",
}

en2Ru = {
    "A": "А",
    "B": "Б",
    "V": "В",
    "G": "Г",
    "D": "Д",
    "E": "Е",
    "2": "Ё",
    "J": "Ж",
    "Z": "З",
    "I": "И",
    "Q": "Й",
    "K": "К",
    "L": "Л",
    "M": "М",
    "N": "Н",
    "O": "О",
    "P": "П",
    "R": "Р",
    "S": "С",
    "T": "Т",
    "U": "У",
    "F": "Ф",
    "H": "Х",
    "C": "Ц",
    "3": "Ч",
    "4": "Ш",
    "W": "Щ",
    "X": "Ъ",
    "Y": "Ы",
    "9": "Ь",
    "6": "Э",
    "7": "Ю",
    "8": "Я",
    " ": " ",
    "-": "-",
    "<": "<",
}

okato2const ={'79': '01',
 '84': '04',
 '80': '02',
 '81': '03',
 '82': '05',
 '26': '06',
 '83': '07',
 '85': '08',
 '91': '09',
 '86': '10',
 '87': '11',
 '88': '12',
 '89': '13',
 '98': '14',
 '90': '15',
 '92': '16',
 '93': '17',
 '94': '18',
 '95': '19',
 '96': '20',
 '97': '21',
 '01': '22',
 '76': '75',
 '30': '41',
 '03': '23',
 '04': '24',
 '57': '59',
 '05': '25',
 '07': '26',
 '08': '27',
 '10': '28',
 '11': '29',
 '12': '30',
 '14': '31',
 '15': '32',
 '17': '33',
 '18': '34',
 '19': '35',
 '20': '36',
 '24': '37',
 '25': '38',
 '27': '39',
 '29': '40',
 '32': '42',
 '33': '43',
 '34': '44',
 '37': '45',
 '38': '46',
 '41': '47',
 '42': '48',
 '44': '49',
 '46': '50',
 '47': '51',
 '22': '52',
 '49': '53',
 '50': '54',
 '52': '55',
 '53': '56',
 '54': '57',
 '56': '58',
 '58': '60',
 '60': '61',
 '61': '62',
 '36': '63',
 '63': '64',
 '64': '65',
 '65': '66',
 '66': '67',
 '68': '68',
 '28': '69',
 '69': '70',
 '70': '71',
 '71': '72',
 '73': '73',
 '75': '74',
 '78': '76',
 '45': '77',
 '40': '78',
 '99': '79',
 '55': '83',
 '67': '86',
 '77': '87',
 '74': '89'
}

const2okato={'01': '79',
 '04': '84',
 '02': '80',
 '03': '81',
 '05': '82',
 '06': '26',
 '07': '83',
 '08': '85',
 '09': '91',
 '10': '86',
 '11': '87',
 '12': '88',
 '13': '89',
 '14': '98',
 '15': '90',
 '16': '92',
 '17': '93',
 '18': '94',
 '19': '95',
 '20': '96',
 '21': '97',
 '22': '01',
 '75': '76',
 '41': '30',
 '23': '03',
 '24': '04',
 '59': '57',
 '25': '05',
 '26': '07',
 '27': '08',
 '28': '10',
 '29': '11',
 '30': '12',
 '31': '14',
 '32': '15',
 '33': '17',
 '34': '18',
 '35': '19',
 '36': '20',
 '37': '24',
 '38': '25',
 '39': '27',
 '40': '29',
 '42': '32',
 '43': '33',
 '44': '34',
 '45': '37',
 '46': '38',
 '47': '41',
 '48': '42',
 '49': '44',
 '50': '46',
 '51': '47',
 '52': '22',
 '53': '49',
 '54': '50',
 '55': '52',
 '56': '53',
 '57': '54',
 '58': '56',
 '60': '58',
 '61': '60',
 '62': '61',
 '63': '36',
 '64': '63',
 '65': '64',
 '66': '65',
 '67': '66',
 '68': '68',
 '69': '28',
 '70': '69',
 '71': '70',
 '72': '71',
 '73': '73',
 '74': '75',
 '76': '78',
 '77': '45',
 '78': '40',
 '79': '99',
 '83': '55',
 '86': '67',
 '87': '77',
 '89': '74'
 }


def latinize(string: str):
    res = [ru2En[el] for el in string.upper()]
    return "".join(res)
def delatinize(string: str):
    res = [en2Ru[el] for el in string.upper()]
    return "".join(res)

def check(input: str,len:int=0, final: bool = False) -> int:
    res = 0
    for i, el in enumerate(input):
        if i % 3 == 0:
            res += int(el) * 7
        elif i % 3 == 1:
            res += int(el) * 3
        elif final:
            res += int(el) * 7
        else:
            res += int(el)
    return res % 10


def dateToString(date: datetime.date):
    month = ("0" + str(date.month))[-2:]
    day = ("0" + str(date.day))[-2:]
    string = f"{str(date.year)[2:]}{month}{day}"
    return string


def formMRZ(surname: str,name: str,patronymic: str,serie: str | int,number: str | int,birthday: datetime.date,gender: str,issueDate: datetime.date,departament: str | int,) -> tuple[str, str]:
    '''Returns first and second lines in Russian National Passport implementation of MRZ,according to personal data provided'''
    topConst = "PNRUS"
    surname = re.sub("[-, ]", "<", surname)
    name = re.sub("[-, ]", "<", name)
    patronymic = re.sub("[-, ]", "<", patronymic)
    person = handleLong(surname, name, patronymic)
    topRow = topConst + person
    serieNumber = str(serie)[:-1] + str(number)
    birthdayMRZ = dateToString(birthday)
    issueMRZ = dateToString(issueDate)
    lastPart = f"{str(serie)[-1]}{issueMRZ}{departament}"
    print(lastPart)
    checkSum1, checkSum2, checkSum3, finalCheckSum = checkAll(
        [serieNumber, birthdayMRZ, lastPart]
    )
    bottomRow = f"{serieNumber}{checkSum1}RUS{birthdayMRZ}{checkSum2}{gender}<<<<<<<{lastPart}<{checkSum3}{finalCheckSum}"
    return topRow, bottomRow

def handleLong(surname, name, patronymic):
    person = ""
    if len(surname) + len(name) + len(patronymic) > 36:
        if len(surname) > 34:
            person = f"{surname[:34]}<<{name[0]}<{patronymic[0]}"
        elif len(surname) + len(name) >= 36:
            lim = 37 - 2 - len(surname)
            person = f"{surname}<<{name[:lim]}<{patronymic[0]}"
        elif len(surname) + len(name) <= 35:
            limPatr = 39 - 2 - 1 - (len(surname) + len(name))
            person = f"{surname}<<{name}<{patronymic[:limPatr]}"
    elif len(surname) + len(name) + len(patronymic) == 36:
        person = f"{surname}<<{name}<{patronymic}"
    else:
        person = f"{surname}<<{name}<{patronymic}" + "<" * (
            36 - (len(surname) + len(name) + len(patronymic))
        )
        
    return person

def validateDate(date:str,dateType="выдачи"):
    if not re.match(r"\d{6}",date):
        print("Неверный формат даты")
        return "010101"
    else:
        errors=[]
        if not re.match(r"\d{2}",date[:2]):
            newDate="01"
            errors.append("неверный год")
        else:
            newDate=date[:2]
        if int(date[2:4])>12 or int(date[2:4])<1:
            newDate+="01"
            errors.append("неверный месяц")
        else:
            newDate+=date[2:4]
        if int(date[4:6])>31 or int(date[2:4])<1:
            newDate+="01"
            errors.append("неверный день")
        elif int(date[4:6])==31 and int(newDate[2:4]) not in [1,3,5,7,8,10,12]:
            newDate+="01"
            errors.append("неверный день")
        elif (int(date[4:6])==30 or (int(date[4:6])==29 and int(date[2:4])%4!=0)) and int(newDate[2:4])==2:
            newDate+="01"
            errors.append("неверный день")
        else:
            
            newDate+=date[4:6]
        errors = ", ".join(errors)
        if len(errors)>0:
            print(f"В дате {dateType} {errors}.")
        return date

def checkAllDebug(data: list[str]):
    checkSum1 = check(data[0])
    print(f"{checkSum1=}")
    checkSum2 = check(data[1])
    print(f"{checkSum2=}")
    checkSum3 = check(data[2])
    print(f"{checkSum3=}")
    # final=check(str(test1)+str(test2)+str(test3),True)
    finalCheckSum = check(
        data[0]
        + str(checkSum1)
        + data[1]
        + str(checkSum2)
        + "0000000"
        + data[2]
        + "0"
        + str(checkSum3)
    )
    print(f"{finalCheckSum=}")
    return checkSum1, checkSum2, checkSum3, finalCheckSum


def checkAll(data: list[str]):
    checkSum1 = check(data[0],9)
    checkSum2 = check(data[1],6)
    checkSum3 = check(data[2],13)
    finalCheckSum = check(
        data[0]
        + str(checkSum1)
        + data[1]
        + str(checkSum2)
        + "0000000"
        + data[2]
        + "0"
        + str(checkSum3),
        39
    )
    return checkSum1, checkSum2, checkSum3, finalCheckSum