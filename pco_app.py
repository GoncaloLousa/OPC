from tkinter import *
import scipy.stats as st
import math
import webbrowser

# Functions
# Newsboy Window
newsboy_fields = ("Cost", "Price sold", "Salvage Value", "Mean", "Standard Deviation")
multiperiod_fields = (
    "Cost", "Order cost", "Interest Rate", "Lead Time", "Mean", "Standard Deviation", "Normal Dist. Time", "p")


# Create newsboy window when commanded
def newsboy_window():
    entries = {}
    newsboy_wd = Toplevel(menu_inicial)
    newsboy_wd.title("Newsboy Model")
    newsboy_wd.geometry("+%d+%d" % (screen_x, screen_y))
    newsboy_wd.iconbitmap(r"usd_icon.ico")
    for field in newsboy_fields:
        frame_newsboy1 = Frame(newsboy_wd)
        lab = Label(frame_newsboy1, width=22, text=field + ": ", anchor='w')
        ent = Entry(frame_newsboy1)
        frame_newsboy1.pack(side=TOP,
                            fill=X,
                            padx=5,
                            pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT,
                 expand=YES,
                 fill=X)
        entries[field] = ent
    calc_button = Button(newsboy_wd, text="Calculate", command=lambda: newsboymain(entries, newsboy_wd))
    calc_button.pack(side=LEFT, padx=20)
    return entries, newsboy_wd


# Calculate Newsboy Model when commanded
def newsboymain(entries, newsboy_wd):
    cost = float(entries['Cost'].get())
    price = float(entries['Price sold'].get())
    salvage = float(entries['Salvage Value'].get())
    mean = float(entries['Mean'].get())
    sd = float(entries['Standard Deviation'].get())

    underage_costs = price - cost
    overage_costs = cost - salvage
    fq = underage_costs / (underage_costs + overage_costs)
    z = st.norm.ppf(fq)
    quantity = sd * z + mean

    print("The optimal quantity to order is: {0}".format(round(quantity)))
    result_newsboy = Label(newsboy_wd, width=22, text="Optimal quantity : {0}".format(round(quantity)))
    result_newsboy.pack(side=BOTTOM)


# Create Multiple Periods window when commanded
def multiperiod_window():
    entries_multi = {}
    multiperiod_wd = Toplevel(menu_inicial)
    multiperiod_wd.title("Multiple Periods Model")
    multiperiod_wd.geometry("+%d+%d" % (screen_x, screen_y))
    multiperiod_wd.iconbitmap(r"usd_icon.ico")
    for field in multiperiod_fields:
        frame_multi1 = Frame(multiperiod_wd)
        lab = Label(frame_multi1, width=22, text=field + ": ", anchor='w')
        ent = Entry(frame_multi1)
        frame_multi1.pack(side=TOP,
                          fill=X,
                          padx=5,
                          pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT,
                 expand=YES,
                 fill=X)
        entries_multi[field] = ent
    calc_button = Button(multiperiod_wd, text="Calculate", command=lambda: multiperiods(entries_multi, multiperiod_wd))
    calc_button.pack(side=LEFT, padx=20)
    return entries_multi, multiperiod_wd


# Calculate Multiple Periods Model when commanded
def multiperiods(entries_multi, multiperiod_wd):
    cost = float(entries_multi['Cost'].get())
    order_cost = float(entries_multi['Order cost'].get())
    int_rate = float(entries_multi['Interest Rate'].get())
    lead_time = float(entries_multi['Lead Time'].get())
    mean = float(entries_multi['Mean'].get())
    sd = float(entries_multi['Standard Deviation'].get())
    normal_time = float(entries_multi['Normal Dist. Time'].get())
    p = float(entries_multi['p'].get())

    if normal_time != lead_time:
        new_mean = mean * (normal_time / (normal_time / lead_time))
        new_sd = math.sqrt((sd * sd) * (normal_time / (normal_time / lead_time)))

    else:
        new_mean = mean
        new_sd = sd

    tau = lead_time / 12
    gama = new_mean / tau
    holding_cost = int_rate * cost

    q_zero = math.sqrt((2 * order_cost * gama) / holding_cost)
    f_zero = 1 - ((q_zero * holding_cost) / (p * gama))
    z_zero = st.norm.ppf(f_zero)
    r_zero = new_sd * z_zero + new_mean
    lz_zero = st.norm.pdf(z_zero) - z_zero * (1 - st.norm.cdf(z_zero))
    n_rzero = new_sd * lz_zero

    n_rnew = n_rzero
    old_q = q_zero
    new_q = 0

    while abs(new_q - old_q) >= 2:
        n_rold = n_rnew
        old_q = new_q
        new_q = math.sqrt((2 * gama * (order_cost + p * n_rold)) / holding_cost)
        f_new = 1 - ((new_q * holding_cost) / (p * gama))
        z_new = st.norm.ppf(f_new)
        r_new = new_sd * z_new + new_mean
        lz_new = st.norm.pdf(z_new) - z_new * (1 - st.norm.cdf(z_new))
        n_rnew = new_sd * lz_new

        if abs(new_q - old_q) <= 2:
            break

    print("This is the optimal order quantity: {0}".format(round(new_q)))
    print("This is the optimal reorder point: {0}".format(round(r_new)))
    result_multi = Label(multiperiod_wd,
                         text="Optimal order quantity : {0} \n Reorder point: {1}".format(round(new_q), round(r_new)))
    result_multi.pack(side=BOTTOM)

