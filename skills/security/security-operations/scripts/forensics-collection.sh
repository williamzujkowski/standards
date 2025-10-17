#!/bin/bash
###############################################################################
# Linux Forensics Evidence Collection Script
# Purpose: Automate collection of forensic evidence from compromised Linux systems
# Usage: sudo ./forensics-collection.sh [output_directory]
# Version: 1.0.0
# NIST: IR-4 (Incident Handling)
###############################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
HOSTNAME=$(hostname)
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
OUTPUT_DIR="${1:-/mnt/evidence/${HOSTNAME}-${TIMESTAMP}}"
EVIDENCE_LOG="${OUTPUT_DIR}/collection.log"

###############################################################################
# Helper Functions
###############################################################################

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$EVIDENCE_LOG"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$EVIDENCE_LOG"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$EVIDENCE_LOG"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
       error "This script must be run as root (sudo)"
       exit 1
    fi
}

###############################################################################
# Main Functions
###############################################################################

initialize() {
    log "=== Linux Forensics Evidence Collection ==="
    log "Hostname: $HOSTNAME"
    log "Timestamp: $TIMESTAMP"
    log "Output Directory: $OUTPUT_DIR"
    
    mkdir -p "$OUTPUT_DIR"/{memory,disk,logs,network,processes,files,artifacts}
    
    log "Directory structure created"
}

collect_chain_of_custody() {
    log "Creating chain of custody documentation"
    
    cat > "${OUTPUT_DIR}/chain-of-custody.txt" << EOL
CHAIN OF CUSTODY

Case Information:
  Hostname: $HOSTNAME
  Collection Date: $(date)
  Collected By: $(whoami)
  Collection Script: $0
  Collection Hash (script): $(sha256sum "$0" | awk '{print $1}')

Evidence Items:
  - Memory dump
  - Disk image
  - System logs
  - Process listings
  - Network connections
  - File artifacts

Collection Method:
  Automated forensic collection script following NIST 800-86 guidelines

Notes:
  All evidence hashed with SHA256 for integrity verification
  System state preserved at time of collection

Investigator Signature: _______________________
Date: $(date)
EOL
    
    log "Chain of custody document created"
}

collect_memory() {
    log "Collecting memory dump (this may take several minutes)"
    
    # Check for LiME kernel module
    if [[ -f "/lib/modules/$(uname -r)/kernel/drivers/lime.ko" ]]; then
        insmod "/lib/modules/$(uname -r)/kernel/drivers/lime.ko" \
            "path=${OUTPUT_DIR}/memory/memory.lime" "format=lime"
        log "Memory captured using LiME"
    else
        warning "LiME module not found. Attempting alternative methods."
        
        # Alternative: Use /proc/kcore (may not be available)
        if [[ -r /proc/kcore ]]; then
            dd if=/proc/kcore of="${OUTPUT_DIR}/memory/memory-kcore.raw" bs=4M
            log "Memory captured using /proc/kcore"
        else
            warning "Unable to capture memory. Install LiME for full memory capture."
        fi
    fi
    
    # Hash memory dump
    if [[ -f "${OUTPUT_DIR}/memory/memory.lime" ]]; then
        sha256sum "${OUTPUT_DIR}/memory/memory.lime" > "${OUTPUT_DIR}/memory/memory.lime.sha256"
    fi
}

collect_system_info() {
    log "Collecting system information"
    
    local INFO_DIR="${OUTPUT_DIR}/artifacts/system-info"
    mkdir -p "$INFO_DIR"
    
    # Basic system info
    uname -a > "${INFO_DIR}/uname.txt"
    hostnamectl > "${INFO_DIR}/hostnamectl.txt" 2>/dev/null || true
    cat /etc/os-release > "${INFO_DIR}/os-release.txt" 2>/dev/null || true
    uptime > "${INFO_DIR}/uptime.txt"
    date > "${INFO_DIR}/date.txt"
    
    # Hardware info
    lscpu > "${INFO_DIR}/lscpu.txt" 2>/dev/null || true
    lspci > "${INFO_DIR}/lspci.txt" 2>/dev/null || true
    lsusb > "${INFO_DIR}/lsusb.txt" 2>/dev/null || true
    
    # Disk info
    df -h > "${INFO_DIR}/df.txt"
    mount > "${INFO_DIR}/mount.txt"
    fdisk -l > "${INFO_DIR}/fdisk.txt" 2>/dev/null || true
    
    log "System information collected"
}

collect_processes() {
    log "Collecting process information"
    
    local PROC_DIR="${OUTPUT_DIR}/processes"
    
    ps auxwww > "${PROC_DIR}/ps-aux.txt"
    ps -ef > "${PROC_DIR}/ps-ef.txt"
    pstree -p > "${PROC_DIR}/pstree.txt"
    top -b -n 1 > "${PROC_DIR}/top.txt"
    
    # Process details
    mkdir -p "${PROC_DIR}/proc-details"
    for pid in /proc/[0-9]*; do
        if [[ -d "$pid" ]]; then
            pid_num=$(basename "$pid")
            {
                echo "=== PID $pid_num ==="
                cat "$pid/cmdline" 2>/dev/null | tr '\0' ' ' || true
                echo ""
                ls -l "$pid/exe" 2>/dev/null || true
                ls -l "$pid/cwd" 2>/dev/null || true
                cat "$pid/environ" 2>/dev/null | tr '\0' '\n' || true
            } > "${PROC_DIR}/proc-details/${pid_num}.txt"
        fi
    done
    
    log "Process information collected"
}

