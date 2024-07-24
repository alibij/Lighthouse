import json
import requests
import base64
from url2json import generateConfig
from common import make_file


def fetch_and_decode_data(url="https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity", is_base64=True):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            decoded_data = base64.b64decode(
                response.content) if is_base64 else response.content
            return decoded_data.decode('utf-8').strip().split('\n')
        else:
            print(
                f"Failed to fetch data from {url}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")


def create_config(server_list: list, fileName='testconfig.json', startPort=10000):
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
        try:
            proxy = generateConfig(url)
        except:
            continue

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

    make_file(json.dumps(default_json, indent=4), fileName)
    # with open(fileName, 'w') as json_file:
    #     json.dump(default_json, json_file, indent=4)

    return {
        'startPort': startPort,
        'lastPort': startport-1,
        'fileName': fileName,
        'serverList': serverList
    }


def main_config(server: str, fileName='config.json', http_port=1081, socks5_port=1080, addrules=True, http=True, socks=True):

    rules = [
        {
            "type": "field",
            "inboundTag": [
                "api"
            ],
            "outboundTag": "api"
        },
        {
            "type": "field",
            "outboundTag": "direct",
            "domain": [
                "domain:example-example.com",
                "domain:example-example2.com"
            ]
        },
        {
            "type": "field",
            "outboundTag": "block",
            "domain": [
                "geosite:category-ads-all"
            ]
        },
        {
            "type": "field",
            "outboundTag": "direct",
            "domain": [
                "geosite:cn",
                "geosite:geolocation-cn"
            ]
        },
        {
            "type": "field",
            "outboundTag": "direct",
            "ip": [
                "geoip:private",
                "geoip:cn"
            ]
        },
        {
            "type": "field",
            "port": "0-65535",
            "outboundTag": "proxy"
        }
    ]
    default_json = {
        "log": {},
        "api": {
            "tag": "api",
            "services": ["HandlerService", "LoggerService", "StatsService"]
        },
        "inbounds": [],
        "outbounds": [
            {
                "tag": "direct",
                "protocol": "freedom",
                "settings": {}
            },
            {
                "tag": "blocked",
                "protocol": "blackhole",
                "settings": {}
            }
        ],
        "routing": {
            "domainStrategy": "AsIs",
            "rules": rules if addrules else []
        }
    }

    proxy = generateConfig(server)
    if socks:
        default_json['inbounds'].append({
            "port": socks5_port,
            "protocol": "socks",
            "settings": {
                "auth": "noauth",
                "udp": True
            }
        })
    if http:
        default_json['inbounds'].append({
            "port": http_port,
            "protocol": "http",
            "settings": {}
        })
    if proxy:
        outbound = proxy['outbounds'][0]
        default_json['outbounds'].append(outbound)

        make_file(json.dumps(default_json, indent=4), fileName)

        return True
    return False


if __name__ == "__main__":
    pass
