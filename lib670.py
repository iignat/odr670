# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 11:40:39 2019

@author: Игнат
"""
import re
xlscols = {}
xlsrows = {}


def getpercentval(col, row, sheet):
    global xlscols
    global xlsrows
    if sheet.cell_value(xlsrows[row], xlscols[col]) == '':
        return '0.00'
    return '{:.2f}'.format(sheet.cell_value(xlsrows[row], xlscols[col]) * 100.00)


def getfloatval(col, row, sheet):
    global xlscols
    global xlsrows
    if sheet.cell_value(xlsrows[row], xlscols[col]) == '':
        return '0.00'
    return '{:.2f}'.format(sheet.cell_value(xlsrows[row], xlscols[col]))


def getstrval(col, row, sheet):
    global xlscols
    global xlsrows
    if sheet.cell_value(xlsrows[row], xlscols[col]) == '':
        return '0.00'
    return str(sheet.cell_value(xlsrows[row], xlscols[col]))


def init(sheet):
    global xlscols
    global xlsrows
    xlscols.clear()

    c, r = findcolrow("Целевые параметры контракта", sheet)
    xlscols['Целевые параметры контракта'] = c
    c, r = findcolrow("Выполнено", sheet)
    xlscols['Выполнено'] = c
    c, r = findcolrow("Сальдо операций", sheet)
    xlscols['Сальдо операций'] = c
    c, r = findcolrow("Движение в рамках контракта", sheet)
    xlscols['Движение в рамках контракта'] = c
    c, r = findcolrow("Привлечение ресурсов с других контрактов", sheet)
    xlscols['Привлечение ресурсов с других контрактов'] = c
    c, r = findcolrow("Привлечение ресурсов организации", sheet)
    xlscols['Привлечение ресурсов организации'] = c
    c, r = findcolrow("Списание в рамках контракта", sheet)
    xlscols['Списание в рамках контракта'] = c
    c, r = findcolrow("Использование ресурсов на другие контракты государственного заказчика", sheet)
    xlscols['Использование ресурсов на другие контракты государственного заказчика'] = c
    c, r = findcolrow("Использование ресурсов на нужды организации", sheet)
    xlscols['Использование ресурсов на нужды организации'] = c

    xlsrows.clear()
    c, r = findcolrow("Финансирование контракта", sheet)
    xlsrows['Финансирование контракта'] = r
    c, r = findcolrow("Денежные средства, полученные от заказчика", sheet)
    xlsrows['Денежные средства, полученные от заказчика'] = r
    c, r = findcolrow("Кредиты банка", sheet)
    xlsrows['Кредиты банка'] = r
    c, r = findcolrow("Задолженность по процентам по кредитам", sheet)
    xlsrows['Задолженность по процентам по кредитам'] = r
    c, r = findcolrow("Задолженность перед поставщиками", sheet)
    xlsrows['Задолженность перед поставщиками'] = r
    c, r = findcolrow("Распределение ресурсов контракта", sheet)
    xlsrows['Распределение ресурсов контракта'] = r
    c, r = findcolrow("Денежные средства", sheet, exactsearch=True)
    xlsrows['Денежные средства'] = r
    c, r = findcolrow("Денежные средства на отдельном счете", sheet)
    xlsrows['Денежные средства на отдельном счете'] = r
    c, r = findcolrow("Денежные средства на депозитах в банке", sheet)
    xlsrows['Денежные средства на депозитах в банке'] = r
    c, r = findcolrow("Авансы, выданные поставщикам", sheet)
    xlsrows['Авансы, выданные поставщикам'] = r
    c, r = findcolrow("Запасы", sheet)
    xlsrows['Запасы'] = r
    c, r = findcolrow("Материалы на складах", sheet)
    xlsrows['Материалы на складах'] = r
    c, r = findcolrow("НДС входящий", sheet)
    xlsrows['НДС входящий'] = r
    c, r = findcolrow("Полуфабрикаты на складах", sheet)
    xlsrows['Полуфабрикаты на складах'] = r
    c, r = findcolrow("Материалы, переданные в переработку", sheet)
    xlsrows['Материалы, переданные в переработку'] = r
    c, r = findcolrow("Расходы будущих периодов", sheet)
    xlsrows['Расходы будущих периодов'] = r
    c, r = findcolrow("Средства производства", sheet)
    xlsrows['Средства производства'] = r
    c, r = findcolrow("Производство", sheet)
    xlsrows['Производство'] = r
    c, r = findcolrow("Затраты на материалы", sheet)
    xlsrows['Затраты на материалы'] = r
    c, r = findcolrow("Затраты на оплату труда", sheet)
    xlsrows['Затраты на оплату труда'] = r
    c, r = findcolrow("Прочие производственные затраты", sheet)
    xlsrows['Прочие производственные затраты'] = r
    c, r = findcolrow("Общепроизводственные затраты", sheet)
    xlsrows['Общепроизводственные затраты'] = r
    c, r = findcolrow("Общехозяйственные затраты", sheet)
    xlsrows['Общехозяйственные затраты'] = r
    c, r = findcolrow("Полуфабрикаты, внутренние работы", sheet)
    xlsrows['Полуфабрикаты, внутренние работы'] = r
    c, r = findcolrow("Выпуск полуфабрикатов, внутренних работ", sheet)
    xlsrows['Выпуск полуфабрикатов, внутренних работ'] = r
    c, r = findcolrow("Выпуск продукции", sheet)
    xlsrows['Выпуск продукции'] = r
    c, r = findcolrow("Готовый товар на складе", sheet)
    xlsrows['Готовый товар на складе'] = r
    c, r = findcolrow("Отгрузка товара, выполнение работ, оказание услуг", sheet)
    xlsrows['Отгрузка товара, выполнение работ, оказание услуг'] = r
    c, r = findcolrow("Себестоимость реализованной продукции", sheet)
    xlsrows['Себестоимость реализованной продукции'] = r
    c, r = findcolrow("Административно-управленческие расходы", sheet)
    xlsrows['Административно-управленческие расходы'] = r
    c, r = findcolrow("Коммерческие расходы", sheet)
    xlsrows['Коммерческие расходы'] = r
    c, r = findcolrow("Проценты по кредитам банка", sheet)
    xlsrows['Проценты по кредитам банка'] = r
    c, r = findcolrow("НДС с выручки от продаж", sheet)
    xlsrows['НДС с выручки от продаж'] = r
    c, r = findcolrow("Прибыль контракта", sheet)
    xlsrows['Прибыль контракта'] = r
    c, r = findcolrow("(+) Привлечение ресурсов в контракт/(-) Перенаправление ресурсов контракта", sheet)
    xlsrows['(+) Привлечение ресурсов в контракт/(-) Перенаправление ресурсов контракта'] = r
    c, r = findcolrow("Списание денежных средств с отдельного счета контракта", sheet)
    xlsrows['Списание денежных средств с отдельного счета контракта'] = r


def getval(name, snum, num, sheet):
    sheet.cell_value(0, 0)
    col, row = findcolrow(name, sheet)
    s = ""
    for i in range(1, num):
        val = sheet.cell_value(row, col + snum + i)
        if type(val) is float:
            val = int(val)
        s += str(val)
    return s


def findcolrow(colname, sheet, exactsearch=False):
    for i in range(sheet.ncols):
        for k in range(sheet.nrows):
            if type(sheet.cell_value(k, i)) is str:
                if not exactsearch:
                    if sheet.cell_value(k, i).find(colname) >= 0:
                        return i, k
                else:
                    if sheet.cell_value(k, i) == colname:
                        return i, k
    return -1, -1


def reformatdate(strdate):
    m = re.findall("[0-9]{2}\.[0-9]{2}\.[0-9]{4}", strdate)
    if m:
        r = strdate.split(".")
        return r[2] + "-" + r[1] + "-" + r[0]
    return strdate
