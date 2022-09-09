import sys
import tkinter as tk
import decimal

# Form
form = tk.Tk()
form.title("Calice")
form.iconphoto(False, tk.PhotoImage(file = "calc.png"))
form.configure(background = "LightSteelBlue")
form.resizable(False, False)
form.geometry("330x448")

# Variable_Switch
set_ab = set_value = oprd_change = fnshd = error = debug_mode = debug_msg_lock = False

# Variable_Ctrl
oprt, dot_ctrl = "null", "0"
oou_ctrl = tk.IntVar()

# Variable_Value
a = b = m = "0"

# Variable_Other
Screen_Text = tk.StringVar()

# Function
def Show_debug_msg(i):
    global debug_msg_lock

    if (debug_mode and (not debug_msg_lock)):
        print("\n" + i + "\n\n" + "set_ab = " + str(set_ab) + ", set_value = " + str(set_value) + ", oprd_change = " + str(oprd_change))
        print("fnshd = " + str(fnshd) + ", error = " + str(error) + "\n")
        print("oprt = " + oprt + ", oou_ctrl = " + str(oou_ctrl.get()) + ", dot_ctrl = " + dot_ctrl + "\n")
        print("a = " + a + ", b = " + b + ", m = " + m + "\n")
    debug_msg_lock = False

def Show(i):
    Screen_Text.set((a + " ") if (not oprd_change) else (b + " "))
    Show_debug_msg(i)

def Execution(i):
    global set_ab, set_value, oprd_change, error, oprt, a, b
    step = "n"

    if (i == "c"):
        set_ab = set_value = False
        if (((decimal.Decimal(a) > decimal.Decimal("0")) or (decimal.Decimal(a) < decimal.Decimal("0"))) or (oprt != "pow") or (decimal.Decimal(b) > decimal.Decimal("0"))):
            try:
                if (oprt == "add"):
                    a = str(decimal.Decimal(a) + decimal.Decimal(b))
                elif (oprt == "sub"):
                    a = str(decimal.Decimal(a) - decimal.Decimal(b))
                elif (oprt == "mul"):
                    a = str(decimal.Decimal(a) * decimal.Decimal(b))
                elif (oprt == "div"):
                    a = str(decimal.Decimal(a) / decimal.Decimal(b))
                elif (oprt == "pow"):
                    a = str(decimal.Decimal(a) ** int(float(b)))
                b = "0"
                if (not fnshd):
                    step = "a" if (len(a) <= 13) else "e"
                else:
                    oprd_change, oprt = False, "null"
                    step = "f"
            except:
                # a/0 error
                step = "e"
        else:
            # 0 pow (0, -b) error
            step = "e"
    if ((i == "f") or (step == "f")):
        # 0 -> out
        # 1 -> up
        # 2 -> 4 out 5 up
        if ((not oprd_change) and (oou_ctrl.get() == 0)):
            a = str(decimal.Decimal(a).quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_DOWN))
        elif ((not oprd_change) and (oou_ctrl.get() == 1)):
            a = str(decimal.Decimal(a).quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_UP))
        elif ((not oprd_change) and (oou_ctrl.get() == 2)):
            a = str(decimal.Decimal(a).quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_HALF_UP))
        elif (oprd_change and (oou_ctrl.get() == 0)):
            b = str(decimal.Decimal(b).quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_DOWN))
        elif (oprd_change and (oou_ctrl.get() == 1)):
            b = str(decimal.Decimal(b).quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_UP))
        elif (oprd_change and (oou_ctrl.get() == 2)):
            b = str(decimal.Decimal(b).quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_HALF_UP))
        if fnshd:
            step = "a" if (len(a) <= 13) else "e"
    if ((i == "e") or (step == "e")):
        error = True
        Screen_Text.set("E ")
    if (step == "a"):
        Screen_Text.set(a + " ")
    Show_debug_msg("Hello World!")

def Rst():
    global set_ab, set_value, fnshd, a, b

    set_ab = True
    if (set_value or fnshd):
        set_value = fnshd = False
        if (not oprd_change):
            a = "0"
        else:
            b = "0"

