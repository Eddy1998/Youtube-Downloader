#!/usr/cbin/env python3
'''
Created on 11 dic 2020

@author: Eddy
'''
from __future__ import unicode_literals
import os
# importing tkinter
from tkinter import *
from tkinter import ttk
# importing YouTube module
import youtube_dl
from datetime import datetime
import time
from tkinter.ttk import Style
import threading

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

VERSION = '0.1'


class DownloaderThread(threading.Thread):
    '''
    Thread class with a stop() method
    The thread itself has to check regularly fot the stopped() contition
    '''
    def __init__(self, *args, **kwargs):
        super(DownloaderThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.launched = True

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while True:
            if self.stopped():
                return
            if self.launched:
                pass


class Menubar:

    def __init__(self, parent):
        font_specs = ('ubuntu', 11)

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

        menubar.add_cascade(label="App", menu=file_dropdown)
        menubar.add_cascade(label="About", menu=about_dropdown)

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
        self.root.geometry("960x320")
        self.root.title("Yt Video Downloader")
        self.root.resizable(False, False)
        self.init_objects()
        self.v_counter = 0
        self.v_down = 0

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
                if not self.ThreadLauncher.stopped():
                    self.ThreadLauncher.stop()
                self.root.destroy()
            else:
                return None
        self.root.destroy()

        # messagebox.showinfo('Running', 'The downloader app is already running')
        # root.destroy()

    def reset_values(self):
        self.v_counter = 0
        self.v_down = 0

    def init_objects(self):
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
            yscrollcommand=self.my_scroll.set)
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
            self.search_frame, textvariable=self.save_path, width=50)
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
        print(self.ThreadLauncher.stopped())
        if not self.ThreadLauncher.stopped():
            print(self.ThreadLauncher.stop())
        # set message download stopped
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
            # print("path where to save %s" % self.where_save)
            download_options = {
                'outtmpl': f'{self.where_save}\%(title)s.%(ext)s',
                'getfilename': '--get-filename',
                '--get-filename': True,
                'progress_hooks': [self.my_hook],
            }
            # myVar.set("Downloading...")
            # root.update()
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
            # print(self.v_counter)
            # print(list_down)
            if (self.v_counter == 0 or
                    (len(list_down) and list_down[0] == '')):
                self.status_text.set("No videos to download")
                return None
            # print(list_links)
            with youtube_dl.YoutubeDL(download_options) as dl:
                self.my_progress.grid()
                self.stop_button1.grid()
                self.global_downloading = True
                for video_link in list_down:
                    if video_link == '':
                        continue
                    # create_progress(my_text1)
                    # message_fin.set("")
                    self.v_down += 1
                    dl.download([video_link])
                self.status_text.set(
                    f"All videos downloaded [{self.v_down}/{self.v_counter}]")
            self.global_downloading = False
            self.stop_button1.grid_remove()
            # link.set("Video downloaded successfully")
        except RuntimeError as e:
            # message_fin.set(e)
            pass
        except Exception as e:
            print(e)
            # myVar.set("Mistake")
            # root.update()
            # message_fin.set("Error downloading Video")
            pass
            # link.set("Enter correct link")

    def my_hook(self, d):
        try:
            # global percentage, curr_progress_bar
            file_tuple = os.path.split(os.path.abspath(d['filename']))
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
                # curr_progress_bar['value'] = 100
                # curr_progress_text.config(
                #    text=f"Downloaded... [{v_down}/{v_counter}] {curr_progress_bar['value']}% \n")

                # print("Done downloading {}".format(file_tuple[1]))
            if d['status'] == 'downloading':
                p = d['_percent_str']
                p = p.replace('%', '')
                # my_progress.setValue(float(p))
                p = d['_percent_str']
                p = p.replace('%', '')
                # if float(p) >= percentage + 2:
                percentage = float(p)
                self.my_progress['value'] = percentage
                # curr_progress_bar['value'] = percentage
                # self.curr_progress_text.config(
                #    text=f"Downloading... [{v_down}/{v_counter}] {curr_progress_bar['value']}%")
                # self.percentage.config(
                #    text=f"Downloading... {self.my_progress['value']}%")
                self.status_text.set(
                    f"Downloading... [{self.v_down}/{self.v_counter}]")
                self.s.configure("LabeledProgressbar",
                                 text=f"{self.my_progress['value']} %      ")
                #    self.my_text1.configure(state='normal')
                #    self.my_text1.insert('end', f"downloading {file_tuple[1]}")
                #    self.my_text1.configure(state='disabled')

                self.root.update_idletasks()
                # print("down %s" % str())
                # print(d['_percent_str'])
                # print(d['filename'], d['_percent_str'], d['_eta_str'])
        except Exception as e:
            print(e)


if __name__ == "__main__":
    root = tk.Tk()
    pt = ytDownloader(root)
    root.mainloop()

