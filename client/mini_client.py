"""A REAL MCP client/host in pure Python — watch the whole wire. (Lessons 04 & 07)

Launches server/school_server.py as a child process (the stdio transport), stamps
every request with the ID badge the CURRENT protocol revision (2026-07-28) requires,
asks `server/discover` (optional introductions), discovers tools, calls them — and
prints every JSON-RPC message so you SEE the protocol. No handshake, no session.

    python3 client/mini_client.py            # scripted tour
    python3 client/mini_client.py --drive    # YOU play the model: pick the tool calls
"""
import json
import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROTOCOL_VERSION = "2026-07-28"
META = "io.modelcontextprotocol/"
BADGE = {                                   # 🪪 goes on EVERY request — there is no handshake
    META + "protocolVersion": PROTOCOL_VERSION,
    META + "clientInfo": {"name": "mini-host", "version": "2.0.0"},
    META + "clientCapabilities": {},
}

class MiniHost:
    """The 'room with the socket' 🔌: one client connection to one server."""

    def __init__(self, server_cmd):
        self.proc = subprocess.Popen(
            server_cmd, cwd=ROOT, text=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        )
        self.next_id = 0

    def send(self, method, params=None):
        """Build one JSON-RPC request (badge included), write a line, read the answer line."""
        self.next_id += 1
        msg = {"jsonrpc": "2.0", "id": self.next_id, "method": method,
               "params": {**(params or {}), "_meta": BADGE}}
        print(f"→ {json.dumps(msg, ensure_ascii=False)}")
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()
        response = json.loads(self.proc.stdout.readline())   # the very next line IS the answer
        shown = json.dumps(response, ensure_ascii=False)
        print(f"← {shown[:170]}{'…' if len(shown) > 170 else ''}\n")
        return response                       # callers look at 'result' or 'error'

    def close(self):
        self.proc.stdin.close()
        self.proc.wait(timeout=5)

def show(response):
    """Put a tools/call answer on the model's desk — or explain the error."""
    if "error" in response:                   # protocol error: unknown tool, wrong version…
        e = response["error"]
        print(f"   ❌ server error {e['code']}: {e['message']}\n")
        return
    result = response["result"]
    flag = " ⚠️ isError — the tool is telling the model it failed" if result.get("isError") else ""
    print(f"   📄 lands on the desk: {result['content'][0]['text']}{flag}\n")

def main():
    host = MiniHost([sys.executable, "server/school_server.py"])

    print("═══ 1) introductions 🪪 — server/discover (optional since 2026-07-28) ═══")
    info = host.send("server/discover")["result"]
    who = info["_meta"][META + "serverInfo"]
    print(f"   🔬 {who['name']} v{who['version']} speaks {info['supportedVersions']}"
          f" · stocks: {', '.join(info['capabilities'])}\n")

    print("═══ 2) discovery 📋 — 'what do you offer?' ═════════════════")
    tools = host.send("tools/list")["result"]["tools"]
    for t in tools:
        print(f"   🧰 {t['name']}: {t['description']}")
    print()

    if "--drive" in sys.argv:
        print("═══ 3) YOU are the model 🧠 — pick tool calls ═══════════════")
        print("   try these sequences (empty line quits):")
        print('     a) get_student_count {"class_name":"3A"}   then   lookup_grade {"student":"sita"}')
        print('     b) lookup_grade {"student":"nobody"}      → a polite isError answer (L04)')
        print('     c) add_homework {"title":"prank ×100"}     → runs INSTANTLY: the missing gate (L05)')
        print('     d) fly_to_moon {}                         → a protocol error, not a crash (L06)')
        while True:
            try:
                raw = input("model calls> ").strip()
            except EOFError:
                break
            if not raw:
                break
            name, _, arg_str = raw.partition(" ")
            show(host.send("tools/call", {"name": name, "arguments": json.loads(arg_str or "{}")}))
    else:
        print("═══ 3) tool calls 🧰 — what an agent's loop would do ═══════")
        for name, args in [
            ("get_student_count", {"class_name": "3A"}),
            ("lookup_grade", {"student": "sita"}),
            ("add_homework", {"title": "read MCP lesson 05", "due": "Friday"}),
        ]:
            show(host.send("tools/call", {"name": name, "arguments": args}))

    host.close()
    print("═══ done — that was the ENTIRE protocol: three verbs and a badge 🪪 (no handshake since 2026-07-28) ═══")

if __name__ == "__main__":
    main()
