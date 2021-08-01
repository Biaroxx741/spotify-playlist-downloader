import os
import ObtenerLinkVideo
import spotipy, requests
# from spotipy.oauth2 import SpotifyClientCredentials

# sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="CLIENT_ID",client_secret="SECRET"))
token = token = requests.get(
        "https://open.spotify.com/get_access_token?reason=transport&productType=web_player"
    ).json()

sp = spotipy.Spotify(auth=token["accessToken"])
tracks = []
incorrecto = True
os.system('cls')
while incorrecto:
    try:
        opcion = int(input('Ingrese una opcion correcta:\n1 - Link completo de la playlist.\n2 - ID de la playlist.\n3 - Salir.\n'))
        while opcion != 1 and opcion != 2 and opcion != 3:
            print('Opcion invalida.')
            opcion = int(input('Ingrese una opcion correcta:\n1 - Link completo de la playlist.\n2 - ID de la playlist.\n3 - Salir.\n'))
        if opcion == 1:
            idVal = input('Ingrese link de la playlist a descargar: ')
            idVal = idVal.split('playlist/')[1].split('?')[0]
        elif opcion == 2:
            idVal = input('Ingrese ID de la playlist a descargar: ')
        else:
            os.system('exit')
        pl_id = f'spotify:playlist:{idVal}'
        result = sp.playlist_items(pl_id, additional_types=['track'])
        incorrecto = False
    except:
        os.system('cls')
        print('ID o URL ingresado invalido, porfavor ingrese uno correcto.')

os.system('cls')
tracks.extend(result['items'])

nombresTema = []
i = 1

for tema in tracks:
    texto = tema['track']['name'] + ' ' + tema['track']['artists'][0]['name']
    nombresTema.append(texto)

a = len(nombresTema)
ObtenerLinkVideo.PrevConfigs()
os.system('cls')
print('Comenzando descarga...')
for temaArreglado in nombresTema:
    print(f'Descargando {temaArreglado}....')
    videoID = ObtenerLinkVideo.GetVideoID(temaArreglado)
    ObtenerLinkVideo.DownloadVid(videoID, temaArreglado)
    print(f'\t{temaArreglado} descargado!')
    print(f'{i}/{a}')
    i += 1

ObtenerLinkVideo.CloseWin()
