import tkinter
import decimal

# Form
form = tkinter.Tk()
form.title("Calice")
form.iconphoto(False, tkinter.PhotoImage(file="calc.png"))
form.configure(background="LightSteelBlue")
form.resizable(False, False)
form.geometry("330x448")

# Variable_Switch
set_ab = set_value = oprd_change = fnshd = error = False

# Variable_Ctrl
oprt, dot_ctrl = "null", "0"
oou_ctrl = tkinter.IntVar()

# Variable_Value
a = b = m = "0"

# Variable_Other
Screen_Text = tkinter.StringVar()


# Function
def show():
    Screen_Text.set((a + " ") if (not oprd_change) else (b + " "))


def execution(i):
    global set_ab, set_value, oprd_change, error, oprt, a, b
    step = "n"

    if i == "c":
        set_ab = set_value = False
        if (((decimal.Decimal(a) > decimal.Decimal("0")) or (decimal.Decimal(a) < decimal.Decimal("0"))) or (
                oprt != "pow") or (decimal.Decimal(b) > decimal.Decimal("0"))):
            try:
                if oprt == "add":
                    a = str(decimal.Decimal(a) + decimal.Decimal(b))
                elif oprt == "sub":
                    a = str(decimal.Decimal(a) - decimal.Decimal(b))
                elif oprt == "mul":
                    a = str(decimal.Decimal(a) * decimal.Decimal(b))
                elif oprt == "div":
                    a = str(decimal.Decimal(a) / decimal.Decimal(b))
                elif oprt == "pow":
                    a = str(decimal.Decimal(a) ** int(float(b)))
                b = "0"
                if not fnshd:
                    step = "a" if (len(a) <= 13) else "e"
                else:
                    oprd_change, oprt = False, "null"
                    step = "f"
            except decimal.DivisionByZero:
                # a/0 error
                step = "e"
        else:
            # 0 pow (0, -b) error
            step = "e"
    if (i == "f") or (step == "f"):
        # 0 -> out
        # 1 -> up
        # 2 -> 4 out 5 up
        if (not oprd_change) and (oou_ctrl.get() == 0):
            a = str(decimal.Decimal(a).quantize(decimal.Decimal(dot_ctrl), rounding=decimal.ROUND_DOWN))
        elif (not oprd_change) and (oou_ctrl.get() == 1):
            a = str(decimal.Decimal(a).quantize(decimal.Decimal(dot_ctrl), rounding=decimal.ROUND_UP))
        elif (not oprd_change) and (oou_ctrl.get() == 2):
            a = str(decimal.Decimal(a).quantize(decimal.Decimal(dot_ctrl), rounding=decimal.ROUND_HALF_UP))
        elif oprd_change and (oou_ctrl.get() == 0):
            b = str(decimal.Decimal(b).quantize(decimal.Decimal(dot_ctrl), rounding=decimal.ROUND_DOWN))
        elif oprd_change and (oou_ctrl.get() == 1):
            b = str(decimal.Decimal(b).quantize(decimal.Decimal(dot_ctrl), rounding=decimal.ROUND_UP))
        elif oprd_change and (oou_ctrl.get() == 2):
            b = str(decimal.Decimal(b).quantize(decimal.Decimal(dot_ctrl), rounding=decimal.ROUND_HALF_UP))
        if fnshd:
            step = "a" if (len(a) <= 13) else "e"
    if (i == "e") or (step == "e"):
        error = True
        Screen_Text.set("E ")
    if step == "a":
        Screen_Text.set(a + " ")


def rst():
    global set_ab, set_value, fnshd, a, b

    set_ab = True
    if set_value or fnshd:
        set_value = fnshd = False
        if not oprd_change:
            a = "0"
        else:
            b = "0"


# Function_Scale
def scale_dot_value_change(i):
    global dot_ctrl

    if int(i) == 0:
        dot_ctrl = "0"
    else:
        dot_ctrl = ("0." + ("0" * int(i)))


