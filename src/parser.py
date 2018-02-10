import ENML_PY as enml
from bs4 import BeautifulSoup
import copy

def ENMLToHTML(content):
    html = enml.ENMLToHTML(content, header=False)
    soup = BeautifulSoup(html, "html.parser")
    
    # convert tables to paragraphs
    for table in soup.find_all('table'):
        # body = table.find('tbody')
        # print("body: {0}".format(body.find_all('tr')))
        # for row in body.find_all('tr'):
        for ele in table.find_all('td'):
            for content in ele.contents:
                if content.name != "p":
                    temp = copy.deepcopy(content)
                    tag = temp.wrap(soup.new_tag('p'))
                    table.insert_before(tag)
                else:
                    tag = copy.deepcopy(content)
                    table.insert_before(tag)
        # remove the table
        table.decompose()
    
    # convert <strong> to <b>
    for tag in soup.find_all('strong'):
        new_tag = soup.new_tag("b")
        new_tag.string = tag.get_text()
        tag.replace_with(new_tag)

    invalid_tags = ['div', 'font']
    for tag in invalid_tags: 
        for match in soup.findAll(tag):
            match.replaceWithChildren()

    # remove \n

    # remove all attributes
    for tag in soup.find_all(True):
        if len(list(tag.stripped_strings)) is 0:
            tag.decompose()
        else:
            tag.attrs = {}              
        
    return soup