# About page
def about_window():
    about_wd = Toplevel(menu_inicial)
    about_wd.title("About")
    about_wd.geometry("+%d+%d" % (screen_x, screen_y))
    about_wd.iconbitmap(r"usd_icon.ico")
    frame_ini = Frame(about_wd)
    frame1 = Frame(about_wd)
    frame2 = Frame(about_wd)
    frame3 = Frame(about_wd)
    frame4 = Frame(about_wd)
    ini_text = Message(frame_ini, text="--> Please use decimal points with '.' in input boxes.\n\nLearn more:")
    info_text2 = Message(frame1, text="\n\nHow to use the Newsboy model (my youtube video): ", font="Calibri 10", justify=LEFT)
    info_text3 = Message(frame2, text="\n\nThe Multi Period Model (optimal Order qtty and Reorder point - my youtube video):", font="Calibri 10", justify=LEFT)
    info_text4 = Message(frame3, text="\n\nCode on my Github page:",font="Calibri 10", justify=LEFT)
    last_text = Message(frame4, text="\n\nThank you for using the program", font="Calibri 10", justify=LEFT)
    botao_1 = Button(frame1, text="Newsboy Model", font="Calibri 10", bd=5, relief="raised", anchor=CENTER, command=newsboy_video)
    botao_2 = Button(frame2, text="Multi Period Model", font="Calibri 10", bd=5, relief="raised", anchor=CENTER, command=multi_video)
    botao_3 = Button(frame3, text="Github", font="Calibri 10", bd=5, relief="raised", anchor=CENTER, command=githublink)

    frame_ini.pack(side=TOP, fill=X, padx=5, pady=5)
    ini_text.pack(side=LEFT, fill=X, padx=5, pady=5)
    frame1.pack(side=TOP, fill=X, padx=5, pady=5)
    info_text2.pack(pady=5, padx=5, side=LEFT)
    botao_1.pack(pady=5, padx=5, side=RIGHT)

    frame2.pack(side=TOP, fill=X, padx=5, pady=5)
    info_text3.pack(pady=5, padx=5, side=LEFT)
    botao_2.pack(pady=5, padx=5, side=RIGHT)
    frame3.pack(side=TOP, fill=X, padx=5, pady=5)
    info_text4.pack(pady=5, padx=5, side=LEFT)
    botao_3.pack(pady=5, padx=5, side=RIGHT)
    frame4.pack(side=TOP, fill=X)
    last_text.pack(pady=5, padx=5, side=BOTTOM)

def newsboy_video():
    webbrowser.open("https://www.youtube.com/watch?v=GpAwCkJBhHI&t=5s&ab_channel=Gon%C3%A7aloLousa")

def multi_video():
    webbrowser.open("https://www.youtube.com/watch?v=Lu9ImEYsudw&t=7s&ab_channel=Gon%C3%A7aloLousa")

def githublink():
    webbrowser.open("https://github.com/GoncaloLousa/OPC")


# Main Window settling
menu_inicial = Tk()
menu_inicial.title("PCO")
WIDTH = 600
HEIGHT = 400
screen_width = menu_inicial.winfo_screenwidth()
screen_height = menu_inicial.winfo_screenheight()
screen_x = screen_width / 2 - WIDTH / 2
screen_y = screen_height / 2 - HEIGHT / 2 - 100
menu_inicial.geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, screen_x, screen_y))
menu_inicial.resizable(True, True)

# Styling
menu_inicial['bg'] = "#FFFFE7"
menu_inicial.iconbitmap(r"usd_icon.ico")

# buttons and labels
botao_1 = Button(menu_inicial,
                 text="Newsboy Model",
                 font="Calibri 10",
                 bd=5,
                 relief="raised",
                 anchor=CENTER, command=newsboy_window)
botao_1.pack(pady=40)

botao_2 = Button(menu_inicial,
                 text="Multi Periods Model",
                 font="Calibri 10",
                 bd=5,
                 relief="raised",
                 anchor=CENTER,
                 command=multiperiod_window)
botao_2.pack(pady=40)

botao_3 = Button(menu_inicial,
                 text="About",
                 font="Calibri 10",
                 bd=5,
                 relief="raised",
                 anchor=CENTER,
                 command=about_window)
botao_3.pack(pady=40)

menu_inicial.mainloop()