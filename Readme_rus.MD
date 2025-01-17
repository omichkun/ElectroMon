# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Оглавление
- [       Оглавление](#-оглавление)
- [       Описание](#-описание)
- [       Реализация](#-реализация)
- [       Требования](#-требования)
- [       Установка](#-установка)
- [       Структура](#-структура)
  - [   Инициализатор устройств (devices.py)](#-инициализатор-устройств-devicespy)
    - [Замеры](#замеры)
    - [Свойства](#свойства)
    - [Источники](#источники)
    - [Ссылки](#ссылки)
    - [Быстрое сохранение и загрузка](#быстрое-сохранение-и-загрузка)
  - [   Обработка столбцов (columns.py)](#-обработка-столбцов-columnspy)
    - [Анализатор столбцов](#анализатор-столбцов)
    - [Столбец времени](#столбец-времени)
  - [   Анализаторы (analyzer.py)](#-анализаторы-analyzerpy)
    - [Импорт данных](#импорт-данных)
    - [Замена данных](#замена-данных)
    - [Счётчик](#счётчик)
    - [Анализатор времени](#анализатор-времени)
    - [Выбор периода](#выбор-периода)
    - [Периоды пустых значений](#периоды-пустых-значений)
    - [Фильтрация](#фильтрация)
    - [Средние значения](#средние-значения)
    - [Распределение значений](#распределение-значений)
    - [Корреляции](#корреляции)
    - [Сигнализаторы](#сигнализаторы)
  - [   Другие модули](#-другие-модули)
- [       Запуск](#-запуск)
  - [   Через интерпретатор Python](#-через-интерпретатор-python)
  - [   Сформировать PDF](#-сформировать-pdf)

&nbsp;

# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Описание

**ElectroMon** - это приложение для мониторинга параметров высокого напряжения.
Оно использует данные, загруженные с устройств, которые производят поминутные замеры на электростанциях, трансформаторах и других электрических устройствах.

&nbsp;

# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Реализация
Основной программный код написан на языке 
**Python** 
с использованием библиотек **pandas** и **numpy** для обработчиков данных.
Графики, диаграммы и выводы в печатный вид создаются с помощью 
**Jupyter Notebook** 
с использованием библиотек **matplotlib** и **reportlab**.

&nbsp;

# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Требования
Для корректной работы требуются дополнительные "классические" библиотеки для Python, все из которых можно загрузить с помощью `pip install`:

Требования по библиотекам перечислены в 
[requirements.txt](requirements.txt) 
в корневой директории.

Фактические устройства используются с использованием кириллических символов. 
Необходимо учитывать особенности кодирования и перевода в программном коде.

&nbsp;

# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Установка

Приложение хранится на [GitHub](https://github.com/sadzax/ElectroMon).

1. Установите [Python v.3.7.+](https://www.python.org/downloads/) 

2. Если вы знакомы с Git, выберите каталог локального компьютера и клонируйте туда репозиторий с помощью команды

`git clone https://github.com/sadzax/ElectroMon.git`

Если у вас не установлен Git, загрузите проект в ZIP-архиве по
[прямой ссылке с GitHub](https://github.com/sadzax/ElectroMon/archive/refs/heads/master.zip) 
и распакуйте его на своем локальном компьютере

3. Скачайте требуемые библиотеки их [requirements.txt](requirements.txt) через `pip install` (см. [Требования](#-требования))
<details><summary>Пример</summary>

Запустите `pip install pandas` в командной строке
</details>

4. Скопируйте выгруженные с устройств файлы во внутреннюю директорию проекта
`/upload/` в зависимости от типа анализируемого устройства
<details><summary>Пример</summary>

Скопируйте файл `UPLOAD001.I` в `c:\users\user\downloads\ElectroMon-master\upload\mon\` для устройства
Мониторинга непрерывного контроля высоковольтных вводов
</details>

Запустите приложение по инструкциям из [Запуска](#-запуск)

&nbsp;

# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Структура
## &nbsp;&nbsp; Инициализатор устройств ([devices.py](devices.py))

### Замеры
ElectroMon получает данные от фактических физических устройств, снимающих показания.

&nbsp;&nbsp; Список доступных устройств и их короткие коды, используемые в программе:
- ``nkvv`` - **Устройство непрерывного контроля и защиты высоковольтных вводов**
- ``kiv`` - **Устройство контроля изоляции вводов**
- ``monitoring`` - **Мониторинг устройств непрерывного контроля и защиты высоковольтных вводов**

### Свойства 
Файл
[Devices](devices.py) 
хранит и возвращает атрибуты для последующей обработки.
Модуль содержит методы установки свойств и статусов устройства, таких как:

- имя устройства
- папка и файлы по умолчанию для загрузки данных
- тип источника данных, используемые разделители
- столбцы, используемые для установки значений измерений и их карты декодирования
- прописанные типичные ошибки измерений устройств
- значения предупредительных и аварийных сигналов для определённых типов измерений
- и т.д.

Рекомендуется использовать переменную `dev` или `device_type` для присваивания кода устройства (например, `'mon'` или `'kiv'`)

<details><summary>Пример инициализатора</summary>

    self.name = 'nkvv'
    self.full_name = 'Устройство непрерывного контроля и защиты высоковольтных вводов'
    self.monitoring_params = {'input': 220000, 'output': 110000}
    self.log_types = {'measure': 'csv', 'event': 'csv'}
    self.file_folder = 'upload/' + name + '/'
    self.file_name_starts = {'measure': 'DB_i'}
    self.file_sep = ';'
    self.file_default_encoding = 'WINDOWS-1251'
    self.file_parse_dates = ['Дата создания записи', 'Дата сохранения в БД']
    self.default_dict_for_replacement_to_nan = {'power': [-300.0, 0.0],
                                                'tg': -10.0,
                                                '∆tg': -10.0,
                                                'c_delta': -10.0,
                                                'c_deviation': 0.0,
                                                'voltage_difference': 0.0}
    self.warning_map = {'∆tg': [1.0, 1.5], '∆C': [3.0, 5.0]}
</details>

### Источники
Исходные данные располагаются в папке `upload/` и должны соответствовать требованиям, описанным в файле 
[devices.py](devices.py) в классе `Device`, 
включая инициализирующие свойства, такие как `self.file_name_starts` или `self.file_name_ends` объектов-устройств. 
При добавлении нового типа файлов/шаблонов эти свойства следует обновлять.

<details><summary>Пример выгруженных с устройств файлов</summary>

    'upload/kiv/MeasJ a284 #572665920 30-12-2022.xlsx' 
    'upload/mon/22_06/21217004.I' 
    'upload/mon/22_07/21217004.I' 
    'upload/mon/22_08/21217004.I' 
    'upload/mon/22_09/21217004.I' 
    'upload/mon/22_10/21217004.I' 
    'upload/mon/22_11/21217004.I' 
    'upload/mon/22_12/21217004.I' 
    'upload/mon/23_01/21217004.I' 
    'upload/nkvv/DB_i.csv;  
</details>

### Ссылки
Функция `links()` содержит основные свойства устройств, возвращаемые в виде списка. 
Метод можно расширить новыми свойствами, но порядок списка не должен изменяться, так как его индексы используются в аналитических функциях.

<details><summary>Текущий список ссылок для получения данных по устройству через функцию</summary>

            self.name,  # 0
            self.file,  # 1
            self.file_sep,  # 2
            self.file_default_encoding,  # 3
            self.file_parse_dates,  # 4
            self.file_list,  # 5
            self.default_dict_for_replacement_to_nan,  # 6
            self.file_parse_dates_basis,  # 7
            self.default_dict_for_dtypes,  # 8
            self.full_name,  # 9
            self.warning_map  # 10
</details>

### Быстрое сохранение и загрузка
Сохраненный кэш данных для устройства может быть сохранен в формате `.pkl` в директории `save/` для дальнейшей быстрой загрузки.

Используйте класс `Pkl` и методы `save()` или `load()` в [devices](devices.py)

<details><summary>Пример быстрого сохранения и загрузки данных </summary>
Сохранение оперируемых данных устройства контроля и изоляции вводов:

    data = devices.Pkl.save(device_type='kiv', data=data)

Загрузка этих данных:

    data = devices.Pkl.load(device_type='kiv')
</details>

## &nbsp;&nbsp; Обработка столбцов ([columns.py](columns.py)) 

### Анализатор столбцов
Функция
`columns_analyzer()`
обрабатывает столбцы данных на основании атрибутов устройства в 
[devices](devices.py)
и создаёт словарь с ключами-индексами и значением-списком со следующими данными:

1. Оригинальное название столбца
2. Параметр замера
3. Код датчика и фазы
4. Параметры напряжения 
5. Краткое имя для обработки
6. Полное имя для обработки
7. Соединение краткого имени и параметра напряжения

[Columns](columns.py) - это модуль, который придаёт столбцам выгруженных с устройств данных как можно большее количество 
свойств для стандартизации, поиска и повышения эффективности в реализации аналитических функций.

Кроме того, 
`columns_analyzer()`
в некоторых случаях создаёт дополнительные колонки, например, для устройства с кодом `'mon'` создаётся колонка, объединяющая разделённые колонки даты и времени замера.

<details><summary>Пример словаря после обработки</summary>

    0: ['Дата создания записи', 'datetime', 'overall', 'no_voltage', 'time', 'time_of_measure', 'time_no_voltage'],
    1: ['Дата сохранения в БД', 'datetime', 'overall', 'no_voltage', 'save', 'time_of_saving', 'save_no_voltage'],
    2: ['U_A1,кВ', 'voltage', 'A1', 'HV', 'U', 'voltage_difference', 'U_HV'],
    3: ['Ia_A1,мА', 'power', 'A1', 'HV', 'Ia', 'power_active', 'Ia_HV'],
    4: ['Ir_A1,мА', 'power', 'A1', 'HV', 'Ir', 'power_reactive', 'Ir_HV'],
    5: ['Tg_A1,%', 'percentage', 'A1', 'HV', 'tg', 'tangent', 'tg_HV'],
    6: ['C_A1,пФ', 'other', 'A1', 'HV', 'C', 'c_deviation', 'C_HV'],
    7: ['DeltaTg_A1,%', 'percentage', 'A1', 'HV', '∆tg', 'tangent_delta', '∆tg_HV'],
    8: ['DeltaC_A1,%', 'percentage', 'A1', 'HV', '∆C', 'c_delta', '∆C_HV'],
    9: ['U_B1,кВ', 'voltage', 'B1', 'HV', 'U', 'voltage_difference', 'U_HV'],
    10: ['Ia_B1,мА', 'power', 'B1', 'HV', 'Ia', 'power_active', 'Ia_HV'],
    11: ['Ir_B1,мА', 'power', 'B1', 'HV', 'Ir', 'power_reactive', 'Ir_HV'],
    12: ['Tg_B1,%', 'percentage', 'B1', 'HV', 'tg', 'tangent', 'tg_HV'],
    13: ['C_B1,пФ', 'other', 'B1', 'HV', 'C', 'c_deviation', 'C_HV'],
    14: ['DeltaTg_B1,%', 'percentage', 'B1', 'HV', '∆tg', 'tangent_delta', '∆tg_HV'],
    15: ['DeltaC_B1,%', 'percentage', 'B1', 'HV', '∆C', 'c_delta', '∆C_HV'],
    16: ['U_C1,кВ', 'voltage', 'C1', 'HV', 'U', 'voltage_difference', 'U_HV'],
    17: ['Ia_C1,мА', 'power', 'C1', 'HV', 'Ia', 'power_active', 'Ia_HV'],
    18: ['Ir_C1,мА', 'power', 'C1', 'HV', 'Ir', 'power_reactive', 'Ir_HV'],
    19: ['Tg_C1,%', 'percentage', 'C1', 'HV', 'tg', 'tangent', 'tg_HV'],
    20: ['C_C1,пФ', 'other', 'C1', 'HV', 'C', 'c_deviation', 'C_HV'],
    21: ['DeltaTg_C1,%', 'percentage', 'C1', 'HV', '∆tg', 'tangent_delta', '∆tg_HV'],
    22: ['DeltaC_C1,%', 'percentage', 'C1', 'HV', '∆C', 'c_delta', '∆C_HV'],
    23: ['U_A2,кВ', 'voltage', 'A2', 'MV', 'U', 'voltage_difference', 'U_MV'],
    24: ['Ia_A2,мА', 'power', 'A2', 'MV', 'Ia', 'power_active', 'Ia_MV'],
    25: ['Ir_A2,мА', 'power', 'A2', 'MV', 'Ir', 'power_reactive', 'Ir_MV'],
    26: ['Tg_A2,%', 'percentage', 'A2', 'MV', 'tg', 'tangent', 'tg_MV'],
    27: ['C_A2,пФ', 'other', 'A2', 'MV', 'C', 'c_deviation', 'C_MV'],
    28: ['DeltaTg_A2,%', 'percentage', 'A2', 'MV', '∆tg', 'tangent_delta', '∆tg_MV'],
    29: ['DeltaC_A2,%', 'percentage', 'A2', 'MV', '∆C', 'c_delta', '∆C_MV'],
    30: ['U_B2,кВ', 'voltage', 'B2', 'MV', 'U', 'voltage_difference', 'U_MV'],
    31: ['Ia_B2,мА', 'power', 'B2', 'MV', 'Ia', 'power_active', 'Ia_MV'],
    32: ['Ir_B2,мА', 'power', 'B2', 'MV', 'Ir', 'power_reactive', 'Ir_MV'],
    33: ['Tg_B2,%', 'percentage', 'B2', 'MV', 'tg', 'tangent', 'tg_MV'],
    34: ['C_B2,пФ', 'other', 'B2', 'MV', 'C', 'c_deviation', 'C_MV'],
    35: ['DeltaTg_B2,%', 'percentage', 'B2', 'MV', '∆tg', 'tangent_delta', '∆tg_MV'],
    36: ['DeltaC_B2,%', 'percentage', 'B2', 'MV', '∆C', 'c_delta', '∆C_MV'],
    37: ['U_C2,кВ', 'voltage', 'C2', 'MV', 'U', 'voltage_difference', 'U_MV'],
    38: ['Ia_C2,мА', 'power', 'C2', 'MV', 'Ia', 'power_active', 'Ia_MV'],
    39: ['Ir_C2,мА', 'power', 'C2', 'MV', 'Ir', 'power_reactive', 'Ir_MV'],
    40: ['Tg_C2,%', 'percentage', 'C2', 'MV', 'tg', 'tangent', 'tg_MV'],
    41: ['C_C2,пФ', 'other', 'C2', 'MV', 'C', 'c_deviation', 'C_MV'],
    42: ['DeltaTg_C2,%', 'percentage', 'C2', 'MV', '∆tg', 'tangent_delta', '∆tg_MV'],
    43: ['DeltaC_C2,%', 'percentage', 'C2', 'MV', '∆C', 'c_delta', '∆C_MV'],
    44: ['Tair,°С', 'temperature', 'overall', 'no_voltage', 'tair', 'temperature_of_air', 'tair_no_voltage'],
    45: ['Tdevice,°С', 'temperature', 'overall', 'no_voltage', 'tdev', 'temperature_of_device', 'tdev_no_voltage'],
    46: ['Tcpu,°С', 'temperature', 'overall', 'no_voltage', 'tcpu', 'temperature_of_cpu', 'tcpu_no_voltage'],
    47: ['Freq,Гц', 'frequency', 'overall', 'no_voltage', 'freq', 'frequency', 'freq_no_voltage'],
    48: ['Unnamed: 48', 'other', 'overall', 'no_voltage', 'no_name', 'no_name', 'no_name_no_voltage']
</details>

### Столбец времени
`time_column()` 
возвращает имя столбца с датой и временем замера в соответствии с атрибутом `self.file_parse_dates` устройства 
`device`
В данном атрибуте содержится список со столбцами, в которых приведены данные даты и времени, основной столбец с объединённой датой и временем замера - первый в списке.

## &nbsp;&nbsp; Анализаторы ([analyzer.py](analyzer.py))

### Импорт данных
Импорт данных производится с помощью функции `get_data()` из рабочих файлов (описаны в [Источники](#источники)). 
В случае, если нужно импортировать несколько файлов и создать непрерывную базу для анализа данных, следует воспользоваться функцией `stack_data()`.
Сбор данных из разных файлов автоматически сортирует их по времени замера и обновляет индексы таблицы.
Рекомендуется использовать переменную `data` для хранения данных и последующей обработки

### Замена данных
Ввиду технических особенностей устройств, в некоторых случаях значение замера означает ошибку в замере (например, значение -300 для силы тока).
Функция `pass_the_nan()` преобразует данные значения в пустые значения в таблице, то есть, реальные значения параметра неизвестны. 

<details><summary>Пример значений по параметрам для замены </summary>

    {
        'power': [-300.0, 0.0],
        'tg': [-10.0],
        '∆tg': [-10.0],
        'c_delta': [-10.0],
        'c_deviation': [0.0],
        'voltage_difference': [0.0]
    }
</details>

`set_dtypes` устанавливает формат значений для определённых столбцов таблицы

Словари данных типов хранятся в объектах класса 
`Device` в файле 
[devices.py](devices.py) 
в следующих атрибутах:
- для замены на пустые значения в `self.default_dict_for_replacement_to_nan` 
- для установления формата значений в `self.default_dict_for_dtypes` 

Результат обработки рекомендуется сохранять в переменную `data`, передавая в функцию так же переменную `data`
    {
        data = analyzer.pass_the_nan(device_type=device_type, data=data, cols=cols)
        data = analyzer.set_dtypes(device_type=device_type, data=data, cols=cols)
    }

### Счётчик
`total_counter()` подсчитывает количество замеров. 

`total_periods()` выдаёт список с датой/временем начала и датой/временем окончания произведения замеров.
Изменить формат вывода даты/времени можно аргумент `format=` по стандартной маске библиотеки `datetime`.

### Анализатор времени
`values_time_analyzer()` проводит анализ на предмет наличия неточностей в интервалах произведения замеров.
По умолчанию, корректных интервалом замера является 1 минута, в качестве допустимой погрешности каждого последующего замера по умолчанию установлен интервал в 3 секунды.
Интервалы можно корректировать с помощью аргумента `time_sequence_min=`, погрешность - с помощью аргумента `inaccuracy_sec=`
Возвращает базу данных со списком найденных ошибок в интервалах замеров.

На основании базы данных со списком найденных ошибок в интервалах замеров `values_time_slicer()` позволяет выявить отрезки с исключительными разрывами интервалов.
Например, в базе данных устройства могут быть данные по кардинально разным периодам, тестовые данные с малым количеством замеров или некорректной датой. 
Функция создаёт словарь со списком срезов, значениями словаря являются отдельные базы данных. 
Для формирования среза необходимо выполнение условия по минимальному количеству замеров, устанавливаемое аргументом `min_values_required=` (по умолчанию 150), и условия по количеству минут в разрыве между данными, устанавливаемому аргументом `minutes_slice_mode=` (по умолчанию 1440, то есть, 1 сутки).

### Выбор периода
`time_period_choose()` позволяет пользователю через ввод установить определённый период для анализа в рамках имеющихся данных.
Функция автоматически сортирует данные их по времени замера и обновляет индексы таблицы.

### Периоды пустых значений
`total_nan_counter()` анализирует процент пустых значений в каждой строке входных данных и возвращает таблицу, которая показывает периоды времени, 
когда процент значений пустых значений по строке превышает заданный порог.
Порог устанавливается аргументом `false_data_percentage=`. По умолчанию 33.0, то есть измерения в момент замера слишком неточные, если более 1/3 измерений в эту минуту являются ошибками. Карту типичных погрешностей измерений приборов можно найти в 
[devices.py](devices.py) 
в атрибуте `self.default_dict_for_replacement_to_nan` устройства - объекта в классе `Device`.
Подробнее об атрибутах см. [Свойства](#свойства)

Если неточных замеров слишком много, рекомендуется использовать 
`total_nan_counter_ease()` 
для объединения непрерывных периодов неточных замеров с большим количеством пустых значений в данных.

### Фильтрация
`data_filter()` возвращает новую таблицу, содержащую только те столбцы, которые соответствуют списку фильтров.
Для фильтрации данных можно использовать как имена столбцов, так и прочие данные (в т.ч. коды мер или краткие названия и т.д.), которые обрабатываются в 
[columns.py](columns.py).
Подробнее о кодах столбцов см. [Анализатор столбцов](#анализатор-столбцов)

### Средние значения
`data_average_finder()`  фильтрует и вычисляет среднее значение указанного списка столбцов в заданном наборе данных.
Функция возвращает словарь с именами столбцов в качестве ключей и соответствующим им средним значением в качестве значений.

### Распределение значений
`data_distribution_finder()` анализирует распределение значений в указанных столбцах данных, полезно для построения гистограмм.

### Корреляции
`data_correlation()` вычисляет корреляцию между изменениями значений в двух отфильтрованных столбцах данных.
Возвращает словарь с параметрами корреляции в качестве ключей и соответствующей последовательностью значений корреляции.
Если вы построите график этих данных, то, например, для 100% прямой корреляции, будет выведен график формата "x = y" с углом наклона 45° (или -45°, если корреляция обратная).
Чем более близок такому графику получившийся, тем более явная корреляция между изменениями значений.

### Сигнализаторы
`warning_finder()` - это базовая функция для анализа предупреждений.
Она определяет временные интервалы, когда определенные параметры превышают пороговые значения предупреждения или аварии, заданные аргументами `warning_param_war=` и `warning_param_acc=`.
Пороговые значения предупредительной и аварийной сигнализации по умолчанию, установлены в
[devices.py](devices.py)
для каждого устройства в свойстве `self.warning_map`.
Подробнее об атрибутах см. [Свойства](#свойства)

Следующим шагом для анализа является использование
`warning_finder_merge()`
для объединения таблиц данных во входном словаре
`log`
и добавления столбцов для параметров предупреждения и сигнализации на основе заданного аргумента
`warn_type=`
и заданных пороговых значений предупредительной и аварийной сигнализации.
Данная функция возвращает таблицу.

Если предупреждений слишком много, то 
`warning_finder_ease()`
может использоваться для накопления и объединения непрерывных периодов предупреждений в базе данных.
Функция использует данные результатов `warning_finder()` и несколько аргументов для фильтрации и обработки данных с целью выявления предупреждающих или аварийных событий.

## &nbsp;&nbsp; Другие модули

[prints.py](prints.py) содержит скрипты для печати сообщений пользователю и запуска функций из других модулей.
Он обрамляет выполнение функций описаниями и текстовой информацией.

[plots.py](plots.py) отрисовывает графики, гистограммы, корреляционные диаграммы и графики рассеивания на основе заданных аналитических данных.

[frontend.py](frontend.py) состоит из скриптов, устанавливающих шрифты, стили, поля, нумерацию страниц, шаблоны, захват выходных данных, текста, графиков и таблиц.

[sadzax.py](sadzax.py) содержит технические скрипты для обработки входных данных, опроса пользователя, преобразования дат и строк, проверки правильности форматов, склонения по падежам в русском языке и так далее.

&nbsp;

# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Запуск

## &nbsp;&nbsp; Через интерпретатор Python
[run.py](run.py) может быть запущен с помощью интерпретатора Python в командной строке

<details><summary>Пример</summary>

`python c:\users\user\downloads\ElectroMon-master\\run.py`
</details>

Для получения полной информации, включая графики, предпочтительнее использовать [Jupyter Notebook](https://jupyter.org/).
Инструкция по его установке [тут](https://jupyter.org/install).

## &nbsp;&nbsp; Сформировать PDF
[output.py](output.py) выполняет то же самое, что описано в [Запуске через интерпретатор](#-через-интерпретатор-python), 
но в конце обработки данных запрашивает у вас имя файла, 
который будет сохранён в корневом каталоге проекта в виде документа с расширением `.pdf`.