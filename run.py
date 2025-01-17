#  ______________________________________ SETTING THE ENVIRONMENT ________________________________
import datetime
import io
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import analyzer
import columns
import devices
import frontend
import plots
import prints
import sadzax
sadzax.Out.reconfigure_encoding()
sadzax.Out.clear_future_warning()


#  ______________________________________ OBTAINING DATA _________________________________________
prints.info('Установление параметров для анализа')

device_type = prints.device_picking()
# device_type = 'mon'
dev = device_type
# prints.file_picking(dev)
# data = devices.Pkl.load(dev)
data = analyzer.stack_data(dev)
cols_list = columns.columns_list_maker(dev, data)
cols = columns.columns_analyzer(dev, cols_list)
del cols_list
data = analyzer.pass_the_nan(device_type=device_type, data=data, cols=cols)  # update data_types
data = analyzer.set_dtypes(device_type=device_type, data=data, cols=cols)
# devices.Pkl.save(device_type=device_type, data=data)


#  ______________________________________ COUNTERS AND TIME ANALYZERS ____________________________
prints.info('Анализ неразрывности замеров и их корректности')

#  Returning total counter of measures and their period
prints.total_log_counter(dev, data)
prints.total_periods(dev, data)

#  Asking for a period to choose
status = sadzax.question(
        f"\n Хотите задать конкретный период анализа между двумя датами?"
        f"\n Eсли нет - то будут проанализированы все доступные периоды замеров\n", yes='y')
if status == 'y':
    data = analyzer.time_period_choose(data, dev)
    prints.total_log_counter(dev, data)
    prints.total_periods(dev, data)


#  Analyzing time measures for sequence errors
values_time_analyzer = analyzer.values_time_analyzer(dev, data, time_sequence_min=1, inaccuracy_sec=3)
prints.values_time_analyzer(dev, data, log=values_time_analyzer)

#  Choosing the slice of time periods (the delimiter for defining a new time slice is 1440 minutes / 1 day)
values_time_slicer = analyzer.values_time_slicer(dev, data, values_time_analyzer,
                                                 minutes_slice_mode=1440, min_values_required=150)
data = prints.values_time_slicer(dev, data, log=values_time_slicer)

#  Analyzing data for false measurements
total_nan_counter = analyzer.total_nan_counter(dev, data, false_data_percentage=30.0)
prints.total_nan_counter(dev, data, false_data_percentage=30.0, log=total_nan_counter)
total_nan_counter_ease = analyzer.total_nan_counter_ease(total_nan_counter)
if total_nan_counter_ease != None:
    print(total_nan_counter_ease)


#  ______________________________________ CORRELATIONS AND AVERAGES ______________________________
prints.info('Анализ трендов и средних показателей')

#  Defining the most usual 'ex'amples (deviation delta and tangent delta) for further correlation analyze
ex1 = '∆C'
ex2 = '∆tg'

print(f'Анализ корреляций (чем более явная корреляция, тем больше отклонение графа от оси шагов:'
      f' вверх для прямой корреляции, вниз - для обратной)')

#  Correlation of ∆C and temperature with a plot
plots.correlation_plot(filter_list1=[ex1], filter_list2=['tair'], device_type=device_type, data=data, cols=cols,
                       title=f"Анализ корреляции данных {ex1} от температуры воздуха")

#  Correlation of ∆tg and temperature with a plot
plots.correlation_plot(filter_list1=[ex2], filter_list2=['tair'], device_type=device_type, data=data, cols=cols,
                       title=f"Анализ корреляции данных {ex2} от температуры воздуха")

#  Average values of ∆C and their distribution
prints.average_printer(ex=ex1, data=data, cols=cols, abs_parameter=True)
plots.histogram([ex1], data=data, cols=cols, title=f'Распределение значений {ex1}')

#  Average values of ∆tg  and their distribution
prints.average_printer(ex=ex2, data=data, cols=cols, abs_parameter=True)
plots.histogram([ex2], data=data, cols=cols, title=f'Распределение значений {ex2}')


#  ______________________________________ WARNINGS AND ACCIDENTS _________________________________
prints.info('Анализ срабатываний предупредительной и аварийной сигнализации')

for k in devices.links(device_type)[10]:
    w0 = devices.links(device_type)[10][k][0]
    w1 = devices.links(device_type)[10][k][1]
    print(
        f'\nПревышение уровней {k} для срабатывания предупредительной (±{w0}) или аварийной (±{w1}) сигнализации: \r')
    #  Main operation
    warning_finder = analyzer.warning_finder([k], dev, data, cols, w0, w1)
    status = sadzax.question(
        f"Вывести кратко? \n (Только срабатывания аварийной сигнализации {k} без предупредительной)"
        f" \n Eсли нет - то будут выведены и предупредительные, и аварийные замеры ", yes='y', no='n')
    warnings_codes_temporal_list = {'acc': 'аварийной'}
    if status == 'n':
        warnings_codes_temporal_list = {'war': 'предупредительной', 'acc': 'аварийной'}
    for warn_code, warn_code_str in warnings_codes_temporal_list.items():
        prints.warning_printer(dev, warning_finder, warn_code, warning_param_war=w0, warning_param_acc=w1)
        warning_finder_ease = analyzer.warning_finder_ease(warning_finder, dev, warn_code, min_values_for_print=10,
                                                           warning_param_war=w0, warning_param_acc=w1)
        print(warning_finder_ease)
        #  Scattering
        warning_finder_merge = analyzer.warning_finder_merge(warning_finder, dev, data, warn_code, w0, w1)
        plots.scatter(df=warning_finder_merge, device_type=dev, title=f'График {warn_code_str} сигнализации')


#  ______________________________________ DATA ENG. ______________________________________________

main_graph_params = {
    'U': 'График изменения значений напряжений',
    'Ia': 'График изменения активной составляющей токов утечек',
    'Ir': 'График изменения реактивной составляющей токов утечек',
    'tg': 'График изменения значений tgδ',
    'C': 'График изменения значений емкостей С1',
    '∆tg': 'График изменения значений ∆tgδ (изменение tgδ относительно начальных значений)',
    '∆C': 'График изменения значений ∆C/C1 (изменение емкостей С1 относительно начальных значений)'
}

for code_key, code_desc in {'_HV': ' со стороны высокого напряжения',
                            '_MV': ' со стороны среднего напряжения'}.items():
    prints.info(f'Анализ значений параметров высоковольтных вводов в фазах А, В и С{code_desc}')
    for key, desc in main_graph_params.items():
        input_y = key + code_key
        title = desc + code_desc
        prints.print_flat_graph(input_y=[input_y], device_type=dev, data=data, cols=cols, title=title)
