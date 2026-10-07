---
title: "Your data is already a graph"
date: "2026-07-22"
order: 4
category: "Field guides"
dek: "Graph engineering explained with customer feedback: store the relationships, not just the rows, so the expensive judgments outlive the query."
---

Here's a question most feedback systems handle badly: **are the enterprise accounts complaining about setup in their reviews the same ones filing support tickets about it?**

You can answer it with a query. Then come the follow-ups: which of them renew soon? Who owns that part of the product? Each one is another query, and none of the answers build on each other. Six months later you have a folder of one-off SQL and still no picture of the problem.

The data was stored in a shape that throws away what matters most: what's connected to what.

## A row hides the connections

<svg viewBox="0 0 700 250" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="One row of customer feedback broken into the five things hiding inside it: the customer Acme Corp, the segment Enterprise, the evidence Review 812, the product area SSO setup, and the issue slow time-to-value. The row names all five and connects none of them." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <defs>
    <marker id="gr-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker>
    <marker id="gr-c" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#B01E36"/></marker>
  </defs>
  <style>
    .gr-sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#666;}
    .gr-smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .gr-band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .gr-acc{font:700 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#B01E36;}
    .gr-edge{font:600 8px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
  </style>
  <text x="350" y="14" text-anchor="middle" class="gr-band">ONE ROW · and the five things hiding inside it</text>
  <rect x="30" y="26" width="640" height="56" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <line x1="190" y1="26" x2="190" y2="82" stroke="#000" stroke-width="1"/>
  <line x1="350" y1="26" x2="350" y2="82" stroke="#000" stroke-width="1"/>
  <line x1="510" y1="26" x2="510" y2="82" stroke="#000" stroke-width="1"/>
  <text x="110" y="46" text-anchor="middle" class="gr-sm">CUSTOMER</text>
  <text x="110" y="66" text-anchor="middle" class="gr-smb">Acme Corp</text>
  <text x="270" y="46" text-anchor="middle" class="gr-sm">PLAN</text>
  <text x="270" y="66" text-anchor="middle" class="gr-smb">Enterprise</text>
  <text x="430" y="46" text-anchor="middle" class="gr-sm">RATING</text>
  <text x="430" y="66" text-anchor="middle" class="gr-smb">2 of 5</text>
  <text x="590" y="46" text-anchor="middle" class="gr-sm">WHAT THEY WROTE</text>
  <text x="590" y="66" text-anchor="middle" class="gr-smb">"SSO setup took us 3 days"</text>
  <line x1="350" y1="82" x2="350" y2="104" stroke="#000" stroke-width="1.2"/>
  <line x1="89" y1="104" x2="611" y2="104" stroke="#000" stroke-width="1.2"/>
  <line x1="89" y1="104" x2="89" y2="150" stroke="#000" stroke-width="1.2" marker-end="url(#gr-a)"/>
  <line x1="219.5" y1="104" x2="219.5" y2="150" stroke="#000" stroke-width="1.2" marker-end="url(#gr-a)"/>
  <line x1="350" y1="104" x2="350" y2="150" stroke="#000" stroke-width="1.2" marker-end="url(#gr-a)"/>
  <line x1="480.5" y1="104" x2="480.5" y2="150" stroke="#000" stroke-width="1.2" marker-end="url(#gr-a)"/>
  <line x1="611" y1="104" x2="611" y2="150" stroke="#000" stroke-width="1.2" marker-end="url(#gr-a)"/>
  <rect x="30" y="152" width="118" height="46" fill="#fff" stroke="#000" stroke-width="1.3"/>
  <text x="89" y="172" text-anchor="middle" class="gr-sm">CUSTOMER</text>
  <text x="89" y="187" text-anchor="middle" class="gr-smb">Acme Corp</text>
  <rect x="160.5" y="152" width="118" height="46" fill="#fff" stroke="#000" stroke-width="1.3"/>
  <text x="219.5" y="172" text-anchor="middle" class="gr-sm">SEGMENT</text>
  <text x="219.5" y="187" text-anchor="middle" class="gr-smb">Enterprise</text>
  <rect x="291" y="152" width="118" height="46" fill="#fff" stroke="#000" stroke-width="1.3"/>
  <text x="350" y="172" text-anchor="middle" class="gr-sm">EVIDENCE</text>
  <text x="350" y="187" text-anchor="middle" class="gr-smb">Review #812</text>
  <rect x="421.5" y="152" width="118" height="46" fill="#fff" stroke="#000" stroke-width="1.3"/>
  <text x="480.5" y="172" text-anchor="middle" class="gr-sm">PRODUCT AREA</text>
  <text x="480.5" y="187" text-anchor="middle" class="gr-smb">SSO setup</text>
  <rect x="552" y="152" width="118" height="46" fill="#fff" stroke="#000" stroke-width="1.3"/>
  <text x="611" y="172" text-anchor="middle" class="gr-sm">ISSUE</text>
  <text x="611" y="187" text-anchor="middle" class="gr-smb">Slow time-to-value</text>
  <text x="350" y="224" text-anchor="middle" class="gr-sm">The row names all five things. It records none of the connections between them.</text>
  <text x="350" y="240" text-anchor="middle" class="gr-acc">The connections are the part worth keeping.</text>
</svg>

Ten thousand rows like this contain thousands of customers and dozens of real issues, but the table only stores text that mentions them. Every analysis rebuilds the connections from scratch, then throws them away.

A graph stores them. **Nodes** are things: a customer, an issue, a review. **Edges** are relationships: *Acme* wrote *Review #812*, which is about *setup friction*. "These two complaints are the same problem" stops being a conclusion someone reaches and discards. It becomes an edge, written down once, dated, and correctable.

## The hard parts are judgment calls

Picking a database is easy. The engineering is in four decisions:

- **What gets to be a node.** If you'd ever want to count it, own it, or attach a decision to it, it's a node. Make "issue" a node and you can ask who owns it and whether it spans two products.
- **Which records are the same thing.** "Acme Corp," "ACME," and "acme.com" are one customer. A graph with three Acmes looks authoritative while getting every count wrong.
- **One meaning per edge.** A review can *mention* billing while being *about* onboarding. Blur those and every answer is too broad.
- **Who drew each edge.** Model-proposed or human-confirmed, with a confidence and a date, so a person can fix a wrong one.

## The question, answered

<svg viewBox="0 0 700 500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A graph traversal: two enterprise customers, Acme Corp and Globex, connect by WROTE and FILED edges to three pieces of evidence · two reviews and a support ticket. All three connect by IS_ABOUT edges, highlighted in red, to a single issue node: setup friction. That issue connects by an OWNED_BY edge to the onboarding area and the platform team. The answer is a three-hop walk that carries revenue along with it." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <defs>
    <marker id="g2-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker>
    <marker id="g2-c" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#B01E36"/></marker>
  </defs>
  <style>
    .g2-sm{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#666;}
    .g2-smb{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .g2-band{font:700 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .g2-acc{font:700 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#B01E36;}
    .g2-accs{font:400 8.5px "IBM Plex Mono",ui-monospace,monospace;fill:#B01E36;}
    .g2-edge{font:600 8px "IBM Plex Mono",ui-monospace,monospace;fill:#000;}
    .g2-edgec{font:600 8px "IBM Plex Mono",ui-monospace,monospace;fill:#B01E36;}
  </style>
  <text x="350" y="16" text-anchor="middle" class="g2-band">THE QUESTION · is it the same thing, in two different channels?</text>
  <text x="350" y="33" text-anchor="middle" class="g2-sm">two accounts · three pieces of evidence · one issue · one owner</text>

  <rect x="16" y="70" width="150" height="58" fill="#fff" stroke="#000" stroke-width="1.3"/>
  <text x="91" y="88" text-anchor="middle" class="g2-sm">CUSTOMER</text>
  <text x="91" y="103" text-anchor="middle" class="g2-smb">Acme Corp</text>
  <text x="91" y="118" text-anchor="middle" class="g2-sm">Enterprise · $840k</text>

  <rect x="16" y="250" width="150" height="58" fill="#fff" stroke="#000" stroke-width="1.3"/>
  <text x="91" y="268" text-anchor="middle" class="g2-sm">CUSTOMER</text>
  <text x="91" y="283" text-anchor="middle" class="g2-smb">Globex</text>
  <text x="91" y="298" text-anchor="middle" class="g2-sm">Enterprise · $1.2M</text>

  <rect x="250" y="54" width="150" height="44" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="325" y="72" text-anchor="middle" class="g2-sm">EVIDENCE</text>
  <text x="325" y="87" text-anchor="middle" class="g2-smb">Review #812</text>

  <rect x="250" y="130" width="150" height="44" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="325" y="148" text-anchor="middle" class="g2-sm">EVIDENCE</text>
  <text x="325" y="163" text-anchor="middle" class="g2-smb">Ticket #4471</text>

  <rect x="250" y="260" width="150" height="44" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="325" y="278" text-anchor="middle" class="g2-sm">EVIDENCE</text>
  <text x="325" y="293" text-anchor="middle" class="g2-smb">Review #903</text>

  <rect x="484" y="140" width="190" height="68" fill="#fff" stroke="#B01E36" stroke-width="2"/>
  <text x="579" y="162" text-anchor="middle" class="g2-sm">ISSUE</text>
  <text x="579" y="179" text-anchor="middle" class="g2-smb">Setup friction (SSO)</text>
  <text x="579" y="196" text-anchor="middle" class="g2-accs">2 accounts · $2.0M</text>

  <rect x="484" y="370" width="190" height="48" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="579" y="390" text-anchor="middle" class="g2-sm">ROUTES TO</text>
  <text x="579" y="405" text-anchor="middle" class="g2-smb">Onboarding · Platform</text>

  <line x1="166" y1="92" x2="250" y2="78" stroke="#000" stroke-width="1.2" marker-end="url(#g2-a)"/>
  <text x="208" y="78" text-anchor="middle" class="g2-edge">WROTE</text>
  <line x1="166" y1="110" x2="250" y2="150" stroke="#000" stroke-width="1.2" marker-end="url(#g2-a)"/>
  <text x="208" y="126" text-anchor="middle" class="g2-edge">FILED</text>
  <line x1="166" y1="281" x2="250" y2="282" stroke="#000" stroke-width="1.2" marker-end="url(#g2-a)"/>
  <text x="208" y="276" text-anchor="middle" class="g2-edge">WROTE</text>

  <line x1="400" y1="76" x2="484" y2="158" stroke="#B01E36" stroke-width="1.6" marker-end="url(#g2-c)"/>
  <text x="442" y="112" text-anchor="middle" class="g2-edgec">IS_ABOUT</text>
  <line x1="400" y1="152" x2="484" y2="172" stroke="#B01E36" stroke-width="1.6" marker-end="url(#g2-c)"/>
  <text x="442" y="156" text-anchor="middle" class="g2-edgec">IS_ABOUT</text>
  <line x1="400" y1="282" x2="484" y2="200" stroke="#B01E36" stroke-width="1.6" marker-end="url(#g2-c)"/>
  <text x="442" y="236" text-anchor="middle" class="g2-edgec">IS_ABOUT</text>

  <line x1="579" y1="208" x2="579" y2="368" stroke="#000" stroke-width="1.2" marker-end="url(#g2-a)"/>
  <text x="589" y="292" class="g2-edge">OWNED_BY</text>

  <line x1="20" y1="340" x2="20" y2="424" stroke="#B01E36" stroke-width="2.5"/>
  <text x="32" y="354" class="g2-acc">THE EDGE THAT DOES THE WORK</text>
  <text x="32" y="370" class="g2-sm">IS_ABOUT is a judgment: this evidence describes that</text>
  <text x="32" y="384" class="g2-sm">underlying problem. A model proposes it. A human confirms</text>
  <text x="32" y="398" class="g2-sm">it. It carries a date, a confidence, and a name.</text>
  <text x="32" y="418" class="g2-smb">Get that edge wrong and every count downstream is wrong.</text>

  <rect x="16" y="440" width="674" height="48" fill="#f3f3f3" stroke="#000" stroke-width="1.3"/>
  <text x="32" y="460" class="g2-band">THE ANSWER IS A WALK</text>
  <text x="32" y="477" class="g2-sm">customer → evidence → issue → owner. Three hops, no new schema, and the revenue rides along.</text>
</svg>

No custom query. The answer is a path through things that were already connected, and the next question is usually just one more step.

## Why now, and when not to

Graphs used to die because tagging documents by hand was too slow. Now a model proposes the nodes and edges, and a person checks them in seconds. And good AI retrieval needs structure: text that *sounds* similar isn't always *related*.

But graphs cost real effort. If your data is clean and nobody asks follow-up questions, use a table. Reach for a graph when the relationships are the point, and when someone needs to correct a judgment instead of re-running a query.
