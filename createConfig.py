import json
import requests
import base64
from url2json import generateConfig


def fetch_and_decode_data(url="https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity"):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            decoded_data = base64.b64decode(response.content)
            return decoded_data.decode('utf-8').strip().split('\n')
        else:
            print(
                f"Failed to fetch data from {url}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")


def create_config(server_list: list, fileName='config.json', startPort=10000):
    startport = startPort
    default_json = {
        "log": {
            "access": "",
            "error": "",
            "loglevel": "warning"
        },
        "inbounds": [],
        "outbounds": [{
            "tag": "direct",
            "protocol": "freedom",
            "settings": {}
        },
            {
            "tag": "block",
            "protocol": "blackhole",
            "settings": {
                "response": {
                    "type": "http"
                }
            }
        }],
        "routing": {
            "domainStrategy": "IPIfNonMatch",
            "rules": []
        }
    }
    serverList = []
    for url in server_list:
        proxy = generateConfig(url)

        if proxy:

            outbound = proxy['outbounds'][0]
            outbound['tag'] = f'out{startport}'
            default_json['outbounds'].append(outbound)

            default_json['inbounds'].append({
                "tag": f'in{startport}',
                "port": startport,
                "listen": "127.0.0.1",
                "protocol": "http"
            })

            default_json['routing']['rules'].append(
                {
                    "type": "field",
                    "inboundTag": [
                        f'in{startport}'
                    ],
                    "outboundTag": f'out{startport}'
                }
            )
            serverList.append(url)
            startport += 1

    with open(fileName, 'w') as json_file:
        json.dump(default_json, json_file, indent=4)

    return {
        'startPort': startPort,
        'lastPort': startport-1,
        'fileName': fileName,
        'serverList': serverList
    }


if __name__ == '__main__':
    server_list = fetch_and_decode_data()
    print(create_config(server_list))
