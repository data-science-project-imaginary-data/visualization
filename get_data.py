from dotenv import load_dotenv
import os
from pymongo import MongoClient
import urllib
from collections import defaultdict
from datetime import datetime
import json


def main():
    load_dotenv()

    try:
        username = urllib.parse.quote_plus(os.getenv('MONGO_USERNAME'))
        password = urllib.parse.quote_plus(os.getenv('MONGO_PASSWORD'))
        host = os.getenv('MONGO_HOST')
    except TypeError:
        print('Please set environment variables first!')
        return

    connection_string = f'mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority'  # noqa: E501
    client = MongoClient(connection_string)
    db = client['myDB']
    col = db['data']

    G = {
        'V': defaultdict(list),
        'E': []
    }

    by_district_sum = defaultdict(float)
    by_district_count = defaultdict(int)
    by_province_sum = defaultdict(float)
    by_province_count = defaultdict(int)
    province_district_edges = defaultdict(list)
    district_type_edges = defaultdict(float)
    district_type_count = defaultdict(int)

    for entry in col.find({}, limit=20):
    # for entry in col.find():
        seconds_taken = (datetime.strptime(entry['last_activity'], '%Y-%m-%d %H:%M:%S.%f+00')
                  - datetime.strptime(entry['timestamp'], '%Y-%m-%d %H:%M:%S.%f+00')).total_seconds()  # noqa: E501

        province = entry['province']
        district = entry['district']
        by_district_sum[district] += seconds_taken
        by_district_count[district] += 1
        by_province_sum[province] += seconds_taken
        by_province_count[province] += 1
        province_district_edges[province].append(district)

        types = entry['type']
        if not isinstance(types, list):
            continue

        for type_ in types:
            if type_ == '':
                type_ = 'ไม่ระบุ'
            dt = f'{district}-{type_}'
            district_type_edges[dt] += seconds_taken
            district_type_count[dt] += 1

    # district nodes
    for district, sec_sum in by_district_sum.items():
        G['V']['district'].append({'id': district, 'label': district, 'seconds': sec_sum / by_district_count[district]})  # noqa: E501
    # province nodes
    for province, sec_sum in by_province_sum.items():
        G['V']['province'].append({'id': province, 'label': province, 'seconds': sec_sum / by_province_count[province]})  # noqa: E501
    # connect province to district
    for province, districts in province_district_edges.items():
        for district in districts:
            G['E'].append({'source': province, 'target': district})

    # type nodes, edges
    for k, sec_sum in district_type_edges.items():
        G['V']['type'].append({'id': k, 'label': k.split('-')[1], 'seconds': sec_sum / district_type_count[k]})  # noqa: E501
        district, type_ = k.split('-')
        # connect district to type
        G['E'].append({'source': district, 'target': k})

    with open('data.json', 'w', encoding='utf8') as f:
        json.dump(G, f, ensure_ascii=False)


if __name__ == '__main__':
    main()
