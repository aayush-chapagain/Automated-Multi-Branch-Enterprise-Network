import subprocess
import pymysql
from datetime import datetime

class NetworkHealthAlgorithm:
    def __init__(self):
        self.db = pymysql.connect(
            host='localhost', user='netadmin',
            password='cisco123', database='enterprise_network'
        )
        self.weights = {
            'connectivity': 0.6,
            'response_time': 0.4
        }

    def ping_device(self, ip):
        try:
            result = subprocess.run(
                ['ping', '-c', '2', '-W', '1', ip],
                capture_output=True, timeout=5
            )
            if result.returncode == 0:
                output = result.stdout.decode()
                for line in output.split('\n'):
                    if 'avg' in line:
                        avg_time = float(line.split('/')[4])
                        return True, avg_time
                return True, 0
            return False, 0
        except:
            return False, 0

    def calculate_health_score(self, ip):
        reachable, response_time = self.ping_device(ip)
        if not reachable:
            return 0

        connectivity_score = 100
        if response_time < 10:
            response_score = 100
        elif response_time < 50:
            response_score = 80
        elif response_time < 100:
            response_score = 60
        else:
            response_score = 40

        health = (connectivity_score * self.weights['connectivity'] +
                 response_score * self.weights['response_time'])
        return round(health, 2)

    def save_to_db(self, device_id, score, status):
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO monitoring_logs (device_id, metric_type, metric_value)
            VALUES (%s, 'health_score', %s)
        """, (device_id, str(score)))

        severity = 'critical' if score == 0 else 'warning' if score < 70 else 'info'
        if score < 70:
            cursor.execute("""
                INSERT INTO alerts (device_id, alert_type, message, severity)
                VALUES (%s, 'health', %s, %s)
            """, (device_id, f'Health score: {score}', severity))
        self.db.commit()

    def run(self):
        print("=" * 60)
        print("Enterprise Network Health Score Algorithm")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        cursor = self.db.cursor()
        cursor.execute("SELECT id, hostname, ip_address, site FROM devices")
        devices = cursor.fetchall()

        site_scores = {'HQ': [], 'BranchA': [], 'BranchB': []}

        for device in devices:
            device_id, hostname, ip, site = device
            score = self.calculate_health_score(ip)
            status = 'active' if score > 0 else 'offline'

            cursor.execute("""
                UPDATE devices SET status=%s WHERE id=%s
            """, (status, device_id))

            self.save_to_db(device_id, score, status)

            icon = '✅' if score >= 70 else '⚠️' if score > 0 else '❌'
            print(f"{icon} {hostname:10} | {ip:15} | Score: {score:6}/100 | {status}")

            if site in site_scores:
                site_scores[site].append(score)

        self.db.commit()

        print("\n" + "=" * 60)
        print("SITE HEALTH SUMMARY")
        print("=" * 60)
        for site, scores in site_scores.items():
            if scores:
                avg = round(sum(scores) / len(scores), 2)
                print(f"{site:10}: {avg}/100")

        print("\n✅ Health scores saved to MySQL!")

if __name__ == '__main__':
    health = NetworkHealthAlgorithm()
    health.run()
