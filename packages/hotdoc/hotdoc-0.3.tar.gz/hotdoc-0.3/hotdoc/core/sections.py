# -*- coding: utf-8 -*-

import os
import json

from pandocfilters import BulletList, Plain, Link, Para, Emph, Str, Space
from datetime import datetime

from .symbols import *
from .gnome_markdown_filter import GnomeMarkdownFilter
from .doc_tool import doc_tool
from ..lexer_parsers.doxygen_block_parser import parse_doxygen_comment
from ..utils.loggable import Loggable, ProgressBar
from .pandoc_interface import translator


class TypedSymbolsList (object):
    def __init__ (self, name):
        self.name = name
        self.symbols = []


class SectionSymbol (Symbol):
    def __init__(self, *args):
        Symbol.__init__ (self, *args)
        self.symbols = []
        self.sections = []

        self.typed_symbols = {}
        self.typed_symbols[FunctionSymbol] = TypedSymbolsList ("Functions")
        self.typed_symbols[CallbackSymbol] = TypedSymbolsList ("Callback Functions")
        self.typed_symbols[FunctionMacroSymbol] = TypedSymbolsList ("Function Macros")
        self.typed_symbols[ConstantSymbol] = TypedSymbolsList ("Constants")
        self.typed_symbols[ExportedVariableSymbol] = TypedSymbolsList ("Exported Variables")
        self.typed_symbols[StructSymbol] = TypedSymbolsList ("Data Structures")
        self.typed_symbols[EnumSymbol] = TypedSymbolsList ("Enumerations")
        self.typed_symbols[AliasSymbol] = TypedSymbolsList ("Aliases")
        self.parsed_contents = None
        self.formatted_contents = None
        if self.comment is not None and self.comment.title is not None:
            self.link.title = self.comment.title

    def _register_typed_symbol (self, symbol_type, symbol_type_name):
        self.typed_symbols[symbol_type] = TypedSymbolsList (symbol_type_name)

    def do_format (self):
        for symbol in self.symbols:
            if symbol.do_format ():
                typed_symbols_list = self.typed_symbols [type (symbol)]
                typed_symbols_list.symbols.append (symbol)
        return Symbol.do_format(self)

    def add_symbol (self, symbol):
        symbol.link.pagename = self.link.pagename
        for l in symbol.get_extra_links():
            l.pagename = self.link.pagename
        self.symbols.append (symbol)

    def get_short_description (self):
        if not self.comment:
            return ""
        if not self.comment.short_description:
            return ""
        return self.comment.short_description

    def get_title (self):
        if not self.comment:
            return ""
        if not self.comment.title:
            return ""
        return self.comment.title


class SectionFilter (GnomeMarkdownFilter, Loggable):
    def __init__(self, directory, doc_formatter, symbol_factory=None):
        GnomeMarkdownFilter.__init__(self, directory)
        Loggable.__init__(self)
        self.sections = []
        self.__current_section = None
        self.__symbols = doc_tool.source_scanner.symbols
        self.__symbol_factory = symbol_factory
        self.__doc_formatter = doc_formatter
        self.__created_section_names = []

    def parse_extensions (self, key, value, format_, meta):
        if key == "BulletList" and not "ignore_bullet_points" in meta['unMeta']:
            res = []
            for val in value:
                content = val[0]['c'][0]
                if content['t'] == "Link":
                    symbol_name = content['c'][0][0]['c']
                    symbol = self.__symbols.get(symbol_name)

                    if symbol:
                        comment_block = doc_tool.comments.get (symbol_name)
                        if comment_block:
                            sym = self.__symbol_factory.make (symbol,
                                    comment_block)
                            if sym:
                                self.__current_section.add_symbol (sym)
                                #self.__current_section.deps.add('"%s"' % comment_block.position.filename)
                                #self.__current_section.deps.add('"%s"' %
                                #        str(symbol.location.file))
                        else:
                            self.warning ("Found a symbol for empty link with"
                                    " name %s but no comment block associated" %
                                    symbol_name)
                    else:
                        self.warning ("Found an empty link with name %s but no"
                        " symbol was found" % symbol_name)

                res.append (val)
            if res:
                return BulletList(res)
            return []

        return GnomeMarkdownFilter.parse_extensions (self, key, value, format_,
                meta)

    def __parse_link (self, value):
        res = None
        old_section = self.__current_section

        path = os.path.join (self.directory, value[1][0])
        if self.parse_file (path, old_section, value[0][0]['c']):
            value[1][0] = os.path.splitext(value[1][0])[0] + ".html"

            # Let's check if we can get a better title
            title = self.__current_section.get_title()
            if title:
                value[0][0]['c'] = title
            res = self.__current_section.get_short_description()

        self.__current_section = old_section
        return res

    def parse_header (self, key, value, format_, meta):
        if value[2][0]['t'] == 'Link':
            res = self.__parse_link (value[2][0]['c'])
            if res:
                description = translator.markdown_to_json (res).decode('utf-8')
                description = json.loads(description)
                value[2].append (Space ())
                value[2].append (Str (u'—'))
                value[2].append (Space())
                for val in description[1][0]['c']:
                    value[2].append (val)

    def parse_file (self, filename, parent=None, section_name=None):
        path = filename
        if not os.path.isfile (path):
            return False

        name = os.path.basename(os.path.splitext(filename)[0])
        if name in self.__created_section_names:
            return True

        comment = None
        if section_name is None:
            section_name = name

        comment = doc_tool.comments.get("SECTION:%s" %
                section_name.lower())

        symbol = self.__symbols.get(name)
        if not symbol:
            self.debug ("Creating section %s with no symbol associated" % name)
            symbol = name
        else:
            self.debug ("Creating section %s with a symbol associated" % name)

        self.__created_section_names.append (name)
        section = self.__symbol_factory.make_section (symbol, comment)
        section.source_file = os.path.abspath(path)

        if self.__current_section:
            self.__current_section.sections.append (section)
        else:
            self.sections.append (section)

        self.__current_section = section
        pagename = "%s.%s" % (name, "html")
        self.__current_section.link.pagename = pagename

        with open (path, 'r') as f:
            contents = f.read()
            res = self.filter_text (contents)
            if not self.__current_section.symbols:
                self.__current_section.parsed_contents = res

        #self.dag.add ('"%s"' % os.path.basename(filename), list(self.__current_section.deps))
        return True

    def __update_dependencies (self, sections):
        for s in sections:
            if not s.symbols:
                doc_tool.dependency_tree.add_dependency (s.source_file,
                        None)
            for sym in s.symbols:
                if not hasattr (sym._symbol, "location"):
                    continue

                filename = str (sym._symbol.location.file)
                doc_tool.dependency_tree.add_dependency (s.source_file, filename)
                comment_filename = sym.comment.filename
                doc_tool.dependency_tree.add_dependency (s.source_file, comment_filename)

            self.__update_dependencies (s.sections)

    def create_symbols (self, filename):
        n = datetime.now()

        self.info ("starting")
        if doc_tool.dependency_tree.initial:
            self.parse_file (os.path.join(self.directory, filename))
        else:
            for filename in doc_tool.dependency_tree.stale_sections:
                self.parse_file (filename)

        n = datetime.now()
        self.__update_dependencies (self.sections)
        self.info ("done")
