#!/usr/cbin/env python3
"""
Created on 11 dic 2020

@author: Eddy
for audio and video conversion is necessary the ffmpeg,
ffprobe and ffplay1 on the same path of this script, that you can download in:
http://web.archive.org/web/20200917010927/https://ffmpeg.zeranoe.com/builds/
Download the zip and extract the .exe files like this:

 folder/
    -downloader.py
    -ffmpeg.exe
    -ffmprobe.exe
    -ffplay1

"""
from __future__ import unicode_literals
import os
import time
import threading
# importing YouTube module
import youtube_dl
import ctypes
import inspect
from datetime import datetime
# importing tkinter
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Style
from tkinter import filedialog
from tkinter import messagebox

VERSION = '0.2'

# dictionaries with all languages available
language = {
    'ENG': {
        'title': 'Welcome to Youtube Video Downloader App',
        'copy': 'copy',
        'Copy': 'Copy',
        'Paste': 'Paste',
        'paste': 'paste',
        'Cut': 'Cut',
        'cut': 'cut',
        'title_entry': 'Enter the Youtube links bellow',
        'one_line': 'one link per line',
        'save_title': 'Save videos in:',
        'browse': 'Browse',
        'clear': 'Clear',
        'start_download': 'Start download',
        'stop_download': 'Stop download',
        'down_videos_stopped': 'Download stopped',
        'running': 'Running',
        'running_msg': 'The downloader app is already running',
        'running_msg_1': 'The downloader app is running',
        'url_invalid': 'Url not valid at line',
        'no_videos': 'No videos to download',
        'all_downloaded': 'All videos downloaded',
        'starts_down_video': 'Video download starts',
        'video_downloaded': 'Video downloaded',
        'downloading': 'Downloading',
        'downloaded': 'Downloaded',
        'close_app': 'do you want to close the app?',
        'app': 'App',
        'language': 'Language',
        'about': 'About',
        'exit': 'Exit',
        'release_notes': 'Release Notes',
        'version': 'Version'
    },
    'ESP': {
        'title': 'Welcome to Youtube Video Downloader App',
        'copy': 'copiar',
        'Copy': 'Copiar',
        'Paste': 'Pegar',
        'paste': 'pegar',
        'Cut': 'Cortar',
        'cut': 'cortar',
        'title_entry': 'Agrega los enlaces de Youtube aquí',
        'one_line': 'un enlace por línea',
        'save_title': 'Guardar videos en:',
        'browse': 'Buscar',
        'clear': 'Limpiar',
        'start_download': 'Iniciar descarga',
        'stop_download': 'Cancelar descarga',
        'down_videos_stopped': 'Descarga cancelada',
        'running': 'Descargando',
        'running_msg': 'la aplicación ya se está ejecutando',
        'running_msg_1': 'la aplicación se está ejecutando',
        'url_invalid': 'Enlace no correcto en la línea',
        'no_videos': 'No Hay videos para descargar',
        'all_downloaded': 'Todos los videos descargados',
        'starts_down_video': 'Empieza la descarga del video',
        'video_downloaded': 'Video descargado',
        'downloading': 'Descargando',
        'downloaded': 'Descargado',
        'close_app': 'quieres cerrar la aplicación?',
        'exit': 'Cerrar',
        'app': 'App',
        'language': 'Idioma',
        'about': 'Acerca',
        'release_notes': 'Notas de lanzamiento',
        'version': 'Versión'

    },
    'PRT': {
        'title': 'Welcome to Youtube Video Downloader App',
        'copy': 'copiar',
        'Copy': 'Copiar',
        'Paste': 'Colar',
        'paste': 'colar',
        'Cut': 'Recortar',
        'cut': 'recortar',
        'title_entry': 'Adicione os links do Youtube aqui',
        'one_line': 'um link por linha',
        'save_title': 'Salvar vídeos em:',
        'browse': 'Busca',
        'clear': 'Limpar',
        'start_download': 'Iniciar o download',
        'stop_download': 'Parar o download',
        'down_videos_stopped': 'Download parado',
        'running': 'Descarregando',
        'running_msg': 'o aplicativo já está rodando',
        'running_msg_1': 'o aplicativo está rodando',
        'url_invalid': 'Link incorreto na linha',
        'no_videos': 'Nenhum vídeo para baixar',
        'all_downloaded': 'todos os vídeos baixados',
        'starts_down_video': 'O download do vídeo começa',
        'video_downloaded': 'Vídeo baixado',
        'downloading': 'Baixando',
        'downloaded': 'Baixado',
        'close_app': 'quer fechar o aplicativo?',
        'exit': 'Fechar',
        'app': 'App',
        'language': 'Idioma',
        'about': 'Sobre',
        'release_notes': 'Notas de lançamento',
        'version': 'Versão'
    },
    'ITA': {
        'title': 'Welcome to Youtube Video Downloader App',
        'copy': 'copia',
        'Copy': 'Copia',
        'Paste': 'Incolla',
        'paste': 'incolla',
        'Cut': 'Taglia',
        'cut': 'taglia',
        'title_entry': 'Inserisci i link di Youtube qui',
        'one_line': 'un link per riga',
        'save_title': 'Salva i video in:',
        'browse': 'Cerca',
        'clear': 'Pulisci',
        'start_download': 'Inizia download',
        'stop_download': 'Ferma download',
        'down_videos_stopped': 'Download fermato',
        'running': 'Scaricando',
        'running_msg': 'Il download dei video è già in corso',
        'running_msg_1': 'Il download dei video è in corso',
        'url_invalid': 'Link non corretto alla riga',
        'no_videos': 'Nessun video da scaricare',
        'all_downloaded': 'Tutti i video scaricati',
        'starts_down_video': 'Inizia il download del video',
        'video_downloaded': 'Video scaricato',
        'downloading': 'Scaricando',
        'downloaded': 'Scaricato',
        'close_app': 'vuoi chiudere l''app?',
        'exit': 'Chiudi',
        'app': 'App',
        'language': 'Lingua',
        'about': 'About',
        'release_notes': 'Note di Rilascio',
        'version': 'Versione'

    }

}

