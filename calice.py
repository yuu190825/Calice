import sys
import tkinter as tk
import decimal

# Ready to 3.0

# Form
form = tk.Tk()
form.title("Calice")
form.iconphoto(False, tk.PhotoImage(file = "./rec/calc.png"))
form.configure(background = "LightSteelBlue")
form.resizable(False, False)
form.geometry("330x454")

# Variable_Switch
set_ab = set_value = oprd_change = fnshd = error = dot_mode = debug_mode = debug_msg_lock = False

# Variable_Ctrl
oprt = "null"
oou_ctrl, dot_ctrl = 2, '0'

# Variable_Value
a = b = m = decimal.Decimal('0')
dot, dot_count = decimal.Decimal('0.1'), '0.0'

# Variable_Other
Screen_Text = tk.StringVar()

# Function
def Show_debug_msg():
    global debug_msg_lock

    if (debug_mode and (not debug_msg_lock)):
        print("\n" + "set_ab = " + str(set_ab) + ", set_value = " + str(set_value) + ", oprd_change = " + str(oprd_change))
        print("fnshd = " + str(fnshd) + ", error = " + str(error) + ", dot_mode = " + str(dot_mode) + "\n")
        print("oprt = " + oprt + ", oou_ctrl = " + str(oou_ctrl) + ", dot_ctrl = " + dot_ctrl + "\n")
        print("a = " + str(a) + ", b = " + str(b) + ", m = " + str(m))
        print("dot = " + str(dot) + ", dot_count = " + dot_count + "\n")
    debug_msg_lock = False

def Show():
    if (((not dot_mode) or (dot_mode and (dot < decimal.Decimal('0.1'))))):
        Screen_Text.set((str(a) + " ") if (not oprd_change) else (str(b) + " "))
    elif (dot_mode and (dot == decimal.Decimal('0.1'))):
        Screen_Text.set((str(a) + ". ") if (not oprd_change) else (str(b) + ". "))
    Show_debug_msg()

def Execution(i):
    global set_ab, set_value, oprd_change, error, dot_mode, oprt, a, b, dot, dot_count
    step = "n"

    if (i == "c"):
        set_ab, set_value, dot_mode, dot, dot_count = False, False, False, decimal.Decimal('0.1'), '0.0'
        try:
            if (oprt == "add"):
                a += b
            elif (oprt == "sub"):
                a -= b
            elif (oprt == "mul"):
                a *= b
            elif (oprt == "div"):
                a /= b
            elif (oprt == "pow"):
                a = a ** b
            b = decimal.Decimal('0')
            if (not fnshd):
                step = "a" if (len(str(a)) <= 13) else "e"
            else:
                oprd_change, oprt = False, "null"
                step = "f"
        except:
            # a/0 error
            step = "e"
    if ((i == "f") or (step == "f")):
        # 0 -> out
        # 1 -> up
        # 2 -> 4 out 5 up
        if ((not oprd_change) and (oou_ctrl == 0)):
            a = a.quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_DOWN)
        elif ((not oprd_change) and (oou_ctrl == 1)):
            a = a.quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_UP)
        elif ((not oprd_change) and (oou_ctrl == 2)):
            a = a.quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_HALF_UP)
        elif (oprd_change and (oou_ctrl == 0)):
            b = b.quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_DOWN)
        elif (oprd_change and (oou_ctrl == 1)):
            b = b.quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_UP)
        elif (oprd_change and (oou_ctrl == 2)):
            b = b.quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_HALF_UP)
        if fnshd:
            step = "a" if (len(str(a)) <= 13) else "e"
    if ((i == "e") or (step == "e")):
        error = True
        Screen_Text.set("E ")
    if (step == "a"):
        Screen_Text.set(str(a) + " ")
    Show_debug_msg()

def Rst():
    global set_ab, set_value, fnshd, a, b

    set_ab = True
    if (set_value or fnshd):
        set_value = fnshd = False
        if (not oprd_change):
            a = decimal.Decimal('0')
        else:
            b = decimal.Decimal('0')

# Function_Scale
def Scale_oou_value_change(i):
    global oou_ctrl

    oou_ctrl = int(i)
    Show_debug_msg()

