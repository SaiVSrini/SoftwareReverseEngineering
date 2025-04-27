# SoftwareReverseEngineering
📖 What is RegDropMap?

RegDropMap is a lightweight forensic tool that parses RegShot diff files, identifies registry-based persistence mechanisms, and visualizes dropped file paths linked to registry keys.

	It is designed to help:
	
	🕵️ Forensic analysts
	
	🛡️ Malware researchers
	
	🔒 Security professionals
accomplish the following:

	✅ Detect suspicious persistence techniques
	✅ Map malware’s registry-to-file behaviors
	✅ Identify dropped files in unusual or hidden locations (like %Temp%, %AppData%, etc.)
	✅ Automate tedious manual analysis of large diff.txt registry files

⚡ Features
Real-world log compatibility — Robust parsing of messy RegShot outputs

Automatic Flagging — Highlights suspicious behaviors (e.g., Suspicious Folder, Incomplete Path)

Visualizations — Generate clear and insightful:

	📊 Flag frequency charts
	
	🥧 Folder-based risk pie charts
	
	🔗 Interactive Sankey diagrams (Registry ➔ Dropped File flow)
	
	🕸️ Network graphs of persistence links

Extensible & Scriptable — Modular structure for easy upgrades
