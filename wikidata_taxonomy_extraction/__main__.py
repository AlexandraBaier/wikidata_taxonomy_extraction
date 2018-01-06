import argparse
import logging
import os
import sys

import wikidata_taxonomy_extraction as wte


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dump', help='Path to Wikidata JSON dump.', type=str)
    parser.add_argument('-f', '--full', help='Additionally extract class objects. Requires second read of dump.',
                        action='store_true')
    parser.add_argument('-v', '--verbose', help='Prints progress log to stdout.',
                        action='store_true')
    args = parser.parse_args()

    if not os.path.isfile(args.dump):
        sys.exit(f'ERROR: Provided file "{args.dump}" does not exist.')

    if args.verbose:
        logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO)
        logging.info('verbose active')

    dump_base = os.path.splitext(os.path.splitext(args.dump)[0])[0]
    nodes_path = dump_base + '.nodes.taxonomy.csv'
    edges_path = dump_base + '.edges.taxonomy.csv'

    logging.info(f'start extracting taxonomy from "{args.dump}"')
    try:
        nodes, edges = wte.extract_taxonomy_graph(wte.read_json_dump(args.dump))
    except IOError:
        sys.exit(f'Could not read dump at {args.dump}.')

    with open(nodes_path, mode='wt') as f:
        f.write('class\n')
        f.writelines([f'{node}\n' for node in nodes])
    logging.info(f'wrote classes to {nodes_path}')

    with open(edges_path, mode='wt') as f:
        f.write('subclass,superclass\n')
        f.writelines(f'{subclass},{superclass}\n' for subclass, superclass in edges)
    logging.info(f'wrote subclass-of relations to {edges_path}')

    if args.full:
        logging.info('--full option selected, extract all classes')
        classes_path = dump_base + '.classes.taxonomy.jsonl'

        try:
            str_entities = wte.read_json_dump(args.dump)
        except IOError:
            sys.exit(f'Could not read dump at {args.dump}.')

        classes_written = 0
        with open(classes_path, mode='wt') as f:
            for str_class in wte.filter_by_ids(str_entities, nodes):
                f.write(str_class + '\n')
                classes_written += 1
                if classes_written % 100000 == 0:
                    logging.info(f'extraction progress: {int(100 * classes_written/len(nodes))}%')
                if classes_written == len(nodes):
                    break
        logging.info(f'wrote classes objects to {classes_path}')


if __name__ == '__main__':
    main()
