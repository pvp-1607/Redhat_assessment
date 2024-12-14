import argparse
import re
import sys

TIMESTAMP_PATTERN = r"\b\d{2}:\d{2}:\d{2}\b"
IPV4_PATTERN = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
IPV6_PATTERN = r"(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}))"

def parse_args():
    parser = argparse.ArgumentParser(description="Log Parser Utility")
    parser.add_argument("file", nargs="?", type=argparse.FileType('r'), default=sys.stdin,
                        help="Log file to parse (default: stdin)")
    parser.add_argument("-f", "--first", type=int, help="Print first NUM lines")
    parser.add_argument("-l", "--last", type=int, help="Print last NUM lines")
    parser.add_argument("-t", "--timestamps", action="store_true", help="Print lines with timestamps")
    parser.add_argument("-i", "--ipv4", action="store_true", help="Print lines with IPv4 addresses")
    parser.add_argument("-I", "--ipv6", action="store_true", help="Print lines with IPv6 addresses")
    return parser.parse_args()

def highlight(pattern, text):
    return re.sub(pattern, lambda m: f"\033[91m{m.group(0)}\033[0m", text)

def process_lines(lines, args):
    result = lines
    if args.first:
        result = result[:args.first]
    if args.last:
        result = result[-args.last:]
    if args.timestamps:
        result = [line for line in result if re.search(TIMESTAMP_PATTERN, line)]
    if args.ipv4:
        result = [line for line in result if re.search(IPV4_PATTERN, line)]
        result = [highlight(IPV4_PATTERN, line) for line in result]
    if args.ipv6:
        result = [line for line in result if re.search(IPV6_PATTERN, line)]
        result = [highlight(IPV6_PATTERN, line) for line in result]
    return result

def main():
    args = parse_args()
    lines = args.file.read().splitlines()
    filtered_lines = process_lines(lines, args)
    for line in filtered_lines:
        print(line)

if __name__ == "__main__":
    main()
