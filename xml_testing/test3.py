import pm_parser

file_list =[]
file='pubmed_result_tighe.xml'
file_list.append(file)

file_list[0]

# path_xml = list_xml_path(path)


parse_pubmed_xml(file, include_path=False)

parse_pubmed_xml_to_df(file)


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
    dict_out = {'full_title': full_title.strip(),
            'abstract': abstract,
            'journal_title': journal_title,
            'pmid': pmid,
            'pmc': pmc,
            'publisher_id': pub_id,
            # 'author_list': author_list,
            # 'affiliation_list': affiliation_list,
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

    # pm_docs = filter(partial(is_not, None), pm_docs)  # remove None
    pm_docs_df = pd.DataFrame(pm_docs) # turn to pandas DataFrame

    # remove empty abstract
    if remove_abstract:
        pm_docs_df = pm_docs_df[pm_docs_df.abstract != ''].reset_index().drop('index', axis=1)

    return pm_docs_df

dodf = parse_pubmed_xml_to_df(path)
dodf