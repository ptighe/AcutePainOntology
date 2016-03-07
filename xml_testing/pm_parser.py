#From https://github.com/titipata/pubmed_parser
#Citation: Titipat Achakulvisut, Daniel E. Acuna (2015) "Pubmed Parser" http://github.com/titipata/pubmed_parser


import os
import pandas as pd
from lxml import etree
from itertools import chain
from functools import partial
from operator import is_not
from lxml.etree import tostring
# from funcy import flatten

# from compiler.ast import flatten

__all__ = [
    'list_xml_path',
    'parse_pubmed_xml',
    'parse_pubmed_xml_to_df',
    'pretty_print_xml',
]


def list_xml_path(path_dir):
    """
    List full xml path under given directory `path_dir`
    """
    fullpath = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(path_dir)) for f in fn]
    path_list = [folder for folder in fullpath if os.path.splitext(folder)[-1] == ('.nxml' or '.xml')]
    return path_list


def stringify_children(node):
    """
    Filters and removes possible Nones in texts and tails
    ref: http://stackoverflow.com/questions/4624062/get-all-text-inside-a-tag-in-lxml
    """
    parts = ([node.text] +
             list(chain(*([c.text, c.tail] for c in node.getchildren()))) +
             [node.tail])
    return ''.join(filter(None, parts))


def stringify_affiliation(node):
    """
    Filters and removes possible Nones in texts and tails
    ref: http://stackoverflow.com/questions/4624062/get-all-text-inside-a-tag-in-lxml
    """
    parts = ([node.text] +
             list(chain(*([c.text if (c.tag != 'label' and c.tag !='sup') else '', c.tail] for c in node.getchildren()))) +
             [node.tail])
    return ' '.join(filter(None, parts))


def recur_children(node):
    """
    Recursive through node to when it has multiple children
    """
    if len(node.getchildren()) == 0:
        parts = ([node.text or ''] + [node.tail or '']) if (node.tag != 'label' and node.tag !='sup') else ([node.tail or ''])
        return parts
    else:
        parts = ([node.text or ''] +
                 [recur_children(c) for c in node.getchildren()] +
                 [node.tail or ''])
        return parts


def stringify_affiliation_rec(node):
    """
    Flatten and join list to string
    ref: http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python
    """
    parts = recur_children(node)
    return ' '.join(flatten(parts)).strip()


def zip_author(author):
    """
    Give a list of author and its affiliation keys
    in this following format
    [first_name, last_name, [key1, key2]]
    return [[first_name, last_name, key1], [first_name, last_name, key2]] instead
    """
    author_zipped = list(zip([[author[0], author[1]]]*len(author[-1]), author[-1]))
    return map(lambda x: x[0] + [x[-1]], author_zipped)


def flatten_zip_author(author_list):
    """
    Apply zip_author to author_list and flatten it
    """
    author_zipped_list = map(zip_author, author_list)
    return list(chain.from_iterable(author_zipped_list))


def parse_pubmed_xml(path, include_path=False):
    """
    Given single xml path, extract information from xml file
    and return parsed xml file in dictionary format.
    """
    try:
        tree = etree.parse(path)
    except:
        try:
            tree = etree.fromstring(path)
        except:
            raise Exception("It was not able to read a path, a file-like object, or a string as an XML")

    try:
        title = ' '.join(tree.xpath('//title-group/article-title/text()')).replace('\n', ' ')
        sub_title = ' '.join(tree.xpath('//title-group/subtitle/text()')).replace('\n', ' ').replace('\t', ' ')
        full_title = title + ' ' + sub_title
    except:
        full_title = ''
    try:
        abstract = ' '.join(tree.xpath('//abstract//text()'))
    except:
        abstract = ''
    try:
        journal_title = tree.xpath('//journal-title-group/journal-title')[0].text
    except:
        try:
            journal_title = tree.xpath('/article/front/journal-meta/journal-title/text()')[0]
        except:
            journal_title = ''
    try:
        pmid = tree.xpath('//article-meta/article-id[@pub-id-type="pmid"]')[0].text
    except:
        pmid = ''
    try:
        pmc = tree.xpath('//article-meta/article-id[@pub-id-type="pmc"]')[0].text
    except:
        pmc = ''
    try:
        pub_id = tree.xpath('//article-meta/article-id[@pub-id-type="publisher-id"]')[0].text
    except:
        pub_id = ''
    try:
        pub_year = tree.xpath('//pub-date/year/text()')[0]
    except:
        pub_year = ''
    try:
        subjects = ','.join(tree.xpath('//article-categories//subj-group//text()'))
    except:
        subjects = ''

    # create affiliation dictionary
    aff_id = tree.xpath('//aff[@id]/@id')
    if len(aff_id) == 0:
        aff_id = ['']  # replace id with empty list

    aff_name = tree.xpath('//aff[@id]')
    aff_name_list = []
    for node in aff_name:
        aff_name_list.append(stringify_affiliation_rec(node))
    affiliation_list = map(list, zip(aff_id, map(lambda x: x.strip().replace('\n', ' '), aff_name_list)))  # create dictionary

    tree_author = tree.xpath('//contrib-group/contrib[@contrib-type="author"]')

    author_list = []
    for el in tree_author:
        el0 = el.findall('xref[@ref-type="aff"]')
        try:
            rid_list = [tmp.attrib['rid'] for tmp in el0]
        except:
            rid_list = ''
        try:
            author_list.append([el.find('name/surname').text, el.find('name/given-names').text, rid_list])
        except:
            author_list.append(['', '', rid_list])
    author_list = flatten_zip_author(author_list)

    dict_out = {'full_title': full_title.strip(),
                'abstract': abstract,
                'journal_title': journal_title,
                'pmid': pmid,
                'pmc': pmc,
                'publisher_id': pub_id,
                'author_list': author_list,
                'affiliation_list': affiliation_list,
                'publication_year': pub_year,
                'subjects': subjects}
    if include_path:
        dict_out['path_to_file'] = path
    return dict_out


def parse_pubmed_xml_to_df(paths, include_path=False, remove_abstract=False):
    """
    Given list of xml paths, return parsed DataFrame

    path_list: list of xml paths
    remove_abs: if true, remove row of dataframe if parsed xml contains empty abstract
    path_xml: if true, concat path to xml file when constructing DataFrame
    """
    pm_docs = []
    if not isinstance(paths, list):
        pm_docs = [parse_pubmed_xml(paths, include_path=include_path)] # in case providing single path
    else:
        # else for list of paths
        for path in paths:
            pm_dict = parse_pubmed_xml(path, include_path=include_path)
            pm_docs.append(pm_dict)

    pm_docs = filter(partial(is_not, None), pm_docs)  # remove None
    pm_docs_df = pd.DataFrame(pm_docs) # turn to pandas DataFrame

    # remove empty abstract
    if remove_abstract:
        pm_docs_df = pm_docs_df[pm_docs_df.abstract != ''].reset_index().drop('index', axis=1)

    return pm_docs_df


def pretty_print_xml(path):
    """
    Given a XML path, file-like, or string, print a pretty xml version of it
    """
    try:
        tree = etree.parse(path)
    except:
        try:
            tree = etree.fromstring(path)
        except:
            raise Exception("It was not able to read a path, a file-like object, or a string as an XML")

    print (tostring(tree, pretty_print=True))


def chunks(l, n):
    """
    Yield successive n-sized chunks from l
    Suppose we want to chunk all path list into smaller chunk
    example: chunks(path_list, 10000)
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]


xmlfile='pubmed_result_tighe.xml'
dunno = list_xml_path(xmlfile)
parse_pubmed_xml_to_df(dunno)