import PySimpleGUI as sg
from PIL import Image
import io
import requests
import os
from PIL.ExifTags import TAGS, GPSTAGS


image_atual = None
image_path = None


def resize_image(img):
    img = img.resize((800, 600), Image.Resampling.LANCZOS) 
    return img

def open_image(filename):
    global image_atual
    global image_path
    image_path = filename
    image_atual = Image.open(filename)    
    
    resized_img = resize_image(image_atual)
    #Converte a image PIL para o formato que o PySimpleGUI
    img_bytes = io.BytesIO() #Permite criar objetos semelhantes a arquivos na memÃ³ria RAM
    resized_img.save(img_bytes, format='PNG')
    window['-IMAGE-'].update(data=img_bytes.getvalue())

def save_image(filename):
    global image_atual
    if image_atual:
        with open(filename, 'wb') as file:
            image_atual.save(file)



def info_image():
    global image_atual
    global image_path
    if image_atual:
        largura, altura = image_atual.size
        formato = image_atual.format
        tamanho_bytes = os.path.getsize(image_path)
        tamanho_mb = tamanho_bytes / (1024 * 1024)
        exif_table = {}
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            exif_table[decoded] = value
        gps_info = {}
        for key in exif_table['GPSInfo'].keys():
            decode = GPSTAGS.get(key,key)
            gps_info[decode] = exif_table['GPSInfo'][key]
        sg.popup(f"Tamanho: {largura} x {altura}\nFormato: {formato}\nTamanho em MB: {tamanho_mb:.2f}\nLocal: {gps_info['GPSLatitude']}")


layout = [
    [sg.Menu([['Arquivo', ['Abrir', 'Abrir URL', 'Salvar', 'Fechar']], 
                ['Ajuda', ['Sobre']],
                ['Info', ['Dados da Imagem']]])],
    [sg.Image(key='-IMAGE-', size=(800,600))],
]

window = sg.Window('Menu e Get File', layout, resizable=True)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Fechar':
        break
    elif event == 'Abrir':
        arquivo = sg.popup_get_file('Selecionar image', file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
        if arquivo:
            open_image(arquivo)

    elif event == 'Abrir URL':
        url = sg.popup_get_text('Digite a URL da imagem')
        if url:
            response = requests.get(url)
            open_image(io.BytesIO(response.content))
    elif event == 'Dados da Imagem':
        info_image()
        get_exif(arquivo)at s
    elif event == 'Salvar':
        if image_atual:
            arquivo = sg.popup_get_file('Salvar image como', save_as=True, file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
            if arquivo:
                save_image(arquivo)
    elif event == 'Sobre':
        sg.popup('Desenvolvido pelo BCC - 6 semestre. \n\n Julia ')

window.close()
