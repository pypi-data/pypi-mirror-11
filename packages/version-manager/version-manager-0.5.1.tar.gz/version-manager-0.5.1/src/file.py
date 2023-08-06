import os
import re
from repoze.lru import CacheMaker
from src.config import load_config
from src.parser.parser import PARSER_REGISTRY
from colorama import Fore, Back, Style

cache_maker = CacheMaker()

__author__ = 'ahmetdal'

version_pattern = re.compile(r'((\d)+.?)+')


class File:
    def __init__(self, name, path, parser, color=Fore.WHITE):
        self.name = name
        self.path = path
        self.parser = parser
        self.color = color
        if not self.parser:
            raise Exception("Parser must be given.")

    @property
    @cache_maker.lrucache(maxsize=300, name="content")
    def content(self):
        with open(self.path, 'r') as f:
            return f.read()

    @property
    @cache_maker.lrucache(maxsize=300, name="current_version")
    def current_version(self):
        current_version = self.parser.current_version(self.content)
        if not current_version:
            print("%sNo version definition is found in file %s" % (self.color, self.path))
        return current_version

    def update_version(self, new_version):
        print('%sFile %s is now on version %s' % (self.color, self.path, self.current_version))
        new_content = self.parser.update_version(self.content, new_version)
        with open(self.path, 'w') as f:
            f.write(new_content)
        cache_maker.clear("current_version")
        cache_maker.clear("content")
        print('%sFile %s is updated to version %s\n' % (self.color, self.path, self.current_version))

    def next_version(self):
        raise NotImplementedError()

    def previous_version(self):
        raise NotImplementedError()


loaded_files = []


class FileLoader:
    def __init__(self):
        self.config = load_config()
        self.files = self.config.get("files", [])
        self.excludes = self.config.get("excludes", [])

    def load(self):
        for dirpath, dirnames, files in os.walk('./'):
            for exclude in self.excludes:
                try:
                    dirnames.remove(exclude)
                except ValueError:
                    pass

                try:
                    files.remove(exclude)
                except ValueError:
                    pass

            for f in files:
                config_files = filter(lambda x: x.get('name') == f, self.files)
                for config_file in config_files:
                    parser_type = config_file.get('parser', 'regexp')
                    color = config_file.get('color', Fore.WHITE)
                    ParserClass = PARSER_REGISTRY.get(parser_type)
                    if ParserClass:
                        parser = ParserClass(*config_file.get('args', []), **config_file.get('kwargs', {}))
                        loaded_files.append(File(config_file.get('name'), os.path.abspath(os.path.join(dirpath, f)), parser, color=color))
                    else:
                        raise Exception("No registered with parser type %s. Available parsers are %s" % (parser_type, ','.join(PARSER_REGISTRY.keys())))


FileLoader().load()
loaded_files = sorted(loaded_files, key=lambda f: f.name)
