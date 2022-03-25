import sys
import threading
import time
import tkinter as tk
import decimal
from datetime import datetime, timezone, timedelta
import csv

# Form
form = tk.Tk()
form.title("Calice")
form.iconphoto(False, tk.PhotoImage(file = "./rec/calc.png"))
form.configure(background = "LightSteelBlue")
form.resizable(False, False)
form.geometry("312x418")

# Variable_Switch
# oprd_change : a or b
L_mode = unlckable = unlckng = T_mode = set_ab = set_value = oprd_change = fnshd = error = dot_mode = debug_mode = debug_msg_lock = False

# Variable_Ctrl
# oprt : add(+) or sub(-) or mul(*) or div(/) or pow(^)
# oou_ctrl : default = 4 out 5 up
oprt = "null"
oou_ctrl, dot_ctrl = 2, '0'

# Variable_Value
a = b = m = decimal.Decimal('0')
dot, dot_count = decimal.Decimal('0.1'), '0.0'

# Variable_Time
Y_to_MyY = 0
month = day = hour = minute = ""

# Variable_PW
unlckng_PW = ""

# Variable_Other
Screen_Text = tk.StringVar()

# List_Set
app_set = []

# Thread
def Time_show():
    global Y_to_MyY, month, day, hour, minute

    while True:
        time_get = datetime.utcnow().replace(tzinfo = timezone.utc)
        tz_set = time_get.astimezone(timezone(timedelta(hours = int(app_set[0][1]))))
        Y_to_MyY = int(tz_set.strftime("%Y")) - 2020
        month = tz_set.strftime("%m")
        day = tz_set.strftime("%d")
        hour = tz_set.strftime("%H")
        minute = tz_set.strftime("%M")
        if (L_mode and unlckable):
            Screen_Text.set("(L) M%d/%s/%s %s:%s" % (Y_to_MyY, month, day, hour, minute))
        elif ((not L_mode) and T_mode):
            Screen_Text.set("M%d/%s/%s %s:%s" % (Y_to_MyY, month, day, hour, minute))
        time.sleep(1)

t = threading.Thread(target = Time_show, daemon = True)

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

def Show(i = "n"):
    if ((i == "n") and error):
        Screen_Text.set("E ")
    elif ((i == "n") and ((not dot_mode) or (dot_mode and (dot < decimal.Decimal('0.1'))))):
        Screen_Text.set((str(a) + " ") if (not oprd_change) else (str(b) + " "))
    elif ((i == "n") and dot_mode and (dot == decimal.Decimal('0.1'))):
        Screen_Text.set((str(a) + ". ") if (not oprd_change) else (str(b) + ". "))
    elif ((i == "a")):
        Screen_Text.set(str(a) + " ")
    Show_debug_msg()

def Chack_a():
    global error

    if (len(str(a)) <= 13):
        Show("a")
    else:
        error = True
        Show()

def Fmt():
    global a, b

    if ((not oprd_change) and (oou_ctrl == 0)): # out
            a = a.quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_DOWN)
    elif ((not oprd_change) and (oou_ctrl == 1)): # up
            a = a.quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_UP)
    elif ((not oprd_change) and (oou_ctrl == 2)): # 4 out 5 up
            a = a.quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_HALF_UP)
    elif (oprd_change and (oou_ctrl == 0)):
            b = b.quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_DOWN)
    elif (oprd_change and (oou_ctrl == 1)):
            b = b.quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_UP)
    elif (oprd_change and (oou_ctrl == 2)):
            b = b.quantize(decimal.Decimal(dot_ctrl), rounding = decimal.ROUND_HALF_UP)
    if fnshd:
        Chack_a()

