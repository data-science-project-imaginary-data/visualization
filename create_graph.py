import json
from pyvis.network import Network


def main():
    try:
        with open('data.json', 'r', encoding='utf8') as f:
            G = json.load(f)
    except FileNotFoundError:
        print('Get data first!')
        return

    V = G['V']
    prov_nodes = V['province']
    dist_nodes = V['district']
    type_nodes = V['type']
    E = G['E']

    net = Network(height='1024px', width='100%',
                  bgcolor='#222222', font_color='white')

    for v in prov_nodes:
        net.add_node(v['id'], label=v['label'],
                     title=time_data_label(v['seconds']),
                     color='#ff0000')
    for v in dist_nodes:
        net.add_node(v['id'], label=v['label'],
                     title=time_data_label(v['seconds']),
                     color='#00ff00')
    for v in type_nodes:
        net.add_node(v['id'], label=v['label'],
                     title=time_data_label(v['seconds']),
                     color='#0000ff')

    for e in E:
        print(e)
        net.add_edge(e['source'], e['target'])

    net.show('index.html', notebook=False)


def time_data_label(seconds):
    mins = seconds / 60
    hours = mins / 60
    days = hours / 24

    seconds = int(seconds)
    mins = int(mins)
    hours = int(hours)
    days = int(days)

    return f'{seconds} วินาที\n{mins} นาที\n{hours} ชั่วโมง\n{days} วัน'


if __name__ == '__main__':
    main()
