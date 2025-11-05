# app.py
from flask import Flask, request, redirect, Response
from datetime import datetime, timedelta
import os, time, threading, json, queue
from werkzeug.middleware.proxy_fix import ProxyFix
from urllib import request as urlrequest
from urllib.error import URLError, HTTPError
import random

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# ------------ API documentation route ------------
@app.route('/')
def api_documentation():
    """API documentation home page"""
    return "Hello! This is the TV Scraper API. Try <a href='/now-playing'>/now-playing</a> or <a href='/health'>/health</a>"

@app.route('/test')
def test_route():
    """Simple test route"""
    return "Test route works!"

@app.route('/refresh')
def refresh_now_playing():
    """Force refresh the now-playing data"""
    global now_playing
    now_playing = get_current_or_next_today_slim()
    return Response(json.dumps({
        "message": "Now playing data refreshed",
        "count": len(now_playing),
        "programs": now_playing
    }, ensure_ascii=False, indent=2), mimetype="application/json")

# ------------ simple health endpoints ------------
@app.route('/health')
def health_check():
    """Basic health check endpoint"""
    return Response(json.dumps({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "tv-scraper-api"
    }, ensure_ascii=False), mimetype="application/json")

@app.route('/status')
def status():
    """Service status summary"""
    try:
        stats = {"database": "not_found"}
        
        # Try to get basic stats if database exists
        db_path = os.getenv('DB_PATH', '/app/data/tvguide.db')
        if os.path.exists(db_path):
            stats = {
                "database": "connected",
                "channels": ["BBC Earth", "Discovery Channel", "National Geographic"],
                "last_check": datetime.now().isoformat()
            }
        
        return Response(json.dumps({
            "service": "TV Program Scraper API",
            "version": "1.0.0",
            "status": "operational",
            "timestamp": datetime.now().isoformat(),
            "stats": stats
        }, ensure_ascii=False), mimetype="application/json")
        
    except Exception as e:
        return Response(json.dumps({
            "service": "TV Program Scraper API",
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }, ensure_ascii=False), status=500, mimetype="application/json")

# ------------ data sources ------------
FILES = ["tv_programs_Disc.txt", "tv_programs_BBC.txt", "tv_programs_NatGeo.txt"]

# ------------ in-memory state ------------
now_playing = []     # list of {channel, title, start, date, csfd_id}
latest_viewers = []  # list of {channel, viewers} (viewers as string)

# Per-channel smoothed viewer state (float) + timestamp
_viewer_state = {}     # {"Discovery Channel": 3123.0, "BBC Earth": 2875.0, ...}
_viewer_state_ts = {}  # {"Discovery Channel": datetime(...), ...}

# ------------ https redirect (optional) ------------
FORCE_HTTPS = os.getenv("FORCE_HTTPS", "1") == "1"

@app.before_request
def _force_https():
    if getattr(app, "_ssl_enabled", False) and FORCE_HTTPS:
        proto = request.headers.get("X-Forwarded-Proto", request.scheme)
        if proto != "https":
            url = request.url.replace("http://", "https://", 1)
            return redirect(url, code=301)

