import collections
from statistics import mean, median
from contextlib import redirect_stdout
from requests import Session


def beautiful_list_with_measurements(list_with_row_data: list):
    """

    :param list_with_row_data:
    :return:
    """
    some_dick = collections.defaultdict(dict)
    for i in list_with_row_data:
        name, service, _, percent = i.strip('()').split(',')
        some_dick[name].setdefault(service, []).append(int(percent))
    return dict(some_dick)


def calculating_values(some_dick: dict):
    new_dick = collections.defaultdict(dict)
    for x, y in some_dick.items():
        for z, w in y.items():
            new_dick[x][z] = {'main': mean(w), 'mediana': median(w)}
    return dict(new_dick)


def calculating_usage(some_dick: dict):
    new_dick = collections.defaultdict(dict)
    for x, y in some_dick.items():
        for z, w in y.items():
            new_dick[x][z] = {'main': w['main'],
                              'median': w['mediana'],
                              'intensivity': calculating_intensivity(w['mediana']),
                              'usage_type': calculating_usage_type(w['main'], w['mediana'])}
    return dict(new_dick)


def calculating_intensivity(median: float):
    intensivity = ''
    if median <= 30:
        intensivity = 'low'
    elif 60 >= median > 30:
        intensivity = 'moderate'
    elif 90 >= median > 60:
        intensivity = 'high'
    else:
        intensivity = 'transcendental'
    return intensivity


def calculating_usage_type(mean: float, median: float):
    """R%= N1/N2×100%"""
    usage_type = ''
    proc = mean / median * 100
    if proc < 75:
        usage_type = 'low'
    elif 75 < proc <= 125:
        usage_type = 'stable'
    else:
        usage_type = 'surges'
    return usage_type


def parser(row_data: str):
    """

    :param row_data:
    :return:
    """
    some_dick = {}
    split_by_companies_name = row_data.split('$')
    for i in split_by_companies_name:
        company_name, row_mesurments = i.split('|')
        list_with_row_mesurmemts = row_mesurments.split(';')
        dict_with_values = beautiful_list_with_measurements(list_with_row_mesurmemts)
        dict_with_main_and_mediane = calculating_values(dict_with_values)
        with_usage_statistic = calculating_usage(dict_with_main_and_mediane)
        some_dick[company_name] = with_usage_statistic
    return some_dick


def decision_about_service(usage_type: str, intensivity: str):
    value_to_return = ''
    if intensivity == 'low':
        value_to_return = 'cancel'
    elif intensivity == 'transcendental':
        value_to_return = 'power_up'
    elif intensivity == 'moderate' and usage_type == 'low':
        value_to_return = 'cancel'
    elif intensivity == 'moderate' and usage_type in ['stable', 'surges']:
        value_to_return = 'as at is'
    elif intensivity == 'high' and usage_type in ['stable', 'low']:
        value_to_return = 'as at is'
    elif intensivity == 'high' and usage_type == 'surges':
        value_to_return = 'power up'
    return value_to_return


def print_to_file(data_to_print: dict):
    with open('out.txt', 'w') as f:
        with redirect_stdout(f):
            print('|Resource|Dimension|mean|median|usage_type|intensivity|decision|')
            for i in data_to_print.values():
                for x, y in i.items():
                    for z, w in y.items():
                        print(f'|{x}|{z}|{w["main"]}|{w["median"]}|{w["usage_type"]}|{w["intensivity"]}|'
                              f'{decision_about_service(w["usage_type"], w["intensivity"])}|')


def get_log():
    s = Session()
    base_url = 'http://localhost:21122/'
    endpoint = 'monitoring/infrastructure/using/summary/1'
    r = s.get(base_url + endpoint)
    return r.text


def main():
    input_data = get_log()
    print_to_file(parser(input_data))


if __name__ == '__main__':
    main()

