import re
from collections import Counter

def parse_log_line(line):
    # Regular expression to parse a common log line format
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<date>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<size>\d+|-) "(?P<referrer>.*?)" "(?P<user_agent>.*?)"'
    )
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    return None

def analyze_log_file(log_file_path):
    with open(log_file_path, 'r') as file:
        log_lines = file.readlines()

    requests = []
    status_codes = []
    ip_addresses = []

    for line in log_lines:
        parsed_line = parse_log_line(line)
        if parsed_line:
            requests.append(parsed_line['request'])
            status_codes.append(parsed_line['status'])
            ip_addresses.append(parsed_line['ip'])

    return requests, status_codes, ip_addresses

def generate_report(requests, status_codes, ip_addresses):
    # Count 404 errors
    error_404_count = status_codes.count('404')

    # Most requested pages
    most_requested_pages = Counter(requests).most_common(5)

    # IP addresses with the most requests
    most_common_ips = Counter(ip_addresses).most_common(5)

    report = f"""
    Log File Analysis Report
    ------------------------
    Total 404 Errors: {error_404_count}

    Most Requested Pages:
    ---------------------
    """
    for page, count in most_requested_pages:
        report += f"{page} : {count} requests\n"

    report += "\nIP Addresses with the Most Requests:\n-----------------------------------\n"
    for ip, count in most_common_ips:
        report += f"{ip} : {count} requests\n"

    return report

if __name__ == "__main__":
    LOG_FILE_PATH = 'path/to/your/logfile.log'

    requests, status_codes, ip_addresses = analyze_log_file(LOG_FILE_PATH)
    report = generate_report(requests, status_codes, ip_addresses)

    print(report)

    with open('log_analysis_report.txt', 'w') as report_file:
        report_file.write(report)
