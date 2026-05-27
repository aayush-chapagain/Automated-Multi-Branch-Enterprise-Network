# Automated Multi-Branch Enterprise Network

> **Final Year Project — BSc. CSIT, Semester VII**  
> Lumbini City College, Tribhuvan University, Nepal — 2023–2027

---

## 👥 Team

| Name | Symbol No. | Role |
|---|---|---|
| Aayush Chapagain | 72012062 | Network Engineer & Automation |
| Sanchhep Raj Shrestha | 72012077 | Network Engineer & Documentation |

**Supervisor:** Mr. Kamal Bahadur Thapa  
**Department:** Computer Science and Information Technology  
**College:** Lumbini City College, Tilottama-04, Rupandehi, Nepal

---

## 📌 Project Overview

A production-grade **Automated Multi-Branch Enterprise Network** designed, manually configured, and validated in PNetLab using Cisco IOS virtual devices. The system integrates industry-standard routing protocols, IPsec VPN security, Python-based automation, graph-based shortest path algorithms, and a real-time Network Operations Center (NOC) dashboard.

```
3 Sites · 26 Cisco IOS Devices · 5 Python Scripts · 6 Dashboard Modules
```

---

## 🏗️ Network Architecture

```
┌─────────────────────────────────────────────────┐
│          ISP Cloud (OSPF Process 100)           │
│     ISP001 ── ISP002 ── ISP003 ── ISP004        │
└──────┬──────────────┬──────────────┬────────────┘
       │              │              │
  Branch A           HQ           Branch B
  (10.2.0.0/16)  (10.1.0.0/16)  (10.3.0.0/16)
  7 Devices        12 Devices      7 Devices
  A-CR1            HQ-CR1/CR2      B-CR1
  A-DSW1/2         HQ-DSW1~4       B-DSW1/2
  A-ASW1~4         HQ-ASW1~6       B-ASW1~4
```

**Three-tier hierarchical model:**
- **Core Layer** — OSPF, IPsec VPN, NAT/PAT, ACL, SSH
- **Distribution Layer** — HSRP v2, EtherChannel LACP, OSPF, DHCP Relay
- **Access Layer** — VLANs, 802.1Q Trunking, PortFast, BPDU Guard

---

## ⚙️ Protocols Configured (Manual CLI)

| Category | Protocols |
|---|---|
| Routing | OSPF Area 0 (Process 1 internal · Process 100 ISP) |
| Security | IPsec Site-to-Site VPN (AES-256 · SHA-256 · DH Group 14) |
| Redundancy | HSRP v2 (Priority 110/90) · EtherChannel LACP |
| Switching | VLANs 10/20/30/99 · 802.1Q Trunking · STP Rapid-PVST |
| Services | NAT/PAT · Extended ACL · DHCP · DHCP Relay · SSH v2 |
| Management | SNMP · Syslog (UDP 514) · PortFast · BPDU Guard |

---

## 🐍 Python Automation Scripts

| Script | Purpose | Schedule |
|---|---|---|
| `health_score.py` | Weighted health scoring — ICMP ping based (60% connectivity + 40% RTT) | Every 60s via cron |
| `dijkstra.py` | Shortest path algorithm O((V+E)logV) on network topology graph | On demand |
| `cloud_backup.py` | MySQL dump → GitHub push | Every 6hrs via cron |
| `backup_configs.py` | IOS config backup via Netmiko SSH | Auto + Manual |
| `app.py` | Flask REST API — 9 endpoints serving NOC dashboard | Always running |

---

## 📊 NOC Dashboard Modules

Access at: `http://10.1.10.50:5000`

| Module | Description |
|---|---|
| **Overview** | Live health scores, device counts, alerts, Network SLA, site health bar chart |
| **Command Center** | Browser-based SSH terminal — execute any IOS command on all 26 devices |
| **Path Analysis** | Interactive Dijkstra + Bellman-Ford with step-by-step trace and comparison |
| **Monitoring** | Device status donut charts, alert feed |
| **Syslog Viewer** | Real-time log stream from all devices — severity filter + search |
| **Config Backup** | MySQL backup list, GitHub sync status, manual backup trigger |

---

## 🗄️ Database Schema (MySQL)

Database: `enterprise_network`

| Table | Rows | Contents |
|---|---|---|
| `devices` | 26 | Device inventory — hostname, IP, type, site, status |
| `monitoring_logs` | 719+ | Health scores, path results, command logs |
| `alerts` | 403+ | Auto-generated critical alerts for offline devices |
| `config_backups` | 0 | IOS config backups (pending SSH reachability) |

---

## 🧪 Test Results