def Count():
    global set_ab, set_value, oprd_change, error, dot_mode, oprt, a, b, dot, dot_count

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
            Chack_a()
        else:
            oprd_change, oprt = False, "null"
            Fmt()
    except: # a/0 error
        error = True
        Show()

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
    global L_mode, unlckable, unlckng, T_mode, set_ab, set_value, oprd_change, fnshd, error, dot_mode, oprt, a, b, dot, dot_count, unlckng_PW

    if ((i == "l") and (not L_mode)):
        L_mode = True
        label_Screen.configure(anchor = "center")
        Screen_Text.set("(L) M%d/%s/%s %s:%s" % (Y_to_MyY, month, day, hour, minute))
        unlckable = True
    elif ((i == "l") and L_mode and unlckable):
        label_Screen.configure(anchor = "w")
        Screen_Text.set(" PW : ")
        unlckable, unlckng = False, True
    elif ((not L_mode) and (i == "t") and (not T_mode)):
        T_mode = True
        label_Screen.configure(anchor = "center")
        Screen_Text.set("M%d/%s/%s %s:%s" % (Y_to_MyY, month, day, hour, minute))
    elif ((not L_mode) and (i == "t") and T_mode):
        T_mode = False
        label_Screen.configure(anchor = "e")
        Show()
    elif ((not L_mode) and (not T_mode) and (i == "c")):
        set_ab, set_value, oprd_change, fnshd, error, dot_mode, oprt, a, b, dot, dot_count = False, False, False, False, False, False, "null", decimal.Decimal('0'), decimal.Decimal('0'), decimal.Decimal('0.1'), '0.0'
        Show()
    elif ((not L_mode) and (not T_mode) and (not error) and (i == "bs")):
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
    elif ((not L_mode) and (not T_mode) and (not error) and (i == "pon")):
        if (not oprd_change):
            a *= decimal.Decimal('-1')
        else:
            b *= decimal.Decimal('-1')
        Show()
    elif ((not L_mode) and (not T_mode) and (not error) and (i == "sqrt")):
        set_value, dot_mode, dot, dot_count = True, False, decimal.Decimal('0.1'), '0.0'
        try:
            if (not oprd_change):
                a = a.sqrt()
            else:
                b = b.sqrt()
            Fmt()
        except: # (-a).sqrt() or (-b).sqrt() error
            error = True
        Show()
    elif ((not L_mode) and (not T_mode) and (not error) and (i == "dot")):
        if (((not oprd_change) and (len(str(a)) < 12)) or (oprd_change and (len(str(b)) < 12))):
            Rst()
            dot_mode = True
            Show()
    elif ((not L_mode) and (not T_mode) and (not error) and (i == "equ")):
        fnshd = True
        Count()
    elif (unlckng and (i == "bs")):
        if (unlckng_PW != ""):
            unlckng_PW = unlckng_PW[:-1]
            Screen_Text.set(" PW : " + ("*" * len(unlckng_PW)))
    elif (unlckng and (i == "equ")):
        unlckng = False
        if (unlckng_PW == app_set[1][1]):
            L_mode = False
            if (not T_mode):
                label_Screen.configure(anchor = "e")
                Show()
            else:
                label_Screen.configure(anchor = "center")
                Screen_Text.set("M%d/%s/%s %s:%s" % (Y_to_MyY, month, day, hour, minute))
        else:
            label_Screen.configure(anchor = "center")
            Screen_Text.set("(L) M%d/%s/%s %s:%s" % (Y_to_MyY, month, day, hour, minute))
            unlckable = True
        unlckng_PW = ""

def Button_function_m_clck(i):
    global set_value, dot_mode, debug_msg_lock, a, b, m, dot, dot_count

    if ((not L_mode) and (not T_mode) and (i == "mc")):
        m = decimal.Decimal('0')
        Show_debug_msg()
    elif ((not L_mode) and (not T_mode) and (not error)):
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

    if ((not L_mode) and (not T_mode) and (not error)):
        fnshd = False
        if (not oprd_change):
            set_ab, set_value, oprd_change, dot_mode, dot, dot_count = False, False, True, False, decimal.Decimal('0.1'), '0.0'
        elif (oprd_change and set_ab):
            debug_msg_lock = True
            Count()
        if (not error):
            oprt = i
        Show_debug_msg()

def Button_number_clck(i):
    global a, b, dot, dot_count, unlckng_PW

    if ((not L_mode) and (not T_mode) and (not error)):
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
    elif unlckng:
        unlckng_PW += str(i)
        Screen_Text.set(" PW : " + ("*" * len(unlckng_PW)))

# Screen
label_Screen = tk.Label(form, anchor = "e", bd = 1, bg = "AliceBlue", fg = "Black", font = ("Noto Sans", 21), relief = "sunken", textvariable = Screen_Text)

label_Screen.place(x = 81, y = 6, width = 225, height = 50)

Show() # load