collect_network() {
    log "Collecting network information"
    
    local NET_DIR="${OUTPUT_DIR}/network"
    
    # Network connections
    netstat -anp > "${NET_DIR}/netstat-anp.txt" 2>/dev/null || ss -anp > "${NET_DIR}/ss-anp.txt"
    lsof -i > "${NET_DIR}/lsof-network.txt" 2>/dev/null || true
    
    # Network configuration
    ip addr show > "${NET_DIR}/ip-addr.txt"
    ip route show > "${NET_DIR}/ip-route.txt"
    iptables -L -n -v > "${NET_DIR}/iptables.txt" 2>/dev/null || true
    
    # DNS
    cat /etc/resolv.conf > "${NET_DIR}/resolv.conf" 2>/dev/null || true
    cat /etc/hosts > "${NET_DIR}/hosts" 2>/dev/null || true
    
    # ARP cache
    ip neigh show > "${NET_DIR}/arp.txt" 2>/dev/null || arp -a > "${NET_DIR}/arp.txt"
    
    log "Network information collected"
}

collect_logs() {
    log "Collecting system logs"
    
    local LOGS_DIR="${OUTPUT_DIR}/logs"
    
    # Copy main log directories
    rsync -av --ignore-errors /var/log/ "${LOGS_DIR}/var-log/" 2>/dev/null || \
        cp -r /var/log "${LOGS_DIR}/var-log" 2>/dev/null || true
    
    # Journal logs (systemd)
    if command -v journalctl &> /dev/null; then
        journalctl --no-pager > "${LOGS_DIR}/journalctl-all.txt" 2>/dev/null || true
        journalctl --no-pager --priority=3 > "${LOGS_DIR}/journalctl-errors.txt" 2>/dev/null || true
    fi
    
    # Auth logs
    cat /var/log/auth.log > "${LOGS_DIR}/auth.log" 2>/dev/null || \
        cat /var/log/secure > "${LOGS_DIR}/secure" 2>/dev/null || true
    
    # Syslog
    cat /var/log/syslog > "${LOGS_DIR}/syslog" 2>/dev/null || \
        cat /var/log/messages > "${LOGS_DIR}/messages" 2>/dev/null || true
    
    log "System logs collected"
}

