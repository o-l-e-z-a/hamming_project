import math
import yaml
import json


def get_parser_values(data, *args, **kwargs):
    result = []
    for a in args:
        var = data.get(a, None)
        if var:
            result.append(var)
    for k in kwargs:
        var = data.get(k, None)
        if var:
            result.append(var)
    return result


def yaml_parser(name, *args, **kwargs):
    with open(name, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return get_parser_values(data, *args, **kwargs)


def txt_parser(name, *args, **kwargs):
    result = []
    with open(name) as file:
        for row in file:
            row = row.replace('\n', '')
            if any(a in row for a in args) or any(k in row for k in kwargs):
                result.append(int(row.split(':')[1]))
    return result


def json_parser(name, *args, **kwargs):
    with open(name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return get_parser_values(data, *args, **kwargs)


CONFIG_PARSER = {
    'yaml': yaml_parser,
    'txt': txt_parser,
    'json': json_parser
}


def config_parser(name, *args, **kwargs) -> list:
    """ Парсер конфиг-файла """
    try:
        result = CONFIG_PARSER[name.split('.')[1]](name, *args, **kwargs)
    except FileNotFoundError:
        result = []
    except KeyError:
        result = []
    return result


def get_power_of_two(n: int) -> list:
    return [pow(2, i) - 1 for i in range(int(math.log(n, 2)) + 1)]
