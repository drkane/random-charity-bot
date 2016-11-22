# adapted from https://github.com/OpenDataServices/grantnav/blob/master/dataload/fetch_charity_data.py

from html.parser import HTMLParser
import requests
from io import StringIO
import zipfile
import os
import csv
import titlecase
import json
import configargparse
import re
import gzip

current_dir = os.path.dirname(os.path.realpath(__file__))

latest_zip_file = os.path.join(current_dir, 'charity_registry.zip')
charity_names_json = os.path.join(current_dir, 'charity_names.json')


def title_exceptions(word, **kwargs):

    word_test = word.strip("(){}<>.")

    # lowercase words
    if word_test.lower() in ['a', 'an', 'of', 'the', 'is', 'or']:
        return word.lower()
        
    # uppercase words
    if word_test.upper() in ['UK', 'FM', 'YMCA', 'PTA', 'PTFA', 
            'NHS', 'CIO', 'U3A', 'RAF', 'PFA', 'ADHD', 
            'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 
            'AFC', 'CE', 'CIC'
        ]:
        return word.upper()
        
    # words with only vowels that aren't all uppercase
    if word_test.lower() in ['st','mr','mrs','ms','ltd','dr','cwm','clwb','drs']:
        return None
        
    # words with number ordinals
    ord_numbers_re = re.compile("([0-9]+(?:st|nd|rd|th))")
    if bool(ord_numbers_re.search(word_test.lower())):
        return word.lower()
    
    # words with dots/etc in the middle
    for s in [".", "'", ")"]:
        dots = word.split(s)
        if(len(dots)>1):
            # check for possesive apostrophes
            if s=="'" and dots[-1].upper()=="S":
                return s.join( [titlecase.titlecase( i, title_exceptions ) for i in dots[:-1]] + [dots[-1].lower()] )
            # check for you're and other contractions
            if word_test.upper() in ["YOU'RE","DON'T","HAVEN'T"]:
                return s.join( [titlecase.titlecase( i, title_exceptions ) for i in dots[:-1]] + [dots[-1].lower()] )
            return s.join( [titlecase.titlecase( i, title_exceptions ) for i in dots] )
        
    # words with only vowels in (treat as acronyms)
    vowels = re.compile("[AEIOUYaeiouy]")
    if not bool(vowels.search(word_test)):
        return word.upper()
    
    return None

class getFirstExtractFile(HTMLParser):
    def __init__(self, *args, **kw):
        self.first_url = None
        super().__init__(*args, **kw)

    def handle_starttag(self, tag, attrs):
        if self.first_url:
            return
        href = dict(attrs).get('href')
        if href:
            if 'RegPlusExtract' in href:
                self.first_url = href


def download_latest_file(url):
    parser = getFirstExtractFile()
    parser.feed(requests.get(url).text)
    response = requests.get(parser.first_url)

    with open(latest_zip_file, 'wb+') as fd:
        for chunk in response.iter_content(10000):
            fd.write(chunk)


# Partially copied from https://github.com/ncvo/charity-commission-extract/blob/master/bcp.py
def convert(bcpdata, lineterminator=b'*@@*', delimiter=b'@**@', quote=b'"', newdelimiter=b',', col_headers=None, escapechar=b'\\', newline=b'\n'):
    bcpdata = bcpdata.replace(escapechar, escapechar + escapechar)
    bcpdata = bcpdata.replace(quote, escapechar + quote)
    bcpdata = bcpdata.replace(delimiter, quote + newdelimiter + quote)
    bcpdata = bcpdata.replace(lineterminator, quote + newline + quote)
    return b'"' + bcpdata + b'"'


def get_json(data_json):
    zipped_data = zipfile.ZipFile(latest_zip_file, 'r')

    name_mapping = {}
    
    # get names
    csv_text = convert(zipped_data.open('extract_charity.bcp').read()).decode('latin_1')
    csv_text = csv_text.replace('\0', '')
    for line in csv.reader(StringIO(csv_text)):
        if len(line)>1 and line[1] == '0' and line[3] == 'R':
            name_mapping[line[0]] = {
                "title": titlecase.titlecase(line[2].strip(), title_exceptions) ,
                "website": 'http://beta.charitycommission.gov.uk/charity-details/?regid=' + line[0] + '&subid=0'
            }
    
    # get websites
    csv_text = convert(zipped_data.open('extract_main_charity.bcp').read()).decode('latin_1')
    csv_text = csv_text.replace('\0', '')
    for line in csv.reader(StringIO(csv_text)):
        try:
            if line[0] in name_mapping and line[9] != "":
                name_mapping[line[0]]["website"] = line[9]
        except:
            print(line, ' not converted')

    with gzip.open(data_json, 'w+') as json_file:
        json.dump(name_mapping, json_file, sort_keys=True, indent=4)

if __name__ == '__main__':
    p = configargparse.ArgParser(ignore_unknown_config_file_keys=True)
    p.add('-c', '--my-config', required=True, default="example.cfg", is_config_file=True, help='config file path')
    
    # filename of charity data file
    p.add("-f", "--data-file", default="charity_names.json.gz", help="Location of charity data file")
    
    # filename of charity data file
    p.add("-u", "--data-url", default='http://data.charitycommission.gov.uk/default.aspx', help="URL of charity data")
    
    options = p.parse_args()
    
    # action
    #download_latest_file(options.data_url)
    get_json(options.data_file)
    # os.remove(latest_zip_file)
