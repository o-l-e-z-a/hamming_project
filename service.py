import time
import math
import os.path
import json
import yaml
import zipfile


def get_parser_values(data, *args, **kwargs) -> list:
    """ Парсер словареобразных структур """
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


def yaml_parser(name: str, *args, **kwargs) -> list:
    """ Парсер yaml-файла """
    with open(name, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return get_parser_values(data, *args, **kwargs)


def txt_parser(name: str, *args, **kwargs) -> list:
    """ Парсер текстового файла """
    result = []
    with open(name) as file:
        for row in file:
            row = row.replace('\n', '')
            if any(a in row for a in args) or any(k in row for k in kwargs):
                result.append(int(row.split(':')[1]))
    return result


def json_parser(name: str, *args, **kwargs):
    """ Парсер json-файла """
    with open(name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return get_parser_values(data, *args, **kwargs)


CONFIG_PARSER = {
    'yaml': yaml_parser,
    'txt': txt_parser,
    'json': json_parser
}


def config_parser(name: str, *args, **kwargs) -> list:
    """ Парсер конфиг-файла """
    try:
        result = CONFIG_PARSER[name.split('.')[1]](name, *args, **kwargs)
    except FileNotFoundError:
        result = []
    except KeyError:
        result = []
    except IndexError:
        result = []
    return result


def get_power_of_two(n: int) -> list:
    """ Получить индексы степеней 2"""
    return [pow(2, i) - 1 for i in range(int(math.log(n, 2)) + 1)]


def unpacked_zip(files: str, archive_dir) -> None:
    """ Распаковка архива в директорию"""
    with zipfile.ZipFile(files) as zip_file:
        zip_file.extractall(archive_dir)


def get_all_files_name_from_dir(files: str, ) -> list:
    """ Поиск всех файлов в дириктории"""
    files_names = []
    for p, d, f in os.walk(files):
        for file in f:
            files_names.append(os.path.join(p, file))
    return files_names


def file_distribution(files: str, archive_dir: str = '.') -> list:
    """ Поиск всех файлов """
    files_names = []
    if os.path.isfile(files):
        if zipfile.is_zipfile(files):
            unpacked_zip(files, os.path.dirname(files))
            zip_file_path = os.path.join(archive_dir, files.split('.')[0])
            files_names += get_all_files_name_from_dir(zip_file_path)
            os.remove(files)
        else:
            files_names.append(files)
    elif os.path.isdir(files):
        files_names += get_all_files_name_from_dir(files)
    else:
        print('Неверное имя файла')
        exit()
    return files_names


def make_file_dir(file, writed_dir, change_dirs=True):
    """ создание директорий для декодируемых файлов"""
    if change_dirs:
        dirs = os.path.dirname(file)
        dirs = dirs.replace('/encode', '/decode')
        try:
            os.mkdir(dirs)
        except FileExistsError:
            pass
    else:
        dirs = f'{writed_dir}' + '\\' + os.path.dirname(file)
    path = ''
    for dir in dirs.split('\\'):
        path = os.path.join(path, dir)
        if not os.path.exists(f'{path}'):
            try:
                os.mkdir(f'{path}')
            except FileExistsError:
                continue


def time_track(func):
    """ таймер работы программы"""
    def surrogate(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        ended_at = time.time()
        elapsed = round((ended_at - started_at) / 60, 4)
        print(f'Функция работала {elapsed} минуты(ы)')
        return result
    return surrogate
