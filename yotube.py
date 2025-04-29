from pytube import YouTube

url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'  # link de teste que sempre funciona

try:
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    video.download(output_path='C:/Users/hub.esilvestre_huben/Desktop')
    print('Download concluído!')
except Exception as e:
    print(f'Ocorreu um erro: {e}')