# ------------ parsing helpers ------------
def parse_programs(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    blocks = content.strip().split('----------------------------------------')
    programs = []
    for block in blocks:
        lines = block.strip().split('\n')
        record = {}
        for line in lines:
            if ': ' in line:
                key, value = line.split(': ', 1)
                record[key.strip()] = value.strip()
        if record:
            programs.append(record)
    return programs

def _as_dt(date_str, hm_str):
    if not date_str or not hm_str:
        return None
    try:
        d = datetime.strptime(date_str, '%d.%m.%Y').date()
        t = datetime.strptime(hm_str, '%H:%M').time()
        return datetime.combine(d, t)
    except ValueError:
        return None

def _channel_name_from_file(filename: str) -> str:
    base = os.path.splitext(os.path.basename(filename))[0]  # tv_programs_Disc
    short = base.replace("tv_programs_", "")
    mapping = {
        "Disc": "Discovery Channel",
        "BBC": "BBC Earth",
        "NatGeo": "National Geographic",
    }
    return mapping.get(short, short)

# ------------ selection (programs for today) ------------
def get_current_or_next_today_slim():
    import sqlite3
    
    now = datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    current_time = now.strftime('%H:%M:%S')
    
    db_path = os.getenv('DB_PATH', '/app/data/tvguide.db')
    if not os.path.exists(db_path):
        return []
    
    result = []
    try:
        conn = sqlite3.connect(db_path)
        
        # Get channels
        cursor = conn.execute("SELECT DISTINCT channel FROM program_info")
        channels = [row[0] for row in cursor.fetchall()]
        
        for channel in channels:
            # Query for current programs
            query = '''
                SELECT pi.title, pi.channel, ps.start_time, ps.end_time, ps.air_date
                FROM program_info pi
                JOIN program_schedule ps ON pi.id = ps.program_id
                WHERE ps.air_date = ? 
                  AND pi.channel = ?
                  AND ps.start_time <= ? 
                  AND ps.end_time > ?
                ORDER BY ps.start_time
                LIMIT 1
            '''
            
            cursor = conn.execute(query, (today_str, channel, current_time, current_time))
            current_result = cursor.fetchone()
            
            if current_result:
                program = {
                    'channel': current_result[1],
                    'title': current_result[0], 
                    'start': current_result[2],
                    'date': today_str,
                    'csfd_id': ''
                }
                result.append(program)
            else:
                # If no current program, find next program
                next_query = '''
                    SELECT pi.title, pi.channel, ps.start_time, ps.end_time, ps.air_date
                    FROM program_info pi
                    JOIN program_schedule ps ON pi.id = ps.program_id
                    WHERE ps.air_date = ? 
                      AND pi.channel = ?
                      AND ps.start_time > ?
                    ORDER BY ps.start_time
                    LIMIT 1
                '''
                
                cursor = conn.execute(next_query, (today_str, channel, current_time))
                next_result = cursor.fetchone()
                
                if next_result:
                    program = {
                        'channel': next_result[1],
                        'title': next_result[0], 
                        'start': next_result[2],
                        'date': today_str,
                        'csfd_id': ''
                    }
                    result.append(program)
        
        conn.close()
    except Exception as e:
        print(f"Database error in get_current_or_next_today_slim: {e}")
        return []
    
    return result

# ------------ subscriptions infra (SSE + webhooks) ------------
_sse_clients = set()
_sse_lock = threading.Lock()
_webhook_urls = set()
_webhook_lock = threading.Lock()

def _broadcast_to_subscribers(payload):
    data_str = json.dumps(payload, ensure_ascii=False)

    # SSE queues
    with _sse_lock:
        dead = []
        for q in _sse_clients:
            try:
                q.put_nowait(data_str)
            except Exception:
                dead.append(q)
        for q in dead:
            _sse_clients.discard(q)

    # Webhooks (fire-and-forget)
    def _post_webhooks(body: bytes):
        with _webhook_lock:
            urls = list(_webhook_urls)
        for url in urls:
            try:
                req = urlrequest.Request(
                    url=url,
                    data=body,
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                urlrequest.urlopen(req, timeout=5)
            except (HTTPError, URLError, TimeoutError):
                pass

    threading.Thread(target=_post_webhooks, args=(data_str.encode("utf-8"),), daemon=True).start()

# ------------ server-side config ------------
CONFIG = {
    # Update cadence
    "VIEWERS_INTERVAL_SEC": 15,
    # hard bounds for viewers
    "BASELINE_MIN": 2000,
    "BASELINE_MAX": 5000,
    # smoothing
    "SMOOTH_ALPHA": 0.35,
    # SSE ping (0 disables)
    "SSE_KEEPALIVE_SEC": 0,
}

# Hour-of-day weights (local time): (lo, hi, multiplier)
HOUR_BANDS_V2 = [
    (20, 22, 1.85),  # prime peak
    (18, 20, 1.55),  # early prime
    (22, 24, 1.30),  # late evening
    (8,  18, 1.15),  # daytime
    (6,   8, 1.00),  # shoulder
    (0,   2, 0.75),  # after midnight
    (2,   4, 0.55),  # deep night trough
    (4,   6, 0.70),  # very early morning
]

# Per-program popularity (keywords → multiplier).
POPULAR_SHOW_KEYWORDS = {
    # strong boosters
    "avengers": 1.35, "planet earth": 1.30, "frozen planet": 1.28,
    "shark week": 1.30, "apollo": 1.25, "cosmos": 1.25,
    # mild boosters
    "premiere": 1.20, "finale": 1.22, "live": 1.18, "special": 1.15,
}
UNPOPULAR_SHOW_KEYWORDS = {
    "rerun": 0.88, "repeat": 0.90, "marathon": 0.92,
    "behind the scenes": 0.92, "recap": 0.90, "infomercial": 0.80,
}

def _hour_factor_v2(h: int) -> float:
    for lo, hi, f in HOUR_BANDS_V2:
        if lo <= h < hi:
            return f
    return 1.0

def _popularity_factor(title: str | None) -> float:
    """Heuristic multiplier from program title (case-insensitive)."""
    if not title:
        return 1.0
    t = title.lower()
    best = 1.0
    for k, m in POPULAR_SHOW_KEYWORDS.items():
        if k in t:
            best = max(best, m)
    for k, m in UNPOPULAR_SHOW_KEYWORDS.items():
        if k in t:
            best = min(best, m)
    return best

def _clamp_delta_per_tick(prev: float | None, prev_ts: datetime | None,
                          new_val: float, now: datetime) -> float:
    """
    Clamp absolute change to ~25–50 viewers per 15s tick (scaled by actual dt).
    """
    if prev is None or prev_ts is None:
        return new_val
    dt = max(1.0, (now - prev_ts).total_seconds())
    per_tick_cap = random.randint(25, 50)
    scaled_cap = per_tick_cap * (dt / CONFIG["VIEWERS_INTERVAL_SEC"])
    delta = new_val - prev
    if delta > scaled_cap:
        return prev + scaled_cap
    if delta < -scaled_cap:
        return prev - scaled_cap
    return new_val

def generate_viewers_snapshot(now: datetime,
                              current_titles: dict[str, str] | None = None) -> list[dict]:
    """
    Returns: [{ "channel": str, "viewers": str }, ...]
    - Keeps values inside 2000–5000
    - Hour-based factors + per-title popularity
    - Small jitter to avoid being too static
    - Smooth EMA then strict per-tick clamp (~25–50 / 15s)
    """
    global _viewer_state, _viewer_state_ts
    out = []
    bmin, bmax = CONFIG["BASELINE_MIN"], CONFIG["BASELINE_MAX"]

    for filename in FILES:
        channel = _channel_name_from_file(filename)

        # hour & program multipliers
        hour_f = _hour_factor_v2(now.hour)
        title = (current_titles or {}).get(channel)
        pop_f = _popularity_factor(title)

        # start from in-range baseline, modulate and jitter slightly
        baseline = random.randint(bmin, bmax)
        raw = baseline * hour_f * pop_f
        raw = max(bmin, min(bmax, raw))
        jitter = random.uniform(0.97, 1.03)
        target = max(bmin, min(bmax, raw * jitter))

        prev = _viewer_state.get(channel)
        prev_ts = _viewer_state_ts.get(channel)

        # EMA smoothing
        alpha = CONFIG["SMOOTH_ALPHA"]
        ema = target if prev is None else (alpha * target + (1 - alpha) * prev)

        # strict per-tick clamp
        clamped = _clamp_delta_per_tick(prev, prev_ts, ema, now)

        # enforce hard bounds
        clamped = max(bmin, min(bmax, clamped))

        _viewer_state[channel] = clamped
        _viewer_state_ts[channel] = now
        out.append({"channel": channel, "viewers": str(int(round(clamped)))})
    return out

# ------------ endpoints ------------
@app.get("/viewers")
def viewers_pull():
    """Plain JSON pull of the latest viewers array (no SSE framing)."""
    return Response(json.dumps(latest_viewers, ensure_ascii=False, indent=2),
                    mimetype="application/json")

@app.get("/subscribe")
def subscribe_sse():
    """SSE stream that emits ONLY the viewers array each time."""
    client_q = queue.Queue(maxsize=10)
    with _sse_lock:
        _sse_clients.add(client_q)

    def event_stream():
        # initial snapshot
        yield f"data: {json.dumps(latest_viewers, ensure_ascii=False)}\n\n"
        last_send = time.time()
        keepalive = CONFIG["SSE_KEEPALIVE_SEC"]

        while True:
            try:
                msg = client_q.get(timeout=1)
                yield f"data: {msg}\n\n"
                last_send = time.time()
            except queue.Empty:
                if keepalive > 0 and (time.time() - last_send) > keepalive:
                    yield ": ping\n\n"
                    last_send = time.time()

    headers = {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache, no-transform",
        "Connection": "keep-alive",
    }
    return Response(event_stream(), headers=headers)

@app.post("/subscribe-webhook")
def subscribe_webhook():
    body = request.get_json(silent=True) or {}
    url = (body.get("url") or "").strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        return Response(json.dumps({"error": "Provide absolute http(s) URL"}),
                        status=400, mimetype="application/json")
    with _webhook_lock:
        _webhook_urls.add(url)
    return Response(json.dumps({"ok": True, "subscribed": url}),
                    mimetype="application/json")

@app.post("/unsubscribe-webhook")
def unsubscribe_webhook():
    body = request.get_json(silent=True) or {}
    url = (body.get("url") or "").strip()
    with _webhook_lock:
        _webhook_urls.discard(url)
    return Response(json.dumps({"ok": True, "unsubscribed": url}),
                    mimetype="application/json")

@app.route('/now-playing-direct')
def now_playing_direct():
    """Direct database query for current programs (bypasses global variable)"""
    import sqlite3
    
    now = datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    current_time = now.strftime('%H:%M:%S')
    
    db_path = os.getenv('DB_PATH', '/app/data/tvguide.db')
    if not os.path.exists(db_path):
        return Response(json.dumps({"error": "Database not found"}), mimetype="application/json")
    
    result = []
    try:
        conn = sqlite3.connect(db_path)
        
        # Get all current programs
        query = '''
            SELECT pi.title, pi.channel, ps.start_time, ps.end_time
            FROM program_info pi
            JOIN program_schedule ps ON pi.id = ps.program_id
            WHERE ps.air_date = ? 
              AND ps.start_time <= ? 
              AND ps.end_time > ?
            ORDER BY pi.channel, ps.start_time
        '''
        
        cursor = conn.execute(query, (today_str, current_time, current_time))
        programs = cursor.fetchall()
        
        for program in programs:
            result.append({
                "channel": program[1],
                "title": program[0],
                "start": program[2],
                "end": program[3],
                "date": today_str.replace('-', '.'),  # Convert to DD.MM.YYYY format
                "csfd_id": ""
            })
        
        conn.close()
        
    except Exception as e:
        return Response(json.dumps({"error": f"Database error: {str(e)}"}), mimetype="application/json")
    
    return Response(json.dumps(result, ensure_ascii=False, indent=2), mimetype="application/json")

@app.route('/now-playing')
def now_playing_api():
    """Programs (pull) - fixed to query database directly."""
    import sqlite3
    
    # Get fresh data directly from database instead of relying on global variable
    now = datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    current_time = now.strftime('%H:%M:%S')
    
    db_path = os.getenv('DB_PATH', '/app/data/tvguide.db')
    
    slim = []
    try:
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            
            # Get current programs for each channel
            query = '''
                SELECT pi.title, pi.channel, ps.start_time, ps.end_time
                FROM program_info pi
                JOIN program_schedule ps ON pi.id = ps.program_id
                WHERE ps.air_date = ? 
                  AND ps.start_time <= ? 
                  AND ps.end_time > ?
                ORDER BY pi.channel, ps.start_time
            '''
            
            cursor = conn.execute(query, (today_str, current_time, current_time))
            programs = cursor.fetchall()
            
            for program in programs:
                slim.append({
                    "channel": program[1],
                    "title": program[0],
                    "start": program[2],
                    "date": now.strftime('%d.%m.%Y'),
                    "csfd_id": ""
                })
            
            conn.close()
            
    except Exception as e:
        print(f"Error in now_playing_api: {e}")
    
    data = json.dumps(slim, ensure_ascii=False, indent=2)
    return Response(data, mimetype="application/json")

# ------------ schedulers ------------
def _titles_from_now_playing() -> dict[str, str]:
    return {p.get("channel", ""): p.get("title", "") for p in now_playing}

def scheduler_loop_programs():
    """Keeps /now-playing data fresh (pull only)."""
    global now_playing
    last_sig = None
    while True:
        new_now = get_current_or_next_today_slim()
        sig = tuple((p["channel"], p["title"], p["start"], p["date"]) for p in new_now)
        if sig != last_sig:
            now_playing = new_now
            last_sig = sig
        time.sleep(30)

def scheduler_loop_viewers():
    """Generates and pushes viewer counts periodically (push only)."""
    global latest_viewers
    while True:
        now = datetime.now()
        latest_viewers = generate_viewers_snapshot(now, _titles_from_now_playing())
        _broadcast_to_subscribers(latest_viewers)  # push the raw array to SSE/Webhooks
        time.sleep(CONFIG["VIEWERS_INTERVAL_SEC"])

# ------------ main ------------
if __name__ == '__main__':
    # Seed initial values so first requests aren’t empty
    now_playing = get_current_or_next_today_slim()

    # seed viewer state and latest snapshot with timestamps
    seed = []
    now = datetime.now()
    for filename in FILES:
        ch = _channel_name_from_file(filename)
        base = random.randint(CONFIG["BASELINE_MIN"], CONFIG["BASELINE_MAX"])
        _viewer_state[ch] = float(base)
        _viewer_state_ts[ch] = now
        seed.append({"channel": ch, "viewers": str(base)})
    latest_viewers = seed

    # Start both schedulers
    threading.Thread(target=scheduler_loop_programs, daemon=True).start()
    threading.Thread(target=scheduler_loop_viewers, daemon=True).start()

    cert_file = os.getenv('SSL_CERT_FILE', 'cert.pem')
    key_file  = os.getenv('SSL_KEY_FILE', 'key.pem')
    ssl_ctx = None
    if os.path.exists(cert_file) and os.path.exists(key_file):
        ssl_ctx = (cert_file, key_file)
        app._ssl_enabled = True
    else:
        app._ssl_enabled = False  # HTTP only

    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5001)), threaded=True,
            ssl_context=ssl_ctx)
