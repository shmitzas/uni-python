#!/usr/bin/env python
import os
import sys

# File reading, start of code
if __name__ == '__main__':
    ip = []
    status = []
    transfer_size = []
    filename = sys.argv[1]

    try:
        if os.stat(filename).st_size > 0:
            with open(filename, 'r') as logfile:
                for line in logfile:
                    tmp = line.split()
                    ip.append(tmp[0])
                    status.append(tmp[8])
                    transfer_size.append(tmp[9])
        else:
            print('File', filename, 'is empty!')
            exit()
    except OSError:
        print('File', filename, 'does not exist!')
        exit()
    except IndexError:
        print('Data in', filename, 'is formated not in "Common Log Format"!')
        exit()

# Grouping
    unique_ip = []
    unique_status = []
    i = 0
    print('Group results by:\n')
    group_by = int(input('1 - IP\n2 - HTTP status code\nInput: '))
    if group_by == 1:
        for match in (ip):
            if match not in unique_ip:
                unique_ip.append(match)
    if group_by == 2:
        for match in (status):
            if match not in unique_status:
                unique_status.append(match)

# Calculation
    ip_request_count = []
    status_request_count = []
    print('\nSort results by:\n')
    calc_mode = int(input(
        '1 - Request count \n2 - Request count percentage of all logged requests\n3 - Total number of bytes transferred \n\nInput: '))
    if group_by == 1:
        for unique_ip_match in unique_ip:
            count = 0
            for ip_match in ip:
                if unique_ip_match == ip_match:
                    count += 1
            ip_request_count.append(count)
        
        if calc_mode == 1:
            ip_request_count, unique_ip = zip(*sorted(zip(ip_request_count, unique_ip), reverse=True))
            for i in range(len(unique_ip)):
                print('IP: [' + str(unique_ip[i]) + '] has ' + str(ip_request_count[i]) + ' requests')
        if calc_mode == 2:
            ip_request_count, unique_ip = zip(*sorted(zip(ip_request_count, unique_ip), reverse=True))
            for i in range(len(unique_ip)):
                print('IP: [' + str(unique_ip[i]) + '] has ' + str(round(ip_request_count[i]/len(ip)*100, 2)) + '% of all requests')
        if calc_mode == 3:
            bytes_count = []
            for i in range(len(unique_ip)):
                tmp_size = 0
                for j in range(len(ip)):
                    if unique_ip[i] == ip[j]:
                        if transfer_size[j] == '-':
                            transfer_size[j] = 0
                        tmp_size += int(transfer_size[j])
                bytes_count.append(tmp_size)
            bytes_count, unique_ip = zip(*sorted(zip(bytes_count, unique_ip), reverse=True))
            for i in range(len(unique_ip)):
                print('IP: [' + str(unique_ip[i]) + '] transfered ' + str(bytes_count[i]) + ' bytes')

    if group_by == 2:
        for unique_status_match in unique_status:
            count = 0
            for status_match in status:
                if unique_status_match == status_match:
                    count += 1
            status_request_count.append(count)
        
        if calc_mode == 1:
            status_request_count, unique_status = zip(*sorted(zip(status_request_count, unique_status), reverse=True))
            for i in range(len(unique_status)):
                print('STATUS CODE: [' + str(unique_status[i]) + '] has ' + str(status_request_count[i]) + ' requests')
        if calc_mode == 2:
            status_request_count, unique_status = zip(*sorted(zip(status_request_count, unique_status), reverse=True))
            for i in range(len(unique_status)):
                print('STATUS CODE: [' + str(unique_status[i]) + '] has ' + str(round(status_request_count[i]/len(status)*100, 2)) + '% of all requests')
        if calc_mode == 3:
            bytes_count = []
            for i in range(len(unique_status)):
                tmp_size = 0
                for j in range(len(status)):
                    if unique_status[i] == status[j]:
                        if transfer_size[j] == '-':
                            transfer_size[j] = 0
                        tmp_size += int(transfer_size[j])
                bytes_count.append(tmp_size)
            bytes_count, unique_status = zip(*sorted(zip(bytes_count, unique_status), reverse=True))
            for i in range(len(unique_status)):
                print('STATUS CODE: [' + str(unique_status[i]) + '] transfered ' + str(bytes_count[i]) + ' bytes')