# Function_Button
def button_function_clck(i):
    global set_ab, set_value, oprd_change, fnshd, error, oprt, a, b

    if i == "c":
        set_ab, set_value, oprd_change, fnshd, error, oprt, a, b = False, False, False, False, False, "null", "0", "0"
        show()
    elif (not error) and (i == "bs"):
        if not oprd_change:
            a = a[:-1]
            if a == "":
                a = "0"
        else:
            b = b[:-1]
            if b == "":
                b = "0"
        show()
    elif (not error) and (i == "pon"):
        if not oprd_change:
            if (decimal.Decimal(a) > decimal.Decimal("0")) or (decimal.Decimal(a) < decimal.Decimal("0")):
                a = str(decimal.Decimal(a) * decimal.Decimal("-1"))
        else:
            if (decimal.Decimal(b) > decimal.Decimal("0")) or (decimal.Decimal(b) < decimal.Decimal("0")):
                b = str(decimal.Decimal(b) * decimal.Decimal("-1"))
        show()
    elif (not error) and (i == "sqrt"):
        set_value = True
        try:
            if not oprd_change:
                a = str(decimal.Decimal(a).sqrt())
            else:
                b = str(decimal.Decimal(b).sqrt())
            execution("f")
            show()
        except decimal.InvalidOperation:
            # (-a).sqrt() or (-b).sqrt() error
            execution("e")
    elif (not error) and (i == "dot"):
        rst()
        if (not oprd_change) and (len(a) < 12):
            if not ("." in a):
                a += "."
        elif oprd_change and (len(b) < 12):
            if not ("." in b):
                b += "."
        show()
    elif (not error) and (i == "equ"):
        fnshd = True
        execution("c")


def button_function_m_clck(i):
    global set_value, a, b, m

    if i == "mc":
        m = "0"
    elif (not error) and (i == "mr"):
        rst()
        set_value = True
        if not oprd_change:
            a = m
        else:
            b = m
        show()
    elif (not error) and (i == "mw") and (not oprd_change):
        m = str(decimal.Decimal(m) + decimal.Decimal(a))
    elif (not error) and (i == "mw") and oprd_change:
        m = str(decimal.Decimal(m) + decimal.Decimal(b))


def button_oprt_clck(i):
    global set_ab, set_value, oprd_change, fnshd, oprt

    if not error:
        fnshd = False
        if not oprd_change:
            set_ab, set_value, oprd_change = False, False, True
        elif oprd_change and set_ab:
            execution("c")
        if not error:
            oprt = i


def button_number_clck(i):
    global a, b

    if not error:
        rst()
        if (not oprd_change) and (len(a) < 13):
            if a == "0":
                a = ""
            a += i
        elif oprd_change and (len(b) < 13):
            if b == "0":
                b = ""
            b += i
        show()


# Screen
label_Screen = tkinter.Label(form, anchor="e", bd=1, bg="AliceBlue", fg="Black", font=("Noto Sans", 24),
                             relief="sunken", textvariable=Screen_Text)

label_Screen.place(x=6, y=6, width=318, height=50)

show()

# Scale
scale_OutOrUp = tkinter.Scale(form, activebackground="LightSteelBlue", bd=2.5, bg="LightSteelBlue", fg="Black",
                              font=("Noto Sans", 12), orient="horizontal", showvalue=False, tickinterval=1, to=2,
                              troughcolor="Black", variable=oou_ctrl)
scale_Dot = tkinter.Scale(form, activebackground="LightSteelBlue", bd=2.5, bg="LightSteelBlue",
                          command=scale_dot_value_change, fg="Black", font=("Noto Sans", 12), orient="horizontal",
                          showvalue=False, tickinterval=1, to=3, troughcolor="Black")

scale_OutOrUp.place(x=6, y=62, width=156)
scale_Dot.place(x=168, y=62, width=156)

scale_OutOrUp.set(2)

# Button_Function
button_BS = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                           command=lambda x="bs": button_function_clck(x), fg="Black", font=("Noto Sans", 18),
                           text="<-")
button_C = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                          command=lambda x="c": button_function_clck(x), fg="Black", font=("Noto Sans", 18), text="C")
button_PosOrNeg = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                                 command=lambda x="pon": button_function_clck(x), fg="Black", font=("Noto Sans", 18),
                                 text="+/-")
button_Sqrt = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                             command=lambda x="sqrt": button_function_clck(x), fg="Black", font=("Noto Sans", 18),
                             text="sqrt")
