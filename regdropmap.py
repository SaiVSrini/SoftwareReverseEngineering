
import argparse
import os
import webbrowser
from utils.parser import parse_regshot_diff
from utils.analyzer import analyze_registry_entries
from utils.visualizer import (
    plot_flag_frequency,
    plot_suspicious_folder_pie,
    plot_persistence_graph,
    plot_persistence_sankey,
    plot_persistence_hive,
    plot_force_bipartite_graph 
)

def main():
    parser = argparse.ArgumentParser(description="Registry Dropper Tracker Tool")
    parser.add_argument('-i', '--input', required=True, help='Path to RegShot diff.txt file')
    parser.add_argument('-o', '--output', default='output', help='Output directory to save results')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')  # Added verbose flag
    args = parser.parse_args()

    if args.verbose:
        print("[+] Verbose mode enabled.")

    print("[+] Parsing RegShot diff...")
    entries = parse_regshot_diff(args.input)
    print(f"[+] {len(entries)} registry entries found.")

    print("[+] Analyzing entries...")
    entries = analyze_registry_entries(entries)

    print("[+] Generating visualizations...")
    plot_flag_frequency(entries, args.output)
    plot_suspicious_folder_pie(entries, args.output)
    plot_persistence_graph(entries, args.output)
    sankey_path = plot_persistence_sankey(entries, args.output)
    plot_persistence_hive(entries, args.output)
    plot_force_bipartite_graph(entries, args.output)


    # Automatically open the sankey HTML if it exists
    if sankey_path and os.path.exists(sankey_path):
        print(f"[+] Opening Sankey Diagram: {sankey_path}")
        webbrowser.open(f"file://{os.path.abspath(sankey_path)}")

    print("[+] Done.")

# after plotting Force Bipartite Graph
    bipartite_path = plot_force_bipartite_graph(entries, args.output)
    if bipartite_path:
        print(f"[+] Opening Force-directed Bipartite Graph: {bipartite_path}")
        webbrowser.open('file://' + os.path.realpath(bipartite_path))

if __name__ == "__main__":
    main()
