import tkinter as tk
from tkinter import *
from threading import Thread
import os

try:
    import parser

except ValueError:
    print('Failed to import file "parser.py"!')

row = 1.0


def toggle_entry_state():
    if var_tags.get() == 1:
        entry_choice_class.configure(state="normal")
    else:
        entry_choice_class.configure(state="disabled")


def proxy_state():
    if var_proxy.get() == 1:
        entry_choice_proxy_http.configure(state="normal")
        entry_choice_proxy_https.configure(state="normal")
    else:
        entry_choice_proxy_http.configure(state="disabled")
        entry_choice_proxy_https.configure(state="disabled")


def download_images():
    global row

    row += 1
    fr_logs_text.insert(str(row), f'Parsing <{entry_url.get()}>...\n')
    url = entry_url.get()
    form = format_var.get()
    path = None
    headers = None

    if var_tags.get() == 1:
        tags = entry_choice_class.get()
    else:
        tags = None
    if entry_path_save.get() is None:
        path = "parsed_images"
    else:
        path = entry_path_save.get()

    if entry_choice_proxy_https.get() is None or entry_choice_proxy_http.get() is None:
        proxies = None

    else:
        proxies = {"http": entry_choice_proxy_http.get(), "https": entry_choice_proxy_https.get()}
    if parser.check_response(url, proxies=proxies, headers=headers) is None:
        fr_logs_text.insert(str(row), f'Error, code of response: {parser.check_response(url, proxies=proxies, headers=headers).status_code}\n')
        print(parser.check_response(url, proxies=proxies, headers=headers))
    else:
        fr_logs_text.insert(str(row), f'Proxy: {proxies}\n')
        fr_logs_text.insert(str(row), f'Headers: {headers}\n')
        fr_logs_text.insert(str(row), f'Path: {path}\n')
        fr_logs_text.insert(str(row), f'Code of response: {parser.check_response(url, proxies=proxies, headers=headers).status_code}\n')
        fr_logs_text.insert(str(row), f'Downloading images from <{url}>...\n')
        print(parser.check_response(url, proxies=proxies, headers=headers))
        try:
            parser.download_images(url=url, path=path, default_format=form, tags=tags, proxies=proxies, headers=headers)
            fr_logs_text.insert(str(row), f'Parsing <{url}> completed!\n')
        except Exception as e:
            fr_logs_text.insert(str(row), f'Error: {e}\n')
            print(e)


def download_images_thread():
    Thread(target=download_images).start()


root = Tk()
root.geometry('800x500')
root.title('Images Parser by cbFelix')
root.resizable(False, False)
root.iconbitmap(None)

fr_preview = Frame(root, width=796, height=2, borderwidth=1, relief='solid')
fr_preview.pack(side=TOP)

fr_main = Frame(root, width=783, height=145, borderwidth=1, relief='solid')
fr_main.pack(side=TOP, pady=1)
fr_main.grid_propagate(False)

lb_title = Label(fr_preview,
                 text='Image Parser',
                 font=('Arial', 40), width=25)
lb_title.grid(column=2, row=0)

lb_preview_info = Label(fr_preview,
                        text='With this application you can parse all \nthe images from the site, only this applies to all images, \nincluding the logo and so on!',
                        font=('Arial', 12))
lb_preview_info.grid(column=2, row=1)

lb_url_name = Label(fr_main, text='URL: ', width=4, font=('Arial', 12))
lb_url_name.grid(column=1, row=0, padx=3, pady=10)
entry_url = Entry(fr_main, width=50)
entry_url.grid(column=2, row=0, pady=10)

lb_save_path = Label(fr_main, text='Save directory: ', width=15, font=('Arial', 12))
lb_save_path.grid(column=1, row=1, padx=3, pady=10)
entry_path_save = Entry(fr_main, width=50)
entry_path_save.grid(column=2, row=1, pady=10)

lb_parse_path_info = Label(fr_main, name='lb_parse_path', text='*Default: this-directory/parsed_images/', width=35, font=('Arial', 10), fg='gray')
lb_parse_path_info.grid(column=2, row=2, padx=3)

parse_btn = Button(fr_main, name='parse button', text='Parse', command=download_images_thread, width=5, font=('Arial', 10))
parse_btn.grid(column=3, row=0, padx=10, pady=10)

format_var = StringVar(root)
format_var.set("png")
formats = ["png", "jpg", "jpeg", "raw"]
format_menu = OptionMenu(fr_main, format_var, *formats)
format_menu.grid(column=4, row=0, padx=10)

entry_choice_class = Entry(fr_main, width=20, bg='white', state='disabled')
entry_choice_class.grid(column=5, row=1)

var_tags = IntVar()
checkbox_class_allow = Checkbutton(fr_main, text="class", variable=var_tags, command=toggle_entry_state, onvalue=1, offvalue=0)
checkbox_class_allow.grid(column=5, row=0, padx=10)

lb_proxy_https = Label(fr_main, text='http: ', width=4, font=('Arial', 12))
lb_proxy_https.grid(column=4, row=2)
entry_choice_proxy_http = Entry(fr_main, width=20, bg='white', state='disabled')
entry_choice_proxy_http.grid(column=5, row=2)

lb_proxy_https = Label(fr_main, text='https: ', width=4, font=('Arial', 12))
lb_proxy_https.grid(column=4, row=3)
entry_choice_proxy_https = Entry(fr_main, width=20, bg='white', state='disabled')
entry_choice_proxy_https.grid(column=5, row=3)

var_proxy = IntVar()
checkbox_allow_proxy = Checkbutton(fr_main, text="proxy", variable=var_proxy, command=proxy_state, onvalue=1, offvalue=0)
checkbox_allow_proxy.grid(column=3, row=2, padx=10)


fr_console = Frame(root, width=783, height=185, borderwidth=1, relief='solid')
fr_console.pack(side=TOP, pady=1)
fr_console.grid_propagate(False)
fr_console.pack_propagate(False)

lb_logs = Label(fr_console, text='Logs: ', width=10, font=('Arial', 12))
lb_logs.pack()

fr_logs_text = Text(fr_console, width=783, height=185)
fr_logs_text.pack()

fr_footer = Frame(root, width=783, height=50, borderwidth=1, relief='solid')
fr_footer.pack(side=TOP, pady=1)
fr_footer.grid_propagate(False)

lb_about = Label(fr_footer, text='Made by @cbFelix', font=('Arial', 14), width=34)
lb_about.grid(column=0, row=0)
lb_version = Label(fr_footer, text='Version: 1.1', font=('Arial', 14), width=15)
lb_version.grid(column=1, row=0)

root.mainloop()
