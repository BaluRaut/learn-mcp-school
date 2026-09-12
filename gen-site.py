#!/usr/bin/env python3
"""Generate the learn-mcp-school docs: index, lesson-diagrams, use-cases."""
GH = "https://github.com/BaluRaut/learn-mcp-school/blob"
P1, P2 = "#7c3aed", "#ea580c"

L = [
 (1,"lesson-01-why-mcp","01-why-mcp","🍝 Why MCP","The adapter drawer (N×M) → the standard socket (N+M).",35,P1),
 (2,"lesson-02-architecture","02-architecture","🏫 Architecture","Room (host) · wall socket (client) · instrument (server).",35,P1),
 (3,"lesson-03-primitives","03-primitives","🧰 The three shelves","Tools, resources, prompts — model, app and user each decide one.",35,P1),
 (4,"lesson-04-the-wire","04-the-wire","🤝 The wire","Three verbs and a handshake — the whole protocol, message by message.",40,P1),
 (5,"lesson-05-transports-security","05-transports-security","🚧 Transports &amp; trust","Direct plug vs extension cord — and the three rules of not getting burned.",40,P1),
 (6,"lesson-06-build-a-server","06-build-a-server","🔬 Build a server","110 honest lines: the wrapped thing, the shelf, the dispatcher, the plumbing.",45,P2),
 (7,"lesson-07-build-a-client","07-build-a-client","🔌 Build a client","The side with the power — the model asks, the HOST does.",45,P2),
 (8,"lesson-08-use-cases","08-use-cases","🌍 Real-world use cases","Coding, support, data, meetings, reports — with sequence diagrams.",40,P2),
]

BASE_CSS = """
  :root { --bg:#f8fafc; --card:#fff; --ink:#0f172a; --muted:#475569; --line:#e2e8f0; --accent:#7c3aed; --ok:#16a34a; --blue:#2563eb; }
  @media (prefers-color-scheme: dark) { :root { --bg:#0b1220; --card:#131c2e; --ink:#e2e8f0; --muted:#94a3b8; --line:#253349; } }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); color:var(--ink); font-family:-apple-system,"Segoe UI",Helvetica,Arial,sans-serif; line-height:1.6; }
  .wrap { max-width:1080px; margin:0 auto; padding:28px 20px 60px; }
  a { color:var(--blue); } h1 { font-size:2rem; line-height:1.25; } h2 { font-size:1.4rem; margin:44px 0 6px; }
  .sub { color:var(--muted); max-width:74ch; }
  .chips { display:flex; flex-wrap:wrap; gap:8px; margin:16px 0 8px; }
  .chip { border:1px solid var(--line); background:var(--card); border-radius:999px; padding:6px 14px; font-size:.85rem; color:var(--muted); }
  .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:14px; margin-top:16px; }
  .lesson { background:var(--card); border:1px solid var(--line); border-top:5px solid var(--c,var(--accent)); border-radius:14px; padding:16px; display:flex; flex-direction:column; gap:6px; }
  .lesson .top { display:flex; align-items:center; gap:10px; }
  .lesson .num { flex:none; width:30px; height:30px; border-radius:50%; background:var(--c,var(--accent)); color:#fff; display:inline-flex; align-items:center; justify-content:center; font-weight:800; font-size:.9rem; }
  .lesson h3 { font-size:1.02rem; line-height:1.3; } .lesson .ana { color:var(--muted); font-size:.9rem; }
  .lesson code { font-size:.78rem; background:var(--bg); border:1px solid var(--line); border-radius:6px; padding:1px 6px; }
  .lesson a.go { margin-top:auto; font-weight:600; font-size:.9rem; text-decoration:none; } .lesson a.go+a.go { margin-top:0; } .lesson a.go:hover { text-decoration:underline; }
  .callout { background:var(--card); border:1px solid var(--line); border-left:6px solid var(--ok); border-radius:14px; padding:18px 20px; margin-top:16px; }
  pre { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:14px 16px; overflow-x:auto; font-size:.88rem; margin-top:12px; }
  .btn { display:inline-block; background:var(--accent); color:#fff; border-radius:10px; padding:10px 18px; text-decoration:none; font-weight:700; margin:14px 10px 0 0; }
  .btn.alt { background:transparent; color:var(--ink); border:1px solid var(--line); }
  .vs { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:14px; margin-top:16px; }
  .vcol { background:var(--card); border:1px solid var(--line); border-radius:14px; padding:18px; } .vcol h3 { margin-bottom:8px; }
  .vcol ul { margin-left:18px; color:var(--muted); font-size:.93rem; }
  .toc { display:flex; flex-wrap:wrap; gap:8px; margin:18px 0 6px; }
  .toc a { border:1px solid var(--line); background:var(--card); border-radius:999px; padding:5px 12px; font-size:.82rem; color:var(--muted); text-decoration:none; }
  .toc a:hover { color:var(--ink); border-color:var(--muted); }
  footer { margin-top:56px; border-top:1px solid var(--line); padding-top:18px; color:var(--muted); font-size:.88rem; }
"""
DSEC_CSS = """
  .dsec { background:var(--card); border:1px solid var(--line); border-top:6px solid var(--c,var(--accent)); border-radius:16px; padding:22px 22px 16px; margin-top:26px; scroll-margin-top:16px; }
  .dsec h2 { font-size:1.25rem; display:flex; align-items:center; gap:10px; }
  .dsec h2 .ln { flex:none; width:32px; height:32px; border-radius:50%; background:var(--c,var(--accent)); color:#fff; display:inline-flex; align-items:center; justify-content:center; font-size:.95rem; font-weight:800; }
  .dsec p.d { color:var(--muted); font-size:.95rem; margin:6px 0 4px; }
  .dsec svg { width:100%; height:auto; display:block; margin-top:10px; } .dsec .foot { margin-top:8px; font-size:.92rem; }
  .box { fill:var(--card); stroke:var(--c,var(--accent)); stroke-width:2; }
  .soft { fill:var(--bg); stroke:var(--line); stroke-width:1.5; }
  .dead { fill:var(--bg); stroke:var(--muted); stroke-width:1.5; stroke-dasharray:6 5; }
  .t { font:600 14px -apple-system,"Segoe UI",sans-serif; fill:var(--ink); }
  .s { font:12px -apple-system,"Segoe UI",sans-serif; fill:var(--muted); } .m { text-anchor:middle; }
  .arr { stroke:#64748b; stroke-width:2; fill:none; marker-end:url(#arw); } .dash { stroke-dasharray:6 5; }
  .life { stroke:#94a3b8; stroke-width:1.5; stroke-dasharray:4 5; }
  .nc { fill:var(--c,var(--accent)); } .nt { font:700 12px -apple-system,sans-serif; fill:#fff; text-anchor:middle; }
"""
MARKER = '<svg width="0" height="0" style="position:absolute"><defs><marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#64748b"/></marker></defs></svg>'

