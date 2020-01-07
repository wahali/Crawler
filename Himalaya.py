import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.88 Safari/537.36 '
}

response = requests.get('https://fdfs.xmcdn.com/group46/M0B/92/89/wKgKj1s_E6ejVIv2AABJtaEZhqs849.m4a', headers=headers)
# print(response.status_code)
with open(' /i/ — sit 坐.m4a', 'wb') as f:
    f.write(response.content)
