import matplotlib.pyplot as plt
import pandas as pd
import analyzer
import columns


#  Simple graph
def flat_graph(input_x: list = None,
               input_y: list = None,
               device_type='nkvv',
               data: pd.core = None,
               cols: dict = None,
               title='',
               size_x: int = 14,
               size_y: int = 6):
    if data is None:
        data = analyzer.get_data(device_type=device_type)
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
    if input_x is None:
        input_x = [columns.time_column(device_type=device_type, data=data)]
    if input_y is None:
        input_y = ['∆tg_HV', '∆tg_MV']
    fig, axs = plt.subplots(figsize=(size_x, size_y))
    axs.grid(axis='both', color='gray', linestyle='--')
    plt.title(title)
    df_x = analyzer.data_filter(input_x, cols=cols, data=data)
    plt.xlabel(str(df_x.columns[0]))
    df_y = analyzer.data_filter(input_y, cols=cols, data=data)
    plt.ylabel(', '.join(input_y))
    legend = []
    for y_name in [col for col in df_y.columns]:
        x = df_x[df_x.columns[0]].tolist()
        y = df_y[y_name].tolist()
        legend.append(y_name)
        axs.plot(x, y)
    plt.legend(legend)


#  Histogram for raw data and distribution data
def histogram(value,
              bins=333,
              device_type='nkvv',
              title='',
              data_distribution_parameter=False,
              cols=None,
              data: pd.core = None,
              unite_parameter=False):
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
    if data is None:
        data = analyzer.get_data(device_type=device_type)
    legend = []
    if isinstance(value, str) is True:
        data[value].hist(bins=bins)
        plt.title(title)
    if isinstance(value, list) is True:
        if data_distribution_parameter is True:
            data_distribution = analyzer.data_distribution_finder(value, data=data, cols=cols,
                                                                  unite_parameter=unite_parameter)
            for i in data_distribution:
                legend.append(i)
                data_distribution[i].hist(bins=bins)
        else:
            df = analyzer.data_filter(value, data=data, cols=cols)
            for i in df:
                legend.append(i)
                df[i].hist(bins=bins)
        plt.legend(legend)
        plt.title(title)
        plt.xlabel(', '.join(value))
        plt.ylabel('Количество значений')


#  Correlation Plot
def correlation_plot(filter_list1=None,
                     filter_list2=None,
                     device_type='nkvv',
                     title='',
                     cols=None,
                     data: pd.core = None):
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
    if data is None:
        data = analyzer.get_data(device_type=device_type)
    if filter_list1 is None:
        filter_list1 = ['∆tg_HV']
    if filter_list2 is None:
        filter_list2 = ['∆tg_MV']
    cr = analyzer.data_correlation(filter_list1=filter_list1,
                                   filter_list2=filter_list2,
                                   cols=cols,
                                   data=data)
    keys_list = [key for key in cr.keys()]
    fig, axs = plt.subplots()
    axs.grid(axis='both', color='gray', linestyle='--')
    max_len = 0
    plt.title(title)
    legend = []
    for i in range(len(cr.keys())):
        if len(cr[keys_list[i]]) > max_len:
            max_len = len(cr[keys_list[i]])
            axs.set_ylim(max_len * -1, max_len)
            axs.set_xlim(0, max_len)
            legend.append(keys_list[i])
        plt.xlabel('Шаги')
        plt.ylabel('Совпадения')
        y = cr[keys_list[i]]
        legend.append(keys_list[i])
        axs.plot([i for i in range(max_len)], y)
    plt.legend(legend)


#  Warning plots
def scatter(input_x: list = None,
            input_y: list = None,
            device_type='mon',
            df: pd.core = None,
            cols_inside: dict = None,
            title: str = '',
            size_x: int = 14,
            size_y: int = 6,
            color=None,
            area=None):
    """
    Designed to get dataframes from analyzer.warning_finder_merge function
    """
    #  If there are only datetime and '+' and '-' warnings - don't scatter it
    if df.shape[1] < 4:
        pass
    else:
        if df is None:
            df = analyzer.get_data(device_type=device_type)
        if cols_inside is None:
            cols_inside = columns.columns_analyzer(device_type=device_type, list_for_columns=list(df.columns))
        if input_x is None:
            input_x = [columns.time_column(device_type=device_type, data=df)]
        if input_y is None:
            input_y = []
            for a_column in list(df.columns):
                if a_column in input_x:
                    pass
                else:
                    input_y.append(a_column)
        fig, axs = plt.subplots(figsize=(size_x, size_y))
        axs.grid(axis='both', color='gray', linestyle='--')
        plt.title(title)
        df_x = analyzer.data_filter(input_x, cols=cols_inside, data=df)
        plt.xlabel(str(df_x.columns[0]))
        df_y = analyzer.data_filter(input_y, cols=cols_inside, data=df)
        plt.ylabel('Значения по (' + ', '.join(input_y) + ')')
        legend = []
        for y_name in [col for col in df_y.columns]:
            x = df_x[df_x.columns[0]].tolist()
            y = df_y[y_name].tolist()
            if y_name.find('отриц.') != -1 or y_name.find('полож.') != -1:
                axs.scatter(x, y, c='k', marker='.', s=2)
            else:
                axs.scatter(x, y, c=color, s=area)
                legend.append(y_name)
        plt.legend(legend)