def Scale_dot_value_change(i):
    global dot_ctrl

    if int(i) == 0:
        dot_ctrl = '0'
    else:
        dot_ctrl = ('0.' + ('0' * int(i)))
    Show_debug_msg()

# Function_Button
def Button_function_clck(i):
    global set_ab, set_value, oprd_change, fnshd, error, dot_mode, oprt, a, b, dot, dot_count

    if (i == "c"):
        set_ab, set_value, oprd_change, fnshd, error, dot_mode, oprt, a, b, dot, dot_count = False, False, False, False, False, False, "null", decimal.Decimal('0'), decimal.Decimal('0'), decimal.Decimal('0.1'), '0.0'
        Show()
    elif ((not error) and (i == "bs")):
        if (dot_mode and (dot_count != '0.0')):
            dot, dot_count = (dot / decimal.Decimal('0.1')), dot_count[:-1]
            if (not oprd_change):
                a = a.quantize(decimal.Decimal(dot_count[:-1]), rounding = decimal.ROUND_DOWN)
            else:
                b = b.quantize(decimal.Decimal(dot_count[:-1]), rounding = decimal.ROUND_DOWN)
        elif (dot_mode and (dot_count == '0.0')):
            dot_mode = False
            if (not oprd_change):
                a = a.quantize(decimal.Decimal('0'), rounding = decimal.ROUND_DOWN)
            else:
                b = b.quantize(decimal.Decimal('0'), rounding = decimal.ROUND_DOWN)
        elif ((not dot_mode) and (not oprd_change)):
            a /= decimal.Decimal('10')
            a = a.quantize(decimal.Decimal('0'), rounding = decimal.ROUND_DOWN)
        elif ((not dot_mode) and oprd_change):
            b /= decimal.Decimal('10')
            b = b.quantize(decimal.Decimal('0'), rounding = decimal.ROUND_DOWN)
        Show()
    elif ((not error) and (i == "pon")):
        if (not oprd_change):
            if (a != decimal.Decimal('0')):
                a *= decimal.Decimal('-1')
        else:
            if (b != decimal.Decimal('0')):
                b *= decimal.Decimal('-1')
        Show()
    elif ((not error) and (i == "sqrt")):
        set_value, dot_mode, dot, dot_count = True, False, decimal.Decimal('0.1'), '0.0'
        try:
            if (not oprd_change):
                a = a.sqrt()
            else:
                b = b.sqrt()
            Execution("f")
            Show()
        except:
            # (-a).sqrt() or (-b).sqrt() error
            Execution("e")
    elif ((not error) and (i == "dot")):
        if (((not oprd_change) and (len(str(a)) < 12)) or (oprd_change and (len(str(b)) < 12))):
            Rst()
            dot_mode = True
            Show()
    elif ((not error) and (i == "equ")):
        fnshd = True
        Execution("c")

def Button_function_m_clck(i):
    global set_value, dot_mode, debug_msg_lock, a, b, m, dot, dot_count

    if (i == "mc"):
        m = decimal.Decimal('0')
        Show_debug_msg()
    elif (not error):
        if (i == "mr"):
            Rst()
            set_value, dot_mode, debug_msg_lock, dot, dot_count = True, False, True, decimal.Decimal('0.1'), '0.0'
            if (not oprd_change):
                a = m
            else:
                b = m
            Show()
        elif ((i == "msub") and (not oprd_change)):
            m -= a
        elif ((i == "msub") and oprd_change):
            m -= b
        elif ((i == "madd") and (not oprd_change)):
            m += a
        elif ((i == "madd") and oprd_change):
            m += b
        Show_debug_msg()

def Button_oprt_clck(i):
    global set_ab, set_value, oprd_change, fnshd, dot_mode, debug_msg_lock, oprt, dot, dot_count

    if (not error):
        fnshd = False
        if (not oprd_change):
            set_ab, set_value, oprd_change, dot_mode, dot, dot_count = False, False, True, False, decimal.Decimal('0.1'), '0.0'
        elif (oprd_change and set_ab):
            debug_msg_lock = True
            Execution("c")
        if (not error):
            oprt = i
        Show_debug_msg()

