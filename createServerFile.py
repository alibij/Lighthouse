import base64
from common import make_file

def server_list_file (server:list) :
    
    clashFile = ''
    serverfile = ''
    activeServer = sorted(server, key=lambda x: x['downloadSpeed'], reverse=True)
    for i in activeServer:
        clashFile += f'{i["connectionUrl"]}\n'
        serverfile += f'{i}\n'

    encoded_bytes = base64.b64encode(clashFile.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')

    make_file(serverfile, "./serverlist.txt")
    make_file(encoded_string, "./clashfile.txt")