def head(title, desc):
    return (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
      f'<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{title}</title>\n'
      f'<meta name="description" content="{desc}">\n<style>{BASE_CSS}{DSEC_CSS}</style>\n</head>\n<body>\n')

B='<rect class="box"'; S='<rect class="soft"'; D='<rect class="dead"'; DASH=' dash'
def t(x,y,s): return f'<text class="t m" x="{x}" y="{y}">{s}</text>'
def sm(x,y,s): return f'<text class="s m" x="{x}" y="{y}">{s}</text>'
def num(x,y,n): return f'<g transform="translate({x},{y})"><circle r="11" class="nc"/><text class="nt" dy="4">{n}</text></g>'
def arr(a,b,c,d,dash=""): return f'<line class="arr{dash}" x1="{a}" y1="{b}" x2="{c}" y2="{d}"/>'

# ---------- sequence-diagram builder 🎼 ----------
def seq(participants, messages, note=None):
    """participants: [label,...]; messages: (frm,to,n,label) or ('note', text); self-msg if frm==to."""
    W = 940
    xs = [int(W*(i+0.5)/len(participants)) for i in range(len(participants))]
    y = 96; out = []
    body = []
    for m in messages:
        if m[0] == 'note':
            body.append(f'<rect class="soft" x="90" y="{y-16}" width="{W-180}" height="30" rx="8"/>' + sm(W//2, y+4, m[1]))
            y += 46; continue
        frm, to, n, label = m
        x1, x2 = xs[frm], xs[to]
        if frm == to:
            body.append(arr(x1, y, x1+70, y) + arr(x1+70, y, x1+70, y+18) + arr(x1+70, y+18, x1+4, y+18))
            body.append(sm(x1+150, y+4, label)); body.append(num(x1-20, y, n)); y += 44
        else:
            dash = DASH if x2 < x1 else ""
            body.append(arr(x1, y, x2 + (-6 if x2>x1 else 6), y, dash))
            body.append(sm((x1+x2)//2, y-10, label)); body.append(num((x1+x2)//2, y+16, n)); y += 46
    H = y + 20
    for i, p in enumerate(participants):
        out.append(f'<rect class="box" x="{xs[i]-85}" y="16" width="170" height="44" rx="10"/>' + t(xs[i], 44, p))
        out.append(f'<line class="life" x1="{xs[i]}" y1="60" x2="{xs[i]}" y2="{H-10}"/>')
    if note: out.append(sm(W//2, H-2, note)); H += 14
    return f'<svg viewBox="0 0 {W} {H}" role="img">' + "".join(out) + "".join(body) + '</svg>'

# ---------- lesson diagrams ----------
SVG = {}
SVG[1]=(f'<svg viewBox="0 0 940 300" role="img">{D} x="40" y="60" width="270" height="150" rx="12"/>{t(175,95,"🍝 before: N×M adapters")}{sm(175,122,"IDE×GitHub · chatbot×GitHub ·")}{sm(175,144,"agent×GitHub · every pair,")}{sm(175,166,"hand-built, none reusable")}'
 f'{B} x="400" y="40" width="230" height="90" rx="12"/>{t(515,72,"🏫 hosts - standard sockets")}{sm(515,98,"IDE · chatbot · agent")}'
 f'{B} x="400" y="150" width="230" height="90" rx="12"/>{t(515,182,"🔬 servers - standard plugs")}{sm(515,208,"GitHub · files · your DB")}'
 f'{arr(310,135,396,90)}{arr(310,150,396,190)}{num(353,120,1)}'
 f'<line class="arr" x1="515" y1="130" x2="515" y2="146"/>{num(545,138,2)}'
 f'{B} x="710,"'.replace('x="710,"','x="710" y="95" width="200" height="90" rx="12"/>') + t(810,127,"🔌 N+M")+sm(810,153,"write once,")+sm(810,175,"plug in everywhere")+arr(630,140,706,140)+num(668,123,3)+'</svg>')
SVG[2]=seq(["🧠 model","🏫 host","🔌 client","🔬 server"],
 [(0,1,1,"'I want lookup_grade(sita)' — in words"),
  ('note',"the host DECIDES — permission checks live here 🚧"),
  (1,2,2,"approved → forward"),(2,3,3,"tools/call over the socket"),
  (3,2,4,"result"),(2,0,5,"→ lands on the model's desk 📄")],
 "the model only ever ASKS · the host does · the server answers")
SVG[3]=(f'<svg viewBox="0 0 940 300" role="img">{B} x="40" y="50" width="270" height="200" rx="14"/>{t(175,82,"🧰 TOOLS")}{sm(175,108,"actions with inputs:")}{sm(175,130,"lookup_grade · add_homework")}{S} x="65" y="150" width="220" height="80" rx="10"/>{sm(175,180,"WHO decides: the MODEL")}{sm(175,202,"(host permitting)")}'
 f'{B} x="340" y="50" width="270" height="200" rx="14"/>{t(475,82,"📁 RESOURCES")}{sm(475,108,"readable context:")}{sm(475,130,"file:// · db://students/3A")}{S} x="365" y="150" width="220" height="80" rx="10"/>{sm(475,180,"WHO decides: the APP")}{sm(475,202,"(what goes on the desk)")}'
 f'{B} x="640" y="50" width="270" height="200" rx="14"/>{t(775,82,"📜 PROMPTS")}{sm(775,108,"suggested recipes:")}{sm(775,130,"/summarize-ticket")}{S} x="665" y="150" width="220" height="80" rx="10"/>{sm(775,180,"WHO decides: the USER")}{sm(775,202,"(menus, slash-commands)")}'
 f'{num(40,50,1)}{num(340,50,2)}{num(640,50,3)}{sm(475,285,"three shelves, three deciders — say it twice and you know more MCP than most 😄")}</svg>')
SVG[4]=seq(["🔌 client","🔬 server"],
 [(0,1,1,"initialize {protocolVersion, clientInfo}"),
  (1,0,2,"{protocolVersion, capabilities:{tools}, serverInfo}"),
  (0,1,3,"notifications/initialized — no id, no reply"),
  (0,1,4,"tools/list"),
  (1,0,5,"{tools:[{name, description, inputSchema}…]}"),
  (0,1,6,'tools/call {name:"lookup_grade", arguments:{student:"sita"}}'),
  (1,0,7,'{content:[{type:"text", text:"Sita (3A) has grade A+."}]}')],
 "three verbs and a handshake — run python3 client/mini_client.py and watch these exact lines")
SVG[5]=(f'<svg viewBox="0 0 940 300" role="img">{B} x="40" y="40" width="420" height="110" rx="14"/>{t(250,70,"🔌 stdio - the direct plug")}{sm(250,96,"host launches server as child process;")}{sm(250,118,"JSON per line on stdin/stdout · local things")}{num(40,40,1)}'
 f'{B} x="490" y="40" width="420" height="110" rx="14"/>{t(700,70,"📡 HTTP - the extension cord")}{sm(700,96,"same messages over HTTP + auth (OAuth);")}{sm(700,118,"remote/shared things · team DB, SaaS")}{num(490,40,2)}'
 f'{D} x="40" y="175" width="270" height="100" rx="12"/>{sm(175,205,"🚧 rule 1: a server =")}{sm(175,227,"installed software with")}{sm(175,249,"YOUR permissions")}'
 f'{D} x="340" y="175" width="270" height="100" rx="12"/>{sm(475,205,"🚧 rule 2: tool results may")}{sm(475,227,"carry prompt injection —")}{sm(475,249,"treat as data, not commands")}'
 f'{D} x="640" y="175" width="270" height="100" rx="12"/>{sm(775,205,"🚧 rule 3: WRITES get a")}{sm(775,227,"human gate — reads may flow,")}{sm(775,249,"add_homework waits for a click")}{num(640,175,3)}</svg>')
SVG[6]=(f'<svg viewBox="0 0 940 300" role="img">{B} x="40" y="40" width="420" height="100" rx="12"/>{t(250,70,"1 🗄️ the wrapped thing")}{sm(250,96,"toy DB here — YOUR Postgres/API in real life;")}{sm(250,118,"MCP is just the plug on the front")}{num(40,40,1)}'
 f'{B} x="490" y="40" width="420" height="100" rx="12"/>{t(700,70,"2 📋 the shelf: TOOLS")}{sm(700,96,"name · description (FOR THE MODEL!) ·")}{sm(700,118,"inputSchema — rich schemas steer behavior")}{num(490,40,2)}'
 f'{B} x="40" y="165" width="420" height="100" rx="12"/>{t(250,195,"3 🔀 run_tool() dispatcher")}{sm(250,221,"plain Python if-ladder — unit-testable,")}{sm(250,243,"no protocol in sight")}{num(40,165,3)}'
 f'{B} x="490" y="165" width="420" height="100" rx="12"/>{t(700,195,"4 🔧 main() plumbing")}{sm(700,221,"line in → JSON-RPC → line out · flush=True!")}{sm(700,243,"errors = polite isError content, never a crash")}{num(490,165,4)}'
 f'{sm(475,290,"server/school_server.py — 110 lines, all four parts visible · the official SDKs automate exactly this")}</svg>')
SVG[7]=seq(["🧑 you (--drive)","🏫 MiniHost","🔬 school_server"],
 [(0,1,1,'"call lookup_grade {student: sita}"'),
  ('note',"⚡ the POWER moment: the host decides (real hosts: permission prompt here 🚧)"),
  (1,2,2,"tools/call {…, id:4}"),
  (2,1,3,"{id:4, content:[…grade A+…]}"),
  (1,0,4,"📄 lands on the desk")],
 "client/mini_client.py — swap the input() for a model API call and you have a real agent host")
SVG[8]=(f'<svg viewBox="0 0 940 300" role="img">{B} x="40" y="40" width="270" height="100" rx="12"/>{t(175,70,"🐙 coding assistant")}{sm(175,96,"issue → code → tests → PR")}{sm(175,118,"(PR waits for your click 🚧)")}{num(40,40,1)}'
 f'{B} x="340" y="40" width="270" height="100" rx="12"/>{t(475,70,"🎧 support desk")}{sm(475,96,"orders DB (read-only!) + docs")}{sm(475,118,"→ grounded answer + receipts")}{num(340,40,2)}'
 f'{B} x="640" y="40" width="270" height="100" rx="12"/>{t(775,70,"📊 data analyst")}{sm(775,96,"query_db → make_chart")}{sm(775,118,"SELECT-only via scoped account")}{num(640,40,3)}'
 f'{B} x="190" y="165" width="270" height="100" rx="12"/>{t(325,195,"📅 meeting-prep butler")}{sm(325,221,"calendar + CRM + email —")}{sm(325,243,"3 servers, one desk (N+M!)")}{num(190,165,4)}'
 f'{B} x="490" y="165" width="270" height="100" rx="12"/>{t(625,195,"📁 report robot")}{sm(625,221,"read folder → summarize →")}{sm(625,243,"slack_post gated by a click 🚧")}{num(490,165,5)}'
 f'{sm(475,292,"each drawn twice on the use-cases page: numbered flow + full sequence diagram →")}</svg>')

def dsec(n):
    _,slug,folder,title,ana,_,color = L[n-1]
    return (f'\n<section class="dsec" id="l{n:02d}" style="--c:{color}">\n'
      f'  <h2><span class="ln">{n}</span> {title}</h2>\n  <p class="d">{ana}</p>\n  {SVG[n]}\n'
      f'  <p class="foot"><a href="{GH}/{slug}/lessons/{folder}/README.md">Read full lesson {n:02d} →</a></p>\n</section>\n')
ALL_DSECS = "".join(dsec(n) for n in range(1,9))

def card(n):
    _,slug,folder,title,ana,_,color = L[n-1]
    return (f'    <div class="lesson" style="--c:{color}"><div class="top"><span class="num">{n}</span><h3>{title}</h3></div>'
      f'<span class="ana">{ana}</span><code>{slug}</code>'
      f'<a class="go" href="{GH}/{slug}/lessons/{folder}/README.md">Read lesson →</a>'
      f'<a class="go" href="lesson-diagrams.html#l{n:02d}">See the diagram ↗</a></div>')

INDEX = head("Learn MCP the school way — with a real server & client",
  "8 lessons on the Model Context Protocol with a real zero-dependency server and client, plus 5 real-world use cases with flow and sequence diagrams.") + MARKER + f'''
<div class="wrap">
  <header>
    <h1>🔌 Learn MCP the school way</h1>
    <p class="sub">The Model Context Protocol — the standard plug between AI apps and the world —
    taught with a difference: <b>the protocol is IN the repo</b>. A real MCP server and a real
    host/client, ~200 lines of pure Python, zero dependencies. You read every byte that moves.</p>
    <div class="chips">
      <span class="chip">🤝 the handshake</span><span class="chip">🧰 tools/resources/prompts</span>
      <span class="chip">🔬 real server code</span><span class="chip">🔌 real client code</span>
      <span class="chip">🌍 5 use cases</span><span class="chip">🎼 sequence diagrams</span>
    </div>
  </header>

  <div class="vs">
    <div class="vcol" style="border-top:5px solid {P1}">
      <h3>📖 Part 1 — THE PROTOCOL (1–5)</h3>
      <ul>
        <li>the adapter drawer 🍝 → the standard socket 🔌</li>
        <li>rooms, sockets, instruments — who talks to whom</li>
        <li>three shelves; three verbs and a handshake 🤝</li>
        <li>stdio vs HTTP + the three trust rules 🚧</li>
      </ul>
    </div>
    <div class="vcol" style="border-top:5px solid {P2}">
      <h3>🔧 Part 2 — BUILD &amp; DEPLOY (6–8)</h3>
      <ul>
        <li>read a real server: 110 honest lines 🔬</li>
        <li>read a real host — where the power lives 🔌</li>
        <li>5 production-shaped use cases, drawn twice 🌍</li>
        <li>--drive mode: YOU play the model 🧠</li>
      </ul>
    </div>
  </div>

  <pre><code># the 60-second wow — the ENTIRE protocol, live:
git clone https://github.com/BaluRaut/learn-mcp-school.git &amp;&amp; cd learn-mcp-school
python3 client/mini_client.py          # watch every JSON-RPC message
python3 client/mini_client.py --drive  # YOU pick the tool calls</code></pre>

  <h2 id="big-picture">🗺️ The big picture — one diagram, both worlds</h2>
  <p class="sub">Click for the <a href="images/big-picture-4k.png">4K version</a>.</p>
  <figure style="background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;margin-top:16px">
    <a href="images/big-picture-4k.png"><img src="images/big-picture.svg" alt="The big picture: the MCP protocol, then building servers and clients and deploying five real-world use cases" loading="lazy" style="width:100%;height:auto;border-radius:8px;background:#fff"></a>
  </figure>

  <h2 id="lessons">🎓 The 8 lessons</h2>
  <p class="sub">One git branch = one idea; branch 05 contains lessons 01–05. Deep-dive companion to the
  <a href="https://baluraut.github.io/learn-ai-school/">AI course</a>'s bonus lesson 13.</p>
  <div class="grid">
{chr(10).join(card(n) for n in range(1,9))}
  </div>

  <div class="callout">🌍 <b>The showcase:</b> <a href="use-cases.html">5 real-world use cases</a> —
  coding assistant, support desk, data analyst, meeting-prep butler, report robot — each with a
  numbered flow diagram AND a full sequence diagram.</div>

  <h2 id="diagrams">📐 The lesson diagrams — follow the numbers</h2>
  <p class="sub">Purple = the protocol, orange = build &amp; deploy. Lessons 02, 04 and 07 are drawn as
  <b>sequence diagrams</b> — the natural language of protocols. Also on a
  <a href="lesson-diagrams.html">standalone page</a>.</p>
{ALL_DSECS}
  <a class="btn" href="{GH}/lesson-01-why-mcp/lessons/01-why-mcp/README.md">Start Lesson 01 →</a>
  <a class="btn alt" href="use-cases.html">🌍 The 5 use cases</a>
  <a class="btn alt" href="lesson-diagrams.html">📐 All 8 lesson diagrams</a>
  <a class="btn alt" href="https://baluraut.github.io/learn-ai-school/">🧠 The AI course</a>

  <footer>
    Learn MCP School · the protocol is in the repo ·
    <a href="https://github.com/BaluRaut/learn-mcp-school">github.com/BaluRaut/learn-mcp-school</a> ·
    spec &amp; SDKs: <a href="https://modelcontextprotocol.io">modelcontextprotocol.io</a> ·
    sibling: <a href="https://baluraut.github.io/learn-agents-school/">the Agents school</a> 📋
  </footer>
</div>
</body>
</html>
'''

DIAGRAMS = head("Lesson diagrams — Learn MCP School",
  "All 8 MCP lessons as numbered diagrams — including sequence diagrams of the wire.") + MARKER + f'''
<div class="wrap">
<header>
  <p><a href="index.html">← Back to the course home</a></p>
  <h1>📐 The 8 lessons as diagrams</h1>
  <p class="sub">Purple = the protocol (1–5) · orange = build &amp; deploy (6–8). Lessons 02, 04, 07
  are sequence diagrams — the natural language of protocols.</p>
  <nav class="toc">
    <a href="#l01">1 Why MCP</a><a href="#l02">2 Architecture</a><a href="#l03">3 Shelves</a>
    <a href="#l04">4 The wire</a><a href="#l05">5 Trust</a><a href="#l06">6 Server</a>
    <a href="#l07">7 Client</a><a href="#l08">8 Use cases</a>
  </nav>
</header>
{ALL_DSECS}
<footer>
  Learn MCP School · <a href="index.html">Course home</a> · <a href="use-cases.html">Use cases</a> ·
  <a href="https://github.com/BaluRaut/learn-mcp-school">GitHub</a>
</footer>
</div>
</body>
</html>
'''

# ---------- use cases: flow + sequence each ----------
def uc(idx, id_, color, title, story, flow_svg, seq_svg, why):
    return f'''
<section class="dsec" id="{id_}" style="--c:{color}">
  <h2><span class="ln">{idx}</span> {title}</h2>
  <p class="d">{story}</p>
  <p class="sub" style="margin-top:10px"><b>The flow, numbered:</b></p>
  {flow_svg}
  <p class="sub" style="margin-top:14px"><b>The sequence, message by message:</b></p>
  {seq_svg}
  <p class="d" style="margin-top:10px">💡 <b>Why MCP here:</b> {why}</p>
</section>'''

def flow(boxes, arrows, note=None, H=230):
    out = [f'<svg viewBox="0 0 940 {H}" role="img">']
    for (x,y,w,h,title,sub,n) in boxes:
        out.append(f'{B} x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>' + t(x+w//2, y+30, title) + (sm(x+w//2, y+54, sub) if sub else ""))
        if n: out.append(num(x, y, n))
    for (a,b,c,d,dash) in arrows:
        out.append(arr(a,b,c,d, DASH if dash else ""))
    if note: out.append(sm(470, H-12, note))
    out.append('</svg>')
    return "".join(out)

UC1_FLOW = flow(
 [(30,40,170,70,"🧑 'fix issue #42'","",1),(260,40,190,70,"🐙 get_issue","the complaint",2),
  (510,40,190,70,"📁 read_file","the code",3),(760,40,150,70,"🧪 run_tests","",4),
  (510,140,190,70,"🚧 'allow PR?'","the human gate",5),(760,140,150,70,"✅ PR created","",6)],
 [(200,75,256,75,0),(450,75,506,75,0),(700,75,756,75,0),(835,110,620,150,0),(700,175,756,175,0)],
 "one goal, three servers, one gate — the shape of every coding-agent story")
UC1_SEQ = seq(["🏫 IDE host","🧠 model","🐙 GitHub srv","📁 files srv"],
 [(0,1,1,"goal + tool shelves"),(1,2,2,"get_issue(42) — via host"),(2,1,3,"bug report → desk"),
  (1,3,4,"read_file(buggy.py)"),(3,1,5,"code → desk"),(1,0,6,"proposes create_pr(fix)"),
  ('note',"🚧 host asks the human: 'allow PR?' — click ✓"),(0,2,7,"create_pr → PR exists")])

UC2_FLOW = flow(
 [(30,40,200,70,"🧑 'where's my refund?'","",1),(300,40,190,70,"🗄️ orders DB","SELECT-only!",2),
  (550,40,190,70,"📚 docs server","refund policy",3),(300,140,440,70,"✅ grounded answer + receipts 🧾","open-book, MCP-style",4)],
 [(230,75,296,75,0),(490,75,546,75,0),(645,110,560,140,0),(395,110,395,136,0)],
 "RAG's open-book exam (AI course L10) wearing standard plugs")
UC2_SEQ = seq(["🎧 support app","🧠 model","🗄️ orders srv","📚 docs srv"],
 [(0,1,1,"customer question + shelves"),(1,2,2,"lookup_order(#8412) — read-only"),
  (2,1,3,"order status → desk"),(1,3,4,"get_policy('refunds')"),(3,1,5,"policy text → desk"),
  (1,0,6,"answer citing order + policy 🧾")],
 "the DB account behind the server can ONLY read — AWS course L03's least privilege")

UC3_FLOW = flow(
 [(30,40,220,70,"🧑 'best product last month?'","",1),(320,40,180,70,"🗄️ query_db","scoped account",2),
  (560,40,180,70,"📈 make_chart","",3),(320,140,420,70,"✅ numbers + picture","in the chat",4)],
 [(250,75,316,75,0),(500,75,556,75,0),(650,110,540,140,0)],
 "rich inputSchema (enums, read-only) is what keeps 'analyst' from becoming 'DROP TABLE' 😅")
UC3_SEQ = seq(["💬 chat app","🧠 model","🗄️ SQL srv","📈 chart srv"],
 [(0,1,1,"question + shelves"),(1,2,2,"query_db(SELECT top products…)"),(2,1,3,"rows → desk"),
  (1,3,4,"make_chart(rows, 'bar by region')"),(3,1,5,"chart image → desk"),(1,0,6,"summary + chart")])

UC4_FLOW = flow(
 [(30,40,200,70,"🧑 'prep me for the 3pm'","",1),(300,40,180,70,"📅 get_event","who + what",2),
  (540,40,180,70,"🏢 crm_lookup","the company",3),(300,140,180,70,"✉️ recent_threads","the history",4),
  (540,140,200,70,"📋 one tidy brief","",5)],
 [(230,75,296,75,0),(480,75,536,75,0),(390,110,390,136,0),(480,175,536,175,0)],
 "THREE servers, one room, one desk — the N+M payoff in a single request")
UC4_SEQ = seq(["🤖 assistant","🧠 model","📅 calendar","🏢 CRM","✉️ email"],
 [(0,1,1,"'prep me' + shelves"),(1,2,2,"get_event(3pm)"),(2,1,3,"attendees, agenda → desk"),
  (1,3,4,"crm_lookup(Acme)"),(3,1,5,"account notes → desk"),(1,4,6,"recent_threads(attendees)"),
  (4,1,7,"last emails → desk"),(1,0,8,"the brief 📋")])

UC5_FLOW = flow(
 [(30,40,190,70,"🧑 'summarize + post'","",1),(280,40,170,70,"📁 list_dir","",2),
  (510,40,170,70,"📄 read_file ×N","",3),(280,140,200,70,"🧠 summarize","on the desk",4),
  (540,140,200,70,"🚧 'post to #team?'","the gate",5),(770,140,140,70,"💬 posted","",6)],
 [(220,75,276,75,0),(450,75,506,75,0),(595,110,420,140,0),(480,175,536,175,0),(740,175,766,175,0)],
 "reads flowed freely; the ONE write waited for a click — L05's rule 3 in production")
UC5_SEQ = seq(["🤖 agent host","🧠 model","📁 files srv","💬 Slack srv"],
 [(0,1,1,"goal + shelves"),(1,2,2,"list_dir(reports/)"),(2,1,3,"7 files → desk"),
  (1,2,4,"read_file(each) — loop"),(2,1,5,"contents → desk"),(1,1,6,"writes the summary"),
  (1,0,7,"proposes slack_post(#team, summary)"),
  ('note',"🚧 human gate: 'post this?' — shown in full, click ✓"),(0,3,8,"slack_post → 💬 posted")])

USECASES = head("5 real-world use cases — Learn MCP School",
  "Five production-shaped MCP setups — coding assistant, support desk, data analyst, meeting prep, report robot — each with a numbered flow diagram and a full sequence diagram.") + MARKER + f'''
<div class="wrap">
<header>
  <p><a href="index.html">← Back to the course home</a></p>
  <h1>🌍 Five real-world use cases</h1>
  <p class="sub">Production-shaped MCP setups, each drawn twice: the <b>numbered flow</b> (what
  happens) and the <b>sequence diagram</b> (who says what to whom, in order). Every one is
  lesson 04's seven messages, repeated — read one wire, read them all. Companion to
  <a href="{GH}/lesson-08-use-cases/lessons/08-use-cases/README.md">lesson 08</a>.</p>
  <nav class="toc">
    <a href="#uc1">1 Coding assistant</a><a href="#uc2">2 Support desk</a>
    <a href="#uc3">3 Data analyst</a><a href="#uc4">4 Meeting prep</a><a href="#uc5">5 Report robot</a>
  </nav>
</header>
{uc(1,"uc1",P2,"🐙 The coding assistant — IDE + GitHub + files",
  "“Fix issue #42.” Read the complaint, read the code, run the tests, draft the PR — and the PR waits for a human click.",
  UC1_FLOW, UC1_SEQ,
  "the same GitHub server works in every IDE and agent — write once, plug in everywhere (L01's N+M).")}
{uc(2,"uc2",P2,"🎧 The support desk — orders DB + docs",
  "“Where's my refund?” Look up the order (read-only), fetch the policy, answer with receipts.",
  UC2_FLOW, UC2_SEQ,
  "grounding beats guessing (AI course L09) — and the read-only scoped account makes the worst case boring.")}
{uc(3,"uc3",P2,"📊 The data analyst — SQL + charts",
  "“Which product sold best last month, per region?” Query, chart, explain — in the chat.",
  UC3_FLOW, UC3_SEQ,
  "one SQL server serves every team's AI app; schema design (L06) is the guardrail.")}
{uc(4,"uc4",P2,"📅 The meeting-prep butler — calendar + CRM + email",
  "“Prep me for the 3 pm.” Event, company, threads — three servers braided into one brief.",
  UC4_FLOW, UC4_SEQ,
  "three integrations that used to be three custom projects are now three config lines.")}
{uc(5,"uc5",P2,"📁 The report robot — files + Slack",
  "“Summarize this folder's weekly reports and post to #team.” Reads flow; the one write gates.",
  UC5_FLOW, UC5_SEQ,
  "automation with a human gate on the only irreversible step — L05 rule 3, shipped.")}
<footer>
  Learn MCP School · <a href="index.html">Course home</a> ·
  <a href="lesson-diagrams.html">Lesson diagrams</a> ·
  <a href="https://github.com/BaluRaut/learn-mcp-school">GitHub</a>
</footer>
</div>
</body>
</html>
'''

import os
os.makedirs('docs', exist_ok=True)
open('docs/index.html','w').write(INDEX)
open('docs/lesson-diagrams.html','w').write(DIAGRAMS)
open('docs/use-cases.html','w').write(USECASES)
print("generated: index dsec =", INDEX.count('class="dsec"'),
      "| diagrams =", DIAGRAMS.count('class="dsec"'),
      "| use-case sections =", USECASES.count('class="dsec"'),
      "| sequence svgs =", USECASES.count('class="life"') and (INDEX+USECASES).count('<line class="life"'))
