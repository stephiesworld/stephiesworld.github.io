---
title: "Customer feedback, start to finish"
date: "2026-07-22"
order: 4
category: "Field guides"
dek: "What an AI first pass does to 10,000 pieces of feedback, why a person still reviews it, and why the answer belongs in a graph."
---

"AI triages customer feedback" sounds like either a toy that writes summaries nobody reads or a machine that replaces the operations team. It's neither. I built [Cherry](https://cherry-topaz.vercel.app) to find out what it actually is. The answer has three parts: the model compresses, a person corrects, and a graph remembers.

## The model compresses

Say a company gets 10,000 pieces of feedback in a week. The first pass turns that pile into a short list of issues, each with its evidence attached.

<svg viewBox="0 0 680 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A funnel: 10,000 raw records shrink to 8,500 with substance, 5,500 after deduplication, about 180 candidate clusters, about 40 new issues, and roughly 18 items a human deeply reads · 15 ambiguous clusters plus 3 escalations." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <style>
    .fn-n{font:700 13px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .fn-nw{font:700 13px "IBM Plex Mono",ui-monospace,monospace;fill:#fff4e6;}
    .fn-l{font:400 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#c4c0cf;}
    .fn-s{font:400 9px "IBM Plex Mono",ui-monospace,monospace;fill:#a9a6b8;}
  </style>
  <rect x="20" y="16" width="640" height="50" rx="5" fill="#262b4a" stroke="#8f8cab" stroke-width="1.2"/>
  <text x="340" y="38" text-anchor="middle" class="fn-n">10,000</text>
  <text x="340" y="54" text-anchor="middle" class="fn-l">raw records · one week, every channel</text>
  <line x1="340" y1="66" x2="340" y2="82" stroke="#8f8cab" stroke-width="1.1"/>
  <text x="354" y="78" class="fn-s">− 1,500 with nothing actionable</text>
  <rect x="70" y="82" width="540" height="50" rx="5" fill="#262b4a" stroke="#8f8cab" stroke-width="1.2"/>
  <text x="340" y="104" text-anchor="middle" class="fn-n">~8,500</text>
  <text x="340" y="120" text-anchor="middle" class="fn-l">contain something actionable</text>
  <line x1="340" y1="132" x2="340" y2="148" stroke="#8f8cab" stroke-width="1.1"/>
  <text x="354" y="144" class="fn-s">− 3,000 near-duplicates collapse</text>
  <rect x="125" y="148" width="430" height="50" rx="5" fill="#2b3054" stroke="#8f8cab" stroke-width="1.2"/>
  <text x="340" y="170" text-anchor="middle" class="fn-n">~5,500</text>
  <text x="340" y="186" text-anchor="middle" class="fn-l">substantive, after dedupe</text>
  <line x1="340" y1="198" x2="340" y2="214" stroke="#8f8cab" stroke-width="1.1"/>
  <text x="354" y="210" class="fn-s">semantic clustering, evidence attached</text>
  <rect x="220" y="214" width="240" height="50" rx="5" fill="#31365c" stroke="#8f8cab" stroke-width="1.2"/>
  <text x="340" y="236" text-anchor="middle" class="fn-n">~180</text>
  <text x="340" y="252" text-anchor="middle" class="fn-l">candidate clusters</text>
  <line x1="340" y1="264" x2="340" y2="280" stroke="#8f8cab" stroke-width="1.1"/>
  <text x="354" y="276" class="fn-s">120 attach to existing work instead</text>
  <rect x="265" y="280" width="150" height="50" rx="5" fill="#383d66" stroke="#8f8cab" stroke-width="1.2"/>
  <text x="340" y="302" text-anchor="middle" class="fn-n">~40</text>
  <text x="340" y="318" text-anchor="middle" class="fn-l">genuinely new issues</text>
  <line x1="340" y1="330" x2="340" y2="346" stroke="#8f8cab" stroke-width="1.1"/>
  <text x="354" y="342" class="fn-s">25 route with high confidence</text>
  <rect x="294" y="346" width="92" height="50" rx="5" fill="#6b2346" stroke="#8f8cab" stroke-width="1.2"/>
  <text x="340" y="376" text-anchor="middle" class="fn-nw">~18</text>
  <text x="400" y="368" class="fn-n" fill="#ff7a92">deeply read by humans</text>
  <text x="400" y="384" class="fn-l">15 ambiguous clusters + 3 escalations</text>
  <text x="20" y="426" class="fn-s">Bar widths are compressed · drawn to true scale, the bottom rows would be invisible, which is the point.</text>
  <text x="20" y="440" class="fn-s">Everything outside the red band gets sampled and audited rather than read.</text>
</svg>

Ordinary software handles the facts: counts, accounts, revenue, ticket IDs. The model makes one judgment: are these reports the same problem? It can fail two ways. **Missed duplicates** split one issue five ways. **False duplicates** are worse: five complaints that the product "forgets," with five different causes and owners, merged into one useless cluster.

## A person corrects

If the model is good enough to triage, why does a person still review it?

- **The model doesn't know what it was never told.** "Checkout is terrible" looks like a bug. The PM knows checkout was redesigned yesterday, on purpose.
- **Someone has to decide what good looks like.** "Customers hate pricing" might be three problems wearing one trench coat: a confusing page, surprise fees, and enterprise billing.
- **People are strange.** "I LOVE waiting 45 minutes for support" is not praise. So Cherry shows its least confident calls first.

<svg viewBox="0 0 680 230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Without correction: feedback to model to output, a straight line. With correction: the model proposes, a human edits, the edit is measured, and the improvement feeds back into the model's future behavior." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <defs>
    <marker id="ha" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#a7a3c4"/></marker>
    <marker id="hc" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#ff7a92"/></marker>
  </defs>
  <style>
    .hlbl{font:600 10px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .hsm{font:400 9px "IBM Plex Mono",ui-monospace,monospace;fill:#a9a6b8;}
  </style>
  <text x="8" y="20" class="hsm">WITHOUT CORRECTION · a line: tomorrow is exactly as good as today</text>
  <rect x="8" y="34" width="130" height="36" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="73" y="56" text-anchor="middle" class="hlbl">FEEDBACK</text>
  <line x1="138" y1="52" x2="188" y2="52" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#ha)"/>
  <rect x="190" y="34" width="130" height="36" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="255" y="56" text-anchor="middle" class="hlbl">MODEL</text>
  <line x1="320" y1="52" x2="370" y2="52" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#ha)"/>
  <rect x="372" y="34" width="130" height="36" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="437" y="56" text-anchor="middle" class="hlbl">OUTPUT</text>
  <text x="8" y="118" class="hsm" fill="#ff7a92">WITH CORRECTION · a loop: each fix also improves tomorrow</text>
  <rect x="8" y="132" width="118" height="36" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="67" y="154" text-anchor="middle" class="hlbl">FEEDBACK</text>
  <line x1="126" y1="150" x2="158" y2="150" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#ha)"/>
  <rect x="160" y="132" width="118" height="36" fill="#20253f" stroke="#8f8cab" stroke-width="1.5"/>
  <text x="219" y="149" text-anchor="middle" class="hlbl">MODEL</text>
  <text x="219" y="162" text-anchor="middle" class="hsm">proposes</text>
  <line x1="278" y1="150" x2="310" y2="150" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#ha)"/>
  <rect x="312" y="132" width="118" height="36" fill="#20253f" stroke="#ff7a92" stroke-width="2"/>
  <text x="371" y="149" text-anchor="middle" class="hlbl">HUMAN</text>
  <text x="371" y="162" text-anchor="middle" class="hsm">edits</text>
  <line x1="430" y1="150" x2="462" y2="150" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#ha)"/>
  <rect x="464" y="132" width="118" height="36" fill="#20253f" stroke="#8f8cab" stroke-width="1.5"/>
  <text x="523" y="149" text-anchor="middle" class="hlbl">MEASURE</text>
  <text x="523" y="162" text-anchor="middle" class="hsm">did the edit help?</text>
  <path d="M 582 168 C 620 210, 260 226, 219 172" fill="none" stroke="#ff7a92" stroke-width="1.6" marker-end="url(#hc)"/>
  <text x="400" y="216" text-anchor="middle" class="hsm" fill="#ff7a92">what helped becomes tomorrow's behavior · prompts, retrieval, evals</text>
</svg>

A correction you don't measure is just an opinion with edit access. I learned that the embarrassing way: Cherry's quality score once went *down* after a good correction, because applying it re-ran the whole triage and the grader was comparing two random drafts. Now a correction changes only what it needs to, and a falling correction rate means the system is learning.

## A graph remembers

Then come the follow-ups. Are the enterprise accounts complaining about setup in reviews the same ones filing tickets about it? Who owns that? In a table, every answer is a new query and none of them build on each other. In a graph, "these two complaints are the same problem" becomes an edge: written once, dated, and correctable.

<svg viewBox="0 0 700 500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A graph traversal: two enterprise customers, Acme Corp and Globex, connect by WROTE and FILED edges to three pieces of evidence · two reviews and a support ticket. All three connect by IS_ABOUT edges, highlighted in red, to a single issue node: setup friction. That issue connects by an OWNED_BY edge to the onboarding area and the platform team. The answer is a three-hop walk that carries revenue along with it." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <defs>
    <marker id="g2-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#a7a3c4"/></marker>
    <marker id="g2-c" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#ff7a92"/></marker>
  </defs>
  <style>
    .g2-sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#a9a6b8;}
    .g2-smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .g2-band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .g2-acc{font:700 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#ff7a92;}
    .g2-accs{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#ff7a92;}
    .g2-edge{font:600 8px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .g2-edgec{font:600 8px "IBM Plex Mono",ui-monospace,monospace;fill:#ff7a92;}
  </style>
  <text x="350" y="16" text-anchor="middle" class="g2-band">THE QUESTION · is it the same thing, in two different channels?</text>
  <text x="350" y="33" text-anchor="middle" class="g2-sm">two accounts · three pieces of evidence · one issue · one owner</text>

  <rect x="16" y="70" width="150" height="58" fill="#20253f" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="91" y="88" text-anchor="middle" class="g2-sm">CUSTOMER</text>
  <text x="91" y="103" text-anchor="middle" class="g2-smb">Acme Corp</text>
  <text x="91" y="118" text-anchor="middle" class="g2-sm">Enterprise · $840k</text>

  <rect x="16" y="250" width="150" height="58" fill="#20253f" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="91" y="268" text-anchor="middle" class="g2-sm">CUSTOMER</text>
  <text x="91" y="283" text-anchor="middle" class="g2-smb">Globex</text>
  <text x="91" y="298" text-anchor="middle" class="g2-sm">Enterprise · $1.2M</text>

  <rect x="250" y="54" width="150" height="44" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="325" y="72" text-anchor="middle" class="g2-sm">EVIDENCE</text>
  <text x="325" y="87" text-anchor="middle" class="g2-smb">Review #812</text>

  <rect x="250" y="130" width="150" height="44" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="325" y="148" text-anchor="middle" class="g2-sm">EVIDENCE</text>
  <text x="325" y="163" text-anchor="middle" class="g2-smb">Ticket #4471</text>

  <rect x="250" y="260" width="150" height="44" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="325" y="278" text-anchor="middle" class="g2-sm">EVIDENCE</text>
  <text x="325" y="293" text-anchor="middle" class="g2-smb">Review #903</text>

  <rect x="484" y="140" width="190" height="68" fill="#20253f" stroke="#ff7a92" stroke-width="2"/>
  <text x="579" y="162" text-anchor="middle" class="g2-sm">ISSUE</text>
  <text x="579" y="179" text-anchor="middle" class="g2-smb">Setup friction (SSO)</text>
  <text x="579" y="196" text-anchor="middle" class="g2-accs">2 accounts · $2.0M</text>

  <rect x="484" y="370" width="190" height="48" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="579" y="390" text-anchor="middle" class="g2-sm">ROUTES TO</text>
  <text x="579" y="405" text-anchor="middle" class="g2-smb">Onboarding · Platform</text>

  <line x1="166" y1="92" x2="250" y2="78" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#g2-a)"/>
  <text x="208" y="78" text-anchor="middle" class="g2-edge">WROTE</text>
  <line x1="166" y1="110" x2="250" y2="150" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#g2-a)"/>
  <text x="208" y="126" text-anchor="middle" class="g2-edge">FILED</text>
  <line x1="166" y1="281" x2="250" y2="282" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#g2-a)"/>
  <text x="208" y="276" text-anchor="middle" class="g2-edge">WROTE</text>

  <line x1="400" y1="76" x2="484" y2="158" stroke="#ff7a92" stroke-width="1.6" marker-end="url(#g2-c)"/>
  <text x="442" y="112" text-anchor="middle" class="g2-edgec">IS_ABOUT</text>
  <line x1="400" y1="152" x2="484" y2="172" stroke="#ff7a92" stroke-width="1.6" marker-end="url(#g2-c)"/>
  <text x="442" y="156" text-anchor="middle" class="g2-edgec">IS_ABOUT</text>
  <line x1="400" y1="282" x2="484" y2="200" stroke="#ff7a92" stroke-width="1.6" marker-end="url(#g2-c)"/>
  <text x="442" y="236" text-anchor="middle" class="g2-edgec">IS_ABOUT</text>

  <line x1="579" y1="208" x2="579" y2="368" stroke="#8f8cab" stroke-width="1.2" marker-end="url(#g2-a)"/>
  <text x="589" y="292" class="g2-edge">OWNED_BY</text>

  <line x1="20" y1="340" x2="20" y2="424" stroke="#ff7a92" stroke-width="2.5"/>
  <text x="32" y="354" class="g2-acc">THE EDGE THAT DOES THE WORK</text>
  <text x="32" y="370" class="g2-sm">IS_ABOUT is a judgment: this evidence describes that</text>
  <text x="32" y="384" class="g2-sm">underlying problem. A model proposes it. A human confirms</text>
  <text x="32" y="398" class="g2-sm">it. It carries a date, a confidence, and a name.</text>
  <text x="32" y="418" class="g2-smb">Get that edge wrong and every count downstream is wrong.</text>

  <rect x="16" y="440" width="674" height="48" fill="#262b4a" stroke="#8f8cab" stroke-width="1.3"/>
  <text x="32" y="460" class="g2-band">THE ANSWER IS A WALK</text>
  <text x="32" y="477" class="g2-sm">customer → evidence → issue → owner. Three hops, no new schema, and the revenue rides along.</text>
</svg>

The hard part isn't the database. It's deciding what gets to be a node, knowing that "Acme Corp," "ACME," and acme.com are one customer, keeping one meaning per edge, and recording who drew each edge so a person can fix it. If your data is clean and nobody asks follow-up questions, use a table.

## The job that's left

The first pass automates the reading, tagging, and copying. What's left for people is harder and better: deciding what good looks like, keeping the evals honest, and checking whether any of it changes what gets built.
