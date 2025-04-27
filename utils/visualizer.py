# utils/visualizer.py

import os
import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go

def ensure_output_dir(output_dir):
    """Ensure the output directory exists."""
    os.makedirs(output_dir, exist_ok=True)

def plot_flag_frequency(entries, output_dir):
    ensure_output_dir(output_dir)
    flag_counts = {}
    for entry in entries:
        for flag in entry.flags:
            flag_counts[flag] = flag_counts.get(flag, 0) + 1

    if not flag_counts:
        print("[!] No flags found to plot.")
        return

    plt.figure(figsize=(10, 6))
    plt.bar(flag_counts.keys(), flag_counts.values(), color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.title('Flag Frequency Across Registry Entries')
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'flag_frequency.png')
    plt.savefig(output_path)
    plt.close()
    print(f"[+] Saved flag frequency bar chart to {output_path}")

def plot_suspicious_folder_pie(entries, output_dir):
    ensure_output_dir(output_dir)
    suspicious = sum(1 for entry in entries if "Suspicious Folder" in entry.flags)
    normal = len(entries) - suspicious

    if suspicious + normal == 0:
        print("[!] No entries to plot pie chart.")
        return

    labels = ['Suspicious Folder', 'Normal Folder']
    sizes = [suspicious, normal]
    colors = ['red', 'green']

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Dropped Files in Suspicious vs Normal Folders')
    output_path = os.path.join(output_dir, 'suspicious_folder_pie.png')
    plt.savefig(output_path)
    plt.close()
    print(f"[+] Saved suspicious folder pie chart to {output_path}")

def plot_persistence_graph(entries, output_dir):
    ensure_output_dir(output_dir)
    G = nx.DiGraph()

    for entry in entries:
        if entry.file_path:
            G.add_edge(entry.reg_key, entry.file_path)

    if not G.nodes:
        print("[!] No graph nodes to plot.")
        return

    node_count = len(G.nodes)
    k_value = 2.5 if node_count < 20 else 3.0

    plt.figure(figsize=(24, 18))
    pos = nx.spring_layout(G, k=k_value, iterations=200)

    registry_nodes = [node for node in G.nodes if node.startswith('HKEY')]
    file_nodes = [node for node in G.nodes if not node.startswith('HKEY')]

    nx.draw_networkx_nodes(G, pos,
                           nodelist=registry_nodes,
                           node_color='red',
                           node_size=1500,
                           alpha=0.9)

    nx.draw_networkx_nodes(G, pos,
                           nodelist=file_nodes,
                           node_color='skyblue',
                           node_size=1300,
                           alpha=0.8)

    nx.draw_networkx_edges(G, pos,
                           arrows=True,
                           arrowstyle='-|>',
                           arrowsize=30,
                           edge_color='gray',
                           width=2)

    nx.draw_networkx_labels(G, pos,
                            font_size=10,
                            verticalalignment='center')

    plt.title('Persistence Registry Key ➔ Dropped File Map', fontsize=18)
    plt.axis('off')
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'persistence_graph.png')
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[+] Saved spring persistence graph to {output_path}")

def plot_persistence_sankey(entries, output_dir):
    ensure_output_dir(output_dir)

    registry_keys = []
    dropped_files = []

    for entry in entries:
        if entry.file_path:
            registry_keys.append(entry.reg_key)
            dropped_files.append(entry.file_path)

    if not registry_keys or not dropped_files:
        print("[!] No data for Sankey diagram.")
        return None

    all_nodes = list(set(registry_keys + dropped_files))
    node_indices = {node: idx for idx, node in enumerate(all_nodes)}

    sources = [node_indices[reg] for reg in registry_keys]
    targets = [node_indices[file] for file in dropped_files]
    values = [1] * len(sources)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes,
            color="blue"
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values
        )
    )])

    fig.update_layout(title_text="Persistence Registry ➔ Dropped File Map (Sankey Diagram)", font_size=10)
    output_path = os.path.join(output_dir, 'persistence_sankey.html')
    fig.write_html(output_path)
    print(f"[+] Saved interactive Sankey diagram to {output_path}")

    return output_path
