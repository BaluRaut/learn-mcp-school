"""A REAL MCP server in pure Python — the whole thing, readable. (Lessons 04 & 06)

Speaks the actual protocol: JSON-RPC 2.0, one message per line, over stdio.
Exposes three TOOLS wrapping a tiny school "database". Any MCP host that
can launch a stdio server can plug this in — or use our client/mini_client.py.

    python3 client/mini_client.py        # watch the full wire conversation
"""
import json
import sys

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
        return f"No student named {args['student']!r} found."
    if name == "add_homework":
        HOMEWORK.append({"title": args["title"], "due": args.get("due", "someday")})
        return f"Added ✏️ — homework list is now: {json.dumps(HOMEWORK)}"
    raise ValueError(f"unknown tool {name!r}")

# ---- the protocol plumbing: JSON-RPC over stdio, one message per line -------
def reply(msg_id, result):
    print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": result}), flush=True)

def reply_error(msg_id, code, message):
    print(json.dumps({"jsonrpc": "2.0", "id": msg_id,
                      "error": {"code": code, "message": message}}), flush=True)

def main():
    for line in sys.stdin:                      # the socket: read one message per line
        line = line.strip()
        if not line:
            continue
        msg = json.loads(line)
        method, msg_id = msg.get("method"), msg.get("id")

        if method == "initialize":              # 🤝 the handshake (lesson 04, step 1)
            reply(msg_id, {
                "protocolVersion": "2025-06-18",
                "capabilities": {"tools": {}},   # "I offer tools" (no resources/prompts here)
                "serverInfo": {"name": "school-server", "version": "1.0.0"},
            })
        elif method == "notifications/initialized":
            pass                                 # a notification: no id, no reply needed
        elif method == "tools/list":             # 📋 "what do you offer?" (step 2)
            reply(msg_id, {"tools": TOOLS})
        elif method == "tools/call":             # 🧰 "do the thing" (step 3)
            params = msg.get("params", {})
            try:
                text = run_tool(params["name"], params.get("arguments", {}))
                reply(msg_id, {"content": [{"type": "text", "text": text}]})
            except Exception as e:
                reply(msg_id, {"content": [{"type": "text", "text": f"tool error: {e}"}],
                               "isError": True})
        elif msg_id is not None:                 # unknown request → standard error
            reply_error(msg_id, -32601, f"method not found: {method}")

if __name__ == "__main__":
    main()
