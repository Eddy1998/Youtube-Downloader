#!/usr/cbin/env python3
'''
Created on 11 dic 2020

@author: Eddy
'''
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
from pprint import pprint

VERSION = '0.1'

# dictionaries with all languages avaiable
language = {
    'ENG': {
        'title': 'Yt Video Downloader eng',
        'copy': 'copy',
        'Copy': 'Copy',
        'Paste': 'Paste',
        'paste': 'paste',
        'Cut': 'Cut',
        'cut': 'cut',
        'title_entry': 'Enter the Youtube links bellow',
        'one_line': 'one link per line',
        'save_title': 'Save videos in',
        'browse': 'Browse',
        'clear': 'Clear',
        'start_download': 'Start download'
    },
    'ESP': {
        'title': 'Yt Video Downloader esp',
        'copy': 'copiar',
        'Copy': 'Copiar',
        'Paste': 'Pegar',
        'paste': 'pegar',
        'Cut': 'Cortar',
        'cut': 'cortar',
        'title_entry': 'Agrega los enlaces de Youtube aquí',
        'one_line': 'un enlace por línea',
        'save_title': 'Guardar videos en',
        'browse': 'Busca',
        'clear': 'Limpiar',
        'start_download': 'Iniciar Descarga'
    },
    'PRT': {
        'title': 'Yt Video Downloader',
        'copy': 'copiar',
        'Copy': 'Copiar',
        'Paste': 'Colar',
        'paste': 'colar',
        'Cut': 'Recortar',
        'cut': 'recortar',
        'title_entry': 'Adicione os links do Youtube aqui',
        'one_line': 'um link por linha',
        'save_title': 'Salvar vídeos em',
        'browse': 'Busca',
        'clear': 'Limpar',
        'start_download': 'Iniciar o download'
    },
    # TODO
    'ITA': {
        'title': 'Yt Video Downloader',
        'copy': 'copia',
        'Copy': 'Copia',
        'Paste': 'Incolla',
        'paste': 'incolla',
        'Cut': 'Taglia',
        'cut': 'taglia',
        'title_entry': 'Inserisci i link di Youtube qui',
        'one_line': 'un link per riga',
        'save_title': 'Salva i video in',
        'browse': 'Cerca',
        'clear': 'Pulisci',
        'start_download': 'Inizia download'

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
        self.set_language(self.default_language)

    def get_language(self, lang):
        return self.languages[lang]

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

        menubar = tk.Menu(parent.root, font=font_specs)
        parent.root.config(menu=menubar)

        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        # file_dropdown.add_separator()
        file_dropdown.add_command(label="Esci",
                                  command=parent.prevent_close)

        about_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        about_dropdown.add_command(label="Note di Rilascio",
                                   command=self.show_release_notes)
        about_dropdown.add_separator()
        about_dropdown.add_command(label="About",
                                   command=self.show_about_message)
        language_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        language_dropdown.add_command(label="English",
                                   command=self.change_language(parent, 'ENG'))
        language_dropdown.add_command(label="Spanish",
                                   command=self.change_language(parent, 'ESP'))
        language_dropdown.add_command(label="Italian",
                                      command=self.change_language(parent, 'ITA'))
        language_dropdown.add_command(label="Portuguese",
                                      command=self.change_language(parent, 'PRT'))

        menubar.add_cascade(label="App", menu=file_dropdown)
        menubar.add_cascade(label="Language", menu=language_dropdown)
        menubar.add_cascade(label="About", menu=about_dropdown)

    def change_language(self, parent, language):
        parent.lang.set_language(language)
        parent.root.update_idletasks()

    @staticmethod
    def show_about_message():
        box_title = "Yt Downloader"
        box_message = "Youtube Video Downloader using Tkinter and Python"
        messagebox.showinfo(box_title, box_message)

    @staticmethod
    def show_release_notes():
        box_title = "Reselase Notes"
        box_message = f"Version {VERSION} - EA"
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
        self.root.geometry("960x320")
        # self.root.title("Yt Video Downloader")
        self.root.title(self.lang.title)
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

        # root is your root window
        self.root.protocol('WM_DELETE_WINDOW', self.prevent_close)

        # def doSomething():
        #    # check if saving
        #    # if not:

    def prevent_close(self):
        '''
        Check if Thread is running then delete it
        :return: None
        '''
        _title = ''
        _message = ''
        if self.global_downloading:
            _title = "App running"
            _message = "The downloader is running"\
                "\n do you want to close the app?"
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

        self.lb_title = Label(
            self.root, text="Welcome to Youtube Video Downloader App",
            font="consolas 14 bold")
        self.lb_title.grid(row=0, column=0, columnspan=3, padx=(10, 20))

        Label(
            self.root, text="Enter the Youtube links bellow",
            font="consolas 11").grid(row=1, column=0)
        Label(
            self.root, text="one link per line", font="Consolas 10").grid(
            row=2, column=0)

        # frame for text wher put the links
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
        self.clear_button = Button(
            self.button_frame, text="clear", command=self.clear_text)
        self.clear_button.grid(row=0, column=0, padx=10)

        self.down_button1 = Button(
            self.button_frame, text="Start download", command=self.launch_down,
            fg="blue")
        self.down_button1.grid(row=0, column=1, padx=10)

        #stop button
        self.button_frame1 = Frame(self.root)
        self.button_frame1.grid(row=4, column=1, padx=10, pady=10)
        self.stop_button1 = Button(
            self.button_frame1, text="Stop download", command=self.stop_download,
            fg="red")
        self.stop_button1.grid(row=0, column=0, padx=10)
        self.stop_button1.grid_remove()

        Label(
            self.root, text="Save videos in:",
            font="Consolas 11").grid(row=1, column=1)

        # frame for path and button
        self.search_frame = Frame(self.root)
        self.search_frame.grid(row=2, column=1, sticky='w', padx=10)
        self.path_saver = Entry(
            self.search_frame, textvariable=self.save_path, width=65)
        self.path_saver.grid(row=0, column=0, sticky='w')
        self.button2 = Button(
            self.search_frame, text="Browse", command=self.browse_button)
        self.button2.grid(row=0, column=1)

        # adding status frame
        self.status_frame = Frame(self.root, bd=1, relief=SUNKEN)
        self.status_frame.grid(
            row=5, column=0, columnspan=3, sticky=W + E, pady=(20, 0))

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
            yscrollcommand=self.scr_deb.set, bg="lightgrey")
        self.scr_deb.config(command=self.my_text1.yview)
        self.scr_deb.pack(side=RIGHT, fill=Y)
        self.deb_frame.grid(row=3, column=1, columnspan=2, padx=10)

        self.my_text1.pack(side=LEFT, fill=BOTH, expand=YES)

        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)

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
        stop download thread and reset all necesary values
        '''
        if not self.ThreadLauncher.stopped():
            self.ThreadLauncher.terminate()
        self.ThreadLauncher.join()
        # reset values
        self.global_downloading = False
        # set message download stopped
        self.status_text.set('Download video stopped')
        # hide stop button
        self.stop_button1.grid_remove()
        return None

    def launch_down(self):
        if self.global_downloading:
            messagebox.showinfo('Running', 'The downloader app is already running')
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
            self.where_save = self.save_path.get()
            self.my_progress.grid_remove()
            download_options = {
                'outtmpl': f'{self.where_save}\%(title)s.%(ext)s',
                'getfilename': '--get-filename',
                '--get-filename': True,
                'progress_hooks': [self.my_hook],
            }
            list_links = self.my_text.get(1.0, END)
            list_down = list_links.splitlines()
            list_down = [line.rstrip('\n') for line in list_down]
            # check for correct links
            c_l = 0
            for v_l in list_down:
                c_l += 1
                if v_l.count('http') > 1:
                    self.status_text.set(f"Url not valid at line: {c_l}")
                    raise RuntimeError(f"Url not valid at line: {c_l}")

            self.v_counter = len(list_down)
            # check if empty list
            if (self.v_counter == 0 or
                    (len(list_down) and list_down[0] == '')):
                self.status_text.set("No videos to download")
                return None
            with youtube_dl.YoutubeDL(download_options) as dl:
                self.my_progress.grid()
                self.stop_button1.grid()
                self.global_downloading = True
                for video_link in list_down:
                    if video_link == '':
                        continue
                    self.v_down += 1
                    dl.download([video_link])
                self.status_text.set(
                    f"All videos downloaded [{self.v_down}/{self.v_counter}]")
            self.global_downloading = False
            self.stop_button1.grid_remove()
            # link.set("Video downloaded successfully")
        except RuntimeError as e:
            self.status_text.set(e)
            pass
        except Exception as e:
            self.status_text.set(e)
            self.global_downloading = False
            # hide stop button
            self.stop_button1.grid_remove()
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
                    'end', f"{self.v_down}) Start video download:"
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
                self.my_text1.insert('end', f"{self.v_down}) Video Downloaded\n")
                self.my_text1.configure(state='disabled')
                # self.percentage.config(
                #    text=f"Downloaded... {self.my_progress['value']}%")
                self.s.configure("LabeledProgressbar",
                                 text=f"{self.my_progress['value']} %      ")
                self.status_text.set(
                    f"Downloaded... [{self.v_down}/{self.v_counter}]")
                self.root.update_idletasks()

            if d['status'] == 'downloading':
                p = d['_percent_str']
                p = p.replace('%', '')
                p = d['_percent_str']
                p = p.replace('%', '')
                percentage = float(p)
                self.my_progress['value'] = percentage
                self.status_text.set(
                    f"Downloading... [{self.v_down}/{self.v_counter}]")
                self.s.configure("LabeledProgressbar",
                                 text=f"{self.my_progress['value']} %      ")
                self.root.update_idletasks()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    root = tk.Tk()
    pt = ytDownloader(root)
    root.mainloop()

