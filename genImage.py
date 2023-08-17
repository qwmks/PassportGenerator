import pandas as pd
import numpy as np
from PIL import Image
from trdg.generators import GeneratorFromStrings
from mrzCheck import formMRZ,latinize
from genPassportData import generateData

dir="v3"
count = 10
passports = generateData(count)
strings=[]
for passport in passports:
    print(passport)
    first,second=formMRZ(
            latinize(passport.surname),
            latinize(passport.name),
            latinize(passport.patronymic),
            passport.series,
            passport.number,
            passport.birthday,
            passport.gender,
            passport.issueDate,
            passport.codeDep,
        )
    strings.append(first)
    strings.append(second)

generator = GeneratorFromStrings(
    strings,
    count=len(strings),
    fonts=["data/ocr-b.ttf"],
    blur=1,
    character_spacing=5,
    background_type=4,
    image_dir = 'data/bg'
    # size=24,

)
i=0


mid= Image.open("data/MRZBack.jpg")
i=1
dfMrz=pd.DataFrame(columns=['Filename', 'Words'])

for img, lbl in generator:
    if lbl[0]=="P":
        first=img
        prev=lbl
    else:
        wholeImg = np.vstack([first,mid.resize(first.size),img.resize(first.size)])
        dfMrz = dfMrz.append({'Filename' : f'{i}.png', 'Words' : f"{prev}\n{lbl}",}, ignore_index = True)
        im=Image.fromarray(wholeImg)
        im.save(f'output_images/test/{i}.png')
        i+=1
dfMrz.to_csv('output_images/test/labels.csv')