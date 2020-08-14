from sys import argv
from bs4 import BeautifulSoup, Comment
import argparse
import requests
import os

parser = argparse.ArgumentParser()
parser.add_argument('--url', help='The target url')
parser.add_argument('-f', help='The files with the urls')
parser.add_argument('-o', help='The output file')
parser.add_argument('--save_dir', help='It will creat a dir to save the output', action='store_true')
parser.add_argument('--comments', help='Grab the comments on the page', action='store_true')
args = parser.parse_args()

if args.f:
    if args.save_dir:
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
                
                if args.save_dir:
                    with open(url.replace('http://', '').replace('https://', ''), 'a+') as output:
                        for link in soup.find_all('a', href=True):
                            print(link['href'])
                            output.write(link['href']+'\n')
                elif args.comments:
                        print(f'{"=" * 20} {url} {"=" * 20}\n')
                        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                            print(comment, '\n')
                else:
                    for link in soup.find_all('a', href=True):
                        print(link['href'])
            except ConnectionRefusedError:
                print('Connection Refused at', url)
            except Exception as err:
                print('Something gone WRONG!')
                print(err)
                #exit()
else:
    try:
        resp = requests.get(args.url).text
        soup = BeautifulSoup(resp, 'html.parser')
        
        if args.o:
            with open(args.o, 'w+') as output:
                for link in soup.find_all('a', href=True):
                    print(link['href'])
                    output.write(link['href']+'\n')
        elif args.comments:
            print(f'{"=" * 20} {url} {"=" * 20}\n')
            for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                print(comment,'\n')
            print('=' * 45)
        else:
            for link in soup.find_all('a', href=True):
                print(link['href'])
    except ConnectionRefusedError:
        print('Connection Refused at', url)
    except Exception as err:
        print('Somthing gone WRONG!')
        print(err)
        #exit()

