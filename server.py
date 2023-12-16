import socket
from pink_floyd_handler import *

# init the socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to the ip (0.0.0.0) and the port (80) of the server
# 0.0.0.0 accepts connection from any ip that can route to it
server_ip = "0.0.0.0"
server_port = 80
server_recv_bytes = 1024

serverSocket.bind((server_ip, server_port))
print(f"socket bind to {server_ip}:{server_port}")

print(f"Initiating database")
DB = init_DB()


# start listening to incoming connections
# adding number argument to the listen function sets a threshold to the number of client
# that can be connected to the server
serverSocket.listen()


def handle_client():
    # accepts a client and gets its socket and the address
    clientSocket, address = serverSocket.accept()

    with clientSocket:
        print(f"Client {address} connected to server")
        clientSocket.send(menu.encode())

        while True:
            # argument in the recv function is the bytes that's being received from the client
            data = clientSocket.recv(server_recv_bytes)

            if not data:
                break

            data = data.decode()
            if not data.isdigit():
                clientSocket.send(b"input should be a number between 1 and 8")
                continue

            data = int(data)
            print(f"{address}> {data}")
            if data == 8:
                # exit
                break

            elif data == 1:
                clientSocket.sendall(("Albums:\n" + "\n".join(DB.keys())).encode())
            elif data == 2:
                clientSocket.send(b"Please enter album name")
                album_name = clientSocket.recv(server_recv_bytes).decode()
                album_name = album_name.lower()

                if album_name in DB.keys():
                    clientSocket.send(("Songs:\n" + "\n".join(DB[album_name]['songs'].keys())).encode())
                else:
                    clientSocket.send(b"You enter album name which isn't one of the options")
            elif (data == 3) or (data == 4):

                client_field_req = 'duration' if data == 3 else 'lyrics'

                clientSocket.send(b"Please enter song name")
                song_name = clientSocket.recv(server_recv_bytes).decode()
                song_name = song_name.lower()

                flag = True
                for album in DB.values():
                    if song_name in album['songs'].keys():
                        clientSocket.send(album['songs'][song_name][client_field_req].encode())
                        flag = False
                        break
                if flag:
                    clientSocket.send(b"Didn't find the song you were looking for")
            # elif data == 4:
            #     clientSocket.send(b"Please enter song name")
            #     song_name = clientSocket.recv(server_recv_bytes).decode()
            #     song_name = song_name.lower()
            #
            #     flag = True
            #     for album in DB.values():
            #         if song_name in album['songs'].keys():
            #             clientSocket.send(album['songs'][song_name]['lyrics'].encode())
            #             flag = False
            #             break
            #     if flag:
            #         clientSocket.send(b"Didn't find the song you were looking for")
            #
            elif data == 5:
                clientSocket.send(b"Please enter song name")
                song_name = clientSocket.recv(server_recv_bytes).decode()
                song_name = song_name.lower()

                flag = True
                for __album_name, album in DB.items():
                    if song_name in album['songs'].keys():
                        clientSocket.send(__album_name.encode())
                        flag = False
                        break
                if flag:
                    clientSocket.send(b"Didn't find the song you were looking for")
            elif data == 6:
                clientSocket.send(b"Please enter song name")
                song_name = clientSocket.recv(server_recv_bytes).decode()
                song_name = song_name.lower()

                matched_songs = []

                flag = True
                for album in DB.values():
                    for song in album['songs'].keys():
                        if song.__contains__(song_name):
                            matched_songs.append(song)
                clientSocket.send(("Matched songs:\n" + "\n".join(matched_songs)).encode())
            elif data == 7:
                clientSocket.send(b"Please enter lyrics")
                lyrics = clientSocket.recv(server_recv_bytes).decode()
                lyrics = lyrics.lower()

                matched_songs = []

                flag = True
                for album in DB.values():
                    for __song_name, song in album['songs'].items():
                        if song['lyrics'].__contains__(lyrics):
                            matched_songs.append(__song_name)
                clientSocket.send(("Matched songs:\n" + "\n".join(matched_songs)).encode())

                # clientSocket.send(get_all_songs_by_lyrics(lyrics=lyrics).encode())


while True:
    handle_client()




