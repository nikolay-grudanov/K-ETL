import json
import pandas as pd
from datetime import datetime

# TODO Добавить выбор файла
with open("input/example.json", "r") as read_file:
    jsonStructure = json.load(read_file)


def mapper_type(value):
    if type(value) is str:
        return "Строка"
    if type(value) is int:
        return "Целое число"
    if type(value) is list:
        return "Массив"
    if type(value) is dict:
        return "Объект"
    if type(value) is bool:
        return "Логический тип"
    if type(value) is float:
        return "Число с плавающей запятой"


def mapper(json_value, data, parent=""):
    for key in json_value:
        if type(json_value[key]) is dict:
            data.append([f"{parent + key}", key, mapper_type(json_value[key]), "", "Составной объект, имеет вложения"])
            mapper(json_value[key], data, parent=parent + key + ".")
        elif type(json_value[key]) is list:
            data.append([f"{parent + key}", key, mapper_type(json_value[key]), "", "Массив"])
            try:
                mapper(json_value[key][0], data, parent=parent + key + "[*].")
            except:
                # TODO Стрёмная реализация, подумать как сделать лучше
                if len(json_value[key]) > 0:
                    data.append([f"{parent + key}[*]", "-", mapper_type(json_value[key][0]), json_value[key][0],
                                 "Элемент массива"])
                else:
                    data.append([f"{parent + key}[*]", "-", "-", "-", "Пустой массив"])
        else:
            data.append([f"{parent + key}", key, mapper_type(json_value[key]), json_value[key], ""])

    return data


data_list = []
data_for_df = mapper(jsonStructure, data_list)

df = pd.DataFrame(data_for_df,
                  columns=['Путь к переменной', 'Наименование переменной', 'Тип', 'Пример заполнения', 'Комментарий'])
timeSave = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
# TODO Добавить выбор директории для сохранения
# TODO Добавить выбор формата сохранения
df.to_excel(f'./output/output_{timeSave}.xlsx')

print('fin')
