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
        self.bill_result = None

        self.init_widgets()

    def init_widgets(self):
        frame = Frame(self.master)
        frame.place(relx=0, rely=0, relwidth=1, relheight=0.6)

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

        Label(frame, text='product name', font=(None, 12)).place(relx=0, rely=0.06, relwidth=0.22, relheight=0.05)
        Label(frame, text='amount', font=(None, 12)).place(relx=0.23, rely=0.06, relwidth=0.09, relheight=0.05)
        Label(frame, text='price', font=(None, 12)).place(relx=0.33, rely=0.06, relwidth=0.1, relheight=0.05)
        Label(frame, text='owner', font=(None, 12)).place(relx=0.44, rely=0.06, relwidth=0.13, relheight=0.05)
        Label(frame, text='buyer', font=(None, 12)).place(relx=0.58, rely=0.06, relwidth=0.13, relheight=0.05)
        Label(frame, text='paid', font=(None, 12)).place(relx=0.72, rely=0.06, relwidth=0.1, relheight=0.05)

        self.product_name_var = StringVar()
        self._product_name = ttk.Combobox(frame,
                                          textvariable=self.product_name_var,
                                          postcommand=self.fuzzy_matching)
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
        self._product_list.place(relx=0.01, rely=0.2, relwidth=0.83, relheight=0.77)
        self._product_list['selectmode'] = 'single'

        scroll = Scrollbar(frame, command=self._product_list.yview)
        scroll.place(relx=0.83, rely=0.2, width=15, relheight=0.77)
        self._product_list.configure(yscrollcommand=scroll.set)

        Button(frame, text='delete bill', font=(None, 12),
               command=self.delete_bill).place(relx=0.85, rely=0.22, relwidth=0.14, relheight=0.07)

        Button(frame, text='undo', font=(None, 12),
               command=self.undo).place(relx=0.85, rely=0.32, relwidth=0.14, relheight=0.07)

        Button(frame, text='save', font=(None, 12),
               command=self.save).place(relx=0.85, rely=0.42, relwidth=0.14, relheight=0.07)

        info_frame = Frame(self.master)
        info_frame.place(relx=0, rely=0.6, relwidth=1, relheight=0.4)

        Label(info_frame, text='start date: ', font=(None, 14)).place(relx=0.01, rely=0, relwidth=0.07, relheight=0.1)

        self.start_year_var = StringVar()
        self._start_year = ttk.Combobox(info_frame,
                                        textvariable=self.start_year_var)
        self._start_year.place(relx=0.08, rely=0, relwidth=0.07, relheight=0.1)
        self._start_year['values'] = ['2019', '2020']
        self.start_year_var.set('2019')

        self.start_month_var = StringVar()
        self._start_month = ttk.Combobox(info_frame,
                                         textvariable=self.start_month_var)
        self._start_month.bind('<<ComboboxSelected>>', self._adjust_start_day)
        self._start_month.place(relx=0.15, rely=0, relwidth=0.05, relheight=0.1)
        self._start_month['values'] = [str(i).zfill(2) for i in range(1, 13)]
        self.start_month_var.set('10')

        self.start_day_var = StringVar()
        self._start_day = ttk.Combobox(info_frame,
                                       textvariable=self.start_day_var)
        self._start_day.place(relx=0.2, rely=0, relwidth=0.05, relheight=0.1)
        self._adjust_start_day()
        # self._start_day['values'] = [str(i).zfill(2) for i in range(1, 32 if int(self.start_month_var.get()) in
        #                                                                      [1, 3, 5, 7, 8, 10, 12] else
        #                                                                   (30 if int(self.start_month_var.get()) in
        #                                                                      [2, 4, 6, 9, 11] else 28))]
        self.start_day_var.set('20')

        Label(info_frame, text='end date: ', font=(None, 14)).place(relx=0.25, rely=0, relwidth=0.07, relheight=0.1)

        self.end_year_var = StringVar()
        self._end_year = ttk.Combobox(info_frame,
                                      textvariable=self.end_year_var)
        self._end_year.place(relx=0.32, rely=0, relwidth=0.07, relheight=0.1)
        self._end_year['values'] = ['2019', '2020']
        self.end_year_var.set(self.BC.date[:4])

        self.end_month_var = StringVar()
        self._end_month = ttk.Combobox(info_frame,
                                       textvariable=self.end_month_var)
        self._end_month.bind('<<ComboboxSelected>>', self._adjust_end_day)
        self._end_month.place(relx=0.39, rely=0, relwidth=0.05, relheight=0.1)
        self._end_month['values'] = [str(i).zfill(2) for i in range(1, 13)]
        self.end_month_var.set(self.BC.date[5:7])

        self.end_day_var = StringVar()
        self._end_day = ttk.Combobox(info_frame,
                                     textvariable=self.end_day_var)
        self._end_day.place(relx=0.44, rely=0, relwidth=0.05, relheight=0.1)
        self._adjust_end_day()
        # self._end_day['values'] = [str(i).zfill(2) for i in range(1, 32)]
        self.end_day_var.set(self.BC.date[8:])

        self._info_text = Text(info_frame,
                               font=(None, 12))
        self._info_text.place(relx=0.01, rely=0.1, relwidth=0.83, relheight=0.85)
        self._info_text.insert(0.0, '欢迎使用!')
        self._info_text['state'] = 'disabled'

        Button(info_frame, text='calculate bill', font=(None, 12),
               command=self.calculate_bill).place(relx=0.85, rely=0.05, relwidth=0.14, relheight=0.12)
        Button(info_frame, text='show date', font=(None, 12),
               command=self.show_bill_in_date).place(relx=0.85, rely=0.18, relwidth=0.14, relheight=0.12)
        Button(info_frame, text='show supermarket', font=(None, 12),
               command=self.show_bill_in_supermarket).place(relx=0.85, rely=0.31, relwidth=0.14, relheight=0.12)

    def _adjust_start_day(self, event=None):
        self._start_day['values'] = [str(i).zfill(2) for i in range(1, 32 if int(self.start_month_var.get()) in
                                                                             [1, 3, 5, 7, 8, 10, 12] else
                                                                             (31 if int(self.start_month_var.get()) in
                                                                             [4, 6, 9, 11] else 29))]

    def _adjust_end_day(self, event=None):
        self._end_day['values'] = [str(i).zfill(2) for i in range(1, 32 if int(self.end_month_var.get()) in
                                                                             [1, 3, 5, 7, 8, 10, 12] else
                                                                             (31 if int(self.end_month_var.get()) in
                                                                             [4, 6, 9, 11] else 29))]

    def fuzzy_matching(self):
        user_input = self.product_name_var.get()
        if user_input:
            self._product_name['values'] = [new_product_name for new_product_name in self.product_name
                                            if user_input in new_product_name[:len(user_input)]]
        else:
            self._product_name['values'] = self.product_name

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

    def show_info(self, message):
        self._info_text['state'] = 'normal'
        self._info_text.insert(END, '\n'+message)
        self._info_text['state'] = 'disabled'

    def calculate_bill(self):
        self._info_text['state'] = 'normal'
        self._info_text.delete(0.0, END)
        self.start_date = self.start_year_var.get()+self.start_month_var.get()+self.start_day_var.get()
        self.end_date = self.end_year_var.get()+self.end_month_var.get()+self.end_day_var.get()
        message = '{}年{}月{}日至{}年{}月{}日:'.format(self.start_date[:4], self.start_date[4:6], self.start_date[6:],
                                                self.end_date[:4], self.end_date[4:6], self.end_date[6:])
        self.show_info(message)

        self.bill_result = self.BC.calculate_bill(self.start_date, self.end_date)
        result_in_person = self.bill_result['person']
        if result_in_person:
            summe = 0.0
            for member, bill in result_in_person.items():
                cost = 0.0
                for i, b in enumerate(bill):
                    if i != self.BC.members.index(member) and b[0] != 0.0:
                        to_pay = b[0]
                        paid = b[1]
                        get_from = result_in_person[self.BC.members[i]][self.BC.members.index(member)][0] - \
                                   result_in_person[self.BC.members[i]][self.BC.members.index(member)][1]
                        if to_pay-paid > get_from:
                            message = '{}应付{}欧给{}'.format(self.BC.members_name[member], round(to_pay-paid-get_from, 2),
                                                          self.BC.members_name[self.BC.members[i]])
                            self.show_info(message)
                        elif to_pay == get_from:
                            continue
                    cost += b[0]
                summe += cost
                message = '{}一共花了{}欧\n'.format(self.BC.members_name[member], round(cost, 2))
                self.show_info(message)
            message = '所有人一共花了{}欧'.format(round(summe, 2))
            self.show_info(message)

    def show_bill_in_date(self):
        self.BC.show_bill_in_date(self.start_date, self.end_date)

    def show_bill_in_supermarket(self):
        self.BC.show_supermarket(self.start_date, self.end_date)
