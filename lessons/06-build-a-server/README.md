# 🔬 Lesson 06 — Build a server: 110 honest lines

**📍 You are here:** Lesson **06** of 8 · Previous: `lesson-05-transports-security` · Next: `lesson-07-build-a-client`

---

## 📦 What's in this branch

Lessons 01–05, **plus** the guided read of a REAL MCP server —
[server/school_server.py](../../server/school_server.py) — and your
first extension to it.

## 🧒 Explain like I'm 5

Building an instrument sounds scary until you see one opened up. Ours
has exactly **four parts**, top to bottom of the file:

1. **The thing being wrapped** 🗄️ — a toy database (`DB`, `HOMEWORK`).
   In real servers this is the interesting part: your Postgres, your
   API, your filesystem. MCP is just the plug on the front.
2. **The shelf list** 📋 — `TOOLS`: three entries of name +
   description + inputSchema. Remember L03: **descriptions are for the
   model** — ours say what each tool does AND that `add_homework`
   writes (danger label, L05!).
3. **The dispatcher** 🔀 — `run_tool(name, args)`: a plain Python
   if-ladder doing the actual work. Nothing protocol-ish here — you
   could unit-test it alone.
4. **The plumbing** 🔧 — `main()`: read a line, parse JSON, answer the
   four methods you know from L04 (`initialize`,
   `notifications/initialized`, `tools/list`, `tools/call`), print the
   reply. Errors → polite `isError` content, never a crash.

That's a server. The official SDKs (Python/TypeScript `mcp` packages)
give you decorators, typed schemas, transports and the long tail of the
spec — use them for real work — but they're automating THESE four
parts, and now you've seen the parts.

## 🗺️ Diagram

```mermaid
flowchart TB
    subgraph file["server/school_server.py - the four parts"]
        db["1 🗄️ the wrapped thing<br/>DB + HOMEWORK (yours: Postgres, APIs…)"]
        tools["2 📋 the shelf: TOOLS<br/>name · description(for the model!) · inputSchema"]
        disp["3 🔀 run_tool()<br/>plain Python if-ladder — unit-testable"]
        plumb["4 🔧 main() loop<br/>line in → JSON-RPC → line out"]
    end
    host["🔌 any MCP host"]
    host <-->|"stdio"| plumb
    plumb --> disp --> db
    plumb --> tools
```

## ❓ What (the details worth stealing)

- `flush=True` on every print — stdio servers that forget this "hang"
  mysteriously (the classic first bug: buffered replies never arrive).
- Answer **only what you're asked**; unknown method + id → error
  `-32601`. Notifications get silence, not errors.
- Tool errors as `{"content":[…], "isError": true}` — the model can
  read the failure and try again (an agent's retry loop, AI course
  L11, depends on this!).
- Schemas are contracts: `"enum": ["3A","3B"]` means the model gets
  told the legal values — fewer bad calls, better behavior. Rich
  schemas are cheap model-steering.
- Real-world upgrades from here: the official SDK, `resources/list`
  for report cards (L03's homework!), env-var secrets, and a scoped
  DB account (least privilege — AWS course L03).

## 🤔 Why

Because "we should build an MCP server for our X" is now a sprint
ticket in half the industry — and you can estimate it honestly: the
plug is a day (SDK makes it hours); the REAL work is part 1 (what to
expose) and part 2's descriptions + danger labels (design, L03/L05).
Teams that get those right ship servers agents actually use correctly.

## 🧪 Try it — extend it for real

```bash
# 1) prove the baseline:
python3 client/mini_client.py

# 2) YOUR first tool — add to TOOLS in server/school_server.py:
#    {"name":"list_homework","description":"Show the homework list (read-only).",
#     "inputSchema":{"type":"object","properties":{}}}
#    …and to run_tool():
#    if name == "list_homework":
#        return f"Homework: {json.dumps(HOMEWORK) or '[]'}"

# 3) rerun the client — your tool appears in discovery, callable:
python3 client/mini_client.py --drive
# model calls> list_homework {}
```

Your first MCP server change: shipped. 🔬

## ⏭️ Next

The other side of the socket: reading
**mini_client.py** — and why hosts, not models, hold the power.

```bash
git checkout lesson-07-build-a-client
```
