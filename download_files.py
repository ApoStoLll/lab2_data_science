import urllib.request as urllib2
import datetime
import os
import pandas as pd

def makeFile(index, year1, year2):
    a = [24,25,5,6,27,23,26,7,11,13,14,15,16,17,18,19,21,22,8,9,10,1,3,2,4]
    index = a[index-1]
    now = datetime.datetime.now()
    url = f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={index}&year1={year1}&year2={year2}&type=Mean'
    vhi_url = urllib2.urlopen(url)
    with open(f'vhi_id_{index}_{year1}_{year2}.csv', 'wb') as out:
        out.write(vhi_url.read())
        print (index, "is downloaded...")

def clear():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    filelist = [ f for f in os.listdir(BASE_DIR) if f.endswith(".csv") ]
    for f in filelist:
        os.remove(os.path.join(BASE_DIR, f))

def createAllFiles(year1, year2):
    for i in range(0,25):
        makeFile(i, year1, year2)

def getDf():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    filelist = [ f for f in os.listdir(BASE_DIR) if f.endswith(".csv") ]
    df = pd.concat([readFile(os.path.join(BASE_DIR, f)) for f in filelist], ignore_index=True)
    df = df[df.year != '</pre></tt>']
    df = df[df.VHI != -1]
    return df
    

def readFile(path):
    df = pd.read_csv(path, sep = ',', header=1)
    df.columns = ['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'i']
    index = path.split('_')[2]
    df['province'] = index
    del df['i']
    #df['week']
    return df

def choseLine(typ, df):
    if typ == 'VHI':
        del df['TCI']
        del df['VCI']
    elif typ == 'TCI':
        del df['VHI']
        del df['VCI']
    elif typ == 'VCI':
        del df['TCI']
        del df['VHI']

def week(df, fromm, to):
    df = df[(df.week <= float(to)) & (df.week >= float(fromm))]
    return df

if __name__ == "__main__":
    clear()
    createAllFiles(2000, 2020)