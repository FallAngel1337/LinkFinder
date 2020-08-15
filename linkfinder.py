from sys import argv
from bs4 import BeautifulSoup, Comment
import argparse
import requests
import os

parser = argparse.ArgumentParser()
parser.add_argument('--url', help='The target url')
parser.add_argument('-f', help='The files with the urls')
parser.add_argument('-o', help='The output file')
parser.add_argument('--comments', help='Grab the comments on the page', action='store_true')
args = parser.parse_args()

if args.f:
    args.f = os.path.abspath(args.f)
    try:
        os.mkdir('LinkFinder')
        os.chdir('LinkFinder')
    except FileExistsError:
        os.chdir('LinkFinder')

    with open(args.f, 'r') as urls:
        for url in urls:
            url = url.replace('\n', '')

            try:
                resp = requests.get(url).text
                soup = BeautifulSoup(resp, 'html.parser')

                if args.comments:
                        print(f'{"=" * 20} {url} {"=" * 20}\n')
                        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                            with open(url.replace('http://', '').replace('https://', '')+'_comments', 'a+') as output:
                                for link in soup.find_all('a', href=True):
                                    print(link['href'])
                                    output.write(link['href']+'\n')
                else:
                    with open(url.replace('http://', '').replace('https://', ''), 'a+') as output:
                        for link in soup.find_all('a', href=True):
                            print(link['href'])
                            output.write(link['href']+'\n')
            except ConnectionRefusedError:
                print('Connection Refused at', url)
            except Exception as err:
                print('Something gone WRONG!')
                print(err)
elif args.url:
    try:
        resp = requests.get(args.url).text
        soup = BeautifulSoup(resp, 'html.parser')
        
        if args.o and args.comments:
            print(f'{"=" * 20} {args.url} {"=" * 20}\n')
            with open(args.o, 'a+') as output:
                for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                    print(comment, '\n')
                    output.write(comment+'\n')

        elif args.o:
            with open(args.o, 'w+') as output:
                for link in soup.find_all('a', href=True):
                    print(link['href'])
                    output.write(link['href']+'\n')
        else:
            for link in soup.find_all('a', href=True):
                print(link['href'])
    except ConnectionRefusedError:
        print('Connection Refused at', url)
    except Exception as err:
        print('Somthing gone WRONG!')
        print(err)
