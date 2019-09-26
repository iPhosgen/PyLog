import inspect
import json
import logging
import os

from .targets import targets


class LoggingException(Exception):
    pass


class Logger:
    """Basic logger class"""

    configuration = {}
    targets = {}
    logger = logging.getLogger('PyLog')

    @classmethod
    def getLogger(cls, name):
        logger = logging.getLogger(name)

        if not cls.configuration:
            cls.__read_config_file()

        if cls.configuration['_is_valid']:
            for rule in [rule for rule in cls.configuration['rules'] if rule['_is_valid']]:
                if name.startswith(rule['name'].split('*')[0]):
                    logger.handlers.clear()

                    for target in rule['write-to']:
                        logger.addHandler(cls.targets[target])

                    logger.setLevel(logging._nameToLevel(rule['min-level'].upper()))

                    return logger

        logger.setLevel(logging.INFO)
        return logger

    # TODO: Add absolute path to project root + config file name
    @classmethod
    def __read_config_file(cls):
        file_path = ''

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                try:
                    cls.configuration = json.load(file)
                    cls.__validate_targets()
                    cls.__prepare_targets()
                    cls.__validate_rules()

                    cls.configuration['_is_valid'] = True
                except Exception:
                    cls.logger.exception('Configuration file syntax error')
                    cls.configuration['_is_valid'] = False
        else:
            cls.logger.error('Configuration file not found')
            cls.configuration['_is_valid'] = False

    # TODO: Add arguments filling
    @classmethod
    def __prepare_targets(cls):
        for target in [target for target in cls.configuration['targets'] if target['_is_valid']]:
            args = list(inspect.signature(targets[target['type']].__init__).parameters)[1:]
            handler = targets[target['type']]()
            cls.targets[target['name']] = handler


    @classmethod
    def __validate_rules(cls):
        for rule in cls.configuration['rules']:
            rule['_is_valid'] = True

            # Validate rule name
            if not rule.get('name', False):
                cls.logger.warning('Invalid rule name. Rule: %s', rule)
                rule['_is_valid'] = False
                continue

            # Validate rule min LEVEL
            if not rule.get('min-level', False) or rule['min-level'] not in logging._nameToLevel.keys():
                cls.logger.warning('Invalid rule min LEVEL. Rule: %s', rule)
                rule['_is_valid'] = False
                continue

            # Validate write to
            if not rule.get('write-tol', False) and not all(elem in rule['write-to'] for elem in cls.targets.keys()):
                cls.logger.warning('Invalid rule write to. Rule: %s', rule)
                rule['_is_valid'] = False
                continue

    @classmethod
    def __validate_targets(cls):
        for target in cls.configuration['targets']:
            target['_is_valid'] = True

            # Validate target name
            if target.get('name', False):
                if target['name'] in cls.targets.keys():
                    cls.logger.warning('Target name must be unique. Target: %s', target)
                    target['_is_valid'] = False
                    continue
            else:
                cls.logger.warning('Invalid target name. Target: %s', target)
                target['_is_valid'] = False
                continue

            # Validate target type
            if not target.get('type', False) or target['type'] not in targets.keys():
                cls.logger.warning('Invalid target type. Target: %s', target)
                target['_is_valid'] = False
                continue

            # Validate arguments
            args = list(inspect.signature(targets[target['type']].__init__).parameters)[1:]

            for arg in args:
                if not target.get(arg, False):
                    cls.logger.warning('Invalid target argument `%s`. Target: %s', arg, target)
                    target['_is_valid'] = False
                    break
