import pandas as pd
import analyzer
import devices
import plots
import sadzax


def info(the_string):
    print(f'\n\n          {the_string}...\r')


def file_picking(device_type='kiv'):
    error = 'Пожалуйста, введите корректное значение: цифру, соответствующую пункту из списка'
    files_list = devices.links(device_type)[5]
    w1 = sadzax.Rus.cases(len(files_list), "Доступен", "Доступно", "Доступно")
    w2 = sadzax.Rus.cases(len(files_list), 'файл', 'файла', 'файлов')
    print(f"{w1} {len(files_list)} {w2} для анализа: ")
    for i in files_list:
        print(f"Файл № {files_list.index(i) + 1}. {i}")
    if len(files_list) == 1:
        print(f"Данный файл выбран для анализа")
        return devices.file_pick(device_type, 0)
    elif len(files_list) > 1:
        while True:
            try:
                choice = int(input('Выберите № файла: '))
                if choice <= 0 or choice > len(files_list):
                    print(error)
                    continue
                print(f"Выбран файл № {choice} - {files_list[choice - 1]}")
                return devices.file_pick(device_type, choice - 1)
            except:
                print(error)
                continue


def total_log_counter(device_type, data):
    info('Подсчёт общего количества записей')
    log_total = analyzer.total_log_counter(device_type=device_type, data=data)
    print(f'Общее число записей в журнале измерений составило {log_total}')


def values_time_analyzer(device_type, data, log: pd.core = None):
    info('Анализ периодичности и неразрывности измерений')
    if log is None:
        log = analyzer.values_time_analyzer(device_type=device_type, data=data)
    if log.shape[0] == 0:
        print(f'Периоды измерений не нарушены')
    else:
        print(f'Выявлено {log.shape[0]} нарушений периодов измерений')
        print(sadzax.question('Хотите вывести подробные данные?', yes=log, no=''))


def values_time_slicer(device_type, data, log: dict = None):
    info('Выбор неразрывного периода для анализа')
    if log is None:
        log = analyzer.values_time_slicer(device_type=device_type, data=data)
    error = 'Пожалуйста, введите корректное значение: цифру, соответствующую пункту из списка срезов'
    l = len(log)
    w1 = sadzax.Rus.cases(l, 'найден', 'найдены', 'найдены')
    w2 = sadzax.Rus.cases(l, 'срез', 'среза', 'срезов')
    print(f"По заданным параметрам {w1} {l} {w2} данных")
    k = [i for i in log.keys()]
    for i in log:
        print(f"Срез данных № {k.index(i)+1}. " + log[i][4])
    if l == 1:
        print(f"Срез данных принят к анализу")
        return log[0][0]
    elif len(log) > 1:
        try:
            inputs = sadzax.Enter.mapped_ints('Введите срезы для анализа (либо введите любой текст,'
                                              ' чтобы взять в анализ их все: ')
            inputs = [x for x in inputs if x in k]
        except ValueError:
            inputs = k
        if len(inputs) < 1:
            inputs = k
        print(f"Выбранные срезы данных: \n")
        data = pd.DataFrame.empty
        for choice in inputs:
            print(f"№ {choice}. " + log[k[choice - 1]][4] + "\n")
            iterated_data = log[k[choice - 1]][0]
            if data is pd.DataFrame.empty:
                data = iterated_data
            else:
                data = pd.concat([data, iterated_data])
            del iterated_data


def total_nan_counter(device_type, data, cols, false_data_percentage: float = 33.0, log: pd.core = None):
    info('Анализ периодов массовой некорректности измерений')
    if log is None:
        log_nans = analyzer.total_nan_counter(device_type=device_type, data=data, cols=cols,
                                              false_data_percentage=false_data_percentage)
    w1 = sadzax.Rus.cases(log_nans.shape[0], "Выявлен", "Выявлено", "Выявлено")
    w2 = sadzax.Rus.cases(log_nans.shape[0], "замер", "замера", "замеров")
    if log_nans.shape[0] == 0:
        print(f"\n Периоды некорректных измерений не выявлены")
    else:
        print(f"\n {w1} {log_nans.shape[0]} {w2} с некорректными данными (там, где"
              f" за один замер зафиксировано более {false_data_percentage}% некорректных данных)")
        print(f"Замеры с некорректными данными составили {round((log_nans.shape[0] / data.shape[0]) * 100, 1)}%"
              f" от общего числа произведённых замеров")
        print(sadzax.question('Хотите вывести примеры некорректных данных?', yes=log_nans, no=''))


def average_printer(ex, data, cols, abs_parameter=True):
    print(f'Среднее значение по {ex}: \r')
    df_average = analyzer.data_average_finder(filter_list=[ex], data=data, cols=cols, abs_parameter=abs_parameter)
    if abs_parameter is True:
        str_adder = 'по модулю '
    else:
        str_adder = ''
    for every_value in df_average:
        print(f'Среднее {str_adder}по {every_value} составило {df_average[every_value]}')
    print(f'Распределение значений {ex} (гистограмма): \r')
    plots.histogram([ex], data=data, cols=cols, title=f'Распределение значений {ex}')


def warning_printer(filter_list_append,
                    device_type: str = 'kiv',
                    data: pd.core = None,
                    cols: dict = None,
                    warning_param1=1.0,
                    warning_param2=1.5,
                    warn_type='accident',
                    abs_parameter=True):
    filter_list = ['time']
    if isinstance(filter_list, list) is False:
        filter_list_append = [filter_list_append]
    for x in filter_list_append:
        filter_list.append(x)
    warning_param = 0.0
    if warn_type == 'warning':
        warning_param = warning_param1
        warn_str = 'предупредительной'
    elif warn_type == 'accident':
        warning_param = warning_param2
        warn_str = 'аварийной'
    log_warn = analyzer.warning_finder(filter_list=filter_list,
                                       device_type=device_type,
                                       data=data,
                                       cols=cols,
                                       warning_amount=warning_param,
                                       abs_parameter=abs_parameter)
    for every_df in log_warn:
        if every_df.empty is True:
            print(f'Превышение уровней {every_df.axes[1].values[1]} '
                  f'для срабатывания {warn_str} (±{warning_param}) сигнализации не выявлено')
        else:
            num = every_df.shape[0]
            print(
                f'Выявлено {num} {sadzax.Rus.cases(num, "превышение", "превышения", "превышений")} (±{warning_param}):'
                f'уровней {every_df.axes[1].values[1]} для срабатывания {warn_str} сигнализации. '
                f'\n Процент срабатывания {round((every_df.shape[0] / data.shape[0]) * 100, 3)}% (от общего'
                f' количества замеров')
            print(sadzax.question('Вывести список?', every_df))


def print_flat_graph(input_x=None, input_y=None, device_type='kiv', data=None, cols=None, title=None):
    info(title)
    plots.flat_graph(input_x=input_x, input_y=input_y, device_type=device_type, data=data, cols=cols, title=title)
