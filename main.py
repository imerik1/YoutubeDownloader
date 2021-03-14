import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
from pytube.exceptions import VideoUnavailable
from pytube import YouTube, Playlist


def getPath():
    root = Tk()
    folder = askdirectory(title='Selecione a pasta')
    if os.path.exists(folder):
        root.destroy()
        return folder
    return getPath()


def download(type, path, array, qualidade):
    if type == 'video':
        for a in array:
            if a.video_codec[:4] == 'avc1':
                if a.resolution == (qualidade + 'p'):
                    print('Seu download está sendo feito')
                    a.download(path)
                    print('Seu download foi concluido')
                    quit()
    else:
        print('Seu download está sendo feito')
        array.download(path)
        print('Seu download foi concluido')


def decision():
    opcaoPrincipal = input('Você irá baixar\n1- Apenas um arquivo\n2- Uma playlist (apenas audio)\nDigite uma opção: ')
    print(" ")
    print('Onde deseja salvar o arquivo?')
    path = getPath()
    print(" ")
    if opcaoPrincipal == '1':
        link = input('Digite o link do vídeo: ')
        yt = YouTube(link)
        video = yt.streams.filter(progressive=True)
        audio = yt.streams.filter(only_audio=True).get_audio_only()
        opcao = input(
            'Você quer o video e audio ou apenas audio?\n1- Para video e audio\n2- Para audio\nDigite a opção: ')
        if opcao == '1':
            print('Escolha uma das opções disponiveis: ')
            for v in video:
                print('- ', v.resolution)
            qualidade = input('Digite uma das resoluções, apenas número\nDigite a qualidade: ')
            download('video', path, video, qualidade)
        elif opcao == '2':
            download('audio', path, audio, '')
        else:
            print('Escolha uma opção valida')
            decision()
            print('')
    elif opcaoPrincipal == '2':
        link = input('Digite o link do playlist: ')
        p = Playlist(link)
        total = 0
        contador = 0
        print('Estamos preparando o download, dependendo do tamanho da playlist pode demorar um pouco')
        for video in p.video_urls:
            try:
                if YouTube(video).check_availability():
                    continue
                else:
                    if YouTube(video).streams.get_audio_only():
                        total = total + 1
            except VideoUnavailable:
                continue

        print('Estamos baixando os audios, foram encontrados ', total, 'audios publicos.')
        for video in p.video_urls:
            try:
                if YouTube(video).check_availability():
                    continue
                else:
                    YouTube(video).streams.get_audio_only().download(path)
                    contador = contador + 1
                    print('O seu download está em ' + str(round(((contador * 100) / total), 1)), '%')
            except VideoUnavailable:
                continue

    else:
        print('Escolha uma opção valida')
        decision()
        print('')

    opcao = input('Você deseja sair? s ou n\nDigite uma opção: ')
    if opcao == 's':
        exit(0)
    else:
        decision()
        print('')


decision()
