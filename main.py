import base64
import asyncio
import json
from createConfig import fetch_and_decode_data, create_config
from startXray import start_core, stop_task
from getPing import testPing


async def removeRemark(url,num):

    mode = url.split('://')
    mode[0] = mode[0].lower()

    if mode[0] in ['ss', 'trojan']:
        return (f'{url.split("#")[0]}#Lighthouse:{num}')

    elif mode[0] in ['vmess', 'vless']:

        decoded_data = base64.b64decode(mode[1])
        u = json.loads(decoded_data.decode('utf-8'))
        u['ps'] = f'Lighthouse:{num}'
        u = json.dumps(u, ensure_ascii=False)
        eb = base64.b64encode(u.encode('utf-8'))
        es = eb.decode('utf-8')
        return (f'{mode[0]}://{es}')


async def main():

    file = create_config(fetch_and_decode_data())

    task = start_core()

    proxies = [
        f'http://127.0.0.1:{i}' for i in range(file['startPort'], file['lastPort']+1)]

    servers = await testPing(proxies=proxies)

    stop_task(task['pid'])
    clashFile = ''
    for i, server in enumerate(servers):
        if server['Ping'] > 0:
            clashFile += str(await removeRemark(file['serverList'][i],i))
            clashFile += '\n'

    encoded_bytes = base64.b64encode(clashFile.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')

    with open("./clashfile.txt", 'w', encoding='utf-8') as f:
        f.write(encoded_string)

if __name__ == "__main__":

    asyncio.run(main())
