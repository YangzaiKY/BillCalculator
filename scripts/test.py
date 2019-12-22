from datetime import datetime
import json

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from billcalculator import BillCalculator

if __name__ == '__main__':
    bc = BillCalculator()
    # date = '20191212'
    # product_name = []
    # price = []
    # owner = []
    # buyer = []
    #
    # product_name.append("BAMI GORENG")
    # price.append("2.49")
    # owner.append("Kangyang Wu")
    # buyer.append("Kangyang Wu")
    #
    # bc.add_new_bill(date, product_name, price, owner, buyer)

    # new_product_name = []
    # price = []
    #
    # while input('是否继续添加：') in ['y', 'Y']:
    #     new_product_name.append(input('新产品：'))
    #     price.append(input('单价：'))
    # bc.add_product_name(new_product_name, price)

    # bc.read_product_name()
    # bc.read_all_history()

    # bc.read_product_name()

    # new_products_name = {}
    # with open('../data/ProductsName.json', 'r') as f:
    #     if f.read():
    #         f.seek(0)
    #         new_products_name = json.load(f)
    #
    # for npn, pr in new_products_name.items():
    #     print(npn, pr)
    # print(len(new_products_name))
    #
    # with open('ProductsName.json', 'r') as f:
    #     if f.read():
    #         f.seek(0)
    #         old_products_name = json.load(f)
    #         for opn, pr in old_products_name.items():
    #             print(opn, pr)
    #             new_products_name[opn] = '{:.2f}'.format(pr)
    #         print(len(old_products_name))
    #
    # with open('../data/ProductsName.json', 'w') as f:
    #     f.write(json.dumps(bc.sort_dict(new_products_name)))

    # summe = {}
    #
    # with open('../data/BillHistory.json', 'r') as f:
    #     if f.read():
    #         f.seek(0)
    #         bill_history = json.load(f)
    #         for date, bill in bill_history.items():
    #             # if date == '20191025':
    #             #     new_bill = []
    #             #     for item in bill:
    #             #         item['owner'] = 'KH KL'
    #             #         new_bill.append(item)
    #             #     bill_history[date] = new_bill
    #             s = 0
    #             for item in bill:
    #                 s += float(item['price'])
    #             summe[date] = round(s, 2)
    #
    # print(summe)
    # key = []
    # for k in summe.keys():
    #     key.append('/'.join([k[:4], k[4:6], k[6:]]))
    # print(key)
    # xs = [datetime.strptime(d, '%Y/%m/%d').date() for d in key]
    # plt.bar(xs, list(summe.values()))
    # plt.xlim(datetime.strptime('2019/10/15', '%Y/%m/%d').date(), datetime.strptime('2019/12/16', '%Y/%m/%d').date())
    # plt.show()

    # bc.calculate_bill()
    # bc.show_bill()

    # add supermarket
    # with open('../data/BillHistory.json', 'r') as f:
    #     if f.read():
    #         f.seek(0)
    #         bill_history = json.load(f)
    #         for date, bill in bill_history.items():
    #             if date in ['20191025', '20191030', '20191102', '20191106', '20191109', '20191112', '20191122',
    #                         '20191126', '20191129', '20191204', '20191207', '20191210', '20191213']:
    #                 for index, item in enumerate(bill):
    #                     item["supermarket"] = 'REWE'
    #                     bill_history[date][index] = item
    #             elif date in ['20191029']:
    #                 for index, item in enumerate(bill):
    #                     item["supermarket"] = 'Asia Kauf'
    #                     bill_history[date][index] = item
    #             else:
    #                 for index, item in enumerate(bill):
    #                     item["supermarket"] = 'other'
    #                     bill_history[date][index] = item
    #             print(date)
    #             for i in bill_history[date]:
    #                 print(i)
    #
    # with open('../data/BillHistory.json', 'w') as f:
    #     f.write(json.dumps(bc.sort_dict(bill_history)))

    # show market
    # supermarkt = ['REWE', 'LiLi', 'Asia Kauf', 'Kaufland', 'ROSSMANN']
    # spent_money = [0.0] * len(supermarkt)
    # with open('../data/BillHistory.json', 'r') as f:
    #     if f.read():
    #         f.seek(0)
    #         bill_history = json.load(f)
    #         for date, bill in bill_history.items():
    #             for index, item in enumerate(bill):
    #                 spent_money[supermarkt.index(item['supermarket'])] += float(item['price'])
    #
    # for su, sp in zip(supermarkt, spent_money):
    #     print(su, round(sp))
    #
    # plt.figure(figsize=(6, 9))
    # labels = supermarkt
    # sizes = spent_money
    # colors = ['red', 'yellowgreen', 'lightskyblue', 'yellow', 'orange']
    # explode = (0, 0, 0, 0, 0)
    #
    # patches, text1, text2 = plt.pie(sizes,
    #                                 explode=explode,
    #                                 labels=labels,
    #                                 colors=colors,
    #                                 autopct='%3.2f%%',
    #                                 shadow=False,
    #                                 startangle=90,
    #                                 pctdistance=0.8,
    #                                 labeldistance=1.2)
    # plt.axis('equal')
    # plt.legend()
    # plt.show()

    # bc.show_supermarket()

    # calculate bill
    # calculate_result = {}
    # for member in bc.members:
    #     calculate_result[member] = [[0.0, 0] for _ in range(4)]
    # with open('../data/BillHistory.json', 'r') as f:
    #     if f.read():
    #         f.seek(0)
    #         bill_history = json.load(f)
    #         for date, bill in bill_history.items():
    #             for b in bill:
    #                 if b['owner'] == 'All':
    #                     for member in bc.members:
    #                         calculate_result[member][bc.members.index(b['buyer'])][0] += float(b['price']) / 4
    #                 else:
    #                     owner = b['owner'].split(' ')
    #                     for member in owner:
    #                         calculate_result[member][bc.members.index(b['buyer'])][0] += float(b['price']) / len(owner)
    # result = 0.0
    # for member in bc.members:
    #     for j in range(4):
    #         calculate_result[member][j][0] = round(calculate_result[member][j][0], 2)
    #         result += calculate_result[member][j][0]
    #
    # member_name = {'KW': '吴康洋', 'KH': '胡凯', 'KL': '赖科', 'YY': '杨晔'}
    #
    # for member, bill in calculate_result.items():
    #     cost = 0.0
    #     for i, b in enumerate(bill):
    #         if i != bc.members.index(member) and b[0] != 0.0:
    #             to_pay = b[0]
    #             get_from = calculate_result[bc.members[i]][bc.members.index(member)][0]
    #             if to_pay > get_from:
    #                 print('{}应付{}欧给{}'.format(member_name[member], round(to_pay-get_from, 2), member_name[bc.members[i]]))
    #             elif to_pay == get_from:
    #                 continue
    #         cost += b[0]
    #     print('{}一共花了{}欧\n'.format(member_name[member], cost))
    # print('所有人一共花了{}欧'.format(round(result, 2)))
    # bc.calculate_bill()
    #
    # bc.show_bill_result()
    # bc.show_bill_in_date()
    # bc.show_supermarket()
    print(bc.date)
    # add new item "paid"
    # with open('../data/BillHistory.json', 'r') as f:
    #     if f.read():
    #         f.seek(0)
    #         bill_history = json.load(f)
    #         for date, bill in bill_history.items():
    #             for i, b in enumerate(bill):
    #                 bill[i]['paid'] = 'no'
    #             bill_history[date] = bill
    #
    # with open('../data/BillHistory.json', 'w') as f:
    #     f.write(json.dumps(bill_history))

    # TODO 用postcommand和输入框中的字符串改变Combobox的value来实现模糊匹配

    # add bill in date of all
    # bill_history = bc.read_all_history()
    # with open('../data/bill_result.json', 'r') as f:
    #     if f.read():
    #         f.seek(0)
    #         bill_result = json.load(f)
    #         for date, result in bill_result['date'].items():
    #             bill_per_person = [0.0]*5
    #             # print(date, result)
    #             for bill in bill_history[date]:
    #                 bill_per_person[4] += float(bill['price'])
    #                 if bill['owner'] == 'All':
    #                     bill_per_person = [round(bill_per_person[i]+float(bill['price'])/4.0, 2)
    #                                        if i < 4 else bill_per_person[i] for i in range(5)]
    #                     continue
    #                 owner = bill['owner'].split(' ')
    #                 # print(owner)
    #                 for ow in owner:
    #                     bill_per_person[bc.members.index(ow)] += float(bill['price']) / len(owner)
    #             bill_per_person = list(map(lambda x: round(x, 2), bill_per_person))
    #             bill_result['date'][date] = bill_per_person
    # with open('../data/bill_result.json', 'w') as f:
    #     f.write(json.dumps(bill_result))