# Function_Scale
def Scale_dot_value_change(i):
    global dot_ctrl

    if int(i) == 0:
        dot_ctrl = "0"
    else:
        dot_ctrl = ("0." + ("0" * int(i)))
    Show_debug_msg(str(i))

# Function_Button
def Button_function_clck(i):
    global set_ab, set_value, oprd_change, fnshd, error, oprt, a, b

    if (i == "c"):
        set_ab, set_value, oprd_change, fnshd, error, oprt, a, b = False, False, False, False, False, "null", "0", "0"
        Show(i)
    elif ((not error) and (i == "bs")):
        if (not oprd_change):
            a = a[:-1]
            if (a == ""):
                a = "0"
        else:
            b = b[:-1]
            if (b == ""):
                b = "0"
        Show(i)
    elif ((not error) and (i == "pon")):
        if (not oprd_change):
            if ((decimal.Decimal(a) > decimal.Decimal("0")) or (decimal.Decimal(a) < decimal.Decimal("0"))):
                a = str(decimal.Decimal(a) * decimal.Decimal("-1"))
        else:
            if ((decimal.Decimal(b) > decimal.Decimal("0")) or (decimal.Decimal(b) < decimal.Decimal("0"))):
                b = str(decimal.Decimal(b) * decimal.Decimal("-1"))
        Show(i)
    elif ((not error) and (i == "sqrt")):
        set_value = True
        try:
            if (not oprd_change):
                a = str(decimal.Decimal(a).sqrt())
            else:
                b = str(decimal.Decimal(b).sqrt())
            Execution("f")
            Show(i)
        except:
            # (-a).sqrt() or (-b).sqrt() error
            Execution("e")
    elif ((not error) and (i == "dot")):
        Rst()
        if ((not oprd_change) and (len(a) < 12)):
            if (not ("." in a)):
                a += "."
        elif (oprd_change and (len(b) < 12)):
            if (not ("." in b)):
                b += "."
        Show(i)
    elif ((not error) and (i == "equ")):
        fnshd = True
        Execution("c")

def Button_function_m_clck(i):
    global set_value, debug_msg_lock, a, b, m

    if (i == "mc"):
        m = "0"
    elif ((not error) and (i == "mr")):
        Rst()
        set_value = debug_msg_lock = True
        if (not oprd_change):
            a = m
        else:
            b = m
        Show("Hello World!")
    elif ((not error) and (i == "msub") and (not oprd_change)):
        m = str(decimal.Decimal(m) - decimal.Decimal(a))
    elif ((not error) and (i == "msub") and oprd_change):
        m = str(decimal.Decimal(m) - decimal.Decimal(b))
    elif ((not error) and (i == "madd") and (not oprd_change)):
        m = str(decimal.Decimal(m) + decimal.Decimal(a))
    elif ((not error) and (i == "madd") and oprd_change):
        m = str(decimal.Decimal(m) + decimal.Decimal(b))
    Show_debug_msg(i)

def Button_oprt_clck(i):
    global set_ab, set_value, oprd_change, fnshd, debug_msg_lock, oprt

    if (not error):
        fnshd = False
        if (not oprd_change):
            set_ab, set_value, oprd_change = False, False, True
        elif (oprd_change and set_ab):
            debug_msg_lock = True
            Execution("c")
        if (not error):
            oprt = i
        Show_debug_msg(i)

def Button_number_clck(i):
    global a, b

    if (not error):
        Rst()
        if ((not oprd_change) and (len(a) < 13)):
            if (a == "0"):
                a = ""
            a += i
        elif (oprd_change and (len(b) < 13)):
            if (b == "0"):
                b = ""
            b += i
        Show(i)

# Screen
label_Screen = tk.Label(form, anchor = "e", bd = 1, bg = "AliceBlue", fg = "Black", font = ("Noto Sans", 21), relief = "sunken", textvariable = Screen_Text)

label_Screen.place(x = 6, y = 6, width = 237, height = 50)

Show("Hello World!")

