from lxml import etree


def get_etree(source):
    return etree.HTML(source)


def cleaned_string(string):
    return " ".join(s for s in string.replace("\t", "").replace("\n", "").replace("/", "").split())


def snaked_string(string):
    return "_".join(string.split()).lower()


def table_to_dict(table):
    table_head, *row_elements = table.xpath('.//div[@class="divTableBody"]/div[@class="divTableRow"]')
    headers = [
        snaked_string(cleaned_string("".join(re.itertext())))
        for re in table_head.xpath('.//div[@class="divTableCell"]')
    ]
    rows = []
    for tr in row_elements:
        row = [cleaned_string(str().join(re.itertext())) for re in tr.xpath('.//div[@class="divTableCell"]')]
        rows.append(row)
    return [dict(zip(headers, r)) for r in rows]
