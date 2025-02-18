import json  
import csv  
import os  

def read_logs(log_file):  
    with open(log_file, 'r', encoding='utf-8') as f:  
        logs = f.readlines()  
    return [json.loads(log.strip(',\n')) for log in logs if log.strip(',\n')]  

def process_logs(logs):  
    processed_logs = []  
    for log in logs:  
        # Filter to include only GET and POST methods and Salesforce URLs  
        if log.get('method') in ['GET', 'POST'] and 'salesforce.com' in log.get('url', ''):  
            processed_log = {  
                'headers_Host': log.get('headers_Host', ''),  
                'url': log.get('url', ''),  
                'method': log.get('method', 'UNKNOWN'),  
                'requestHeaders_Origin': log.get('requestHeaders_Origin', ''),  
                'requestHeaders_Content_Type': log.get('requestHeaders_Content_Type', ''),  
                'responseHeaders_Content_Type': log.get('responseHeaders_Content_Type', ''),  
                'responseHeaders_Content_Disposition': log.get('responseHeaders_Content_Disposition', ''),  
                'responseHeaders_Content_Encoding': log.get('responseHeaders_Content_Encoding', ''),  
                'requestHeaders_Referer': log.get('requestHeaders_Referer', ''),  
                'requestHeaders_Accept': log.get('requestHeaders_Accept', ''),  
                'requestHeaders_Sec_Fetch_Mode': log.get('requestHeaders_Sec_Fetch_Mode', ''),  
                'service': log.get('service', 'Salesforce'),  
                'activityType': log.get('activityType', 'Unknown')  
            }  
            processed_logs.append(processed_log)  
    return processed_logs  

def write_to_csv(processed_logs, output_file):  
    headers = [  
        'headers_Host', 'url', 'method', 'requestHeaders_Origin',  
        'requestHeaders_Content_Type', 'responseHeaders_Content_Type',  
        'requestHeaders_Referer', 'requestHeaders_Accept',  
        'responseHeaders_Content_Disposition', 'responseHeaders_Content_Encoding',  
        'requestHeaders_Sec_Fetch_Mode', 'service', 'activityType'  
    ]  

    # Remove existing file if it exists to avoid appending to old data  
    if os.path.exists(output_file):  
        os.remove(output_file)  

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:  
        writer = csv.DictWriter(file, fieldnames=headers)  
        writer.writeheader()  

        for log in processed_logs:  
            row = {key: log.get(key, '') for key in headers}  
            writer.writerow(row)  

# Paths to input and output files  
logs = read_logs('./all_traffic_logs.json')  
processed_logs = process_logs(logs)  
write_to_csv(processed_logs, './all_traffic_dataset.csv')  

print("Dataset created: all_traffic_dataset.csv")
