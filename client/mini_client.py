"""A REAL MCP client/host in pure Python — watch the whole wire. (Lessons 04 & 07)

Launches server/school_server.py as a child process (the stdio transport),
performs the actual MCP handshake, discovers tools, calls them — and prints
every JSON-RPC message so you SEE the protocol.

    python3 client/mini_client.py            # scripted tour
    python3 client/mini_client.py --drive    # YOU play the model: pick the tool calls
"""
import json
import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class MiniHost:
    """The 'room with the socket' 🔌: one client connection to one server."""

    def __init__(self, server_cmd):
        self.proc = subprocess.Popen(
            server_cmd, cwd=ROOT, text=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        )
        self.next_id = 0

    def send(self, method, params=None, is_notification=False):
        msg = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        if not is_notification:
            self.next_id += 1
            msg["id"] = self.next_id
        print(f"→ {json.dumps(msg)}")
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()
        if is_notification:
            return None
        response = json.loads(self.proc.stdout.readline())
        print(f"← {json.dumps(response)[:160]}{'…' if len(json.dumps(response))>160 else ''}\n")
        return response.get("result", response)

    def close(self):
        self.proc.stdin.close()
        self.proc.wait(timeout=5)

def main():
    host = MiniHost([sys.executable, "server/school_server.py"])

    print("═══ 1) the handshake 🤝 ════════════════════════════════════")
    host.send("initialize", {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "mini-host", "version": "1.0.0"},
    })
    host.send("notifications/initialized", is_notification=True)

    print("═══ 2) discovery 📋 — 'what do you offer?' ═════════════════")
    tools = host.send("tools/list")["tools"]
    for t in tools:
        print(f"   🧰 {t['name']}: {t['description']}")
    print()

    if "--drive" in sys.argv:
        print("═══ 3) YOU are the model 🧠 — pick tool calls ═══════════════")
        print("   examples:  get_student_count {\"class_name\":\"3A\"}")
        print("              lookup_grade {\"student\":\"sita\"}   (empty line quits)")
        while True:
            try:
                raw = input("model calls> ").strip()
            except EOFError:
                break
            if not raw:
                break
            name, _, arg_str = raw.partition(" ")
            result = host.send("tools/call",
                               {"name": name, "arguments": json.loads(arg_str or "{}")})
            print(f"   📄 lands on the desk: {result['content'][0]['text']}\n")
    else:
        print("═══ 3) tool calls 🧰 — what an agent's loop would do ═══════")
        for name, args in [
            ("get_student_count", {"class_name": "3A"}),
            ("lookup_grade", {"student": "sita"}),
            ("add_homework", {"title": "read MCP lesson 05", "due": "Friday"}),
        ]:
            result = host.send("tools/call", {"name": name, "arguments": args})
            print(f"   📄 lands on the desk: {result['content'][0]['text']}\n")

    host.close()
    print("═══ done — that was the ENTIRE protocol: 3 verbs and a handshake 🔌 ═══")

if __name__ == "__main__":
    main()
