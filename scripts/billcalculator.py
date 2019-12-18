import json
import datetime

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


class BillCalculator:
    def __init__(self):
        self.members = ['KW', 'KH', 'KL', 'YY']
        self.members_with_all = ['All',
                                 'KW', 'KH', 'KL', 'YY',
                                 'KW KH', 'KW KL', 'KW YY', 'KH KL', 'KH YY', 'KL YY',
                                 'KW KH KL', 'KW KH YY', 'KW KL YY', 'KH KL YY']
        self.members_name = {'KW': '吴康洋', 'KH': '胡凯', 'KL': '赖科', 'YY': '杨晔'}
        self.supermarket = ['REWE', 'Netto', 'LiLi', 'Asia Kauf', 'Kaufland', 'ROSSMANN']
        self.products_name = None
        self.date = str(datetime.date.today())
        self.bill_history = {}

    def read_all_history(self):
        with open('data/BillHistory.json', 'r') as f:
            if f.read():
                f.seek(0)
                self.bill_history = json.load(f)
        return self.bill_history

    def add_new_bill(self, date=None, product_name=None, amount=None,
                     price=None, owner=None, buyer=None, paid=None, supermarket='REWE'):
        if not date:
            date = self.date
        bill = []
        if product_name and amount and price and owner and buyer and paid:
            for pn, am, pr, ow, bu in zip(product_name, amount, price, owner, buyer, paid):
                bill.append({"product_name": pn, "amount": am, "price": pr, "owner": ow, "buyer": bu,
                             "supermarket": supermarket, "paid": paid})
        with open('data/BillHistory.json', 'r') as f:
            if f.read():
                f.seek(0)
                self.bill_history = json.load(f)
                if date in self.bill_history and bill:
                    self.bill_history[date] += bill
                else:
                    self.bill_history[date] = bill
            else:
                self.bill_history[date] = bill
                print('file is empty!')

        with open('data/BillHistory.json', 'w') as f:
            f.write(json.dumps(self.sort_dict(self.bill_history)))

    def add_product_name(self, new_product_name=None, price=None):
        product_name = {}
        with open('data/ProductsName.json', 'r') as r:
            if r.read():
                r.seek(0)
                product_name = json.load(r)

        with open('data/ProductsName.json', 'w') as f:
            if new_product_name:
                for npn, p in zip(new_product_name, price):
                    product_name[npn] = p
                f.write(json.dumps(self.sort_dict(product_name)))

    def read_product_name(self):
        products_name = None
        with open('data/ProductsName.json', 'r') as f:
            if f.read():
                f.seek(0)
                products_name = json.load(f)
        return products_name

    def sort_dict(self, old_dict):
        keys = sorted(old_dict.keys())
        sorted_dict = {}
        for key in keys:
            sorted_dict[key] = old_dict[key]
        return sorted_dict

    def calculate_bill(self):
        bill_history = self.read_all_history()
        bill_result = {}
        summe = {}
        for date, bill in bill_history.items():
            s = 0
            for item in bill:
                s += float(item['price'])
            summe[date] = round(s, 2)
        if summe:
            bill_result["date"] = self.sort_dict(summe)

        calculate_result = {}
        for member in self.members:
            calculate_result[member] = [[0.0, 0.0] for _ in range(4)]
        for date, bill in bill_history.items():
            for b in bill:
                if b['owner'] == 'All':
                    for member in self.members:
                        calculate_result[member][self.members.index(b['buyer'])][0] += float(b['price']) / 4
                        if b['paid'] == 'yes':
                            calculate_result[member][self.members.index(b['buyer'])][1] += float(b['price']) / 4
                else:
                    owner = b['owner'].split(' ')
                    for member in owner:
                        calculate_result[member][self.members.index(b['buyer'])][0] += float(b['price']) / len(owner)
                        if b['paid'] == 'yes':
                            calculate_result[member][self.members.index(b['buyer'])][1] += float(b['price']) / len(
                                owner)

        for member in self.members:
            for j in range(4):
                calculate_result[member][j][0] = round(calculate_result[member][j][0], 2)

        bill_result["person"] = calculate_result

        spent_money = [0.0] * len(self.supermarket)
        for date, bill in bill_history.items():
            for index, item in enumerate(bill):
                spent_money[self.supermarket.index(item['supermarket'])] += float(item['price'])

        for i, item in enumerate(spent_money):
            spent_money[i] = round(spent_money[i], 2)

        bill_result["supermarket"] = spent_money

        with open('data/bill_result.json', 'w') as f:
            f.write(json.dumps(bill_result))

    def show_bill_result(self):
        calculate_result = None
        with open('data/bill_result.json', 'r') as f:
            if f.read():
                f.seek(0)
                bill_result = json.load(f)
                calculate_result = bill_result["person"]
        if calculate_result:
            summe = 0.0
            for member, bill in calculate_result.items():
                cost = 0.0
                for i, b in enumerate(bill):
                    if i != self.members.index(member) and b[0] != 0.0:
                        to_pay = b[0]
                        paid = b[1]
                        get_from = calculate_result[self.members[i]][self.members.index(member)][0] - \
                                   calculate_result[self.members[i]][self.members.index(member)][1]
                        if to_pay-paid > get_from:
                            print('{}应付{}欧给{}'.format(self.members_name[member], round(to_pay-paid-get_from, 2), self.members_name[self.members[i]]))
                        elif to_pay == get_from:
                            continue
                    cost += b[0]
                summe += cost
                print('{}一共花了{}欧\n'.format(self.members_name[member], round(cost, 2)))
            print('所有人一共花了{}欧'.format(round(summe, 2)))

    def show_bill_in_date(self):
        bill_in_date = None
        with open('data/bill_result.json', 'r') as f:
            if f.read():
                f.seek(0)
                bill_result = json.load(f)
                bill_in_date = bill_result["date"]
        if bill_in_date:
            key = []
            for k in bill_in_date.keys():
                key.append('/'.join([k[:4], k[4:6], k[6:]]))
            xs = [datetime.datetime.strptime(d, '%Y/%m/%d').date() for d in key]
            plt.bar(xs, list(bill_in_date.values()))
            plt.xlim(datetime.datetime.strptime('2019/10/20', '%Y/%m/%d').date(),
                     datetime.datetime.strptime('2019/12/20', '%Y/%m/%d').date())
            plt.show()

    def show_supermarket(self):
        spent_money = None
        with open('data/bill_result.json', 'r') as f:
            if f.read():
                f.seek(0)
                bill_result = json.load(f)
                spent_money = bill_result["supermarket"]

        if spent_money:
            show_with_pie = True
            show_with_barh = True

            if show_with_pie:
                plt.figure(figsize=(9, 9))
                colors = ['red', 'yellowgreen', 'lightskyblue', 'yellow', 'orange', 'green']
                explode = ([0] * len(self.supermarket))

                plt.pie(spent_money,
                        explode=explode,
                        labels=self.supermarket,
                        colors=colors,
                        autopct='%3.2f%%',
                        shadow=False,
                        startangle=90,
                        pctdistance=0.8,
                        labeldistance=1.2)
                plt.axis('equal')
                plt.legend()
                plt.show()

            if show_with_barh:
                supermarket = {su: sp for su, sp in zip(self.supermarket, spent_money)}
                supermarket = sorted(supermarket.items(), key=lambda value: value[1])

                y = []
                x = []
                for key, value in supermarket:
                    y.append(key)
                    x.append(value)
                fig, ax = plt.subplots()
                b = ax.barh(y, x, facecolor='green')
                for index, rect in enumerate(b):
                    w = rect.get_width()
                    ax.text(w, rect.get_y()+rect.get_height()/2, '{:.2f}'.format(x[index]))

                ax.set_yticks(range(len(y)))
                ax.set_yticklabels(y)

                plt.xticks(())
                plt.show()

