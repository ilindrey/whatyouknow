from argparse import ArgumentParser
from data_gen import main

parser = ArgumentParser(description='Data generation.')

parser.add_argument('-s', '--script', default='', metavar='')

parser.add_argument('-f', '--factor',
                    metavar='value',
                    type=int,
                    help='determines the amount of data generated')

args = parser.parse_args()

main(getattr(args, 'factor'))