collect_user_artifacts() {
    log "Collecting user artifacts"
    
    local USER_DIR="${OUTPUT_DIR}/artifacts/users"
    mkdir -p "$USER_DIR"
    
    # User accounts
    cp /etc/passwd "${USER_DIR}/passwd"
    cp /etc/shadow "${USER_DIR}/shadow" 2>/dev/null || true
    cp /etc/group "${USER_DIR}/group"
    
    # Login history
    last -Faixw > "${USER_DIR}/last.txt"
    lastlog > "${USER_DIR}/lastlog.txt"
    w > "${USER_DIR}/w.txt"
    who > "${USER_DIR}/who.txt"
    
    # Command history
    for home_dir in /home/*; do
        if [[ -d "$home_dir" ]]; then
            username=$(basename "$home_dir")
            mkdir -p "${USER_DIR}/${username}"
            
            cp "${home_dir}/.bash_history" "${USER_DIR}/${username}/bash_history" 2>/dev/null || true
            cp "${home_dir}/.zsh_history" "${USER_DIR}/${username}/zsh_history" 2>/dev/null || true
            cp "${home_dir}/.viminfo" "${USER_DIR}/${username}/viminfo" 2>/dev/null || true
            
            # SSH keys and config
            if [[ -d "${home_dir}/.ssh" ]]; then
                cp -r "${home_dir}/.ssh" "${USER_DIR}/${username}/ssh" 2>/dev/null || true
            fi
        fi
    done
    
    log "User artifacts collected"
}

collect_persistence() {
    log "Collecting persistence mechanisms"
    
    local PERSIST_DIR="${OUTPUT_DIR}/artifacts/persistence"
    mkdir -p "$PERSIST_DIR"
    
    # Cron jobs
    crontab -l > "${PERSIST_DIR}/root-crontab.txt" 2>/dev/null || echo "No crontab" > "${PERSIST_DIR}/root-crontab.txt"
    cp /etc/crontab "${PERSIST_DIR}/etc-crontab" 2>/dev/null || true
    cp -r /etc/cron.d "${PERSIST_DIR}/cron.d" 2>/dev/null || true
    cp -r /etc/cron.daily "${PERSIST_DIR}/cron.daily" 2>/dev/null || true
    cp -r /etc/cron.hourly "${PERSIST_DIR}/cron.hourly" 2>/dev/null || true
    
    # Systemd services
    systemctl list-units --type=service > "${PERSIST_DIR}/systemd-services.txt" 2>/dev/null || true
    cp -r /etc/systemd/system "${PERSIST_DIR}/systemd-system" 2>/dev/null || true
    
    # Init scripts
    ls -la /etc/init.d > "${PERSIST_DIR}/init.d-listing.txt" 2>/dev/null || true
    
    # Startup scripts
    cp /etc/rc.local "${PERSIST_DIR}/rc.local" 2>/dev/null || true
    cp /etc/profile "${PERSIST_DIR}/profile" 2>/dev/null || true
    
    log "Persistence mechanisms collected"
}

collect_suspicious_files() {
    log "Collecting suspicious files and indicators"
    
    local FILES_DIR="${OUTPUT_DIR}/files"
    
    # Recently modified files
    find / -type f -mtime -7 2>/dev/null | head -1000 > "${FILES_DIR}/recent-files.txt" || true
    
    # SUID/SGID files
    find / -type f \( -perm -4000 -o -perm -2000 \) -ls 2>/dev/null > "${FILES_DIR}/suid-sgid-files.txt" || true
    
    # World-writable files
    find / -type f -perm -002 -ls 2>/dev/null | head -500 > "${FILES_DIR}/world-writable-files.txt" || true
    
    # Temporary directories
    ls -laR /tmp > "${FILES_DIR}/tmp-listing.txt" 2>/dev/null || true
    ls -laR /var/tmp > "${FILES_DIR}/var-tmp-listing.txt" 2>/dev/null || true
    
    # Web server directories (if present)
    if [[ -d /var/www ]]; then
        find /var/www -type f -name "*.php" -mtime -30 2>/dev/null > "${FILES_DIR}/recent-web-files.txt" || true
    fi
    
    log "Suspicious files collected"
}

create_hashes() {
    log "Creating integrity hashes for all collected evidence"
    
    find "$OUTPUT_DIR" -type f ! -name "*.sha256" -exec sha256sum {} \; > "${OUTPUT_DIR}/evidence-hashes.txt"
    
    log "Integrity hashes created: ${OUTPUT_DIR}/evidence-hashes.txt"
}

create_report() {
    log "Creating collection report"
    
    cat > "${OUTPUT_DIR}/COLLECTION_REPORT.txt" << EOL
FORENSIC EVIDENCE COLLECTION REPORT

System Information:
  Hostname: $HOSTNAME
  Collection Time: $TIMESTAMP
  Kernel: $(uname -r)
  OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)
  Uptime: $(uptime)

Evidence Collected:
  - Memory dump: $(du -h "${OUTPUT_DIR}/memory" | tail -1 | awk '{print $1}')
  - Logs: $(du -h "${OUTPUT_DIR}/logs" | tail -1 | awk '{print $1}')
  - Processes: $(wc -l < "${OUTPUT_DIR}/processes/ps-aux.txt") processes captured
  - Network connections: $(wc -l < "${OUTPUT_DIR}/network/netstat-anp.txt" 2>/dev/null || echo "0") connections
  - User artifacts: $(ls -1 "${OUTPUT_DIR}/artifacts/users" | wc -l) users
  - Persistence mechanisms: Collected from cron, systemd, init
  
Total Evidence Size: $(du -sh "$OUTPUT_DIR" | awk '{print $1}')

Integrity Verification:
  All evidence files hashed with SHA256
  Hash list: ${OUTPUT_DIR}/evidence-hashes.txt

Collection Log:
  ${EVIDENCE_LOG}

Chain of Custody:
  ${OUTPUT_DIR}/chain-of-custody.txt

Next Steps:
  1. Transfer evidence to secure storage
  2. Verify all file hashes
  3. Begin forensic analysis with Autopsy or FTK
  4. Document findings in incident report

Collected by: $(whoami)
Collection completed: $(date)
EOL
    
    log "Collection report created: ${OUTPUT_DIR}/COLLECTION_REPORT.txt"
}

###############################################################################
# Main Execution
###############################################################################

main() {
    check_root
    initialize
    collect_chain_of_custody
    
    log "Starting evidence collection..."
    
    collect_system_info
    collect_processes
    collect_network
    collect_logs
    collect_user_artifacts
    collect_persistence
    collect_suspicious_files
    
    # Memory collection last (most intrusive)
    collect_memory
    
    create_hashes
    create_report
    
    log "=== Collection Complete ==="
    log "Evidence location: $OUTPUT_DIR"
    log "Total size: $(du -sh "$OUTPUT_DIR" | awk '{print $1}')"
    log ""
    log "Next steps:"
    log "  1. Copy evidence to secure storage:"
    log "     rsync -av --progress $OUTPUT_DIR /mnt/forensic-storage/"
    log ""
    log "  2. Verify integrity:"
    log "     cd $OUTPUT_DIR && sha256sum -c evidence-hashes.txt"
    log ""
    log "  3. Begin analysis with Volatility (memory):"
    log "     volatility -f ${OUTPUT_DIR}/memory/memory.lime --profile=LinuxUbuntu2004x64 linux_pslist"
}

main "$@"
