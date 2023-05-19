import json
from pyvis.network import Network


def main():
    try:
        with open('data.json', 'r', encoding='utf8') as f:
            G = json.load(f)
    except FileNotFoundError:
        print('Get data first!')
        return

    net = Network(height='100vh', width='100vw',
                  bgcolor='#343f56', font_color='white')

    V = G['V']
    for nodes, color in ((V['province'], '#f5e6ca'), (V['district'], '#ffb9b9'), (V['type'], 'white')):  # noqa: E501
        for v in nodes:
            title, mins, hours, days = time_data_title(v['seconds'])
            time_label = f'{days} วัน' if days > 0 else f'{hours} ชั่วโมง' if hours > 0 else f'{mins} นาที'  # noqa: E501
            net.add_node(v['id'], label=f"{v['label']}\n{time_label}",
                         title=title,
                         color=color,
                         size=max(5, days / 10))

    for e in G['E']:
        net.add_edge(e['source'], e['target'])

    net.show('index.html', notebook=False)


def time_data_title(seconds):
    mins = seconds / 60
    hours = mins / 60
    days = hours / 24

    seconds = int(seconds)
    mins = int(mins)
    hours = int(hours)
    days = int(days)

    return f'{seconds} วินาที\n{mins} นาที\n{hours} ชั่วโมง\n{days} วัน', mins, hours, days  # noqa: E501


if __name__ == '__main__':
    main()