button_Dot = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                            command=lambda x="dot": button_function_clck(x), fg="Black", font=("Noto Sans", 18),
                            text=".")
button_Equ = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                            command=lambda x="equ": button_function_clck(x), fg="Black", font=("Noto Sans", 18),
                            text="=")

button_BS.place(x=249, y=112, width=75, height=50)
button_C.place(x=6, y=112, width=75, height=50)
button_PosOrNeg.place(x=87, y=112, width=75, height=50)
button_Sqrt.place(x=168, y=112, width=75, height=50)
button_Dot.place(x=87, y=392, width=75, height=50)
button_Equ.place(x=168, y=392, width=75, height=50)

# Button_Function_M
button_MC = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                           command=lambda x="mc": button_function_m_clck(x), fg="Black", font=("Noto Sans", 18),
                           text="MC")
button_MR = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                           command=lambda x="mr": button_function_m_clck(x), fg="Black", font=("Noto Sans", 18),
                           text="MR")
button_MW = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                           command=lambda x="mw": button_function_m_clck(x), fg="Black", font=("Noto Sans", 18),
                           text="MW")

button_MC.place(x=6, y=168, width=75, height=50)
button_MR.place(x=87, y=168, width=75, height=50)
button_MW.place(x=168, y=168, width=75, height=50)

# Button_Oprt
button_Pow = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                            command=lambda x="pow": button_oprt_clck(x), fg="Black", font=("Noto Sans", 18), text="^")
button_Div = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                            command=lambda x="div": button_oprt_clck(x), fg="Black", font=("Noto Sans", 18), text="/")
button_Mul = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                            command=lambda x="mul": button_oprt_clck(x), fg="Black", font=("Noto Sans", 18), text="*")
button_Sub = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                            command=lambda x="sub": button_oprt_clck(x), fg="Black", font=("Noto Sans", 18), text="-")
button_Add = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                            command=lambda x="add": button_oprt_clck(x), fg="Black", font=("Noto Sans", 18), text="+")

button_Pow.place(x=249, y=168, width=75, height=50)
button_Div.place(x=249, y=224, width=75, height=50)
button_Mul.place(x=249, y=280, width=75, height=50)
button_Sub.place(x=249, y=336, width=75, height=50)
button_Add.place(x=249, y=392, width=75, height=50)

# Button_Number
button_7 = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                          command=lambda x="7": button_number_clck(x), fg="Black", font=("Noto Sans", 18), text="7")
button_8 = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                          command=lambda x="8": button_number_clck(x), fg="Black", font=("Noto Sans", 18), text="8")
button_9 = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                          command=lambda x="9": button_number_clck(x), fg="Black", font=("Noto Sans", 18), text="9")
button_4 = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                          command=lambda x="4": button_number_clck(x), fg="Black", font=("Noto Sans", 18), text="4")
button_5 = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                          command=lambda x="5": button_number_clck(x), fg="Black", font=("Noto Sans", 18), text="5")
button_6 = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                          command=lambda x="6": button_number_clck(x), fg="Black", font=("Noto Sans", 18), text="6")
button_1 = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                          command=lambda x="1": button_number_clck(x), fg="Black", font=("Noto Sans", 18), text="1")
button_2 = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                          command=lambda x="2": button_number_clck(x), fg="Black", font=("Noto Sans", 18), text="2")
button_3 = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                          command=lambda x="3": button_number_clck(x), fg="Black", font=("Noto Sans", 18), text="3")
button_0 = tkinter.Button(form, activebackground="SteelBlue", bd=1, bg="SteelBlue",
                          command=lambda x="0": button_number_clck(x), fg="Black", font=("Noto Sans", 18), text="0")

button_7.place(x=6, y=224, width=75, height=50)
button_8.place(x=87, y=224, width=75, height=50)
button_9.place(x=168, y=224, width=75, height=50)
button_4.place(x=6, y=280, width=75, height=50)
button_5.place(x=87, y=280, width=75, height=50)
button_6.place(x=168, y=280, width=75, height=50)
button_1.place(x=6, y=336, width=75, height=50)
button_2.place(x=87, y=336, width=75, height=50)
button_3.place(x=168, y=336, width=75, height=50)
button_0.place(x=6, y=392, width=75, height=50)

# Main
form.mainloop()
