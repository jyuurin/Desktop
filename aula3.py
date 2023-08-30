import PySimpleGUI as sg
from PIL import Image
import io
import requests

def resize_image(image_path):
    img = Image.open(image_path)
    img = img.resize((800, 600), Image.Resampling.LANCZOS)
    return img

def mostrar_tela(imagem):

    

layout = [
    [sg.Menu([['Arquivo', ['Abrir', 'Abrir URL'  ,'Fechar']], ['Ajuda', ['Sobre']], ['Info', ['Dados da Imagem']]])],
    [sg.Image(key = '-IMAGE-', size = (300, 300))],    
]
window = sg.Window('Menu e Get file', layout, resizable=True)

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED or event == 'Fechar':
        break
    elif event == 'Abrir':
        file_path = sg.popup_get_file('Selecione uma imagem', file_types=(("Imagens", "*.jpg *.png"),))
        if file_path:
            resized_image = resize_image(file_path)

            img_bytes = io.BytesIO()
            resized_image.save(img_bytes, format = 'PNG')
            window['-IMAGE-'].update(data= img_bytes.getvalue())

    elif event == 'Abrir URL':
        url = sg.popup_get_text("Cole a url da imagem.")
        if url:
            request = requests.get(url)
            resized_image = resize_image(io.BytesIO(request.content))
            img_bytes = io.BytesIO()
            resized_image.save(img_bytes, format = 'PNG')
            window['-IMAGE-'].update(data= img_bytes.getvalue())
    elif event == 'Sobre':
        sg.popup('Desenvolvido pelo BCC 6 Semestre \n \n Julia')
    elif event == 'Dados da Imagem':
        sg.popup("Tamanho:", resized_image.height, resized_image.width, "\nNome da Imagem:""\nFormato:", resized_image.format, "\nDescrição:", resized_image.format_description)


window.close()