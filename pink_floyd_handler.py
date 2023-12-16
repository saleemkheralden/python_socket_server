ALBUM_DEL = '#'
SONG_DEL = '*'
FIELD_DEL = '::'

menu = """
********************************
Menu
1. List of albums
2. Songs in album
3. Length of a song
4. Get Lyrics of a song
5. Search song in album
6. Search a song by it's name
7. Search a song by it's lyrics
8. Exit
********************************
"""


def init_DB():
    """
        initiate the DB of the albums
    """

    file = open("data/Pink_Floyd_DB.txt", 'r')
    # file = open('Magshimim_task_1/data/Pink_Floyd_DB.txt', 'r')
    content = file.read()
    content = content.lower()

    DB = {}
    albums = split_albums(content)

    for album in albums:
        album_info, album_songs = split_songs(album)
        album_name, album_year = get_album_name_year(album_info)
        DB[album_name] = {'year': album_year, 'songs': {}}
        for song in album_songs:
            name, writer, duration, lyrics = get_song_info(song)
            DB[album_name]['songs'][name] = {'writer': writer, 'duration': duration, 'lyrics': lyrics}

    file.close()
    return DB


def get_song_info(song: str) -> tuple:
    return (e for e in song.split(FIELD_DEL))


def get_album_name_year(album_info: str) -> tuple:
    return (e.replace("\n", "") for e in album_info.split(FIELD_DEL))


def split_songs(album: str) -> tuple:
    """
    :param album: album info (name, year and its songs)
    :return: tuple where the first value is the album name and year and the second value is the songs array
    """
    split_arr = album.split(SONG_DEL)
    return split_arr[0], split_arr[1:]


def split_albums(content: str) -> list:
    """
    :param content: the whole text corpus
    :return: list where each cell is the data for an album
    """
    return content.split(ALBUM_DEL)[1::]




