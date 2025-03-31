import sqlite3


with sqlite3.connect('base.db') as db:
    cursor = db.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS notebook (
        date UNIQUE,
        odo_one DEFAULT '',
        addr_one DEFAULT '',
        luw_one DEFAULT '',
        awning_one TEXT DEFAULT '',
        odo_two DEFAULT '',
        addr_two DEFAULT '',
        luw_two DEFAULT '',
        awning_two TEXT DEFAULT '',
        odo_three DEFAULT '',
        addr_three DEFAULT '',
        luw_three DEFAULT '',
        awning_three TEXT DEFAULT '',
        odo_reset DEFAULT '',
        fuel DEFAULT '',
        brand_fuel DEFAULT '',
        plain_repair DEFAULT '',
        note DEFAULT ''
    )"""
    cursor.execute(query)


def check_date(x):
    if 0 < int(x.split(sep='.')[0]) < 31 and 0 < int(x.split(sep='.')[1]) < 13 and 0 < int(x.split(sep='.')[2]) < 99:
        return True
    else:
        raise ValueError


def check_odo(x):
    if 0 < int(x) < 100000000:
        return True
    else:
        raise ValueError


def check_luw(x):
    if 0 < int(x) < 1000:
        return True
    else:
        raise ValueError


def check_plain_repair(x):
    if x.lower() == 'п' or x.lower() == 'р':
        return True
    else:
        raise ValueError


def check_awning(x):
    if x.lower() == 'д' or x.lower() == 'н':
        return True
    else:
        raise ValueError


def check_fuel(x):
    if 0 < int(x) < 1000:
        return True
    else:
        raise ValueError


def check_mounth(x):
    if 0 < int(x.split(sep='.')[0]) < 13 and 0 < int(x.split(sep='.')[1]) < 99:
        return True
    else:
        raise ValueError


def date_mounth(date):
    return int(date.split('.')[1])


def date_year(date):
    return int(date.split('.')[0])


def convert_mounth(mounth):
    if mounth == 1:
        return 'Январь'
    elif mounth == 2:
        return 'Февраль'
    elif mounth == 3:
        return 'Март'
    elif mounth == 4:
        return 'Апрель'
    elif mounth == 5:
        return 'Май'
    elif mounth == 6:
        return 'Июнь'
    elif mounth == 7:
        return 'Июль'
    elif mounth == 8:
        return 'Август'
    elif mounth == 9:
        return 'Сентябрь'
    elif mounth == 10:
        return 'Октябрь'
    elif mounth == 11:
        return 'Ноябрь'
    elif mounth == 12:
        return 'Декабрь'
    elif mounth.lower() == 'январь':
        return 1
    elif mounth.lower() == 'февраль':
        return 2
    elif mounth.lower() == 'март':
        return 3
    elif mounth.lower() == 'апрель':
        return 4
    elif mounth.lower() == 'май':
        return 5
    elif mounth.lower() == 'июнь':
        return 6
    elif mounth.lower() == 'июль':
        return 7
    elif mounth.lower() == 'август':
        return 8
    elif mounth.lower() == 'сентябрь':
        return 9
    elif mounth.lower() == 'октябрь':
        return 10
    elif mounth.lower() == 'ноябрь':
        return 11
    elif mounth.lower() == 'декабрь':
        return 12


def reverse_date(data):
    def zero_plus(x):
        return '0' + x if len(x) == 1 else x
    one, two, three = data.split('.')[0], data.split('.')[1], data.split('.')[2]
    return f'{zero_plus(three)}.{zero_plus(two)}.{zero_plus(one)}'


def all_date():
    return cursor.execute('SELECT date FROM notebook ORDER BY date').fetchall()


def km_rub(km):
    if km < 500:
        return round(km * 15.66, 3)
    elif 500 <= km < 1000:
        return round(km * 12.615, 3)
    elif 1000 <= km < 1500:
        return round(km * 10.875, 3)
    elif 1500 <= km < 2000:
        return round(km * 10.005, 3)
    elif km >= 2000:
        return round(km * 8.961, 3)


def luw_rub(luw):
    return round(luw * 435, 2)


def awning_rub(awning):
    return round(awning * 1740, 2)


def plain_rub(plain):
    return round(plain * 1305, 2)


def repair_rub(repair):
    return round(repair * 2001, 2)


def record_unload(date, odo, addr, luw, awning):
    date = reverse_date(date)
    if (date,) not in all_date():
        cursor.execute('INSERT OR REPLACE INTO notebook(date, odo_one, addr_one, luw_one, awning_one) VALUES(?,?,?,?,?)', (date, odo, addr, luw, awning,))
    else:
        all_odo = cursor.execute('SELECT odo_one, odo_two, odo_three, odo_reset FROM notebook WHERE date = ?', (date,)).fetchmany()
        if not all_odo[0][3] and not all_odo[0][0] and not all_odo[0][1] and not all_odo[0][2]:
            cursor.execute('UPDATE notebook SET odo_one = ?, addr_one = ?, luw_one = ?, awning_one = ? WHERE date = ?', (odo, addr, luw, awning, date,))
        elif all_odo[0][0] and not all_odo[0][1] and not all_odo[0][2]:
            cursor.execute('UPDATE notebook SET odo_two = ?, addr_two = ?, luw_two = ?, awning_two = ? WHERE date = ?', (odo, addr, luw, awning, date,))
        elif all_odo[0][0] and all_odo[0][1] and not all_odo[0][2]:
            cursor.execute('UPDATE notebook SET odo_three = ?, addr_three = ?, luw_three = ?, awning_three = ? WHERE date = ?', (odo, addr, luw, awning, date,))
        elif all_odo[0][3] and not all_odo[0][0] and not all_odo[0][1] and not all_odo[0][2]:
            cursor.execute('UPDATE notebook SET odo_one = ?, addr_one = ?, luw_one = ?, awning_one = ? WHERE date = ?', (odo, addr, luw, awning, date,))
        else:
            print('Ошибка записи данных! ')  
    db.commit()


def record_zeroing(date, odo):
    date = reverse_date(date)
    if (date,) not in all_date():
        cursor.execute('INSERT OR REPLACE INTO notebook(date, odo_reset) VALUES(?,?)', (date, odo,))
    else:
        cursor.execute('UPDATE notebook SET odo_reset = ?  WHERE date = ?', (odo, date,))
    db.commit()


def record_fuel(date, fuel, brand_fuel):
    date = reverse_date(date)
    if (date,) not in all_date():
        cursor.execute('INSERT OR REPLACE INTO notebook(date, fuel, brand_fuel) VALUES(?,?,?)', (date, fuel, brand_fuel,))
    else:
        cursor.execute('UPDATE notebook SET fuel = ?, brand_fuel = ? WHERE date = ?', (fuel, brand_fuel, date,))
    db.commit()


def record_plain_repair(date, plain_repair):
    date = reverse_date(date)
    if (date,) not in all_date():
        cursor.execute('INSERT OR REPLACE INTO notebook(date, plain_repair) VALUES(?,?)', (date, plain_repair.lower(),))
    else:
        cursor.execute('UPDATE notebook SET plain_repair = ? WHERE date = ?', (plain_repair.lower(), date,))
    db.commit()


def record_note(date, note):
    date = reverse_date(date)
    if (date,) not in all_date():
        cursor.execute('INSERT OR REPLACE INTO notebook(date, note) VALUES(?,?)', (date, note,))
    else:
        cursor.execute('UPDATE notebook SET note = ? WHERE date = ?', (note, date,))
    db.commit()


def delete_to_date(date_to_delete):
    year = date_to_delete.split('.')[2]
    mounth = date_to_delete.split('.')[1]
    day = date_to_delete.split('.')[0]
    check = False
    for i in all_date():
        if int(i[0].split('.')[0]) == int(year) and int(i[0].split('.')[1]) == int(mounth) and int(i[0].split('.')[2]) == int(day):
            check = True
    if not check:
        raise ValueError
    date_to_delete = reverse_date(date_to_delete)
    cursor.execute('DELETE FROM notebook WHERE date = ?', (date_to_delete,))
    db.commit()


def odometr_mounth(mounth, year):
    first_line = None
    all_odo_date = [i for i in cursor.execute('SELECT odo_one, odo_two, odo_three, odo_reset, date FROM notebook ORDER BY date').fetchall() if i[0] or i[1] or i[2] or i[3]]
    last_line = [i for i in all_odo_date if int(i[-1].split('.')[1]) == mounth and int(i[-1].split('.')[0]) == year and not i[3]][-1]
    last_line = (int([i for i in last_line[:3] if i][-1]), last_line[-1])
    for i in all_odo_date:
        if int(i[-1].split('.')[1]) == mounth - 1 and int(i[-1].split('.')[0]) == year:
            if i[0] or (not first_line and i[3]):
                first_line = i
        elif not first_line and int(i[-1].split('.')[1]) == mounth and int(i[-1].split('.')[0]) == year:
            if i[0] or i[3]:
                first_line = i
    if first_line[0]:
        first_line = (int([i for i in first_line[:3] if i][-1]), first_line[-1])
    else:
        first_line = (int(first_line[3]), first_line[-1])
    return last_line[0] - first_line[0], last_line, first_line, all_odo_date


def number_trips_mounth(mounth, year):
    last = odometr_mounth(mounth, year)[1]
    first = odometr_mounth(mounth, year)[2]
    all_odo = odometr_mounth(mounth, year)[3]
    ltm = [i for i in all_odo if int(i[-1].replace('.', '')) >= int(first[-1].replace('.', '')) and int(i[-1].replace('.', '')) <= int(last[-1].replace('.', '')) and (i[0] or i[3] and i[4] == first[-1])]
    ltm.append(('0', '', '', '', ''))
    lst_data_km = []

    def tmp(x):
        tmp = None
        for j in x[:3]:
            if j:
                tmp = j
        if not tmp:
            tmp = x[3]
        return tmp
    
    for index, i in enumerate(ltm[:-1]):
        if index == 0:
            if int(i[4].split('.')[1]) == mounth - 1:
                lst_data_km.append([reverse_date(i[-1]), int(ltm[index + 1][0]) - int(tmp(i))])
            else:
                if i[2]:
                    lst_data_km.append([reverse_date(i[-1]), int(i[1]) - int(i[0])])
                    lst_data_km.append([reverse_date(i[-1]), int(i[2]) - int(i[1])])
                    lst_data_km.append([reverse_date(i[-1]), int(ltm[index + 1][0]) - int(i[2])])                                       
                elif i[1] and not i[2]:
                    lst_data_km.append([reverse_date(i[-1]), int(i[1]) - int(i[0])])
                    lst_data_km.append([reverse_date(i[-1]), int(ltm[index + 1][0]) - int(i[1])])
                elif i[0] and not i[1]:
                    lst_data_km.append([reverse_date(i[-1]), int(ltm[index + 1][0]) - int(i[0])])
                elif not i[0] and i[3]:
                    lst_data_km.append([reverse_date(i[-1]), int(ltm[index + 1][0]) - int(i[3])])
        else:
            if i[2]:
                lst_data_km.append([reverse_date(i[-1]), int(i[1]) - int(i[0])])
                lst_data_km.append([reverse_date(i[-1]), int(i[2]) - int(i[1])])
                lst_data_km.append([reverse_date(i[-1]), int(ltm[index + 1][0]) - int(i[2])])
            elif i[1] and not i[2]:
                lst_data_km.append([reverse_date(i[-1]), int(i[1]) - int(i[0])])
                lst_data_km.append([reverse_date(i[-1]), int(ltm[index + 1][0]) - int(i[1])])
            elif i[0] and not i[1]:
                lst_data_km.append([reverse_date(i[-1]), int(ltm[index + 1][0]) - int(i[0])])
            elif not i[0] and i[3]:
                lst_data_km.append([reverse_date(i[-1]), int(ltm[index + 1][0]) - int(i[3])])
    lst_data_km = lst_data_km[:-1]

    return lst_data_km


def luw_mounth(mounth, year):
    all_luw = [i for i in cursor.execute('SELECT luw_one, luw_two, luw_three, date FROM notebook ORDER BY date').fetchall() if i[0] or i[1] or i[2]]
    lst_luw = []
    for i in all_luw:
        if date_mounth(i[-1]) == mounth and date_year(i[-1]) == year:
            for j in i[:3]:
                if j:
                    lst_luw.append(int(j))
    return sum(lst_luw)


def awning_mounth(mounth, year):
        awning = cursor.execute('SELECT awning_one, awning_two, awning_three, date FROM notebook WHERE awning_one = "д" OR awning_two = "д" OR awning_three = "д"').fetchall()
        res = []
        for i in awning:
            if date_mounth(i[-1]) == mounth and date_year(i[-1]) == year and (mounth == 12 or mounth == 1 or mounth == 2):
                [res.append(j) for j in i if j == 'д']
        db.commit()
        return len(res)


def plain(mounth, year):
    all_plain = [i for i in cursor.execute('SELECT plain_repair, date FROM notebook WHERE plain_repair = "п" OR plain_repair = "П"').fetchall() if i[0]]
    res = []
    for i in all_plain:
        if date_mounth(i[-1]) == mounth and date_year(i[-1]) == year:
            res.append(i[0])
    return len(res)


def repair(mounth, year):
    all_plain = [i for i in cursor.execute('SELECT plain_repair, date FROM notebook WHERE plain_repair = "р" OR plain_repair = "Р"').fetchall() if i[0]]
    res = []
    for i in all_plain:
        if date_mounth(i[-1]) == mounth and date_year(i[-1]) == year:
            res.append(i[0])
    return len(res)


def plain_repair15_15(mounth, year, x='all'):
    check = False
    for i in all_date():
        if int(i[0].split('.')[0]) == int(year) and int(i[0].split('.')[1]) == int(mounth):
            check = True
    if not check:
        raise ValueError
    all_plain_repair = [i for i in cursor.execute('SELECT plain_repair, date FROM notebook WHERE plain_repair = "п" OR plain_repair = "р" ORDER BY date').fetchall()]
    p = []
    r = []
    res1_15 = {'простои': [], 'ремонты': []}
    res16_31 = {'простои': [], 'ремонты': []}
    for i in all_plain_repair:
        if i[0] == 'п' and date_mounth(i[-1]) == mounth and date_year(i[-1]) == year:
            p.append(reverse_date(i[1]))
        elif i[0] == 'р' and date_mounth(i[-1]) == mounth and date_year(i[-1]) == year:
            r.append(reverse_date(i[1]))
    for i in p:
        if 1 <= int(i.split('.')[0]) <= 15:
            res1_15['простои'].append(i)
        elif 16 <= int(i.split('.')[0]) <= 31:
            res16_31['простои'].append(i)
    for i in r:
        if 1 <= int(i.split('.')[0]) <= 15:
            res1_15['ремонты'].append(i)
        elif 16 <= int(i.split('.')[0]) <= 31:
            res16_31['ремонты'].append(i)
    if x == 'one':
        res_p = res1_15['простои']
        res_r = res1_15['ремонты']
        res = 'Нет простоев/ремонтов'
        if res_p and res_r:
            res = f'''простои: 
''' + '\n'.join(res_p) + f'''
ремонты: 
''' + '\n'.join(res_r)
        elif res_p and not res_r:
            res = f'''простои: 
''' + '\n'.join(res_p)
        elif res_r and not res_p:
            res = f'''ремонты: 
''' + '\n'.join(res_r)
        return res
    elif x == 'two':
        res_p = res16_31['простои']
        res_r = res16_31['ремонты']
        res = 'Нет простоев/ремонтов'
        if res_p and res_r:
            res = f'''простои: 
''' + '\n'.join(res_p) + f'''
ремонты: 
''' + '\n'.join(res_r)
        elif res_p and not res_r:
            res = f'''простои: 
''' + '\n'.join(res_p)
        elif res_r and not res_p:
            res = f'''ремонты: 
''' + '\n'.join(res_r)
        return res
    elif x == 'all':
        res_p = res1_15['простои'] + res16_31['простои']
        res_r = res1_15['ремонты'] + res16_31['ремонты']
        res = 'Нет простоев/ремонтов'
        if res_p and res_r:
            res = f'''простои: 
''' + '\n'.join(res_p) + f'''
ремонты: 
''' + '\n'.join(res_r)
        elif res_p and not res_r:
            res = f'''простои: 
''' + '\n'.join(res_p)
        elif res_r and not res_p:
            res = f'''ремонты: 
''' + '\n'.join(res_r)
        return res


def delete_row_by_date(date_to_delete):
    cursor.execute('DELETE FROM notebook WHERE date = ?', (date_to_delete,))
    db.commit()


def moneys(mounth, year):
    res = 0
    for i in range(len(number_trips_mounth(mounth, year))):
        res += km_rub(number_trips_mounth(mounth, year)[i][1])
    # res += luw_rub(luw_mounth(mounth, year))
    res += plain_rub(plain(mounth, year))
    res += repair_rub(repair(mounth, year))
    return round(res, 2)


def info_for_mounth(mounth, year):
    res = f'''
▶  <b>{convert_mounth(mounth)} {year}</b>  ◀
_ _ _ _ _ _ _ _ _ _ _ _
<i>пробег:</i>  {odometr_mounth(mounth, year)[0]} км
<i>рейсов:</i>  {len(number_trips_mounth(mounth, year))}
<i>ПРР:</i>  {luw_mounth(mounth, year)}
<i>расшториваний:</i>  {awning_mounth(mounth, year)}
<i>простоев:</i>  {plain(mounth, year)}
<i>ремонтов:</i>  {repair(mounth, year)}
<i>доход:</i>  {moneys(mounth, year)} руб.
'''
    return res


def day(day):
    try:
        mounth = int(day.split('.')[1])
        year = int(day.split('.')[2])
        last = [i for i in all_date() if int(i[0].split('.')[1]) == mounth and i[0].split('.')[0] == str(year)][-1]
        first = odometr_mounth(mounth, year)[2]
        all = [i for i in cursor.execute('SELECT * FROM notebook ORDER BY date').fetchall() if i[0]]
        adm = [i for i in all if int(i[0].replace('.', '')) >= int(first[-1].replace('.', '')) and int(i[0].replace('.', '')) <= int(last[-1].replace('.', '')) and (i[0])]
        res = []
        for i in adm:
            if i[0] == reverse_date(day):
                if i[1]:
                    odo_one = f'<i>выгрузка:</i>   <b>{i[1]}</b>'
                    res.append(odo_one)
                if i[2]:
                    addr_one = f'<i>адрес:</i>   <b>{i[2]}</b>'
                    res.append(addr_one)
                if i[3]:
                    luw_one = f'<i>ПРР:</i>   <b>{i[3]}</b>'
                    res.append(luw_one)
                if i[4]:
                    awning_one = f'<i>расшторивание:</i>   <b>{i[4]}</b>'
                    res.append(awning_one)
                if i[5]:
                    odo_two = f'<i>выгрузка2:</i>   <b>{i[5]}</b>'
                    res.append(odo_two)
                if i[6]:
                    addr_two = f'<i>адрес2:</i>   <b>{i[6]}</b>'
                    res.append(addr_two)
                if i[7]:
                    luw_two = f'<i>ПРР2:</i>   <b>{i[7]}</b>'
                    res.append(luw_two)
                if i[8]:
                    awning_two = f'<i>расшторивание2:</i>   <b>{i[8]}</b>'
                    res.append(awning_two)
                if i[9]:
                    odo_three = f'<i>выгрузка3:</i>   <b>{i[9]}</b>'
                    res.append(odo_three)
                if i[10]:
                    addr_three = f'<i>адрес3:</i>   <b>{i[10]}</b>'
                    res.append(addr_three)
                if i[11]:
                    luw_three = f'<i>ПРР3:</i>   <b>{i[11]}</b>'
                    res.append(luw_three)
                if i[12]:
                    awning_three = f'<i>расшторивание3:</i>   <b>{i[12]}</b>'
                    res.append(awning_three)
                if i[13]:
                    odo_reset = f'<i>обнуление:</i>   <b>{i[13]}</b>'
                    res.append(odo_reset)
                if i[14]:
                    fuel = f'<i>заправка:</i>   <b>{i[14]}</b>'
                    res.append(fuel)
                if i[15]:
                    brand_fuel = f'<i>бренд АЗС:</i>   <b>{i[15]}</b>'
                    res.append(brand_fuel)
                if i[16]:
                    plain_repair = f'<i>простой/ремонт:</i>   <b>{i[16]}</b>'
                    res.append(plain_repair)
                if i[17]:
                    note = f'<i>комментарий:</i>   <b>{i[17]}</b>'
                    res.append(note)
                return f'''
▶  <b>{reverse_date(i[0])}</b>  ◀
_ _ _ _ _ _ _ _ _ _ _ _
''' + '\n'.join(res)
    except:
        return 'Нет данных!'


def detail_for_mounth(mounth, year):
    all_date_in_mounth = [i for i in all_date() if int(i[0].split('.')[1]) == mounth and int(i[0].split('.')[0]) == year]
    res = []
    for i in all_date_in_mounth:
        res.append(day(reverse_date(*i)))
    if res:
        return res
    else:
        raise ValueError


def fuel_for_mounth(mounth, year):
    check = False
    for i in all_date():
        if int(i[0].split('.')[0]) == int(year) and int(i[0].split('.')[1]) == int(mounth):
            check = True
    if not check:
        raise ValueError
    all_fuel = [i for i in cursor.execute('SELECT date, fuel, brand_fuel FROM notebook ORDER BY date').fetchall()]
    all_fuel_in_mounth = [i for i in all_fuel if int(i[0].split('.')[1]) == mounth and int(i[0].split('.')[0]) == year if i[1]]
    if not all_fuel_in_mounth:
        return "Нет заправок в этом месяце."
    result_string = f"▶  <b>Заправки за {convert_mounth(mounth)} {year}</b>  ◀\n_ _ _ _ _ _ _ _ _ _ _ _\n"
    total_fuel = 0
    for date, fuel, brand in all_fuel_in_mounth:
        result_string += f"<i>{reverse_date(date)}</i>: {fuel} л. ({brand})\n"
        total_fuel += int(fuel)
    result_string += f"_ _ _ _ _ _ _ _ _ _ _ _\n<b>Итого: {total_fuel} л.</b>"
    return result_string
