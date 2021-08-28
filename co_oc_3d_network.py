import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly
import datetime


def apply_js(fig, filename):
  # js読み込み
    with open("plotly_click.js") as f:
        plotly_click_js = f.read()

    # Create <div> element
    plot_div = plotly.io.to_html(
        fig,
        include_plotlyjs=True,
        post_script=plotly_click_js,
        full_html=False,
    )

    # Build HTML
    html_str = """
    <html>
    <head>
    </head>
    <body>
    <div id="plotly-node-info">
    <p>**Node Information**</p>
    </div>
    {plot_div}
    </body>
    </html>
    """.format(
        plot_div=plot_div
    )
    # Write out HTML file
    with open(f"{filename}.html", "w") as f:
        f.write(html_str)


def append_edge_dictionary(dictionary, num, x, y, z, weight):
    for idx in range(len(x)):
        dictionary[f'e{num}']['x'].append(x[idx])
        dictionary[f'e{num}']['y'].append(y[idx])
        dictionary[f'e{num}']['z'].append(z[idx])
        dictionary[f'e{num}']['weight'].append(weight)

    return dictionary


def append_node_dictionary(dictionary, num, x, y, z, frequency, text, info):
    dictionary[f'n{num}']['x'].append(x)
    dictionary[f'n{num}']['y'].append(y)
    dictionary[f'n{num}']['z'].append(z)
    dictionary[f'n{num}']['frequency'].append(frequency)
    dictionary[f'n{num}']['text'].append(text)
    dictionary[f'n{num}']['info'].append(info)

    return dictionary


def create_3d_network(df, target_num=50):
    # 新規グラフを作成
    G = nx.Graph()

    # タプル作成
    kyouki_tuple = [(first, second, count) for first, second,
                    count in zip(df['first'], df['second'], df['count'])]

    # ノードとエッジを追加
    list_edge = kyouki_tuple[:target_num]
    G.add_weighted_edges_from(list_edge)

    # nodeの連結nodeを取得
    neighbors_list = ['<br>'.join(list(nx.all_neighbors(G, t)))
                      for t in list(G.nodes())]

    # 各単語の頻度を計算
    word_frequency = {}
    for node in G.nodes():
        sum = np.sum(df.query(' @node == first or @node == second ')
                     ['count'].to_list())
        word_frequency[node] = sum

    # 各ノード情報を記載
    for idx, text in enumerate(list(G.nodes())):
        G.nodes[text]['node_info'] = {
            'id': idx+1,
            'word': text,
            'frequency': word_frequency[text],
            'neighbors': f'<br>{neighbors_list[idx]}',
        }

    # 図のレイアウトを決める。kの値が小さい程図が密集
    pos = nx.spring_layout(G, k=2.0, dim=3, seed=144)

    # ノードの位置を設定
    for node in G.nodes():
        G.nodes[node]["pos"] = pos[node]

    # エッジの設定
    edge_group = [10, 50, 100]
    edges = dict(e1=dict(x=[], y=[], z=[], weight=[]),
                 e2=dict(x=[], y=[], z=[], weight=[]),
                 e3=dict(x=[], y=[], z=[], weight=[]),
                 e4=dict(x=[], y=[], z=[], weight=[]),)
    for e in G.edges():
        x0, y0, z0 = G.nodes[e[0]]['pos']
        x1, y1, z1 = G.nodes[e[1]]['pos']
        weight = G.edges[e]['weight']
        x_list = [x0, x1, None]
        y_list = [y0, y1, None]
        z_list = [z0, z1, None]

        if weight < edge_group[0]:
            edges = append_edge_dictionary(
                edges, 1, x=x_list, y=y_list, z=z_list, weight=weight)
        elif edge_group[0] <= weight < edge_group[1]:
            edges = append_edge_dictionary(
                edges, 2, x=x_list, y=y_list, z=z_list, weight=weight)
        elif edge_group[1] <= weight < edge_group[2]:
            edges = append_edge_dictionary(
                edges, 3, x=x_list, y=y_list, z=z_list, weight=weight)
        else:
            edges = append_edge_dictionary(
                edges, 4, x=x_list, y=y_list, z=z_list, weight=weight)

    fig = go.Figure()

    line_width = [2.5, 5, 7.5, 10]
    for idx in range(len(line_width)):
        if idx == 3:
            name_text = f'{edge_group[2]} <='
        else:
            name_text = f'< {edge_group[idx]}'
        fig.add_trace(go.Scatter3d(
            name=name_text,
            x=edges[f'e{idx+1}']['x'],
            y=edges[f'e{idx+1}']['y'],
            z=edges[f'e{idx+1}']['z'],
            mode='lines',
            legendgroup='edges',
            legendgrouptitle=dict(text='count'),
            line=dict(width=line_width[idx]),
            customdata=edges[f'e{idx+1}']['weight'],
            hovertemplate="count: %{customdata}<extra></extra>"
        ))

    # ノードの設定
    node_group = [250, 500, 1000]
    nodes = dict(n1=dict(x=[], y=[], z=[], frequency=[], text=[], info=[]),
                 n2=dict(x=[], y=[], z=[], frequency=[], text=[], info=[]),
                 n3=dict(x=[], y=[], z=[], frequency=[], text=[], info=[]),
                 n4=dict(x=[], y=[], z=[], frequency=[], text=[], info=[]),)
    for n in G.nodes():
        x, y, z = G.nodes[n]['pos']
        frequency = word_frequency.get(n)
        text = n
        info = '<br>'.join(
            [f'{k}: {value}' for k, value in G.nodes[n]['node_info'].items()])
        if frequency < node_group[0]:
            nodes = append_node_dictionary(
                nodes, 1, x, y, z, frequency, text, info)
        elif node_group[0] <= frequency < node_group[1]:
            nodes = append_node_dictionary(
                nodes, 2, x, y, z, frequency, text, info)
        elif node_group[1] <= frequency < node_group[2]:
            nodes = append_node_dictionary(
                nodes, 3, x, y, z, frequency, text, info)
        else:
            nodes = append_node_dictionary(
                nodes, 4, x, y, z, frequency, text, info)

    marker_size = [4, 7, 10, 13]
    for idx in range(len(marker_size)):
        if idx == 3:
            name_text = f'{node_group[2]} <='
        else:
            name_text = f'< {node_group[idx]}'
        fig.add_trace(go.Scatter3d(
            name=name_text,
            x=nodes[f'n{idx+1}']['x'],
            y=nodes[f'n{idx+1}']['y'],
            z=nodes[f'n{idx+1}']['z'],
            text=nodes[f'n{idx+1}']['text'],
            customdata=nodes[f'n{idx+1}']['info'],
            textposition='middle center',
            mode='markers+text',
            legendgroup='nodes',
            legendgrouptitle=dict(text='frequency'),
            marker=dict(size=marker_size[idx], line=dict(width=2),
                        color='rgb(200, 150, 150)'),
            hovertemplate="%{customdata}<extra></extra>",
        ))

    layout = go.Layout(
        showlegend=True,
        legend=dict(
            borderwidth=2,
        ),
        scene=dict(
            xaxis=dict(backgroundcolor='rgb(150, 100, 100)'),
            yaxis=dict(backgroundcolor='rgb(100, 150, 100)'),
            zaxis=dict(backgroundcolor='rgb(100, 100, 150)'),
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        clickmode='select+event',
    )

    fig.update_layout(layout)

    # plotly_click.jsを適用する
    #apply_js(fig, 'test3')

    now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    html_file_name = f'{now}_3D_network'
    fig.write_html(f'tmp/{html_file_name}.html', auto_open=False)

    return html_file_name