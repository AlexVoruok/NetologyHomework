import json
from pprint import pprint


class LinkMaker:

    def __init__(self, source, domain, startcounter=0):
        self.source = source
        self.domain = domain
        self.counter = startcounter

    def __iter__(self):
        return self

    def __next__(self):
        try:
            country = self.source[self.counter]['name']['official'].replace(' ', '_')
            genlink = f'{self.domain}{country}'
            rusname = self.source[self.counter]['translations']['rus']['common']
            data_to_write = f'{rusname} - {genlink}'
            self.counter += 1
            return data_to_write

        except IndexError:
            raise StopIteration


if __name__ == '__main__':

    with open('countries.json', 'r') as f:
        sourcedata = json.load(f)

    # pprint(sourcedata[0])
    #
    # for country in sourcedata:
    #     name = country['name']['official'].replace(' ', '_')
    #     pprint(f'https://wikipedia.org/wiki/{name}')

    with open('country_wikilinks.txt', 'w', encoding='utf-8') as wikilinks:
        for link in LinkMaker(sourcedata, 'https://wikipedia.org/wiki/'):
            print(link)
            wikilinks.write(link + '\n')