# Scale
scale_OutOrUp = tk.Scale(form, activebackground = "LightSteelBlue", bd = 2.5, bg = "LightSteelBlue", command = Show_debug_msg, fg = "Black", font = ("Noto Sans", 13), orient = "horizontal", showvalue = False, tickinterval = 1, to = 2, troughcolor = "Black", variable = oou_ctrl)
scale_Dot = tk.Scale(form, activebackground = "LightSteelBlue", bd = 2.5, bg = "LightSteelBlue", command = Scale_dot_value_change, fg = "Black", font = ("Noto Sans", 13), orient = "horizontal", showvalue = False, tickinterval = 1, to = 3, troughcolor = "Black")

scale_OutOrUp.place(x = 6, y = 62, width = 156)
scale_Dot.place(x = 168, y = 62, width = 156)

scale_OutOrUp.set(2)

# Button_Function
button_BS = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "bs": Button_function_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "<-")
button_C = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "c": Button_function_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "C")
button_PosOrNeg = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "pon": Button_function_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "+/-")
button_Sqrt = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "sqrt": Button_function_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "sqrt")
button_Dot = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "dot": Button_function_clck(x), fg = "Black", font = ("Noto Sans", 24), text = ".")
button_Equ = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "equ": Button_function_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "=")

button_BS.place(x = 249, y = 6, width = 75, height = 50)
button_C.place(x = 6, y = 112, width = 75, height = 50)
button_PosOrNeg.place(x = 87, y = 112, width = 75, height = 50)
button_Sqrt.place(x = 168, y = 112, width = 75, height = 50)
button_Dot.place(x = 87, y = 392, width = 75, height = 50)
button_Equ.place(x = 168, y = 392, width = 75, height = 50)

# Button_Function_M
button_MC = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "mc": Button_function_m_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "MC")
button_MR = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "mr": Button_function_m_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "MR")
button_MSub = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "msub": Button_function_m_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "M-")
button_MAdd = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "madd": Button_function_m_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "M+")

button_MC.place(x = 6, y = 168, width = 75, height = 50)
button_MR.place(x = 87, y = 168, width = 75, height = 50)
button_MSub.place(x = 168, y = 168, width = 75, height = 50)
button_MAdd.place(x = 249, y = 168, width = 75, height = 50)

# Button_Oprt
button_Pow = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "pow": Button_oprt_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "^")
button_Div = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "div": Button_oprt_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "/")
button_Mul = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "mul": Button_oprt_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "*")
button_Sub = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "sub": Button_oprt_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "-")
button_Add = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "add": Button_oprt_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "+")

button_Pow.place(x = 249, y = 112, width = 75, height = 50)
button_Div.place(x = 249, y = 224, width = 75, height = 50)
button_Mul.place(x = 249, y = 280, width = 75, height = 50)
button_Sub.place(x = 249, y = 336, width = 75, height = 50)
button_Add.place(x = 249, y = 392, width = 75, height = 50)

# Button_Number
button_7 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "7": Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "7")
button_8 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "8": Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "8")
button_9 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "9": Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "9")
button_4 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "4": Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "4")
button_5 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "5": Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "5")
button_6 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "6": Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "6")
button_1 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "1": Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "1")
button_2 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "2": Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "2")
button_3 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "3": Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "3")
button_0 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "0": Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "0")

button_7.place(x = 6, y = 224, width = 75, height = 50)
button_8.place(x = 87, y = 224, width = 75, height = 50)
button_9.place(x = 168, y = 224, width = 75, height = 50)
button_4.place(x = 6, y = 280, width = 75, height = 50)
button_5.place(x = 87, y = 280, width = 75, height = 50)
button_6.place(x = 168, y = 280, width = 75, height = 50)
button_1.place(x = 6, y = 336, width = 75, height = 50)
button_2.place(x = 87, y = 336, width = 75, height = 50)
button_3.place(x = 168, y = 336, width = 75, height = 50)
button_0.place(x = 6, y = 392, width = 75, height = 50)

# Main
if ((len(sys.argv) == 2) and (sys.argv[1] == "debug")):
    debug_mode = True
form.mainloop()