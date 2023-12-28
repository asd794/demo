import http.client
import requests

def get_tocken():
    Url = 'https://account.kkbox.com/oauth2/token'
    Headers = {'Host' : 'account.kkbox.com' , 'Content-Type' : 'application/x-www-form-urlencoded'}
    Data = {'grant_type' : 'client_credentials' , 'client_id' : '7b735d26dcd962288a61da69eb140b6d' , 'client_secret' : '7c7236be4af999c313a6460e9228b3ab'}
    response = requests.post(url=Url,headers=Headers,data=Data)
    tocken = response.json()['access_token']
    # print(tocken)
    return tocken

def search_artist(keyword):
    Url = 'https://api.kkbox.com/v1.1/search?q='+keyword+'&type=track,album,artist,playlist&territory=TW'
    Headers = {'Host':'api.kkbox.com','Authorization':'Bearer '+get_tocken()}
    response=requests.get(url=Url,headers=Headers)
    result=response.json()
    # print(result)
    print(response.url)
    print(result['artists']['data'][0])
    for i in result['artists']['data']:
        print(i['name'])
# search_artist('jay') # 測試方法search_artist

# 全部排行榜
def charts():
    Url='https://api.kkbox.com/v1.1/charts?territory=TW'
    Headers={'Authorization':'Bearer '+get_tocken(),'Host':'api.kkbox.com'}
    response=requests.get(url=Url,headers=Headers)
    result=response.json()
    dic={}
    count=0
    for i in result['data']:
        array=[]
        array.append(i['id'])
        array.append(i['title'])
        # dic.setdefault(count,array)
        dic[count]=array
        count=count+1
    return dic
# print(charts()) # 測試方法charts
# charts()

# 指定ID排行榜
def a_chart_playlist(chart_id):
    Url='https://api.kkbox.com/v1.1/charts/'+chart_id+'?territory=TW'
    Headers={'accept':'application/json','Authorization':'Bearer '+get_tocken(),'Host':'api.kkbox.com'}
    response=requests.get(url=Url,headers=Headers)
    result=response.json()
    array=[]
    for i in result['tracks']['data']:
        array.append(i['name'])
    dic={result['title']:array}
    return dic
# a_chart_playlist() # 測試方法a_chart_playlist

def tracks_of_a_chart_playlist():
    Url='https://api.kkbox.com/v1.1/charts/X-6lSz-IwzDxkPuDP-/tracks?territory=TW&offset=0&limit=10' # 10筆
    Headers={ 'accept': "application/json",'authorization': "Bearer " + get_tocken(),'Host':'api.kkbox.com'}
    response=requests.get(url=Url,headers=Headers)
    result=response.json()
    for i in result['data']:
        print(i['name'])
# tracks_of_a_chart_playlist() # 測試方法tracks_of_a_chart_playlist


# 官網搜尋範例
# import http.client
# conn = http.client.HTTPSConnection("api.kkbox.com")
# headers = {
#     'accept': "application/json",
#     'authorization': "Bearer "+get_tocken()
#     }
# conn.request("GET", "/v1.1/search?q=Mayday&type=track&territory=TW&offset=0&limit=50", headers=headers)
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))