__all__ = ['extract_taxonomy_graph', 'filter_by_ids', 'is_item', 'extract_id', 'get_subclass_of', 'get_instance_of',
           'read_json_dump']

import bz2
import gzip
import json
import logging
import os
import re
import typing as typ


def read_json_dump(dump_path: str) -> typ.Iterable[str]:
    extension = os.path.splitext(dump_path)[1]

    def open_options():
        if extension == '.gz':
            return gzip.open(dump_path, mode='rt')
        elif extension == '.bz2':
            return bz2.open(dump_path, mode='rt')
        else:
            return open(dump_path, mode='rt')

    with open_options() as f:
        for str_entity in filter(lambda l: l not in {'[', ']'},
                                 map(lambda l: l.strip().rstrip(','), f)):
            yield str_entity


def extract_taxonomy_graph(str_entities: typ.Iterable[str]) -> typ.Tuple[typ.Set[str], typ.Set[typ.Tuple[str, str]]]:
    nodes = set()
    edges = set()

    for idx, str_entity in enumerate(str_entities):
        if is_item(str_entity):
            entity = json.loads(str_entity)
            item_id = entity['id']
            subclass_of = get_subclass_of(entity)
            instance_of = get_instance_of(entity)

            edges.update((item_id, superclass) for superclass in subclass_of)
            nodes.update(subclass_of)
            nodes.update(instance_of)
            if len(subclass_of) > 0:
                nodes.add(item_id)
        if (idx + 1) % 250000 == 0:
            logging.info(f'entities: {idx + 1}\tclasses: {len(nodes)}\tsubclass-of: {len(edges)}')
    logging.info(f'completed extraction of taxonomy:\n- classes = {len(nodes)}\n- subclass-of = {len(edges)}')

    return nodes, edges


def filter_by_ids(str_entities: typ.Iterable[str], entity_ids: typ.Set[str]) -> typ.Iterable[str]:
    return filter(lambda s: extract_id(s) in entity_ids, str_entities)


def is_item(str_entity: str) -> bool:
    return '"id":"Q' in str_entity


def extract_id(str_entity: str) -> str:
    extr_id = None
    match = re.match(r'.*"id":"([Q|P]\d+)".*', str_entity)
    if match is not None:
        extr_id = match.group(1)
    return extr_id


def get_subclass_of(entity: typ.Dict) -> typ.Set[str]:
    return __get_property_entity_values(entity, 'P279')


def get_instance_of(entity: typ.Dict) -> typ.Set[str]:
    return __get_property_entity_values(entity, 'P31')


def __get_property_entity_values(entity: typ.Dict, property_id: str) -> typ.Set[str]:
    return set(map(lambda i: 'Q' + str(i),
                   map(lambda e: e.get('mainsnak').get('datavalue').get('value').get('numeric-id'),
                       filter(lambda e: e.get('mainsnak').get('snaktype') == 'value',
                              entity.get('claims').get(property_id, [])))))
