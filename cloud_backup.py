import subprocess
import os
from datetime import datetime

def git_push(message):
    os.chdir('/home/netadmin/automation')
    subprocess.run(['git', 'add', '.'], check=True)
    result = subprocess.run(['git', 'diff', '--cached', '--quiet'])
    if result.returncode != 0:
        subprocess.run(['git', 'checkout', 'master'], check=False)
        subprocess.run(['git', 'commit', '-m', message], check=True)
        subprocess.run(['git', 'push', 'origin', 'master'], check=True)
        print(f"✅ Pushed to GitHub: {message}")
    else:
        print("ℹ️ Nothing new to push")

def backup_database():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    dump_file = f'/home/netadmin/automation/database/backup_{timestamp}.sql'
    os.makedirs('/home/netadmin/automation/database', exist_ok=True)
    subprocess.run([
        'mysqldump', '-u', 'netadmin', '-pcisco123', 'enterprise_network'
    ], stdout=open(dump_file, 'w'), check=True)
    print(f"✅ Database backed up: {dump_file}")
    return dump_file

if __name__ == '__main__':
    print("=" * 50)
    print("Cloud Backup — Enterprise Network")
    print(f"Time: {datetime.now()}")
    print("=" * 50)
    backup_database()
    git_push(f"chore: auto backup {datetime.now().strftime('%Y-%m-%d %H:%M')}")
