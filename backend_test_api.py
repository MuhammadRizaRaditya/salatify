import requests, json
BASE='http://127.0.0.1:8000'
fails=[]
def check(name, cond, detail=""):
    print(("PASS" if cond else "FAIL"), name, detail if not cond else "")
    if not cond: fails.append(name)

r=requests.post(BASE+'/auth/register', json={'username':'apiuser','email':'api@mail.com','password':'password123'})
check('register', r.status_code==200, r.text)
r=requests.post(BASE+'/auth/register', json={'username':'apiuser','email':'api2@mail.com','password':'password123'})
check('register dup username', r.status_code==400, r.text)
r=requests.post(BASE+'/auth/login', json={'username':'apiuser','password':'password123'})
check('login', r.status_code==200, r.text)
tok=r.json()['access_token']
r=requests.post(BASE+'/auth/login', json={'username':'apiuser','password':'salah'})
check('login wrong pass', r.status_code==400, r.text)
h={'Authorization':'Bearer '+tok}
r=requests.get(BASE+'/auth/me', headers=h)
check('me', r.status_code==200 and r.json()['username']=='apiuser', r.text)
r=requests.post(BASE+'/auth/guest')
check('guest', r.status_code==200, r.text)

r=requests.get(BASE+'/doa/kategori')
check('doa kategori', r.status_code==200 and len(r.json())==14, r.text)
r=requests.get(BASE+'/doa', headers=h)
check('doa list', r.status_code==200 and len(r.json())==14, r.text)
r=requests.get(BASE+'/doa?q=makan', headers=h)
check('doa search', r.status_code==200 and len(r.json())>=1, r.text)
r=requests.get(BASE+'/doa/1', headers=h)
check('doa detail', r.status_code==200, r.text)
r=requests.post(BASE+'/doa/1/favorit', headers=h)
check('doa fav add', r.status_code==200 and r.json().get('favorit')==True, r.text)
r=requests.post(BASE+'/doa/1/favorit', headers=h)
check('doa fav remove', r.status_code==200 and r.json().get('favorit')==False, r.text)

r=requests.get(BASE+'/dzikir', headers=h)
check('dzikir list', r.status_code==200 and len(r.json())>=1, r.text)
r=requests.post(BASE+'/dzikir/riwayat', headers=h, json={'dzikir_id':1,'jumlah':33})
check('dzikir save', r.status_code==200, r.text)
r=requests.get(BASE+'/dzikir/riwayat', headers=h)
check('dzikir history', r.status_code==200 and len(r.json())>=1, r.text)

r=requests.get(BASE+'/prayer/jadwal', params={'latitude':'-6.2','longitude':'106.8','metode':'mwml'}, headers=h)
check('prayer today', r.status_code==200 and 'subuh' in r.json(), r.text)
r=requests.get(BASE+'/prayer/preferensi', headers=h)
check('prayer prefs', r.status_code==200, r.text)
r=requests.put(BASE+'/prayer/preferensi', headers=h, json={'metode':'isna','pengingat_aktif':False})
check('prayer set prefs', r.status_code==200, r.text)

r=requests.post(BASE+'/qibla/hitung', json={'latitude':-6.2,'longitude':106.8}, headers=h)
check('qibla', r.status_code==200 and 'derajat' in r.json(), r.text)

r=requests.get(BASE+'/quran/surah', headers=h)
check('quran list', r.status_code==200 and len(r.json())==10, r.text)
r=requests.get(BASE+'/quran/surah?q=fatihah', headers=h)
check('quran search', r.status_code==200 and len(r.json())==1, r.text)
r=requests.get(BASE+'/quran/surah/1', headers=h)
check('quran detail', r.status_code==200, r.text)
r=requests.post(BASE+'/quran/surah/1/favorit', headers=h)
check('quran fav add', r.status_code==200 and r.json().get('favorit')==True, r.text)

r=requests.get(BASE+'/users/settings', headers=h)
check('settings get', r.status_code==200, r.text)
r=requests.put(BASE+'/users/settings', headers=h, json={'tema_gelap':True})
check('settings put', r.status_code==200 and r.json()['tema_gelap']==True, r.text)
r=requests.put(BASE+'/users/password', headers=h, json={'old_password':'password123','new_password':'barubaru12'})
check('change password', r.status_code==200, r.text)
r=requests.post(BASE+'/auth/login', json={'username':'apiuser','password':'barubaru12'})
check('login new pass', r.status_code==200, r.text)
r=requests.post(BASE+'/auth/logout', headers={'Authorization':'Bearer '+r.json()['access_token']})
check('logout', r.status_code==200, r.text)

print()
print("TOTAL GAGAL:", len(fails), fails if fails else "semua lulus")
