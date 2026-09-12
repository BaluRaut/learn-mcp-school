# 🌍 Lesson 08 — Five real-world use cases (with sequence diagrams)

**📍 You are here:** Lesson **08** of 8 — the final lesson!

---

## 📦 What's in this branch

The complete course, **plus** the payoff: five production-shaped
setups. Each is drawn twice on the site — a numbered flow diagram AND a
step-by-step sequence diagram:
**🌐 [the illustrated use-cases page](https://baluraut.github.io/learn-mcp-school/use-cases.html)** ← open it beside this lesson.

## 🧒 The five, in school words

**1. 🐙 The coding assistant** (IDE + GitHub server + filesystem server)
*"Fix issue #42."* The student reads the complaint (get_issue), reads
the code (read_file), writes a fix, runs the tests (run_tests), drafts
the PR — **create_pr waits for your click** (L05 rule 3).
Why MCP: the same GitHub server works in every IDE and agent — write
once, plug everywhere.

**2. 🎧 The support desk** (support app + orders-DB server + docs server)
Customer: "where's my refund?" → look up the order (read-only!), fetch
the refund policy → grounded answer with receipts — RAG's open-book
exam (AI course L10) wearing MCP plugs. The DB tool is SELECT-only via
a scoped account (AWS course L03's least privilege, verbatim).

**3. 📊 The data analyst** (chat app + SQL server + chart server)
"Which product sold best last month, per region?" → query_db →
make_chart → numbers with a picture. The schema's `enum`/read-only
design (L06) is what keeps "analyst" from becoming "DROP TABLE". 😅

**4. 📅 The meeting-prep butler** (assistant + calendar + CRM + email)
"Prep me for the 3 pm" → get_event → crm_lookup(company) →
recent_threads(attendees) → one tidy brief. THREE servers, one room,
one desk — the N+M payoff in a single request.

**5. 📁 The report robot** (agent + filesystem + Slack server)
"Summarize this folder's weekly reports and post to #team" → list_dir →
read_file ×N → summarize → **slack_post waits for your click** — the
write-gate again, because automation without gates is L05's incident
report.

## 🗺️ Diagram (use case 1, the shape of them all)

```mermaid
sequenceDiagram
    participant U as 🧑 user
    participant H as 🏫 IDE host
    participant M as 🧠 model
    participant G as 🐙 GitHub server
    participant F as 📁 files server
    U->>H: 1 "fix issue #42"
    H->>M: 2 goal + tool shelves
    M->>G: 3 get_issue(42) — via host
    G-->>M: 4 the bug report → desk
    M->>F: 5 read_file(buggy.py)
    F-->>M: 6 code → desk
    M->>H: 7 proposes create_pr(fix)
    H->>U: 8 🚧 "allow PR?" — the human gate
    U->>H: 9 click ✓ → PR exists
```

## ❓ What the five have in common (the checklist you'll reuse)

- **Reads flow, writes gate** — every case marks which tools change
  the world, and those get the click (L05).
- **Least-privilege plumbing** — scoped DB accounts, repo-only tokens
  (the AWS course's IAM instincts, now for AI).
- **Same servers, many rooms** — each server in these stories is
  reusable across apps; that's WHY teams bother (L01's N+M).
- **The desk explains the limits** — huge folders / giant queries hit
  context limits (AI course L08); production versions add pagination
  and summaries server-side.
- **It's all seven messages** — every sequence above is L04's
  handshake-discover-call, repeated. Read one wire, read them all.

## 🧪 Try it — your sixth use case

Pick a REAL workflow from your week (expense report? standup notes?
ticket triage?). On paper: which servers (existing or to-build)? which
tools per server — and which are writes (gates!)? Draw the sequence
diagram in the style above, numbered. If you can draw it, you can
build it — L06 and L07 were the whole toolkit.

## 🎓 The socket is yours

The drawer problem → the three roles → the three shelves → seven wire
messages → the three trust rules → a real server → a real host → five
real deployments. **You didn't just learn MCP — you own a working
implementation of it.** 🔌🎓

```bash
git checkout main
python3 client/mini_client.py --drive    # one last spin, for fun
```
