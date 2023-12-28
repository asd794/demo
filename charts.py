import requests

# 取得Token
def get_access_token():
    #API網址    
    url = "https://account.kkbox.com/oauth2/token" 
    
    #標頭
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "account.kkbox.com"
    }
    #參數
    data = {
        "grant_type": "client_credentials",
        "client_id": "7b735d26dcd962288a61da69eb140b6d",
        "client_secret": "7c7236be4af999c313a6460e9228b3ab"
    }
    access_token = requests.post(url, headers=headers, data=data)
    # print(headers["Host"],data["grant_type"])
    # print(access_token.text)
    # print(access_token.json()["access_token"])
    return access_token.json()['access_token']

# 取得列表
def get_charts():
    # 呼叫方法 get_access_tocken 獲取tocken
    access_token = get_access_token()
    
    #取得音樂排行榜列表API網址
    url = "https://api.kkbox.com/v1.1/charts"
    #標頭
    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + access_token  #帶著存取憑證
    }
    #參數
    params = {
        "territory": "TW"  #台灣領域  
    }
    response = requests.get(url, headers=headers, params=params)
    result = response.json()["data"]
    print(result[0]['id'],result[0]['title'])
    for i in result:
        print(i['id'],i['title'])
get_charts()

