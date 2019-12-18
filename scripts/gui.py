from tkinter import *
from tkinter import ttk
from billcalculator import BillCalculator


class App:
    def __init__(self, master):
        self.master = master
        self.BC = BillCalculator()
        products_info = self.BC.read_product_name()
        if products_info:
            self.product_name, self.price = list(products_info.keys()), list(products_info.values())
        else:
            self.product_name = []
            self.price = []

        self.init_widgets()

    def init_widgets(self):
        frame = Frame(self.master)
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        Label(frame, text='Date:', font=(None, 12)).place(relx=0, rely=0, relwidth=0.1, relheight=0.05)

        self.day_entry = Entry(frame, font=12, width=20)
        self.day_entry.place(relx=0.1, rely=0, relwidth=0.06, relheight=0.05)
        self.day_entry.insert(END, '2019')
        self.month_entry = Entry(frame, font=12, width=20)
        self.month_entry.place(relx=0.17, rely=0, relwidth=0.05, relheight=0.05)
        self.year_entry = Entry(frame, font=12, width=20)
        self.year_entry.place(relx=0.23, rely=0, relwidth=0.05, relheight=0.05)

        Label(frame, text='Supermarket:', font=(None, 12)).place(relx=0.33, rely=0, relwidth=0.1, relheight=0.05)

        self.supermarket_var = StringVar()
        self._supermarket = ttk.Combobox(frame,
                                         textvariable=self.supermarket_var)
        self._supermarket.place(relx=0.45, rely=0, relwidth=0.15, relheight=0.07)
        self._supermarket['values'] = self.BC.supermarket

        Label(frame, text='product name', font=(None, 12)).place(relx=0, rely=0.06, relwidth=0.2, relheight=0.05)
        Label(frame, text='amount', font=(None, 12)).place(relx=0.21, rely=0.06, relwidth=0.09, relheight=0.05)
        Label(frame, text='price', font=(None, 12)).place(relx=0.31, rely=0.06, relwidth=0.1, relheight=0.05)
        Label(frame, text='owner', font=(None, 12)).place(relx=0.42, rely=0.06, relwidth=0.1, relheight=0.05)
        Label(frame, text='buyer', font=(None, 12)).place(relx=0.61, rely=0.06, relwidth=0.1, relheight=0.05)
        Label(frame, text='paid', font=(None, 12)).place(relx=0.68, rely=0.06, relwidth=0.1, relheight=0.05)

        self.product_name_var = StringVar()
        self._product_name = ttk.Combobox(frame,
                                          textvariable=self.product_name_var)
        self._product_name.bind("<<ComboboxSelected>>", self.product_name_selected)
        self._product_name.place(relx=0.01, rely=0.12, relwidth=0.22, relheight=0.07)
        self._product_name['values'] = self.product_name

        self.product_amount_var = StringVar()
        self._product_amount = ttk.Combobox(frame,
                                            textvariable=self.product_amount_var)
        self._product_amount.bind("<<ComboboxSelected>>", self.product_amount_changed)
        self._product_amount.place(relx=0.23, rely=0.12, relwidth=0.09, relheight=0.07)
        self._product_amount['values'] = [1, 2, 3, 4]
        self.product_amount_var.set(1)

        self.price_var = StringVar()
        self._price = ttk.Combobox(frame,
                                  textvariable=self.price_var)
        self._price.place(relx=0.33, rely=0.12, relwidth=0.1, relheight=0.07)
        self._price['values'] = self.price

        self.owner_var = StringVar()
        self._owner = ttk.Combobox(frame,
                                  textvariable=self.owner_var)
        self._owner.place(relx=0.44, rely=0.12, relwidth=0.13, relheight=0.07)
        self._owner['values'] = self.BC.members_with_all

        self.buyer_var = StringVar()
        self._buyer = ttk.Combobox(frame,
                                  textvariable=self.buyer_var)
        self._buyer.place(relx=0.58, rely=0.12, relwidth=0.13, relheight=0.07)
        self._buyer['values'] = self.BC.members

        self.paid_var = StringVar()
        self._paid = ttk.Combobox(frame,
                                   textvariable=self.paid_var)
        self._paid.place(relx=0.72, rely=0.12, relwidth=0.1, relheight=0.07)
        self._paid['values'] = ['yes', 'no']
        self.paid_var.set('no')

        Button(frame, text='Add bill', font=(None, 12),
               command=self.add_bill).place(relx=0.85, rely=0.12, relwidth=0.14, relheight=0.07)

        self.product_list_var = StringVar()
        self._product_list = Listbox(frame, font=(None, 12), listvariable=self.product_list_var)
        self._product_list.place(relx=0.01, rely=0.2, relwidth=0.83, relheight=0.75)
        self._product_list['selectmode'] = 'single'

        scroll = Scrollbar(frame, command=self._product_list.yview)
        scroll.place(relx=0.83, rely=0.2, width=15, relheight=0.75)
        self._product_list.configure(yscrollcommand=scroll.set)

        Button(frame, text='delete bill', font=(None, 12),
               command=self.delete_bill).place(relx=0.85, rely=0.22, relwidth=0.14, relheight=0.07)

        Button(frame, text='undo', font=(None, 12),
               command=self.undo).place(relx=0.85, rely=0.32, relwidth=0.14, relheight=0.07)

        Button(frame, text='save', font=(None, 12),
               command=self.save).place(relx=0.85, rely=0.42, relwidth=0.14, relheight=0.07)

    def product_name_selected(self, event=None):
        if self.product_name_var.get() in self.product_name:
            index = self.product_name.index(self.product_name_var.get())
            self.price_var.set('{:.2f}'.format(float(self.price[index]) * int(self.product_amount_var.get())))

    def product_amount_changed(self, event):
        self.product_name_selected()

    def get_list_value(self):
        # with 'StringVar.get()' man can just get a single string
        a = self.product_list_var.get()[1:-1]
        b = a.strip(',').split("'")
        c = ''
        for i in b:
            c += i
        d = c.split(', ')

        value_list = []
        for item in d:
            value_list.append(item)
        return value_list

    def add_bill(self):
        if '.' not in self.price_var.get() and ',' not in self.price_var.get():
            price = self.price_var.get() + '.00'
        elif ',' in self.price_var.get():
            price = re.sub(',', '.', self.price_var.get())
        else:
            price = self.price_var.get()

        self.product_name.append(self.product_name_var.get())
        self.price.append(price)
        amount = self.product_amount_var.get()

        new_bill = self.product_name_var.get() + ';' + \
                   amount + ';' + \
                   price + ';' + \
                   self.owner_var.get() + ';' + \
                   self.buyer_var.get() + ';' + \
                   self.paid_var.get()
        self._product_list.insert(END, new_bill)

        new_product_name = []
        new_price = []
        for index in range(len(self.product_name)):
            if self.product_name[index] not in self._product_name['values']:
                new_product_name.append(self.product_name[index])
            if self.price[index] not in self._price['values']:
                new_price.append(self.price[index])
        if len(new_product_name) > 0:
            temp = list(self._product_name['values'])
            for item in new_product_name:
                temp.append(item)
            self._product_name['values'] = temp

        if len(new_price) > 0:
            temp = list(self._price['values'])
            for item in new_price:
                temp.append(item)
            self._price['values'] = temp

        self.product_name_var.set('')
        self.product_amount_var.set('1')
        self.price_var.set('')
        self.owner_var.set('')
        self.buyer_var.set('')
        self.paid_var.set('no')
        self._product_name.focus_set()

    def delete_bill(self):
        self.bill_list = self.get_list_value()
        self._product_list.delete(self._product_list.curselection())

    def undo(self):
        self.product_list_var.set(self.bill_list)

    def save(self):
        bill_list = self.get_list_value()
        temp = []
        for item in bill_list:
            temp.append(item.split(';'))
        product_name = []
        amount = []
        price = []
        owner = []
        buyer = []
        paid = []
        for item in temp:
            product_name.append(item[0])
            amount.append(item[1])
            price.append(item[2])
            owner.append(item[3])
            buyer.append(item[4])
            paid.append(item[5])
        get_unit_price = lambda p, a: '{:.2f}'.format(float(p) / float(a))
        unit_price = map(get_unit_price, price, amount)
        self.BC.add_product_name(product_name, unit_price)

        year = self.day_entry.get()
        month = self.month_entry.get()
        day = self.year_entry.get()
        date = year+month+day

        self.BC.add_new_bill(date, product_name, amount, price, owner, buyer, paid,
                             self.supermarket_var.get() if self.supermarket_var.get() else 'REWE')

        self._product_list.delete(0, END)
        self.year_entry.delete(0, END)
        self.month_entry.delete(0, END)
        self.day_entry.delete(0, END)
