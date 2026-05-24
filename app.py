from flask import Flask, jsonify, request, render_template_string
import pymysql
from datetime import datetime

app = Flask(__name__)

def db():
    return pymysql.connect(host='localhost', user='netadmin',
        password='cisco123', database='enterprise_network',
        cursorclass=pymysql.cursors.DictCursor)

def query(sql, args=None):
    conn = db()
    cur = conn.cursor()
    cur.execute(sql, args or ())
    rows = cur.fetchall()
    conn.close()
    return rows

def query_one(sql, args=None):
    conn = db()
    cur = conn.cursor()
    cur.execute(sql, args or ())
    row = cur.fetchone()
    conn.close()
    return row

def execute(sql, args=None):
    conn = db()
    cur = conn.cursor()
    cur.execute(sql, args or ())
    conn.commit()
    conn.close()

# ── API ROUTES ──────────────────────────────────────────────

@app.route('/api/stats')
def api_stats():
    total = query_one("SELECT COUNT(*) as c FROM devices")['c']
    online = query_one("SELECT COUNT(*) as c FROM devices WHERE status='active'")['c']
    offline = query_one("SELECT COUNT(*) as c FROM devices WHERE status='offline'")['c']
    alerts = query_one("SELECT COUNT(*) as c FROM alerts")['c']
    backups = query_one("SELECT COUNT(*) as c FROM config_backups")['c']
    return jsonify(total=total, online=online, offline=offline, alerts=alerts, backups=backups)

@app.route('/api/devices')
def api_devices():
    rows = query("SELECT * FROM devices ORDER BY site, hostname")
    for r in rows:
        r['created_at'] = str(r['created_at'])
    return jsonify(rows)

@app.route('/api/alerts')
def api_alerts():
    rows = query("""SELECT d.hostname, a.alert_type, a.message, a.severity, a.created_at
        FROM alerts a JOIN devices d ON a.device_id=d.id
        ORDER BY a.created_at DESC LIMIT 20""")
    for r in rows:
        r['created_at'] = str(r['created_at'])
    return jsonify(rows)

@app.route('/api/paths')
def api_paths():
    rows = query("""SELECT d.hostname, ml.metric_type, ml.metric_value, ml.logged_at
        FROM monitoring_logs ml JOIN devices d ON ml.device_id=d.id
        WHERE ml.metric_type LIKE 'path_%'
        ORDER BY ml.logged_at DESC LIMIT 5""")
    for r in rows:
        r['logged_at'] = str(r['logged_at'])
    return jsonify(rows)

@app.route('/api/site_health')
def api_site_health():
    rows = query("""SELECT d.site, AVG(CAST(ml.metric_value AS DECIMAL(10,2))) as avg_score
        FROM monitoring_logs ml JOIN devices d ON ml.device_id=d.id
        WHERE ml.metric_type='health_score' GROUP BY d.site""")
    result = {'HQ': 0, 'BranchA': 0, 'BranchB': 0}
    for r in rows:
        result[r['site']] = round(float(r['avg_score']), 1)
    return jsonify(result)

@app.route('/api/site_summary')
def api_site_summary():
    result = []
    for key, name, total in [('HQ','Headquarters',12),('BranchA','Branch A',7),('BranchB','Branch B',7)]:
        online = query_one("SELECT COUNT(*) as c FROM devices WHERE site=%s AND status='active'", (key,))['c']
        offline = query_one("SELECT COUNT(*) as c FROM devices WHERE site=%s AND status='offline'", (key,))['c']
        result.append({'key':key,'name':name,'total':total,'online':online,'offline':offline})
    return jsonify(result)

@app.route('/api/command', methods=['POST'])
def api_command():
    data = request.json
    device_id = data.get('device_id')
    command = data.get('command')
    ip = data.get('ip')
    execute("INSERT INTO monitoring_logs (device_id, metric_type, metric_value) VALUES (%s,'command',%s)",
        (device_id, command))
    try:
        from netmiko import ConnectHandler
        conn = ConnectHandler(device_type='cisco_ios', host=ip,
            username='admin', password='cisco123', secret='cisco123', timeout=10)
        conn.enable()
        output = conn.send_command(command)
        conn.disconnect()
        return jsonify(success=True, output=output)
    except Exception as e:
        return jsonify(success=False, output=str(e))

@app.route('/api/cmd_history')
def api_cmd_history():
    rows = query("""SELECT ml.metric_value, ml.logged_at, d.hostname
        FROM monitoring_logs ml JOIN devices d ON ml.device_id=d.id
        WHERE ml.metric_type='command' ORDER BY ml.logged_at DESC LIMIT 15""")
    for r in rows:
        r['logged_at'] = str(r['logged_at'])
    return jsonify(rows)

@app.route('/api/backups')
def api_backups():
    rows = query("""SELECT id, hostname, backup_date, LENGTH(config_text) as size
        FROM config_backups ORDER BY backup_date DESC LIMIT 10""")
    for r in rows:
        r['backup_date'] = str(r['backup_date'])
    return jsonify(rows)

# ── MAIN PAGE ──────────────────────────────────────────────

@app.route('/')
def index():
    return render_template_string(HTML)

HTML = open('/home/netadmin/automation/index.html').read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
