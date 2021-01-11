# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 11:07:19 2019

@author: Игнат
"""
import glob
import os
import xlrd
import lib670
import xml.etree.ElementTree as ET
import datetime
from xml.dom import minidom
import xmlschema
import logging


now = datetime.datetime.now()
root = ET.Element('ДанныеРаздельногоУчета')

num_process = 0

os.chdir(".\\data")
os.system("del /Q message.*")
os.system("del /Q ..\\out\\message.*")

logging.basicConfig(filename="..\\log\\log.log", level=logging.INFO, filemode="w")

for file in glob.glob("*.xls"):
    logging.info("Обработка " + file)
    wb = xlrd.open_workbook(file)
    sheet = wb.sheet_by_index(1)

    inn = lib670.getval("ИНН организации", 3, 11,  sheet)
    kpp = lib670.getval("КПП организации", 8, 10,  sheet)
    crdate = lib670.getval("Дата составления отчета", 12, 11,  sheet)
    orgname = "Акционерное общество Научно-технический центр \"Альфа-М\""
    igk = lib670.getval("ИГК:", 3, 26, sheet)
    discacc = lib670.getval("Отдельный счет", 8, 21, sheet)
    contnum = lib670.getval("Номер контракта", 3, 44, sheet)
    contdate = lib670.getval("Дата контракта", 5, 11, sheet)
    planedate = lib670.getval("Плановая дата исполнения контракта",
                              17, 11, sheet)

    crdate = lib670.reformatdate(crdate)
    contdate = lib670.reformatdate(contdate)
    planedate = lib670.reformatdate(planedate)

    lib670.init(sheet)

    num_process += 1

    logging.info("ИНН " + inn)
    logging.info("КПП " + kpp)
    logging.info("Дата составления отчета " + crdate)
    logging.info("ИГК " + igk)
    logging.info("Отдельный счет " + discacc)
    logging.info("Номер контракта " + contnum)
    logging.info("Дата контракта " + contdate)
    logging.info("Плановая дата исполнения контракта " + planedate)

    root.attrib['ИННОрганизации'] = '5040036059'
    root.attrib['КППОрганизации'] = '504001001'
    root.attrib['НаименованиеОрганизации'] = orgname
    root.attrib['ГенераторОтчета'] = 'ТурбоБухгалтер 8.0'
    root.attrib['ДатаФормирования'] = now.strftime("%Y-%m-%dT%H:%M:%S")
    root.attrib['xmlns'] = 'http://mil.ru/discreteAccounting'

    contract = ET.SubElement(root, 'Контракт')
    contract.attrib['ДатаСоставленияОтчета'] = crdate
    contract.attrib['ИГК'] = igk
    contract.attrib['НомерОтдельногоСчета'] = discacc
    contract.attrib['НомерКонтракта'] = contnum
    contract.attrib['ДатаЗаключенияКонтракта'] = contdate
    contract.attrib['ПлановаяДатаИсполнения'] = planedate

    contractfinancegroup = ET.SubElement(contract, 'ГруппаФинансированиеКонтракта')
    contractfinancegroup.attrib['ЦелевойОбъемФинансирования'] = lib670.getfloatval('Целевые параметры контракта', 'Финансирование контракта', sheet)
    contractfinancegroup.attrib['ПроцентВыполнения'] = lib670.getpercentval('Выполнено', 'Финансирование контракта', sheet)
    contractfinancegroup.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Финансирование контракта', sheet)

    customermoney = ET.SubElement(contractfinancegroup, 'ДенежныеСредстваЗаказчика')
    customermoney.attrib['ЦенаКонтракта'] = lib670.getfloatval('Целевые параметры контракта', 'Денежные средства, полученные от заказчика', sheet)
    customermoney.attrib['ПроцентВыполнения'] = lib670.getpercentval('Выполнено', 'Денежные средства, полученные от заказчика', sheet)
    customermoney.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Денежные средства, полученные от заказчика', sheet)
    customermoney.attrib['ВозвращеноЗаказчику'] = lib670.getfloatval('Движение в рамках контракта', 'Денежные средства, полученные от заказчика', sheet)
    customermoney.attrib['ВозвращеноЗаказчикуСобственныеСредства'] = lib670.getfloatval('Привлечение ресурсов организации', 'Денежные средства, полученные от заказчика', sheet)
    customermoney.attrib['ПолученоОтЗаказчика'] = lib670.getfloatval('Списание в рамках контракта', 'Денежные средства, полученные от заказчика', sheet)

    bankcredits = ET.SubElement(contractfinancegroup, 'БанковскиеКредиты')
    bankcredits.attrib['ПлановыйОбъемКредитования'] = lib670.getfloatval('Целевые параметры контракта', 'Кредиты банка', sheet)
    bankcredits.attrib['ПроцентВыполнения'] = lib670.getpercentval('Выполнено', 'Кредиты банка', sheet)
    bankcredits.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Кредиты банка', sheet)
    bankcredits.attrib['ПогашеноТелаКредита'] = lib670.getfloatval('Движение в рамках контракта', 'Кредиты банка', sheet)
    bankcredits.attrib['ПогашеноТелаКредитаСобственныеСредства'] = lib670.getfloatval('Привлечение ресурсов организации', 'Кредиты банка', sheet)
    bankcredits.attrib['ПривлеченоКредитов'] = lib670.getfloatval('Списание в рамках контракта', 'Кредиты банка', sheet)

    loaninterest = ET.SubElement(contractfinancegroup, 'ЗадолженностьПоПроцентамКредитов')
    loaninterest.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Задолженность по процентам по кредитам', sheet)
    loaninterest.attrib['ПогашеноПроцентов'] = lib670.getfloatval('Движение в рамках контракта', 'Задолженность по процентам по кредитам', sheet)
    loaninterest.attrib['ПогашеноПроцентовСобственныеСредства'] = lib670.getfloatval('Привлечение ресурсов организации', 'Задолженность по процентам по кредитам', sheet)
    loaninterest.attrib['НачисленоПроцентов'] = lib670.getfloatval('Списание в рамках контракта', 'Задолженность по процентам по кредитам', sheet)

    supplierdebt = ET.SubElement(contractfinancegroup, 'ЗадолженностьПоставщикам')
    supplierdebt.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Задолженность перед поставщиками', sheet)
    supplierdebt.attrib['ОплаченоПоставщикам'] = lib670.getfloatval('Движение в рамках контракта', 'Задолженность перед поставщиками', sheet)
    supplierdebt.attrib['ОплаченоПоставщикамСредстваДругихКонтрактов'] = lib670.getfloatval('Привлечение ресурсов с других контрактов', 'Задолженность перед поставщиками', sheet)
    supplierdebt.attrib['ОплаченоПоставщикамСобственныеСредства'] = lib670.getfloatval('Привлечение ресурсов организации', 'Задолженность перед поставщиками', sheet)
    supplierdebt.attrib['СуммарнаяЗадолженность'] = lib670.getfloatval('Списание в рамках контракта', 'Задолженность перед поставщиками', sheet)

    contractresallocgroup = ET.SubElement(contract, 'ГруппаРаспределениеРесурсовКонтракта')
    contractresallocgroup.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Распределение ресурсов контракта', sheet)

    moneygroup = ET.SubElement(contractresallocgroup, 'ГруппаДенежныеСредства')
    moneygroup.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Денежные средства', sheet)
    moneygroup.attrib['ДенежныеАктивы'] = lib670.getfloatval('Движение в рамках контракта', 'Денежные средства', sheet)
    moneygroup.attrib['ДенежныеАктивыСредстваДругихКонтрактов'] = lib670.getfloatval('Привлечение ресурсов с других контрактов', 'Денежные средства', sheet)
    moneygroup.attrib['ДенежныеАктивыСобственныеСредства'] = lib670.getfloatval('Привлечение ресурсов организации', 'Денежные средства', sheet)
    moneygroup.attrib['ИспользованиеРесурсов'] = lib670.getfloatval('Списание в рамках контракта', 'Денежные средства', sheet)
    moneygroup.attrib['ИспользованиеРесурсовДругиеКонтракты'] = lib670.getfloatval('Использование ресурсов на другие контракты государственного заказчика', 'Денежные средства', sheet)
    moneygroup.attrib['ИспользованиеРесурсовСобственныеСредства'] = lib670.getfloatval('Использование ресурсов на нужды организации', 'Денежные средства', sheet)

    moneydiscacc = ET.SubElement(moneygroup, 'ДенежныеСредстваОтдельныйСчет')
    moneydiscacc.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Денежные средства на отдельном счете', sheet)
    moneydiscacc.attrib['ЗачисленоИсполнениеКонтракта'] = lib670.getfloatval('Движение в рамках контракта', 'Денежные средства на отдельном счете', sheet)
    moneydiscacc.attrib['ЗачисленоИное'] = lib670.getfloatval('Привлечение ресурсов организации', 'Денежные средства на отдельном счете', sheet)
    moneydiscacc.attrib['СписаноИсполнениеКонтракта'] = lib670.getfloatval('Списание в рамках контракта', 'Денежные средства на отдельном счете', sheet)
    moneydiscacc.attrib['СписаноДругиеКонтракты'] = lib670.getfloatval('Использование ресурсов на другие контракты государственного заказчика', 'Денежные средства на отдельном счете', sheet)
    moneydiscacc.attrib['СписаноРасходыОрганизации'] = lib670.getfloatval('Использование ресурсов на нужды организации', 'Денежные средства на отдельном счете', sheet)

    bankdeposits = ET.SubElement(moneygroup, 'БанковскиеДепозиты')
    bankdeposits.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Денежные средства на депозитах в банке', sheet)
    bankdeposits.attrib['ПеречисленоНаДепозит'] = lib670.getfloatval('Движение в рамках контракта', 'Денежные средства на депозитах в банке', sheet)
    bankdeposits.attrib['ВозвращеноСДепозита'] = lib670.getfloatval('Списание в рамках контракта', 'Денежные средства на депозитах в банке', sheet)

    prepayment = ET.SubElement(moneygroup, 'АвансыВыданные')
    prepayment.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Авансы, выданные поставщикам', sheet)
    prepayment.attrib['АвансыИсполнениеКонтракта'] = lib670.getfloatval('Движение в рамках контракта', 'Авансы, выданные поставщикам', sheet)
    prepayment.attrib['АвансыСредстваДругихКонтрактов'] = lib670.getfloatval('Привлечение ресурсов с других контрактов', 'Авансы, выданные поставщикам', sheet)
    prepayment.attrib['АвансыСобственныеСредства'] = lib670.getfloatval('Привлечение ресурсов организации', 'Авансы, выданные поставщикам', sheet)
    prepayment.attrib['ЗачтеноАвансов'] = lib670.getfloatval('Списание в рамках контракта', 'Авансы, выданные поставщикам', sheet)
    prepayment.attrib['СписаноЗадолженностиКооперации'] = lib670.getfloatval('Использование ресурсов на нужды организации', 'Авансы, выданные поставщикам', sheet)

    supplygroup = ET.SubElement(contractresallocgroup, 'ГруппаЗапасы')
    supplygroup.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Запасы', sheet)
    supplygroup.attrib['СформированоЗапасов'] = lib670.getfloatval('Движение в рамках контракта', 'Запасы', sheet)
    supplygroup.attrib['СформированоЗапасовСредстваДругихКонтрактов'] = lib670.getfloatval('Привлечение ресурсов с других контрактов', 'Запасы', sheet)
    supplygroup.attrib['СформированоЗапасовСобственныеСредства'] = lib670.getfloatval('Привлечение ресурсов организации', 'Запасы', sheet)
    supplygroup.attrib['ИспользованоЗапасов'] = lib670.getfloatval('Списание в рамках контракта', 'Запасы', sheet)
    supplygroup.attrib['ИспользованоЗапасовНаДругиеКонтракты'] = lib670.getfloatval('Использование ресурсов на другие контракты государственного заказчика', 'Запасы', sheet)
    supplygroup.attrib['ИспользованоЗапасовНуждыОрганизации'] = lib670.getfloatval('Использование ресурсов на нужды организации', 'Запасы', sheet)

    matinwarehouses = ET.SubElement(supplygroup, 'МатериалыНаСкладах')
    matinwarehouses.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Материалы на складах', sheet)
    matinwarehouses.attrib['ПоступилоМатериалов'] = lib670.getfloatval('Движение в рамках контракта', 'Материалы на складах', sheet)
    matinwarehouses.attrib['ПоступилоМатериаловСредстваДругихКонтрактов'] = lib670.getfloatval('Привлечение ресурсов с других контрактов', 'Материалы на складах', sheet)
    matinwarehouses.attrib['ПоступилоМатериаловСобственныеСредства'] = lib670.getfloatval('Привлечение ресурсов организации', 'Материалы на складах', sheet)
    matinwarehouses.attrib['ИспользованоМатериалов'] = lib670.getfloatval('Списание в рамках контракта', 'Материалы на складах', sheet)
    matinwarehouses.attrib['ИспользованоМатериаловНаДругиеКонтракты'] = lib670.getfloatval('Использование ресурсов на другие контракты государственного заказчика', 'Материалы на складах', sheet)
    matinwarehouses.attrib['ИспользованоМатериаловНуждыОрганизации'] = lib670.getfloatval('Использование ресурсов на нужды организации', 'Материалы на складах', sheet)

    VATincluded = ET.SubElement(supplygroup, 'НДСПоПриобретеннымЦенностям')
    VATincluded.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'НДС входящий', sheet)
    VATincluded.attrib['Выделено'] = lib670.getfloatval('Движение в рамках контракта', 'НДС входящий', sheet)
    VATincluded.attrib['ВключеноВСтоимостьЗапасов'] = lib670.getfloatval('Списание в рамках контракта', 'НДС входящий', sheet)
    VATincluded.attrib['ПринятоКВычету'] = lib670.getfloatval('Использование ресурсов на нужды организации', 'НДС входящий', sheet)

    Semi_finishedinwarehouses = ET.SubElement(supplygroup, 'ПолуфабрикатыНаСкладах')
    Semi_finishedinwarehouses.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Полуфабрикаты на складах', sheet)
    Semi_finishedinwarehouses.attrib['ПоступилоПолуфабрикатов'] = lib670.getfloatval('Движение в рамках контракта', 'Полуфабрикаты на складах', sheet)
    Semi_finishedinwarehouses.attrib['ПоступилоПолуфабрикатовСредстваДругихКонтрактов'] = lib670.getfloatval('Привлечение ресурсов с других контрактов', 'Полуфабрикаты на складах', sheet)
    Semi_finishedinwarehouses.attrib['ПоступилоПолуфабрикатовСобственныеСредства'] = lib670.getfloatval('Привлечение ресурсов организации', 'Полуфабрикаты на складах', sheet)
    Semi_finishedinwarehouses.attrib['ИспользованоПолуфабрикатов'] = lib670.getfloatval('Списание в рамках контракта', 'Полуфабрикаты на складах', sheet)
    Semi_finishedinwarehouses.attrib['ИспользованоПолуфабрикатовНаДругиеКонтракты'] = lib670.getfloatval('Использование ресурсов на другие контракты государственного заказчика', 'Полуфабрикаты на складах', sheet)
    Semi_finishedinwarehouses.attrib['ИспользованоПолуфабрикатовНуждыОрганизации'] = lib670.getfloatval('Использование ресурсов на нужды организации', 'Полуфабрикаты на складах', sheet)

    recycledmaterials = ET.SubElement(supplygroup, 'МатериалыПереданныеВПереработку')
    recycledmaterials.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Материалы, переданные в переработку', sheet)
    recycledmaterials.attrib['ПереданоСтороннемуИсполнителю'] = lib670.getfloatval('Движение в рамках контракта', 'Материалы, переданные в переработку', sheet)
    recycledmaterials.attrib['ПринятоИзПереработки'] = lib670.getfloatval('Списание в рамках контракта', 'Материалы, переданные в переработку', sheet)
    recycledmaterials.attrib['ПринятоИзПереработкиНуждыОрганизации'] = lib670.getfloatval('Использование ресурсов на нужды организации', 'Материалы, переданные в переработку', sheet)

    futurespending = ET.SubElement(supplygroup, 'РасходыБудущихПериодов')
    futurespending.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Расходы будущих периодов', sheet)
    futurespending.attrib['НачисленоРБП'] = lib670.getfloatval('Движение в рамках контракта', 'Расходы будущих периодов', sheet)
    futurespending.attrib['СписаноРБП'] = lib670.getfloatval('Списание в рамках контракта', 'Расходы будущих периодов', sheet)

    meansofproduct = ET.SubElement(supplygroup, 'СредстваПроизводства')
    meansofproduct.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Средства производства', sheet)
    meansofproduct.attrib['ПоступилоСредствПроизводства'] = lib670.getfloatval('Движение в рамках контракта', 'Средства производства', sheet)
    meansofproduct.attrib['ПоступилоСредствПроизводстваСредстваДругихКонтрактов'] = lib670.getfloatval('Привлечение ресурсов с других контрактов', 'Средства производства', sheet)
    meansofproduct.attrib['ПоступилоСредствПроизводстваСобственныеСредства'] = lib670.getfloatval('Привлечение ресурсов организации', 'Средства производства', sheet)
    meansofproduct.attrib['ВыбылоСредствПроизводства'] = lib670.getfloatval('Списание в рамках контракта', 'Средства производства', sheet)
    meansofproduct.attrib['ВыбылоСредствПроизводстваНаДругиеКонтракты'] = lib670.getfloatval('Использование ресурсов на другие контракты государственного заказчика', 'Средства производства', sheet)
    meansofproduct.attrib['ВыбылоСредствПроизводстваНуждыОрганизации'] = lib670.getfloatval('Использование ресурсов на нужды организации', 'Средства производства', sheet)

    prodactiongroup = ET.SubElement(contractresallocgroup, 'ГруппаПроизводство')
    prodactiongroup.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Производство', sheet)
    prodactiongroup.attrib['ПроизводственныеЗатраты'] = lib670.getfloatval('Движение в рамках контракта', 'Производство', sheet)
    prodactiongroup.attrib['ПроизводственныеЗатратыДругихКонтрактов'] = lib670.getfloatval('Привлечение ресурсов с других контрактов', 'Производство', sheet)
    prodactiongroup.attrib['ПроизводственныеЗатратыСобственные'] = lib670.getfloatval('Привлечение ресурсов организации', 'Производство', sheet)
    prodactiongroup.attrib['Выпуск'] = lib670.getfloatval('Списание в рамках контракта', 'Производство', sheet)
    prodactiongroup.attrib['ВыпускНаДругиеКонтракты'] = lib670.getfloatval('Использование ресурсов на другие контракты государственного заказчика', 'Производство', sheet)
    prodactiongroup.attrib['ВыпускНуждыОрганизации'] = lib670.getfloatval('Использование ресурсов на нужды организации', 'Производство', sheet)

    materialcosts = ET.SubElement(prodactiongroup, 'МатериальныеЗатраты')
    materialcosts.attrib['ЦелевойПоказатель'] = lib670.getfloatval('Целевые параметры контракта', 'Затраты на материалы', sheet)
    materialcosts.attrib['ПроцентВыполнения'] = lib670.getpercentval('Выполнено', 'Затраты на материалы', sheet)
    materialcosts.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Затраты на материалы', sheet)
    materialcosts.attrib['СписаноНаЗатраты'] = lib670.getfloatval('Движение в рамках контракта', 'Затраты на материалы', sheet)
    materialcosts.attrib['СписаноЗатратДругихКонтрактов'] = lib670.getfloatval('Привлечение ресурсов с других контрактов', 'Затраты на материалы', sheet)
    materialcosts.attrib['СписаноСобственныхЗатрат'] = lib670.getfloatval('Привлечение ресурсов организации', 'Затраты на материалы', sheet)
    materialcosts.attrib['ИсключеноИзЗатрат'] = lib670.getfloatval('Списание в рамках контракта', 'Затраты на материалы', sheet)
    materialcosts.attrib['ОтнесеноНаДругиеКонтракты'] = lib670.getfloatval('Использование ресурсов на другие контракты государственного заказчика', 'Затраты на материалы', sheet)
    materialcosts.attrib['ОтнесеноНаСобственныеЗатраты'] = lib670.getfloatval('Использование ресурсов на нужды организации', 'Затраты на материалы', sheet)

    payrollcosts = ET.SubElement(prodactiongroup, 'ЗатратыФОТ')
    payrollcosts.attrib['ЦелевойПоказатель'] = lib670.getfloatval('Целевые параметры контракта', 'Затраты на оплату труда', sheet)
    payrollcosts.attrib['ПроцентВыполнения'] = lib670.getpercentval('Выполнено', 'Затраты на оплату труда', sheet)
    payrollcosts.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Затраты на оплату труда', sheet)
    payrollcosts.attrib['ЗарплатаИсполнителей'] = lib670.getfloatval('Привлечение ресурсов организации', 'Затраты на оплату труда', sheet)

    otherprodcosts = ET.SubElement(prodactiongroup, 'ПрочиеПроизводственныеЗатраты')
    otherprodcosts.attrib['ЦелевойПоказатель'] = lib670.getfloatval('Целевые параметры контракта', 'Прочие производственные затраты', sheet)
    otherprodcosts.attrib['ПроцентВыполнения'] = lib670.getpercentval('Выполнено', 'Прочие производственные затраты', sheet)
    otherprodcosts.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Прочие производственные затраты', sheet)
    otherprodcosts.attrib['СписаноНаЗатраты'] = lib670.getfloatval('Движение в рамках контракта', 'Прочие производственные затраты', sheet)
    otherprodcosts.attrib['СписаноЗатратДругихКонтрактов'] = lib670.getfloatval('Привлечение ресурсов с других контрактов', 'Прочие производственные затраты', sheet)
    otherprodcosts.attrib['СписаноСобственныхЗатрат'] = lib670.getfloatval('Привлечение ресурсов организации', 'Прочие производственные затраты', sheet)
    otherprodcosts.attrib['ИсключеноИзЗатрат'] = lib670.getfloatval('Списание в рамках контракта', 'Прочие производственные затраты', sheet)
    otherprodcosts.attrib['ОтнесеноНаДругиеКонтракты'] = lib670.getfloatval('Использование ресурсов на другие контракты государственного заказчика', 'Прочие производственные затраты', sheet)
    otherprodcosts.attrib['ОтнесеноНаСобственныеЗатраты'] = lib670.getfloatval('Использование ресурсов на нужды организации', 'Прочие производственные затраты', sheet)

    totalprodcosts = ET.SubElement(prodactiongroup, 'ОбщепроизводственныеЗатраты')
    totalprodcosts.attrib['ЦелевойПоказатель'] = lib670.getfloatval('Целевые параметры контракта', 'Общепроизводственные затраты', sheet)
    totalprodcosts.attrib['ПроцентВыполнения'] = lib670.getpercentval('Выполнено', 'Общепроизводственные затраты', sheet)
    totalprodcosts.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Общепроизводственные затраты', sheet)
    totalprodcosts.attrib['РазмерЗатрат'] = lib670.getfloatval('Привлечение ресурсов организации', 'Общепроизводственные затраты', sheet)

    generalbuscosts = ET.SubElement(prodactiongroup, 'ОбщехозяйственныеЗатраты')
    generalbuscosts.attrib['ЦелевойПоказатель'] = lib670.getfloatval('Целевые параметры контракта', 'Общехозяйственные затраты', sheet)
    generalbuscosts.attrib['ПроцентВыполнения'] = lib670.getpercentval('Выполнено', 'Общехозяйственные затраты', sheet)
    generalbuscosts.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Общехозяйственные затраты', sheet)
    generalbuscosts.attrib['РазмерЗатрат'] = lib670.getfloatval('Привлечение ресурсов организации', 'Общехозяйственные затраты', sheet)

    semi_prodintwork = ET.SubElement(prodactiongroup, 'ПолуфабрикатыВнутренниеРаботы')
    semi_prodintwork.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Полуфабрикаты, внутренние работы', sheet)
    semi_prodintwork.attrib['СписаноНаЗатраты'] = lib670.getfloatval('Движение в рамках контракта', 'Полуфабрикаты, внутренние работы', sheet)

    released_semi_prodintwork = ET.SubElement(prodactiongroup, 'ВыпускПолуфабрикатовВнутреннихРабот')
    released_semi_prodintwork.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Выпуск полуфабрикатов, внутренних работ', sheet)
    released_semi_prodintwork.attrib['Выпущено'] = lib670.getfloatval('Списание в рамках контракта', 'Выпуск полуфабрикатов, внутренних работ', sheet)

    prodoutput = ET.SubElement(prodactiongroup, 'ВыпускПродукции')
    prodoutput.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Выпуск продукции', sheet)
    prodoutput.attrib['Выпущено'] = lib670.getfloatval('Списание в рамках контракта', 'Выпуск продукции', sheet)

    finishprod = ET.SubElement(contractresallocgroup, 'ГотоваяПродукция')
    finishprod.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Готовый товар на складе', sheet)
    finishprod.attrib['Выпущено'] = lib670.getfloatval('Движение в рамках контракта', 'Готовый товар на складе', sheet)
    finishprod.attrib['ИспользованоСДругихКонтрактов'] = lib670.getfloatval('Привлечение ресурсов с других контрактов', 'Готовый товар на складе', sheet)
    finishprod.attrib['ИспользованоСобственной'] = lib670.getfloatval('Привлечение ресурсов организации', 'Готовый товар на складе', sheet)
    finishprod.attrib['Отгружено'] = lib670.getfloatval('Списание в рамках контракта', 'Готовый товар на складе', sheet)
    finishprod.attrib['ОтгруженоНаДругиеКонтракты'] = lib670.getfloatval('Использование ресурсов на другие контракты государственного заказчика', 'Готовый товар на складе', sheet)
    finishprod.attrib['ОтгруженоНаНуждыОрганизации'] = lib670.getfloatval('Использование ресурсов на нужды организации', 'Готовый товар на складе', sheet)

    shipprodgroup = ET.SubElement(contract, 'ГруппаОтгрузкаПродукцииВыполнениеРабот')
    shipprodgroup.attrib['ЦелевойПоказатель'] = lib670.getfloatval('Целевые параметры контракта', 'Отгрузка товара, выполнение работ, оказание услуг', sheet)
    shipprodgroup.attrib['ПроцентВыполнения'] = lib670.getpercentval('Выполнено', 'Отгрузка товара, выполнение работ, оказание услуг', sheet)
    shipprodgroup.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Отгрузка товара, выполнение работ, оказание услуг', sheet)

    costprice = ET.SubElement(shipprodgroup, 'СебестоимостьПродаж')
    costprice.attrib['ЦелевойПоказатель'] = lib670.getfloatval('Целевые параметры контракта', 'Себестоимость реализованной продукции', sheet)
    costprice.attrib['ПроцентВыполнения'] = lib670.getpercentval('Выполнено', 'Себестоимость реализованной продукции', sheet)
    costprice.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Себестоимость реализованной продукции', sheet)
    costprice.attrib['СебестоимостьКонтракт'] = lib670.getfloatval('Движение в рамках контракта', 'Себестоимость реализованной продукции', sheet)
    costprice.attrib['СебестоимостьНеКонтракт'] = lib670.getfloatval('Привлечение ресурсов организации', 'Себестоимость реализованной продукции', sheet)

    admincosts = ET.SubElement(shipprodgroup, 'АУР')
    admincosts.attrib['ЦелевойПоказатель'] = lib670.getfloatval('Целевые параметры контракта', 'Административно-управленческие расходы', sheet)
    admincosts.attrib['ПроцентВыполнения'] = lib670.getpercentval('Выполнено', 'Административно-управленческие расходы', sheet)
    admincosts.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Административно-управленческие расходы', sheet)
    admincosts.attrib['РазмерЗатрат'] = lib670.getfloatval('Привлечение ресурсов организации', 'Административно-управленческие расходы', sheet)

    commerscosts = ET.SubElement(shipprodgroup, 'КоммерческиеРасходы')
    commerscosts.attrib['ЦелевойПоказатель'] = lib670.getfloatval('Целевые параметры контракта', 'Коммерческие расходы', sheet)
    commerscosts.attrib['ПроцентВыполнения'] = lib670.getpercentval('Выполнено', 'Коммерческие расходы', sheet)
    commerscosts.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Коммерческие расходы', sheet)
    commerscosts.attrib['РазмерЗатрат'] = lib670.getfloatval('Движение в рамках контракта', 'Коммерческие расходы', sheet)

    bankinterest = ET.SubElement(shipprodgroup, 'ПроцентыПоБанковскимКредитам')
    bankinterest.attrib['ЦелевойПоказатель'] = lib670.getfloatval('Целевые параметры контракта', 'Проценты по кредитам банка', sheet)
    bankinterest.attrib['ПроцентВыполнения'] = lib670.getpercentval('Выполнено', 'Проценты по кредитам банка', sheet)
    bankinterest.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Проценты по кредитам банка', sheet)
    bankinterest.attrib['РазмерЗатрат'] = lib670.getfloatval('Движение в рамках контракта', 'Проценты по кредитам банка', sheet)

    VATvalue = ET.SubElement(shipprodgroup, 'НДСПродажи')
    VATvalue.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'НДС с выручки от продаж', sheet)
    VATvalue.attrib['СуммаНДС'] = lib670.getfloatval('Привлечение ресурсов организации', 'НДС с выручки от продаж', sheet)

    profitvalue = ET.SubElement(shipprodgroup, 'Прибыль')
    profitvalue.attrib['ЦелевойПоказатель'] = lib670.getfloatval('Целевые параметры контракта', 'Прибыль контракта', sheet)
    profitvalue.attrib['ПроцентВыполнения'] = lib670.getpercentval('Выполнено', 'Прибыль контракта', sheet)
    profitvalue.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Прибыль контракта', sheet)

    redirectgroup = ET.SubElement(contract, 'ПеренаправлениеПривлечение')
    redirectgroup.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', '(+) Привлечение ресурсов в контракт/(-) Перенаправление ресурсов контракта', sheet)
    redirectgroup.attrib['ПривлеченоСредствДругихКонтрактов'] = lib670.getfloatval('Привлечение ресурсов с других контрактов', '(+) Привлечение ресурсов в контракт/(-) Перенаправление ресурсов контракта', sheet)
    redirectgroup.attrib['ПривлеченоСобственныхСредств'] = lib670.getfloatval('Привлечение ресурсов организации', '(+) Привлечение ресурсов в контракт/(-) Перенаправление ресурсов контракта', sheet)
    redirectgroup.attrib['ИспользованоНаДругиеКонтракты'] = lib670.getfloatval('Использование ресурсов на другие контракты государственного заказчика', '(+) Привлечение ресурсов в контракт/(-) Перенаправление ресурсов контракта', sheet)
    redirectgroup.attrib['ИспользованоНаСобственныеНужды'] = lib670.getfloatval('Использование ресурсов на нужды организации', '(+) Привлечение ресурсов в контракт/(-) Перенаправление ресурсов контракта', sheet)

    writtenoffmoney = ET.SubElement(contract, 'СписаноСредств')
    writtenoffmoney.attrib['ЦелевойПоказатель'] = lib670.getfloatval('Целевые параметры контракта', 'Списание денежных средств с отдельного счета контракта', sheet)
    writtenoffmoney.attrib['ПроцентВыполнения'] = lib670.getpercentval('Выполнено', 'Списание денежных средств с отдельного счета контракта', sheet)
    writtenoffmoney.attrib['СальдоОпераций'] = lib670.getfloatval('Сальдо операций', 'Списание денежных средств с отдельного счета контракта', sheet)

logging.info("Обработано " + str(num_process) + " файлов")
with open('message.xml', 'wb') as f:
   xml_string = ET.tostring(root,  encoding='UTF-8',  method='xml')
   f.write(minidom.parseString(xml_string).toprettyxml(encoding="UTF-8"))
xsd_schema = xmlschema.XMLSchema('..\\bin\\vp.xsd')
if xsd_schema.is_valid('message.xml'):
    os.system('move message.xml ..\\out')
    os.system('call ..\\bin\\sign.bat')
else:
    logging.error("Не пройдена XSD валидация")
    logging.error("Выгрузка не произведена")



