"""A REAL MCP server in pure Python — the whole thing, readable. (Lessons 04 & 06)

Speaks the CURRENT protocol revision (2026-07-28): JSON-RPC 2.0, one message per
line, over stdio. There is no handshake any more — every request carries its own
ID badge (`_meta`), and `server/discover` answers "who are you, what do you speak,
what do you stock?". Exposes three TOOLS wrapping a tiny school "database".
Any modern MCP host that can launch a stdio server can plug this in — or use
our client/mini_client.py.

    python3 client/mini_client.py        # watch the full wire conversation
"""
import json
import sys

PROTOCOL_VERSIONS = ["2026-07-28"]                  # the revisions this instrument speaks
SERVER_INFO = {"name": "school-server", "version": "2.0.0"}
META = "io.modelcontextprotocol/"                   # prefix of the standard _meta keys

# ---- the "instrument" being wrapped: a tiny school database -----------------
DB = {
    "3A": {"aarav": "A", "sita": "A+", "kabir": "B+"},
    "3B": {"meera": "A", "rohan": "B"},
}
HOMEWORK = []  # add_homework writes here (lesson 05: tools that CHANGE things)

# ---- the three tools this server offers ------------------------------------
TOOLS = [
    {
        "name": "get_student_count",
        "description": "How many students are in a class (3A or 3B)?",
        "inputSchema": {
            "type": "object",
            "properties": {"class_name": {"type": "string", "enum": ["3A", "3B"]}},
            "required": ["class_name"],
        },
    },
    {
        "name": "lookup_grade",
        "description": "Look up one student's grade (read-only).",
        "inputSchema": {
            "type": "object",
            "properties": {"student": {"type": "string"}},
            "required": ["student"],
        },
    },
    {
        "name": "add_homework",
        "description": "Add a homework item (WRITES state — hosts should confirm with the user!).",
        "inputSchema": {
            "type": "object",
            "properties": {"title": {"type": "string"}, "due": {"type": "string"}},
            "required": ["title"],
        },
    },
]

def run_tool(name, args):
    """Dispatch a tools/call to real Python. Returns plain text for the model's desk."""
    if name == "get_student_count":
        cls = args["class_name"]
        return f"Class {cls} has {len(DB[cls])} students: {', '.join(DB[cls])}."
    if name == "lookup_grade":
        student = args["student"].lower()
        for cls, students in DB.items():
            if student in students:
                return f"{student.title()} ({cls}) has grade {students[student]}."
        raise LookupError(f"no student named {args['student']!r}")   # → isError, the model can retry
    if name == "add_homework":
        HOMEWORK.append({"title": args["title"], "due": args.get("due", "someday")})
        return f"Added ✏️ — homework list is now: {json.dumps(HOMEWORK)}"
    raise ValueError(f"unknown tool {name!r}")

# ---- the protocol plumbing: JSON-RPC over stdio, one message per line -------
def reply(msg_id, result):
    """Every result carries resultType + the server's own badge (_meta.serverInfo)."""
    result = {"resultType": "complete", **result, "_meta": {META + "serverInfo": SERVER_INFO}}
    print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": result}), flush=True)

def reply_error(msg_id, code, message, data=None):
    err = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": err}), flush=True)

def main():
    for line in sys.stdin:                      # the socket: read one message per line
        line = line.strip()
        if not line:
            continue
        msg = json.loads(line)
        method, msg_id, params = msg.get("method"), msg.get("id"), msg.get("params", {})
        if msg_id is None:                       # a notification: no id → never answered
            continue

        # 🪪 the badge check (lesson 04, step 1): which revision is this request speaking?
        version = params.get("_meta", {}).get(META + "protocolVersion")
        if version not in PROTOCOL_VERSIONS:     # (a legacy `initialize` lands here too)
            reply_error(msg_id, -32022, "Unsupported protocol version",
                        {"supported": PROTOCOL_VERSIONS, "requested": version})
            continue

        if method == "server/discover":          # 🪪 optional introductions (lesson 04, step 1)
            reply(msg_id, {
                "supportedVersions": PROTOCOL_VERSIONS,
                "capabilities": {"tools": {}},   # "I stock tools" (no resources/prompts here)
                "instructions": "A tiny school database: class sizes, grades, homework.",
                "ttlMs": 3600000, "cacheScope": "public",
            })
        elif method == "tools/list":             # 📋 "what do you offer?" (step 2)
            reply(msg_id, {"tools": TOOLS, "ttlMs": 60000, "cacheScope": "public"})
        elif method == "tools/call":             # 🧰 "do the thing" (step 3)
            name = params.get("name")
            if name not in [t["name"] for t in TOOLS]:      # protocol error: no such tool
                reply_error(msg_id, -32602, f"Unknown tool: {name}")
                continue
            try:
                text = run_tool(name, params.get("arguments", {}))
                reply(msg_id, {"content": [{"type": "text", "text": text}], "isError": False})
            except Exception as e:                           # tool error: data for the model
                reply(msg_id, {"content": [{"type": "text", "text": f"tool error: {e}"}],
                               "isError": True})
        else:                                    # unknown request → standard error
            reply_error(msg_id, -32601, f"method not found: {method}")

if __name__ == "__main__":
    main()