| Test Case | Result | Details |
|---|---|---|
| Cross-site ping HQ → Branch A | ✅ PASS | 5/5 · avg 6ms RTT |
| Cross-site ping HQ → Branch B | ✅ PASS | 5/5 · avg 5ms RTT |
| IPsec VPN failover | ✅ PASS | QM_IDLE ACTIVE within 15s |
| OSPF neighbor adjacency | ✅ PASS | All neighbors FULL/DR state |
| HSRP failover | ✅ PASS | Switchover within 10s |
| EtherChannel LACP | ✅ PASS | Port-channel1 bundled (P) |
| VLAN segmentation | ✅ PASS | VLANs 10/20/30/99 active |
| DHCP assignment | ✅ PASS | Correct IP per VLAN pool |
| Algorithm validation | ✅ PASS | Both algorithms identical |
| Health scoring | ✅ PASS | 100/100 all core devices |
| Syslog reception | ✅ PASS | Live events from HQ-CR1 |
| GitHub cloud backup | ✅ PASS | Auto push every 6 hours |
| NOC dashboard | ✅ PASS | All 6 modules functional |

**All 13 test cases passed — 100% success rate ✅**

---

## 📁 Repository Structure

```
Automated-Multi-Branch-Enterprise-Network/
├── app.py                    # Flask REST API (9 endpoints)
├── index.html                # NOC Dashboard frontend
├── health_score.py           # Weighted health scoring algorithm
├── dijkstra.py               # Dijkstra's shortest path algorithm
├── cloud_backup.py           # MySQL → GitHub auto backup
├── backup_configs.py         # IOS config backup via Netmiko
├── path_analysis_section.html # Path analysis module
├── configs/                  # Cisco IOS device configurations
├── database/                 # MySQL backup .sql files
│   └── backup_*.sql
├── diagrams/                 # Network topology and architecture diagrams
├── docs/                     # Final project report
└── pnetlab/                  # PNetLab topology files
```

---

## 🛠️ Tech Stack

```
Network    → Cisco IOS · PNetLab · vIOS · vIOS-L2
Protocols  → OSPF · IPsec · HSRP · EtherChannel · VLAN · NAT · ACL · SSH
Automation → Python 3.10 · Flask · Netmiko · Linux Cron · Git
Database   → MySQL 8.0 · PyMySQL
Monitoring → rsyslog · SNMP · ICMP · Chart.js
Server     → Ubuntu Server 22.04 LTS (10.1.10.50)
Tools      → VMware · MobaXterm · Wireshark · Draw.io
```

---

## 🚀 Setup and Run

### Prerequisites
- PNetLab with Cisco Router and Switch images
- Ubuntu Server 22.04 LTS
- Python 3.10+
- MySQL 8.0

### Installation

```bash
# Clone repository
git clone https://github.com/aayush-chapagain/Automated-Multi-Branch-Enterprise-Network.git
cd Automated-Multi-Branch-Enterprise-Network

# Install Python dependencies
pip install flask netmiko pymysql

# Setup MySQL database
mysql -u root -p < database/setup.sql

# Start NOC Dashboard
python3 app.py
```

### Setup Cron Jobs

```bash
# Edit crontab
crontab -e

# Add these lines
*/1 * * * * python3 /home/netadmin/automation/health_score.py
0 */6 * * * python3 /home/netadmin/automation/cloud_backup.py
```

### Configure Syslog on Cisco Devices

```cisco
logging host 10.1.10.50
logging trap informational
logging on
service timestamps log datetime msec
```

---

## 📈 IP Addressing Summary

| Site | Block | Devices |
|---|---|---|
| Headquarters | 10.1.0.0/16 | 12 |
| Branch A | 10.2.0.0/16 | 7 |
| Branch B | 10.3.0.0/16 | 7 |
| ISP Cloud | 100.0.0.0/8 | 4 |
| Leased Line HQ↔A | 10.0.12.0/30 | P2P |
| Leased Line HQ↔B | 10.0.13.0/30 | P2P |

---


## 👨‍💻 Authors

| Name | Symbol No. | GitHub | LinkedIn |
|---|---|---|---|
| Aayush Chapagain | 72012062 | [@aayush-chapagain](https://github.com/aayush-chapagain) | [Profile](https://linkedin.com/in/aayushchapagain) |
| Sanchhep Raj Shrestha | 72012077 | [@Decent-Aneraj](https://github.com/Decent-Aneraj) | [Profile](https://www.linkedin.com/in/sanchhep-shrestha-b7052237b/) |

---


---

## 📄 License

This project is submitted as a Final Year Project for academic evaluation at Lumbini City College, Tribhuvan University. All rights reserved by the authors.

---

## 🙏 Acknowledgement

Special thanks to **Mr. Kamal Bahadur Thapa** (Project Supervisor) for his continuous guidance and technical support throughout this project.

---

*Lumbini City College · Tribhuvan University · BSc. CSIT 2023–2027*
