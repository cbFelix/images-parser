import tkinter as tk
from tkinter import *

try:
    import parser

except:
    print('Failed to import file "parser.py"!')

row = 1.0


def download_images():
    global row
    row += 1
    fr_logs_text.insert(str(row), f'{parser.check_response(entry_url.get())}\n')
    print(parser.check_response(entry_url.get()))
    url = entry_url.get()
    form = format_var.get()
    if entry_path_save.get() is None:
        path = "parsed_images"
    else:
        path = entry_path_save.get()
    parser.download_images(url, path, format_save=form)


root = Tk()
root.geometry('800x500')
root.title('Images Parser by cbFelix')
root.resizable(False, False)

fr_preview = Frame(root, width=796, height=2, borderwidth=1, relief='solid')
fr_preview.pack(side=TOP)

fr_main = Frame(root, width=783, height=130, borderwidth=1, relief='solid')
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

parse_btn = Button(fr_main, name='parse button', text='Parse', command=download_images, width=5, font=('Arial', 10))
parse_btn.grid(column=3, row=0, padx=10, pady=10)

format_var = StringVar(root)
format_var.set("png")
formats = ["png", "jpg", "jpeg", "raw"]
format_menu = OptionMenu(fr_main, format_var, *formats)
format_menu.grid(column=4, row=0, padx=10)

fr_console = Frame(root, width=783, height=200, borderwidth=1, relief='solid')
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

lb_about = Label(fr_footer, text='Made by Victor "@cbFelix" Lebedev', font=('Arial', 14), width=34)
lb_about.grid(column=0, row=0)
lb_version = Label(fr_footer, text='Version: 1.0', font=('Arial', 14), width=15)
lb_version.grid(column=1, row=0)

root.mainloop()
