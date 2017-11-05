import requests
import json

headers = {'Accept': 'application/json, text/plain, */*',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive', 'Host': 'www.indiegogo.com',
           'If-None-Match': 'W/"fa7571dc6b68ed2ad6b530ca10a18ef3"',
           'Referer': 'https://www.indiegogo.com/explore/home',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
            'Cookie':'ki_t=1482987544992%3B1487728858942%3B1487729104639%3B4%3B16; ki_r=; D_SID=113.104.195.55:YisvIcHF4Z24s3TB2TKbitxWEwrmGlyymljvxklDswE; __ar_v4=MNA52ZMPS5A5HHGLKMZP3O%3A20170602%3A3%7CZIENZZYANBHC5MQ4WYNKZI%3A20170602%3A3%7C6RP73TXU3VCT7KLJC3P7EZ%3A20170602%3A3; __stripe_mid=35ce441a-7019-4221-b482-b0cba67f7fd4; romref=sch-baid; romref_referer_host=www.baidu.com; D_IID=02B91A75-51CD-3F94-A882-07B72A5961C2; D_UID=8506F25A-0F30-31AC-81E7-2864983C64A4; D_ZID=FDDDFB6A-67FA-340D-9C89-564B5A0B9899; D_ZUID=5D0201DE-2FF3-3A22-AD4E-8F28FE310CF0; D_HID=2FCF09D9-15AF-3626-BC88-5C189ABE314C; _ga=GA1.2.378922805.1482987529; _gid=GA1.2.772188293.1496800270; _ceg.s=or7ggq; _ceg.u=or7ggq; __hstc=223492548.37066d182471c31df2df71226efcf1aa.1482987568028.1496806912327.1496885823487.12; __hssrc=1; __hssc=223492548.1.1496885823487; hubspotutk=37066d182471c31df2df71226efcf1aa; locale=en; cohort=www.baidu.com%7Csch-baid%7Cshr-pica%7Csch-baid%7Cshr-pica%7Csch-baid; visitor_id=bba58762b2348bf353961ae7353f1e7ab5ff697484ba0a55993771e32402d354; analytics_session_id=2cab9c7316a54d91e73058b25c9e12748d7b3fda0ea06d63e02fb536b212e3d6; recent_project_ids=2001745%262132365%262115568%262107867%261905844%261637253%262115621%261931378%262063864%261787929%262024430%261978687%261993728%262016897%262023232%261994449%262017684%262022194%261319420%261625355; _session_id=742dc34425f25f0f10f5962f23becc4f'
           }
#获取Tech & Innovation 下的所有的产品列表
flag = 1
pg_num = 0
data = []
currency_t = {
    'USD': 1,
    'GBP': 1.3074,
    'EUR': 1.1607,
    'AUD': 0.765,
    'CAD': 0.7838,
    'CNY': 0.1507,
}

def parseProductList(productlist):
    print(productlist)
    for product in productlist:
        time_left = product['amt_time_left']
        balance = product['balance']
        currency_code = product['currency_code']
        collected_percent = product['collected_percentage']

        if time_left:
            s = time_left.split()[0]
            if s == 'No':
                product['amt_time_left'] = 0
            else:
                product['amt_time_left'] = int(s)

        if collected_percent:
            s = collected_percent[:len(collected_percent)-1]
            s = s.replace(',', '')
            product['collected_percentage'] = float(s)/100


        if balance:
            s = balance.replace(',', '')
            s = s[1:]
            s_float = float(s)
            try:
                s_float = s_float * currency_t[currency_code]
            except KeyError:
                pass

            product['balance'] = s_float

    return productlist

f = open('commu.out','w')

while flag == 1:
    pg_num = pg_num + 1
    payload = {'pg_num': pg_num}
    # r = requests.get("https://www.indiegogo.com/private_api/explore?filter_category=Tech+%26+Innovation&filter_funding=&filter_percent_funded=&filter_quick=popular_all&filter_status=&per_page=100",headers=headers,params=payload)
    # r = requests.get("https://www.indiegogo.com/private_api/explore?filter_category=Creative+Works&filter_funding=&filter_percent_funded=&filter_quick=popular_all&filter_status=&per_page=100",headers=headers,params=payload)

    r = requests.get("https://www.indiegogo.com/private_api/explore?filter_category=Community+Projects&filter_funding=&filter_percent_funded=&filter_quick=popular_all&filter_status=&per_page=100",headers=headers,params=payload)


    productlist = r.json()['campaigns']
    productlist = parseProductList(productlist)
    data += productlist

    if len(productlist) == 0:
        break

f.write(json.dumps(data))
f.close()