# Scale
scale_OutOrUp = tk.Scale(form, activebackground = "LightSteelBlue", bd = 2.5, bg = "LightSteelBlue", command = Scale_oou_value_change, fg = "Black", font = ("Noto Sans", 13), orient = "horizontal", showvalue = False, tickinterval = 1, to = 2, troughcolor = "Black")
scale_Dot = tk.Scale(form, activebackground = "LightSteelBlue", bd = 2.5, bg = "LightSteelBlue", command = Scale_dot_value_change, fg = "Black", font = ("Noto Sans", 13), orient = "horizontal", showvalue = False, tickinterval = 1, to = 3, troughcolor = "Black")

scale_OutOrUp.place(x = 6, y = 62, width = 75) # height = 50
scale_Dot.place(x = 81, y = 62, width = 75) # height = 50

scale_OutOrUp.set(2) # default = 4 out 5 up

# Button_Function
button_L = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "l": Button_function_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "L")
button_T = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "t": Button_function_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "T")
button_BS = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "bs": Button_function_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "<-")
button_C = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "c": Button_function_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "C")
button_PosOrNeg = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "pon": Button_function_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "+/-")
button_Sqrt = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "sqrt": Button_function_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "sqrt")
button_Dot = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "dot": Button_function_clck(x), fg = "Black", font = ("Noto Sans", 24), text = ".")
button_Equ = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "equ": Button_function_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "=")

button_L.place(x = 6, y = 6, width = 75, height = 50)
button_T.place(x = 156, y = 62, width = 75, height = 50)
button_BS.place(x = 231, y = 62, width = 75, height = 50)
button_C.place(x = 6, y = 112, width = 75, height = 50)
button_PosOrNeg.place(x = 81, y = 112, width = 75, height = 50)
button_Sqrt.place(x = 156, y = 112, width = 75, height = 50)
button_Dot.place(x = 81, y = 362, width = 75, height = 50)
button_Equ.place(x = 156, y = 362, width = 75, height = 50)

# Button_Function_M
button_MC = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "mc": Button_function_m_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "MC")
button_MR = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "mr": Button_function_m_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "MR")
button_MSub = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "msub": Button_function_m_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "M-")
button_MAdd = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "madd": Button_function_m_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "M+")

button_MC.place(x = 6, y = 162, width = 75, height = 50)
button_MR.place(x = 81, y = 162, width = 75, height = 50)
button_MSub.place(x = 156, y = 162, width = 75, height = 50)
button_MAdd.place(x = 231, y = 162, width = 75, height = 50)

# Button_Oprt
button_Pow = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "pow": Button_oprt_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "^")
button_Div = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "div": Button_oprt_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "/")
button_Mul = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "mul": Button_oprt_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "*")
button_Sub = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "sub": Button_oprt_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "-")
button_Add = tk.Button(form, activebackground = "SteelBlue", bd = 1, bg = "SteelBlue", command = lambda x = "add": Button_oprt_clck(x), fg = "Black", font = ("Noto Sans", 24), text = "+")

button_Pow.place(x = 231, y = 112, width = 75, height = 50)
button_Div.place(x = 231, y = 212, width = 75, height = 50)
button_Mul.place(x = 231, y = 262, width = 75, height = 50)
button_Sub.place(x = 231, y = 312, width = 75, height = 50)
button_Add.place(x = 231, y = 362, width = 75, height = 50)

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

button_7.place(x = 6, y = 212, width = 75, height = 50)
button_8.place(x = 81, y = 212, width = 75, height = 50)
button_9.place(x = 156, y = 212, width = 75, height = 50)
button_4.place(x = 6, y = 262, width = 75, height = 50)
button_5.place(x = 81, y = 262, width = 75, height = 50)
button_6.place(x = 156, y = 262, width = 75, height = 50)
button_1.place(x = 6, y = 312, width = 75, height = 50)
button_2.place(x = 81, y = 312, width = 75, height = 50)
button_3.place(x = 156, y = 312, width = 75, height = 50)
button_0.place(x = 6, y = 362, width = 75, height = 50)

# Main
if ((len(sys.argv) == 2) and (sys.argv[1] == "debug")):
    debug_mode = True
with open("./rec/set.csv", newline = "") as set_file:
    rows = csv.reader(set_file)
    for row in rows:
        app_set.append(row)
t.start()
form.mainloop()