class Translator:

    def __init__(self, languages):
        # set default languagge
        self.default_language = 'ENG'
        self.current_language = self.default_language
        # load dictionary to libs
        self.languages = languages
        # labels that change when update
        self.list_labels = self.languages.get(self.default_language).items()

        # vars for multi-language labels
        self.title = ''
        self.title_entry = ''
        self.one_line = ''
        self.clear = ''
        self.start_download = ''
        self.stop_download = ''
        self.save_title = ''
        self.browse = ''
        self.down_videos_stopped = ''
        self.running = ''
        self.running_msg = ''
        self.running_msg_1 = ''
        self.url_invalid = ''
        self.no_videos = ''
        self.all_downloaded = ''
        self.starts_down_video = ''
        self.video_downloaded = ''
        self.downloaded = ''
        self.downloading = ''
        self.close_app = ''

        # setting labels with default language
        self.set_language(self.default_language)

    def set_language(self, lang):
        # update current language
        self.current_language = lang
        # get labels for default label
        items_for_curr = self.languages.get(lang)
        for _label, _description in self.list_labels:
            # get from the current language
            new_value = items_for_curr.get(_label)
            if new_value is None:
                # use the desciption
                new_value = _description
            self.__setattr__(_label, new_value)


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class DownloaderThread(threading.Thread):
    '''
    Thread class with a stop() method
    The thread itself has to check regularly fot the stopped() contition
    '''
    def __init__(self, *args, **kwargs):
        super(DownloaderThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.launched = True

    def stopped(self):
        return self._stop_event.is_set()

    def _get_my_tid(self):
        """determines this (self's) thread id"""
        if not self.is_alive():
            raise threading.ThreadError("the thread is not active")

        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        raise AssertionError("could not determine the thread's id")

    def raise_exc(self, exctype):
        """raises the given exception type in the context of this thread"""
        _async_raise(self._get_my_tid(), exctype)

    def terminate(self):
        """raises SystemExit in the context of the given thread, which should
        cause the thread to exit silently (unless caught)"""
        self._stop_event.set()
        self.raise_exc(SystemExit)


class Menubar:

    def __init__(self, parent):
        font_specs = ('consolas', 11)

        self.menubar = tk.Menu(parent.root, font=font_specs)
        self.parent = parent
        self.parent.root.config(menu=self.menubar)

        self.app_dropdown = tk.Menu(self.menubar, font=font_specs, tearoff=0)
        # file_dropdown.add_separator()

        self.app_dropdown = tk.Menu(self.menubar, font=font_specs, tearoff=0)
        # index 1
        self.app_dropdown.add_command(label="Note di Rilascio",
                                      command=self.show_release_notes)
        # index 2
        self.app_dropdown.add_command(label="About",
                                      command=self.show_about_message)
        self.app_dropdown.add_separator()
        # index 3
        self.app_dropdown.add_command(label='Esci',
                                      command=self.parent.prevent_close)
        self.language_dropdown = tk.Menu(self.menubar, font=font_specs, tearoff=0)
        self.language_dropdown.add_command(label="English",
                                           command=lambda: self.parent.change_language('ENG'))
        self.language_dropdown.add_command(label="Español",
                                           command=lambda: self.parent.change_language('ESP'))
        self.language_dropdown.add_command(label="Italiano",
                                           command=lambda: self.parent.change_language('ITA'))
        self.language_dropdown.add_command(label="Português",
                                           command=lambda: self.parent.change_language('PRT'))

        # index 1
        self.menubar.add_cascade(label="App", menu=self.app_dropdown)
        # index 2
        self.menubar.add_cascade(label="Language", menu=self.language_dropdown)

        # set with default language pass by parent
        self.set_language()

    def set_language(self):
        # changing language of menu bar
        self.menubar.entryconfigure(1, label=self.parent.lang.app)
        self.menubar.entryconfigure(2, label=self.parent.lang.language)

        # app about dropdown
        self.app_dropdown.entryconfigure(0, label=self.parent.lang.release_notes)
        self.app_dropdown.entryconfigure(1, label=self.parent.lang.about)
        self.app_dropdown.entryconfigure(3, label=self.parent.lang.exit)

    @staticmethod
    def show_about_message():
        box_title = "Yt Downloader"
        box_message = "Youtube Video Downloader using Tkinter and Python"
        messagebox.showinfo(box_title, box_message)

    def show_release_notes(self):
        box_title = f"{self.parent.lang.release_notes}"
        box_message = f"{self.parent.lang.version} {VERSION} - EA"
        messagebox.showinfo(box_title, box_message)


class Statusbar:

    def __init__(self, parent):
        # font_specs = ('ubuntu', 12)

        self.status = tk.StringVar()
        self.status.set(f"Yt Downloader - {VERSION} EA")

        # label = tk.Label(parent.textarea, textvariable=self.status, fg="black",
        #                 bg="lightgrey", anchor='sw', font=font_specs)
        # label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def update_status(self, *args):
        if isinstance(args[0], bool):
            self.status.set(
                f"Yt Downloader - {VERSION} EA - Il tuo File e' stato salvato!")
        else:
            self.status.set(f"Yt Downloader - {VERSION} EA - {args[0]}")


class ytDownloader:
    """
    ytDownloader e' un youtube video downloader
    """

    def __init__(self, _root):
        # start objects
        self.root = _root
        self.selected_language = 'ENG'
        self.lang = Translator(language)
        self.root.geometry("960x360")

        self.root.title("Yt Video Downloader")
        # self.root.title(self.lang.title)
        self.root.resizable(False, False)
        self.init_objects()
        self.v_counter = 0
        self.v_down = 0
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Cut")
        self.context_menu.add_command(label="Copy")
        self.context_menu.add_command(label="Paste")
        self.downloading = False
        self.global_downloading = False
        self.ThreadLauncher = None
        self.root.protocol('WM_DELETE_WINDOW', self.prevent_close)

    def change_language(self, _language):
        self.lang.set_language(_language)
        self.set_values()
        # changing language menubar
        self.menubar.set_language()
        self.root.update_idletasks()

    def prevent_close(self):
        '''
        Check if Thread is running then delete it
        :return: None
        '''
        _title = ''
        _message = ''
        if self.global_downloading:
            _title = self.lang.running
            _message = f"{self.lang.running_msg_1}"\
                f"\n {self.lang.close_app}"
            question = messagebox.askyesno(
                title=_title, message=_message
            )
            if question:
                # destroy thread runnning
                self.stop_download()
            else:
                return None
        self.root.destroy()

        # messagebox.showinfo('Running', 'The downloader app is already running')
        # root.destroy()

    def reset_values(self):
        self.v_counter = 0
        self.v_down = 0

    def popup(self, event, element):
        self.context_menu.post(event.x_root, event.y_root)
        self.context_menu.entryconfigure("Cut", command=lambda: element.event_generate("<<Cut>>"))
        self.context_menu.entryconfigure("Copy", command=lambda: element.event_generate("<<Copy>>"))
        self.context_menu.entryconfigure("Paste", command=lambda: element.event_generate("<<Paste>>"))

    def init_objects(self):
        def _redo(text_object):
            var = text_object.edit_redo

        def _undo(text_object):
            var = text_object.edit_undo

        self.s = Style(self.root)
        self.s.theme_use('default')
        self.s.layout("LabeledProgressbar",
                      [('LabeledProgressbar.trough',
                        {'children': [('LabeledProgressbar.pbar',
                                       {'side': 'left', 'sticky': 'ns'}),
                                      ("LabeledProgressbar.label",  # label inside the bar
                                       {"sticky": ""})],
                         'sticky': 'nswe'})])
        self.s.configure("LabeledProgressbar", background='#06b025')
        self.font_title = ('consolas', 14)
        self.font_specs = ('consolas', 11)
        # variables used on proccess
        self.link = StringVar()
        self.save_path = StringVar()
        self.save_path.set(os.path.expanduser('~/Downloads'))
        self.title_var = StringVar()
        self.lb_title = Label(
            self.root, textvariable=self.title_var,
            font="consolas 14 bold")
        self.lb_title.grid(row=0, column=0, columnspan=3, padx=(10, 20))
        self.d_descr_link = StringVar()
        self.descr_link = Label(
            self.root, textvariable=self.d_descr_link,
            font="consolas 11")
        self.descr_link.grid(row=1, column=0)
        self.d_lab_one = StringVar()
        self.lab_one = Label(
            self.root, textvariable=self.d_lab_one, font="Consolas 10")
        self.lab_one.grid(row=2, column=0)

        # frame for text where put the links
        self.my_frame = Frame(self.root)
        self.my_scroll = Scrollbar(self.my_frame, orient=VERTICAL)
        self.my_text = Text(
            self.my_frame, width=55, height=8, font=self.font_specs,
            yscrollcommand=self.my_scroll.set, undo=True)
        self.my_text.bind('<Control-z>', _undo(self.my_text))
        self.my_text.bind('<Control-y>', _redo(self.my_text))
        self.my_text.bind("<Button-3>",
                          lambda event, text_element=self.my_text:
                          self.popup(event=event, element=text_element))
        self.my_scroll.config(command=self.my_text.yview)
        self.my_scroll.pack(side=RIGHT, fill=Y)
        self.my_frame.grid(row=3, column=0, padx=10)
        self.my_text.pack()

        # adding buttons
        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=4, column=0, padx=10, pady=10)
        # clear button
        self.d_clear_button = StringVar()
        self.clear_button = Button(
            self.button_frame, textvariable=self.d_clear_button,
            command=self.clear_text)
        self.clear_button.grid(row=0, column=0, padx=10)
        self.d_start_down_btn = StringVar()
        self.start_down_btn = Button(
            self.button_frame, textvariable=self.d_start_down_btn,
            command=self.launch_down, fg="blue")
        self.start_down_btn.grid(row=0, column=1, padx=10)

        #stop button
        self.button_frame1 = Frame(self.root)
        self.button_frame1.grid(row=4, column=1, padx=10, pady=10)
        self.d_stop_button = StringVar()
        self.stop_button = Button(
            self.button_frame1, textvariable=self.d_stop_button, command=self.stop_download,
            fg="red")
        self.stop_button.grid(row=0, column=0, padx=10)
        self.stop_button.grid_remove()
        self.d_lb_save_in = StringVar()
        self.lb_save_in = Label(
            self.root, textvariable=self.d_lb_save_in,
            font="Consolas 11")
        self.lb_save_in.grid(row=1, column=1)

        # frame for path and button
        self.search_frame = Frame(self.root)
        self.search_frame.grid(row=2, column=1, sticky='w', padx=10)
        self.path_saver = Entry(
            self.search_frame, textvariable=self.save_path, width=65)
        self.path_saver.grid(row=0, column=0, sticky='w')
        self.d_brownse_btn = StringVar()
        self.browse_btn = Button(
            self.search_frame, textvariable=self.d_brownse_btn,
            command=self.browse_button)
        self.browse_btn.grid(row=0, column=1)

        # format file option
        # options frame
        self.option_format = IntVar()
        self.option_buttons = Frame(self.root)
        self.option_buttons.grid(row=5, column=0, sticky='w', padx=10)
        self.R1 = Radiobutton(self.option_buttons, text="Video", variable=self.option_format, value=1)
        self.R1.grid(row=0, column=1)
        self.R2 = Radiobutton(self.option_buttons, text="Audio", variable=self.option_format, value=2)
        self.R2.grid(row=0, column=2)
        # set value on audio
        self.option_format.set(2)

        # adding status frame
        self.status_frame = Frame(self.root, bd=1, relief=SUNKEN)
        self.status_frame.grid(
            row=6, column=0, columnspan=3, sticky=W + E, pady=(20, 0))

        Label(
            self.status_frame, text="EA Yt Downloader",
            font="consolas 11 bold").grid(row=0, column=0, padx=10)
        self.status_text = StringVar()
        self.status_text_label = Label(
            self.status_frame, textvariable=self.status_text,
            font="consolas 11").grid(row=0, column=1, sticky='e')
        # adding status bar
        self.my_progress = ttk.Progressbar(self.status_frame, orient=HORIZONTAL,
                                           length=250, mode='determinate',
                                           style="LabeledProgressbar")
        self.my_progress.grid(row=0, column=2, sticky='e')
        # hiding progressbar
        self.my_progress.grid_remove()

        # debug text
        self.deb_frame = Frame(self.root)
        self.scr_deb = Scrollbar(self.deb_frame, orient=VERTICAL)

        self.my_text1 = Text(
            self.deb_frame, state='disabled', width=55, height=8,
            yscrollcommand=self.scr_deb.set, bg="white")
        self.scr_deb.config(command=self.my_text1.yview)
        self.scr_deb.pack(side=RIGHT, fill=Y)
        self.deb_frame.grid(row=3, column=1, columnspan=2, padx=10)

        self.my_text1.pack(side=LEFT, fill=BOTH, expand=YES)

        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)
        self.set_values()

    def set_values(self):
        '''
        setting values of label, messages and buttons
        :return: None
        '''
        try:
            self.title_var.set(self.lang.title)
            self.d_descr_link.set(self.lang.title_entry)
            self.d_lab_one.set(self.lang.one_line)
            self.d_clear_button.set(self.lang.clear)
            self.d_start_down_btn.set(self.lang.start_download)
            self.d_stop_button.set(self.lang.stop_download)
            self.d_lb_save_in.set(self.lang.save_title)
            self.d_brownse_btn.set(self.lang.browse)
        except AttributeError:
            # at the moment do nothing
            pass

    def clear_text(self):
        self.my_text.delete(1.0, END)

    def browse_button(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        # global save_path
        self.filename = filedialog.askdirectory()
        if self.filename != '':
            self.save_path.set(self.filename)

    def stop_download(self):
        '''
        stop download thread and reset all necessary values
        '''
        if not self.ThreadLauncher.stopped():
            self.ThreadLauncher.terminate()
        self.ThreadLauncher.join()
        # reset values
        self.global_downloading = False
        # set message download stopped
        # get message on current lang
        self.status_text.set(self.lang.down_videos_stopped)
        # hide stop button
        self.stop_button.grid_remove()
        return None

    def launch_down(self):
        if self.global_downloading:
            messagebox.showinfo(self.lang.running, self.lang.running_msg)
            return None

        self.ThreadLauncher = DownloaderThread(target=self.download)
        self.ThreadLauncher.start()
        # pass

    def download(self):
        # using try and except to execute program without errors
        try:
            # reset counters
            self.reset_values()
            # global v_counter, v_down
            format_video = ''
            if self.option_format.get() == 1:
                # video
                format_video = 'bestvideo+bestaudio/best'
            elif self.option_format.get() == 2:
                # audio
                format_video = 'bestaudio/best'
            else:
                raise RuntimeError("Opzione formato di download non selezionato")
            self.where_save = self.save_path.get()
            self.my_progress.grid_remove()
            # default for audio format
            for_audio = {'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]}
            download_options = {
                'format': f'{format_video}',
                'outtmpl': f'{self.where_save}\\%(title)s.%(ext)s',
                'getfilename': '--get-filename',
                '--get-filename': True,
                'progress_hooks': [self.my_hook],
            }
            if self.option_format.get() == 2:
                download_options.update(for_audio)

            list_links = self.my_text.get(1.0, END)
            list_down = list_links.splitlines()
            list_down = [line.rstrip('\n') for line in list_down]
            # check for correct links
            c_l = 0
            for v_l in list_down:
                c_l += 1
                if v_l.count('http') > 1 or v_l.count('HTTP') > 1:
                    # self.status_text.set(f"Url not valid at line: {c_l}")
                    raise RuntimeError(f"{self.lang.url_invalid}: {c_l}")

            self.v_counter = len(list_down)
            # check if empty list
            if (self.v_counter == 0 or
                    (len(list_down) and list_down[0] == '')):
                self.status_text.set(self.lang.no_videos)
                return None
            with youtube_dl.YoutubeDL(download_options) as dl:
                self.my_progress.grid()
                self.stop_button.grid()
                self.global_downloading = True
                for video_link in list_down:
                    if video_link == '':
                        continue
                    self.v_down += 1
                    dl.download([video_link])
                self.status_text.set(
                    f"{self.lang.all_downloaded} [{self.v_down}/{self.v_counter}]")
            self.global_downloading = False
            self.stop_button.grid_remove()
            # link.set("Video downloaded successfully")
        except RuntimeError as e:
            self.status_text.set(e)
            pass
        except Exception as e:
            self.status_text.set(e)
            self.global_downloading = False
            # hide stop button
            self.stop_button.grid_remove()
            print(e)
            pass

    def my_hook(self, d):
        try:
            # global percentage, curr_progress_bar
            # tmpfilename
            # here we should check if stop process is requested or not
            file_tuple = os.path.split(os.path.abspath(d['filename']))
            # tmp_file_tuple = os.path.split(os.path.abspath(d['tmpfilename']))
            # print(tmp_file_tuple)
            if not self.downloading:
                self.my_text1.configure(state='normal')
                self.my_text1.insert(
                    'end', f"{self.v_down}) {self.lang.starts_down_video}:"
                           f"\n{file_tuple[1]}\n")
                self.my_text1.configure(state='disabled')
                self.downloading = True

            if d['status'] == 'finished':
                now = datetime.now()
                date_up = time.mktime(now.timetuple())
                os.utime(d['filename'], (date_up, date_up))
                # message_fin.set(f"Video \n {file_tuple[1]} \ndownloaded successfully")
                self.my_progress['value'] = 100
                self.downloading = False
                self.my_text1.configure(state='normal')
                self.my_text1.insert('end', f"{self.v_down}) {self.lang.video_downloaded}\n")
                self.my_text1.configure(state='disabled')
                # self.percentage.config(
                #    text=f"Downloaded... {self.my_progress['value']}%")
                self.s.configure("LabeledProgressbar",
                                 text=f"{self.my_progress['value']} %      ")
                self.status_text.set(
                    f"{self.lang.downloaded}... [{self.v_down}/{self.v_counter}]")
                self.root.update_idletasks()

            if d['status'] == 'downloading':
                p = d['_percent_str']
                p = p.replace('%', '')
                p = d['_percent_str']
                p = p.replace('%', '')
                percentage = float(p)
                self.my_progress['value'] = percentage
                self.status_text.set(
                    f"{self.lang.downloading}... [{self.v_down}/{self.v_counter}]")
                self.s.configure("LabeledProgressbar",
                                 text=f"{self.my_progress['value']} %      ")
                self.root.update_idletasks()
        except Exception as e:
            self.status_text.set(e)
            print(e)
            raise Exception(e)


if __name__ == "__main__":
    print(os.getcwd())
    root = tk.Tk()
    pt = ytDownloader(root)
    root.mainloop()

