import requests, json, asyncio, os
import RSO_Auth
from dotenv import load_dotenv

    # https://api.henrikdev.xyz
    # https://pd.AP.a.pvp.net/

def main():
    load_dotenv(".env")
    valorant = Client()
    valorant.get_auth(os.getenv('val_username'), os.getenv('val_password'))
    valorant.set_base_url(r"https://api.henrikdev.xyz")
    # print(data.json())
    #write_Json("content.txt", data.json())
    #write_Json("dataPlayer.txt", data.json())
    #print(len(data.json()["data"]["Offers"]))

    #print(valorant.get_player_store("BenGorr", "9398"))
    write_Json("allskinids1.txt", valorant.get_skins_content())



class Client():
    def __init__(self, base_url='', access_token='', entitlements_token=''):
        self.set_base_url(base_url)
        self.access_token = access_token
        self.entitlements_token = entitlements_token

    def get_auth(self, username, password):
        data = asyncio.get_event_loop().run_until_complete(RSO_Auth.auth(username, password))
        self.access_token, self.entitlements_token = data

    def set_base_url(self, base_url):
        if base_url == '':
            base_url = r"https://api.henrikdev.xyz"
        self.base_url = base_url.rstrip('/')

    def do(self, method, path, req=None, auth=False):
        try:
            params = json.loads(json.dumps(req))
        except Exception:
            params = None

        headers = {"Authorization": "Bearer " + self.access_token, "X-Riot-Entitlements-JWT": self.entitlements_token} if auth else None
        args = dict(params=params, headers=headers)

        url = self.base_url + path
        resp = requests.request(method, url, **args)
        if resp.status_code == 200:
            return resp
        else:
            print(resp.status_code, resp.text)

    def get_content(self):
        self.set_base_url(r"https://api.henrikdev.xyz")
        return self.do('GET', r'/valorant/v1/content')

    def get_skins_content(self):
        allSkinNames = []
        self.set_base_url(r'https://valorant-api.com/v1')
        content = self.do('GET', r'/weapons/skins').json()
        return content
        for item in content['data']:
            allSkinNames.append({'uuid': item['levels'][0]['uuid'].upper(), 'name': item['displayName'], 'img': item['displayIcon']})
        return allSkinNames

    def get_player(self, name='', tag=''):
        self.set_base_url(r"https://api.henrikdev.xyz")
        return self.do('GET', r'/valorant/v1/account/'+ f"{name}/{tag}")

    def get_store_from_id(self, id=''):
        self.set_base_url(r"https://pd.AP.a.pvp.net/")
        return self.do('GET', r'/store/v2/storefront/' + id, auth=True)

    def get_player_store(self, name, tag):
        player_id = self.get_player(name, tag).json()['data']['puuid']
        store_ids = self.get_store_from_id(player_id).json()['SkinsPanelLayout']['SingleItemOffers']
        #skins_ids = read_Json('content.txt')['skinLevels']
        skins_ids = read_Json('allskinids.txt')
        skins_name = []
        for store_id in store_ids:
            skins_name.append(next(skin for skin in skins_ids if skin['uuid'] == store_id.upper())['name'])
            # print(store_id)
            # for skin_id in skins_ids:
            #     if skin_id['uuid'] == store_id.upper():
            #         skins_name.append({'name': skin_id['name'], 'img': skin_id['img']})
        return skins_name

    def update_content(self, file):
        data = self.get_content()
        write_Json(file, data.json())

def get_skin_name():
    skins_ids = read_Json('content.txt')['skinLevels']
    id = r'2dd042e4-409e-c8ed-ec76-758529e49d99'.upper()
    print(next(item for item in skins_ids if item['id'] == id))

def write_Json(file, data):
    with open(file, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def read_Json(file):
    with open(file, 'r') as infile:
        #use try...except so we dont get error when the file is empty(it will return None if its empty)
        try:
            data = json.load(infile)
            return data
        except json.JSONDecodeError:
            pass

if __name__ == "__main__":
    # get_skin_name()
    main()
