import os
import subprocess
from pathlib import Path
import PySimpleGUI as sg
import threading

def comprimir_pdf(diretorio_origem, diretorio_destino, arquivo):
    caminho_origem = Path(diretorio_origem, arquivo)
    caminho_destino = Path(diretorio_destino, arquivo)
    arg1 = f'-sOutputFile={caminho_destino}'
    
    # if the OS is windowons you need to change the gs command to gswin64c
    gs_args = ['gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4', '-dPDFSETTINGS=/screen', '-dNOPAUSE', '-dBATCH', '-dQUIET', arg1, caminho_origem]
    subprocess.run(gs_args, stdout=subprocess.PIPE)

def comprimir_diretorio(diretorio_origem, diretorio_destino):
    Path(diretorio_destino).mkdir(parents=True, exist_ok=True)
    for arquivo in os.listdir(diretorio_origem):
        if arquivo.lower().endswith('.pdf'):
            comprimir_pdf(diretorio_origem, diretorio_destino, arquivo)

def comprimir_diretorios(diretorios_origem, diretorio_destino, progress_bar):
    for diretorio_origem in diretorios_origem:
        comprimir_diretorio(diretorio_origem, diretorio_destino)
        progress_bar.update(1)

def execute():
    diretorio_origem = sg.popup_get_folder('Selecione o diretório de origem')
    if not diretorio_origem:
        return

    diretorios_origem = []
    for arquivo in os.listdir(diretorio_origem):
        caminho_arquivo = Path(diretorio_origem, arquivo)
        if caminho_arquivo.is_dir():
            diretorios_origem.append(caminho_arquivo)

    if not diretorios_origem:
        sg.popup('Não há diretórios a serem comprimidos')
        return

    diretorio_destino = Path(sg.popup_get_folder('Selecione o diretório de destino para os arquivos comprimidos'))
    if not diretorio_destino:
        return

    progress_bar = sg.ProgressBar(len(diretorios_origem), orientation='h', size=(40, 20))
    progress_bar_window = sg.Window('Compactando diretórios...', [[progress_bar]], no_titlebar=True, keep_on_top=True)
    progress_bar_window.finalize()

    thread = threading.Thread(target=comprimir_diretorios, args=(diretorios_origem, diretorio_destino, progress_bar))
    thread.start()

    while thread.is_alive():
        event, values = progress_bar_window.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break

    progress_bar_window.close()
    sg.popup('Compactação concluída!')

execute()