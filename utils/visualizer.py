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

    plt.figure(figsize=(12, 7))

    labels = list(flag_counts.keys())
    counts = list(flag_counts.values())

    # Create a unique color for each bar
    colors = plt.cm.tab20.colors  # A colormap with many distinct colors
    bar_colors = [colors[i % len(colors)] for i in range(len(labels))]

    bars = plt.bar(labels, counts, color=bar_colors)

    plt.xticks(rotation=45, ha='right')
    plt.title('Flag Frequency Across Registry Entries', fontsize=16)
    plt.ylabel('Count', fontsize=14)
    plt.xlabel('Flags', fontsize=14)
    plt.tight_layout()

    output_path = os.path.join(output_dir, 'flag_frequency.png')
    plt.savefig(output_path)
    plt.close()
    print(f"[+] Saved colorful flag frequency bar chart to {output_path}")


def plot_suspicious_folder_pie(entries, output_dir):
    import os
    import matplotlib.pyplot as plt

    def ensure_output_dir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    ensure_output_dir(output_dir)

    suspicious = sum(1 for entry in entries if "Suspicious Folder" in entry.flags)
    normal = len(entries) - suspicious

    if suspicious + normal == 0:
        print("[!] No entries to plot pie chart.")
        return

    labels = ['Suspicious Folder', 'Normal Folder']
    sizes = [suspicious, normal]
    colors = ['red', 'green']

    fig, ax = plt.subplots(figsize=(7, 7))

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        textprops={'fontsize': 12},
        pctdistance=0.75,
    )

    # Make it a donut chart (optional but looks cleaner)
    centre_circle = plt.Circle((0, 0), 0.50, fc='white')
    fig.gca().add_artist(centre_circle)

    ax.axis('equal')  # Equal aspect ratio ensures the pie is a circle
    plt.title('Dropped Files in Suspicious vs Normal Folders', fontsize=14)

    output_path = os.path.join(output_dir, 'suspicious_folder_pie.png')
    plt.tight_layout()
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

def plot_persistence_hive(entries, output_dir):
    """Generate a clean Hive Plot for registry persistence mapping."""
    os.makedirs(output_dir, exist_ok=True)

    G = nx.DiGraph()

    registry_keys = []
    dropped_files = []

    for entry in entries:
        if entry.file_path:
            registry_keys.append(entry.reg_key)
            dropped_files.append(entry.file_path)
            G.add_edge(entry.reg_key, entry.file_path)

    if not G.nodes:
        print("[!] No nodes available to plot Hive diagram.")
        return

    # Assign positions: X=0 for registry keys, X=1 for dropped files
    pos = {}
    reg_y = 1.0
    drop_y = 1.0

    # Sort for consistent layout
    registry_keys_sorted = sorted(set(registry_keys))
    dropped_files_sorted = sorted(set(dropped_files))

    spacing = 1.5 / max(len(registry_keys_sorted), 1)  # avoid division by zero
    for reg in registry_keys_sorted:
        pos[reg] = (0, reg_y)
        reg_y -= spacing

    spacing = 1.5 / max(len(dropped_files_sorted), 1)
    for drop in dropped_files_sorted:
        pos[drop] = (1, drop_y)
        drop_y -= spacing

    # Drawing
    plt.figure(figsize=(20, 12))
    plt.title('Persistence Registry Key ➔ Dropped File Map (Hive Plot)', fontsize=18)

    # Draw registry nodes (left)
    nx.draw_networkx_nodes(G, pos,
                           nodelist=registry_keys_sorted,
                           node_color='red',
                           node_size=300,
                           label='Registry Keys',
                           alpha=0.8)

    # Draw dropped file nodes (right)
    nx.draw_networkx_nodes(G, pos,
                           nodelist=dropped_files_sorted,
                           node_color='skyblue',
                           node_size=300,
                           label='Dropped Files',
                           alpha=0.8)

    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=False, width=1)

    # Draw labels separately to avoid collision
    for node, (x, y) in pos.items():
        if x == 0:
            plt.text(x - 0.02, y, node, horizontalalignment='right', verticalalignment='center', fontsize=7)
        else:
            plt.text(x + 0.02, y, node, horizontalalignment='left', verticalalignment='center', fontsize=7)

    plt.axis('off')
    plt.legend()
    plt.tight_layout()

    output_path = os.path.join(output_dir, 'persistence_hive.png')
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"[+] Saved Hive Plot persistence graph to {output_path}")
def plot_force_bipartite_graph(entries, output_dir):
    ensure_output_dir(output_dir)

    registry_keys = []
    dropped_files = []

    for entry in entries:
        if entry.file_path:
            registry_keys.append(entry.reg_key)
            dropped_files.append(entry.file_path)

    if not registry_keys or not dropped_files:
        print("[!] No data to plot force bipartite graph.")
        return None

    unique_registry = list(set(registry_keys))
    unique_files = list(set(dropped_files))

    nodes = unique_registry + unique_files
    sources = [nodes.index(r) for r in registry_keys]
    targets = [nodes.index(f) for f in dropped_files]

    colors = ['red' if node in unique_registry else 'skyblue' for node in nodes]

    fig = go.Figure(data=[
        go.Sankey(
            arrangement='snap',
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=nodes,
                color=colors,
            ),
            link=dict(
                source=sources,
                target=targets,
                value=[1] * len(sources),
                color=["gray"] * len(sources),
            )
        )
    ])

    fig.update_layout(
        title_text="Force-directed Bipartite Graph: Registry Keys \u279e Dropped Files",
        font_size=10,
        height=900,
    )

    output_path = os.path.join(output_dir, 'persistence_force_bipartite.html')
    fig.write_html(output_path)
    print(f"[+] Saved interactive Force-directed Bipartite Graph to {output_path}")

    return output_path