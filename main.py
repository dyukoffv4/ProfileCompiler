import re
import os
import io
import json


# simple definitions

def load(filename, buffered=False):
    with open(filename, 'r') as file:
        return io.StringIO(file.read()) if buffered else file.read()


def save(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

# security definitions

def config_validate(config: dict[str, list[dict]]):
    try:
        if type(config) != dict:
            print('Data must be a dictionary')
            return False
        for (k, v) in config.items():
            if type(k) != str:
                print('Data key must be a string')
                return False
            if type(v) != list:
                print('Data value must be a list')
                return False
            for i in v:
                if type(i) != dict:
                    print('Data list value must be a dictionary')
                    return False
                if not all(item in i.keys() for item in ['endpoint', 'type', 'scripts']):
                    print('Data list value must contains:\n\tendpoint: str\n\ttype: str\n\tscripts: list[str]')
                    return False
                if type(i['type']) != str or len(i['type'].strip()) == 0:
                    print('Data type must be a string')
                    return False
                if type(i['endpoint']) != str or len(i['endpoint'].strip()) == 0:
                    print('Data endpoint must be a string')
                    return False
                if type(i['scripts']) != list:
                    print('Data scripts must be a list')
                    return False
                if len(i['scripts']) != 0 and not all(type(script) == str for script in i['scripts']):
                    print('Data scripts value must be a string')
                    return False
        return True
    except json.decoder.JSONDecodeError as error:
        print(error)
        return False

# prettify definitions

def endpoint_prettify(endpoint):
    result: list[list[int]] = []
    depth = 0
    start: int | None = None

    for index, char in enumerate(endpoint):
        if char == "{":
            if depth == 0:
                start = index
            depth += 1

        elif char == "}":
            if depth == 0:
                raise RuntimeError(f'Invalid endpoint: {endpoint}')
            depth -= 1
            if depth == 0 and start is not None:
                result.append([start, index + 1])
                start = None
    if depth != 0:
        raise RuntimeError(f'Invalid endpoint: {endpoint}')

    offset = 0
    for i in result:
        endpoint = endpoint[0:i[0] - offset] + '{}' + endpoint[i[1] - offset:]
        offset += i[1] - i[0] - 2

    return endpoint


def config_prettify(config: dict[str, list[dict]]) -> dict[str, dict[str, list]]:

    # Убрать пробелы из ключей
    old_new = {}
    for (service, items) in config.items():
        if (service_s := service.strip()) != service:
            old_new[service] = service_s
    for service in old_new:
        if config.get(old_new[service]) is not None:
            config[old_new[service]].extend(config.pop(service))
        else:
            config[old_new[service]] = config.pop(service)

    # Заменить плейсхолдеры и убрать пробелы
    for items in config.values():
        for item in items:
            if (type_s := item['type'].strip()) != item['type']:
                item['type'] = type_s
            if (endpoint_s := item['endpoint'].strip()) != item['endpoint']:
                item['endpoint'] = endpoint_s
            if re.search(r'\{[^}]+}', item['endpoint']) is not None:
                item['endpoint'] = endpoint_prettify(item['endpoint'])
            for s, script in enumerate(item['scripts']):
                if (script_s := script.strip()) != script:
                    item['scripts'][s] = script_s
            for k in list(item.keys()):
                if k not in ['scripts', 'type', 'endpoint']:
                    item.pop(k)

    # Объединяем повторные ендпоинты и методы
    new_config: dict[str, dict[str, list]] = {}
    for service in config:
        entries = {}
        for item in config[service]:
            if entries.get(entry := f'{item["type"]} {item["endpoint"]}') is None:
                entries[entry] = []
            entries[entry].extend(item['scripts'])
        new_config[service] = entries
        for entry in new_config[service]:
            new_config[service][entry] = list(set(new_config[service][entry]))

    return new_config

# main

if __name__ == '__main__':
    my_data = json.loads(load(os.path.join(os.path.dirname(__file__), 'configs', 'config.json')))
    if config_validate(my_data):
        my_data = config_prettify(my_data)
        save(os.path.join(os.path.dirname(__file__), 'configs', 'new_config.json'), json.dumps(my_data, indent=4))
