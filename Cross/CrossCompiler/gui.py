from tkinter import filedialog, messagebox
from tkinter import *
import paramiko
import os
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import threading

cwd = os.getcwd()
con_part = f"{cwd}\\ui_py_files"
if not os.path.exists(con_part):
    os.mkdir(con_part)


class APP(Tk):
    def __init__(self):
        super().__init__()
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Set window title
        self.title('RASPBERRY_PI_CC')

        self.wm_iconbitmap(f"{cwd}/argatelogo.ico")
        self.resizable(False, False)
        # Set window size
        self.geometry(
            "+{}+{}".format(int((self.winfo_screenwidth()) / 2),
                            int((self.winfo_screenheight()) / 2)))

        # RASPBERRY PI PART
        self._raspberry_host = StringVar(value="192.168.")
        self._raspberry_port = StringVar(value="22")
        self._raspberry_name = StringVar(value="pi")
        self._raspberry_password = StringVar(value="1234")

        label_font_size = 12
        self._host_label = ttk.Label(self, text='HOST : ', font=('Arial Narrow', label_font_size, 'bold'))
        self._port_label = ttk.Label(self, text='PORT : ', font=('Arial Narrow', label_font_size, 'bold'))
        self._name_label = ttk.Label(self, text='USERNAME : ', font=('Arial Narrow', label_font_size, 'bold'))
        self._pw_label = ttk.Label(self, text='PASSWORD : ', font=('Arial Narrow', label_font_size, 'bold'))
        entry_font_size = 12
        self._host_entry = ttk.Entry(self, textvariable=self._raspberry_host,
                                     font=('Arial Narrow', entry_font_size, 'normal'))
        self._port_entry = ttk.Entry(self, textvariable=self._raspberry_port,
                                     font=('Arial Narrow', entry_font_size, 'normal'))
        self._name_entry = ttk.Entry(self, textvariable=self._raspberry_name,
                                     font=('Arial Narrow', entry_font_size, 'normal'))
        self._pw_entry = ttk.Entry(self, textvariable=self._raspberry_password,
                                   font=('Arial Narrow', entry_font_size, 'normal'))

        _rpi_photo = PhotoImage(file="r_pi_logo.png")
        _rpi_photo = _rpi_photo.subsample(4, 4)
        self._filename = StringVar()
        self._rpi_photo_label = Label(self, image=_rpi_photo)
        self._rpi_photo_label.image = _rpi_photo

        self._cur_row = 0
        self.button_explore = Button(self, text="Browse Files",
                                     command=self.browseFiles)

        # This will create style object
        self._but_style = ttk.Style()

        # This will be adding style, and
        # naming that style variable as
        # W.Tbutton (TButton is used for ttk.Button).
        self._but_style.configure('C.TButton', font=('Arial Narrow', entry_font_size, 'bold'))

        self._connect_button = ttk.Button(self, text="CONNECT TO RASPBERRY", style='C.TButton',
                                          command=self.connect)
        self._but_style.configure('D.TButton', font=('Arial Narrow', entry_font_size + 7, 'bold'))
        self._download_button_raspberry = ttk.Button(self, text="DOWNLOAD NECESSARY PACKAGES TO RASPBERRY",
                                                     style='E.TButton', command=self.downloadPackagesRaspberry,
                                                     state=DISABLED)
        self._download_button_comp = ttk.Button(self, text="DOWNLOAD NECESSARY PACKAGES TO COMPUTER",
                                                style='E.TButton', command=self.downloadPackagesComp,
                                                state=DISABLED)
        self._send_file_button = ttk.Button(self, text="DOWNLOAD .UI FILES", style='D.TButton',
                                            command=self.browseFiles, state=DISABLED)
        bg = "#948d92"
        self._console_label = ttk.Label(self, text='CONSOLE', font=('Arial Narrow', 10, 'italic'), foreground="red",
                                        background=bg)
        self._console_clear_button = Button(self, text='CLEAR', font=('Arial Narrow', 8, 'italic'), foreground="yellow",
                                            command=self.clearTextBox, background=bg)
        self._text_box = ScrolledText(self, width=10, height=10, wrap='word', background=bg, fg="white",
                                      font=('Arial Narrow', 8, 'italic'))

    def start(self):
        self.rowconfigure(0, minsize=15)
        self._cur_row += 1
        self._rpi_photo_label.grid(row=self._cur_row, column=0, rowspan=3, columnspan=2, padx=20)
        self._host_label.grid(row=self._cur_row, column=2)
        self._host_entry.grid(row=self._cur_row, column=3)
        self._name_label.grid(row=self._cur_row, column=5)
        self._name_entry.grid(row=self._cur_row, column=6)
        self.columnconfigure(4, minsize=30)
        self._cur_row += 1
        self._port_label.grid(row=self._cur_row, column=2)
        self._port_entry.grid(row=self._cur_row, column=3)
        self._pw_label.grid(row=self._cur_row, column=5)
        self._pw_entry.grid(row=self._cur_row, column=6)
        self._cur_row += 1
        self._connect_button.grid(row=self._cur_row, column=2, columnspan=5, sticky="nswe", ipady=3, pady=5)
        self._cur_row += 1
        self._download_button_raspberry.grid(row=self._cur_row, columnspan=5, rowspan=3, ipady=10,
                                             sticky="nswe", padx=15, pady=3)
        self._cur_row += 3
        self._download_button_comp.grid(row=self._cur_row, columnspan=5, rowspan=3, ipady=10, sticky="nswe", padx=15)
        self._cur_row += 3
        self._send_file_button.grid(row=self._cur_row, columnspan=5, rowspan=5, ipady=30, sticky="nswe", padx=15,
                                    pady=5)
        self._console_label.grid(row=self._cur_row - 6, column=5, sticky="ws")  # column=6, sticky="es"
        self._text_box.grid(row=self._cur_row - 5, column=5, columnspan=2, rowspan=15, ipady=5, sticky="nswe")
        self._console_clear_button.grid(row=self._cur_row - 6, column=6, sticky="e")  # , column=5, sticky="w"
        self.columnconfigure(7, minsize=20)
        self.rowconfigure(self._cur_row+1, minsize=25)
        self.update()
        space_width = (self.winfo_screenwidth() - self.winfo_width()) // 2
        space_height = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f'+{space_width}+{space_height}')
        self.mainloop()

    def connect(self):
        try:
            self.ssh.connect(self._raspberry_host.get(), int(self._raspberry_port.get()),
                             username=self._raspberry_name.get(),
                             password=self._raspberry_password.get())
        except Exception as e:
            self._text_box.insert(INSERT, f"{e}\n")
            self._connect_button['state'] = NORMAL
            messagebox.showerror("FAIL", "THERE IS AN ERROR PLEASE CHECK INFOS")
        else:
            self._connect_button['state'] = DISABLED
            self._download_button_raspberry['state'] = NORMAL
            self._download_button_comp['state'] = NORMAL
            self._send_file_button['state'] = NORMAL
            messagebox.showinfo("SUCCESS", "SUCCESSFULLY CONNECTED TO SERVER")

    def clearTextBox(self):
        self._text_box.delete(1.0, 'end')

    # file explorer window
    def browseFiles(self):
        self._text_box.insert(INSERT, f"PLEASE WAIT\n")

        def sendFile():
            self._filename = filedialog.askopenfilename(initialdir="/",
                                                        title="Select .ui File",
                                                        filetypes=(("User Interfaces", "*.ui"),))

            original = self._filename
            filename = self._filename.split("/")[-1]
            target = f'{cwd}\\ui_py_files\\{filename[:-3]}'
            stream = os.system(f'pyuic5 -x {original} -o {target}.py')

            self.ssh.exec_command("cd Desktop && mkdir QTFiles")

            ftp_client = self.ssh.open_sftp()
            ftp_client.chdir("/home/pi/Desktop/QTFiles")

            ftp_client.put(f"{cwd}\\ui_py_files\\{filename[:-3]}.py", f"{filename[:-3]}.py")
            ftp_client.close()
            del ftp_client
            self.ssh.exec_command("cd")
            self.ssh.exec_command(f"cd Desktop/QTFiles && DISPLAY=:0.0 python3 {filename[:-3]}.py")
            self._text_box.insert(INSERT, f"INFORMATION MSG : \nFILE SENT!\n")

        t1 = threading.Thread(target=sendFile, daemon=True)
        t1.start()

    def downloadPackagesRaspberry(self):
        self._text_box.insert(INSERT, f"PLEASE WAIT\n")

        def dp():
            stdin, stdout, stderr = self.ssh.exec_command("sudo apt-get install python3-pyqt5 -y --force-yes")
            for line in stdout.readlines():
                self._text_box.insert(INSERT, f"{line}")
            del stdin, stdout, stderr
            self._text_box.insert(INSERT, f"INFORMATION MSG : \nPACKAGES DOWNLOADED!!! SUCCESS\n")

        t1 = threading.Thread(target=dp, daemon=True)
        t1.start()

    def downloadPackagesComp(self):
        self._text_box.insert(INSERT, f"PLEASE WAIT\n")

        def dp():
            os.system(f'pip3 install PyQt5')
            os.system(f'pip3 install pyuic5-tool')
            os.system(f'pip3 install pyqt5-tools')
            self._text_box.insert(INSERT, f"INFORMATION MSG : \nPACKAGES DOWNLOADED!!! SUCCESS\n")

        t1 = threading.Thread(target=dp, daemon=True)
        t1.start()

    def __del__(self):
        self.ssh.close()


app = APP()
app.start()