def Button_number_clck(i):
    global a, b, dot, dot_count

    if (not error):
        Rst()
        if ((not dot_mode) and (not oprd_change) and (len(str(a)) < 13)):
            a *= decimal.Decimal('10')
            a += i
        elif ((not dot_mode) and oprd_change and (len(str(b)) < 13)):
            b *= decimal.Decimal('10')
            b += i
        elif (dot_mode and (not oprd_change) and (len(str(a)) < 13)):
            a += (i * dot)
            dot, dot_count = (dot * decimal.Decimal('0.1')), (dot_count + '0')
        elif (dot_mode and oprd_change and (len(str(b)) < 13)):
            b += (i * dot)
            dot, dot_count = (dot * decimal.Decimal('0.1')), (dot_count + '0')
        Show()

# Screen
label_Screen = tk.Label(form, anchor = "e", bd = 1, bg = "AliceBlue", fg = "Black", font = ("Noto Sans", 21), relief = "sunken", textvariable = Screen_Text)

label_Screen.place(x = 6, y = 6, width = 237, height = 50)

Show()

# Scale
scale_OutOrUp = tk.Scale(form, activebackground = "LightSteelBlue", bd = 2.5, bg = "LightSteelBlue", command = Scale_oou_value_change, fg = "Black", font = ("Noto Sans", 13), orient = "horizontal", showvalue = False, tickinterval = 1, to = 2, troughcolor = "Black")
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
button_C.place(x = 6, y = 118, width = 75, height = 50)
button_PosOrNeg.place(x = 87, y = 118, width = 75, height = 50)
button_Sqrt.place(x = 168, y = 118, width = 75, height = 50)
button_Dot.place(x = 87, y = 398, width = 75, height = 50)
button_Equ.place(x = 168, y = 398, width = 75, height = 50)

# Button_Function_M
button_MC = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "mc": Button_function_m_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "MC")
button_MR = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "mr": Button_function_m_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "MR")
button_MSub = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "msub": Button_function_m_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "M-")
button_MAdd = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "madd": Button_function_m_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "M+")

button_MC.place(x = 6, y = 174, width = 75, height = 50)
button_MR.place(x = 87, y = 174, width = 75, height = 50)
button_MSub.place(x = 168, y = 174, width = 75, height = 50)
button_MAdd.place(x = 249, y = 174, width = 75, height = 50)

# Button_Oprt
button_Pow = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "pow": Button_oprt_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "^")
button_Div = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "div": Button_oprt_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "/")
button_Mul = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "mul": Button_oprt_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "*")
button_Sub = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "sub": Button_oprt_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "-")
button_Add = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "add": Button_oprt_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "+")

button_Pow.place(x = 249, y = 118, width = 75, height = 50)
button_Div.place(x = 249, y = 230, width = 75, height = 50)
button_Mul.place(x = 249, y = 286, width = 75, height = 50)
button_Sub.place(x = 249, y = 342, width = 75, height = 50)
button_Add.place(x = 249, y = 398, width = 75, height = 50)

# Button_Number
button_7 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = decimal.Decimal('7'): Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "7")
button_8 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = decimal.Decimal('8'): Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "8")
button_9 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = decimal.Decimal('9'): Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "9")
button_4 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = decimal.Decimal('4'): Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "4")
button_5 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = decimal.Decimal('5'): Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "5")
button_6 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = decimal.Decimal('6'): Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "6")
button_1 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = decimal.Decimal('1'): Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "1")
button_2 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = decimal.Decimal('2'): Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "2")
button_3 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = decimal.Decimal('3'): Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "3")
button_0 = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = decimal.Decimal('0'): Button_number_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "0")

button_7.place(x = 6, y = 230, width = 75, height = 50)
button_8.place(x = 87, y = 230, width = 75, height = 50)
button_9.place(x = 168, y = 230, width = 75, height = 50)
button_4.place(x = 6, y = 286, width = 75, height = 50)
button_5.place(x = 87, y = 286, width = 75, height = 50)
button_6.place(x = 168, y = 286, width = 75, height = 50)
button_1.place(x = 6, y = 342, width = 75, height = 50)
button_2.place(x = 87, y = 342, width = 75, height = 50)
button_3.place(x = 168, y = 342, width = 75, height = 50)
button_0.place(x = 6, y = 398, width = 75, height = 50)

# Main
if ((len(sys.argv) == 2) and (sys.argv[1] == "debug")):
    debug_mode = True
form.mainloop()