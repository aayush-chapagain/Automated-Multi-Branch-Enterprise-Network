from netmiko import ConnectHandler
import pymysql
from datetime import datetime

class ConfigBackupAlgorithm:
    def __init__(self):
        self.db = pymysql.connect(
            host='localhost', user='netadmin',
            password='cisco123', database='enterprise_network'
        )
        self.credentials = {
            'username': 'admin',
            'password': 'cisco123',
            'secret': 'cisco123'
        }

    def backup_device(self, device_id, hostname, ip, device_type):
        try:
            device_type_netmiko = 'cisco_ios'
            connection = ConnectHandler(
                device_type=device_type_netmiko,
                host=ip,
                username=self.credentials['username'],
                password=self.credentials['password'],
                secret=self.credentials['secret'],
                timeout=10
            )
            connection.enable()
            config = connection.send_command('show running-config')
            connection.disconnect()

            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO config_backups (device_id, config_text)
                VALUES (%s, %s)
            """, (device_id, config))
            self.db.commit()

            print(f"✅ {hostname:10} ({ip:15}) - Backup successful")
            return True

        except Exception as e:
            print(f"❌ {hostname:10} ({ip:15}) - Failed: {str(e)[:50]}")
            return False

    def run(self):
        print("=" * 60)
        print("Network Configuration Backup Algorithm")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        cursor = self.db.cursor()
        cursor.execute("SELECT id, hostname, ip_address, device_type FROM devices")
        devices = cursor.fetchall()

        success = 0
        failed = 0

        for device in devices:
            device_id, hostname, ip, device_type = device
            result = self.backup_device(device_id, hostname, ip, device_type)
            if result:
                success += 1
            else:
                failed += 1

        print("\n" + "=" * 60)
        print(f"✅ Successful backups: {success}")
        print(f"❌ Failed backups   : {failed}")
        print(f"📊 Total devices    : {success + failed}")
        print("=" * 60)

if __name__ == '__main__':
    backup = ConfigBackupAlgorithm()
    backup.run()
