# coding: utf-8

import re
import requests
import pandas as pd

def getHtmlText(url,timeout = 5):
    try:
        r = requests.get(
                         url= url, 
                         timeout = timeout, 
                         headers = {'User-Agent': \
                                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36'}
                         )
        r.encoding = r.apparent_encoding
        r.raise_for_status()
    except:
        print('英雄信息获取失败！ status_code：' + r.status_code)
    else:
        print('英雄信息获取成功！')
#         print(r.request.headers)
        return r.text

def transform(s_matched):
    '''
    提取爬取的英雄信息
    '''
    heroinfo_short = {
                      'name':[],
                      'hero_id':[]
                      }
    
    heroinfo_all = {
                    'hero_id':[],
                    'name':[],
                    'gold':[],
                    'info':[]
                    }
    for i, s in enumerate(s_matched):
        heroinfo_all['hero_id'].append(i)
        for name in re.split('[ ,]',s[1]):
            heroinfo_short['name'].append(name)
            heroinfo_short['hero_id'].append(i)
        
        heroinfo_all['name'].append(re.split('[ ,]',s[1])[1])
        heroinfo_all['gold'].append(color_gold[s[0]])
        heroinfo_all['info'].append(s[2].split()[-1].split('/'))
    return heroinfo_all, heroinfo_short

def getHerosInfo():
    url = 'http://lol.duowan.com/s/ydzySimulator.js?callback=ydzySimulator&_=1569139616375'
    htmlText = getHtmlText(url)

    heros_info = re.findall(r'"color": "(.+)",\r\n\t\t\t\t"name": "(.+)",\r\n\t\t\t\t"tip": "(.+)",\r\n',htmlText)

    heros_info, heros_info_short = transform(heros_info)
    return heros_info, heros_info_short

if __name__ == '__main__':
    color_gold = { 'white':1,
                   'green':2,
                   'blue':3,
                   'purple':4,
                   'gold':5}
    heros_info, heros_info_short = getHerosInfo()
    df = pd.DataFrame(heros_info)
    df.to_csv('heros_info.csv', index= None, encoding= 'utf_8_sig')
    df = pd.DataFrame(heros_info_short)
    df.to_csv('heros_info_short.csv', index= None, encoding= 'utf_8_sig')

