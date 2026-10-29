---
title: "The AI stack, from sand to software"
date: "2026-10-12"
order: 7
category: "Field guides"
dek: "Eight layers between a grain of sand and the answer on your screen, who makes each one, and where the power sits."
---

Most AI news covers one layer at a time. Nvidia's earnings are about chips. A new Claude model is about models. A funding round for Cursor is about apps. Each story makes sense alone, but it's hard to see how they connect. I wanted one map of the whole thing, so I made one.

Here's the short version. **Sand becomes chips. Chips fill buildings. Buildings rent out compute. Compute runs models. Models power apps. Apps reach you.** Everything else is detail on one of those steps.

<svg viewBox="0 0 680 552" xmlns="http://www.w3.org/2000/svg" data-wide role="img" aria-label="The AI stack as eight layers. Software: applications, tooling, models, inference. Infrastructure: cloud, data centers. Hardware: chips and systems, manufacturing. A prompt travels down from you to the chips and the answer streams back up." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <style>
    .st-n{font:600 11px "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.08em;}
    .st-d{font:italic 400 10px "IBM Plex Mono",ui-monospace,monospace;fill:#a9a6b8;}
    .st-c{font:400 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#c4c0cf;}
    .st-z{font:600 8.5px "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.22em;}
    .st-k{font:400 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#c4c0cf;}
    .st-a{animation-duration:9s;animation-iteration-count:infinite;animation-timing-function:linear;}
    .st-down{animation-name:st-down;} .st-up{animation-name:st-up;}
    @keyframes st-down{0%{transform:translateY(0);opacity:0}3%{opacity:1}40%{transform:translateY(409.0px);opacity:1}45%{transform:translateY(409.0px);opacity:0}100%{transform:translateY(409.0px);opacity:0}}
    @keyframes st-up{0%,45%{transform:translateY(409.0px);opacity:0}50%{transform:translateY(409.0px);opacity:1}88%{transform:translateY(0);opacity:1}93%,100%{transform:translateY(0);opacity:0}}
    @keyframes st-work{0%,38%{opacity:0}42%,48%{opacity:1}52%,100%{opacity:0}}
    .st-work{animation-name:st-work;}
    @media (prefers-reduced-motion: reduce){.st-a{animation:none;}.st-pk{display:none;}}
    @keyframes st-l0{0%{opacity:0}5.7%{opacity:0}8.7%{opacity:1}12.7%{opacity:0}79.1%{opacity:0}82.1%{opacity:1}86.1%{opacity:0}100%{opacity:0}} .st-l0{animation-name:st-l0;}
    @keyframes st-l1{0%{opacity:0}10.5%{opacity:0}13.5%{opacity:1}17.5%{opacity:0}74.2%{opacity:0}77.2%{opacity:1}81.2%{opacity:0}100%{opacity:0}} .st-l1{animation-name:st-l1;}
    @keyframes st-l2{0%{opacity:0}15.3%{opacity:0}18.3%{opacity:1}22.3%{opacity:0}69.3%{opacity:0}72.3%{opacity:1}76.3%{opacity:0}100%{opacity:0}} .st-l2{animation-name:st-l2;}
    @keyframes st-l3{0%{opacity:0}20.1%{opacity:0}23.1%{opacity:1}27.1%{opacity:0}64.4%{opacity:0}67.4%{opacity:1}71.4%{opacity:0}100%{opacity:0}} .st-l3{animation-name:st-l3;}
    @keyframes st-l4{0%{opacity:0}26.1%{opacity:0}29.1%{opacity:1}33.1%{opacity:0}58.1%{opacity:0}61.1%{opacity:1}65.1%{opacity:0}100%{opacity:0}} .st-l4{animation-name:st-l4;}
    @keyframes st-l5{0%{opacity:0}30.9%{opacity:0}33.9%{opacity:1}37.9%{opacity:0}53.2%{opacity:0}56.2%{opacity:1}60.2%{opacity:0}100%{opacity:0}} .st-l5{animation-name:st-l5;}
    @keyframes st-l6{0%{opacity:0}37.0%{opacity:0}40.0%{opacity:1}44.0%{opacity:0}47.0%{opacity:0}50.0%{opacity:1}54.0%{opacity:0}100%{opacity:0}} .st-l6{animation-name:st-l6;}
  </style>
  <rect x="88" y="70" width="580" height="46" rx="5" fill="#262b4a" stroke="#8f8cab" stroke-opacity=".55" stroke-width="1"/>
  <rect class="st-a st-l0" x="88" y="70" width="580" height="46" rx="5" fill="#ff7a92" fill-opacity=".1" stroke="#ff7a92" stroke-width="1.3" opacity="0" style="filter:drop-shadow(0 0 6px #ff7a92)"/>
  <line x1="66" y1="93.0" x2="88" y2="93.0" stroke="#8f8cab" stroke-opacity=".5" stroke-dasharray="2 3"/>
  <text x="102" y="89" class="st-n" fill="#ff7a92">APPLICATIONS</text>
  <text x="204.8" y="89" class="st-d">what you actually touch</text>
  <text x="102" y="105" class="st-c">ChatGPT · Claude · Cursor · Cognition · HappyRobot · Bland · Harvey · Perplexity</text>
  <rect x="88" y="123" width="580" height="46" rx="5" fill="#262b4a" stroke="#8f8cab" stroke-opacity=".55" stroke-width="1"/>
  <rect class="st-a st-l1" x="88" y="123" width="580" height="46" rx="5" fill="#ff7a92" fill-opacity=".1" stroke="#ff7a92" stroke-width="1.3" opacity="0" style="filter:drop-shadow(0 0 6px #ff7a92)"/>
  <line x1="66" y1="146.0" x2="88" y2="146.0" stroke="#8f8cab" stroke-opacity=".5" stroke-dasharray="2 3"/>
  <text x="102" y="142" class="st-n" fill="#ff7a92">TOOLING</text>
  <text x="167.8" y="142" class="st-d">the glue between model and app</text>
  <text x="102" y="158" class="st-c">MCP · LangChain · Pinecone · Braintrust · Scale AI · Mercor</text>
  <rect x="88" y="176" width="580" height="46" rx="5" fill="#262b4a" stroke="#8f8cab" stroke-opacity=".55" stroke-width="1"/>
  <rect class="st-a st-l2" x="88" y="176" width="580" height="46" rx="5" fill="#ff7a92" fill-opacity=".1" stroke="#ff7a92" stroke-width="1.3" opacity="0" style="filter:drop-shadow(0 0 6px #ff7a92)"/>
  <line x1="66" y1="199.0" x2="88" y2="199.0" stroke="#8f8cab" stroke-opacity=".5" stroke-dasharray="2 3"/>
  <text x="102" y="195" class="st-n" fill="#ff7a92">MODELS</text>
  <text x="160.4" y="195" class="st-d">the brains, trained once at huge cost</text>
  <text x="102" y="211" class="st-c">Anthropic · OpenAI · Google DeepMind · Meta · xAI · Mistral · DeepSeek · Qwen</text>
  <rect x="88" y="229" width="580" height="46" rx="5" fill="#262b4a" stroke="#8f8cab" stroke-opacity=".55" stroke-width="1"/>
  <rect class="st-a st-l3" x="88" y="229" width="580" height="46" rx="5" fill="#ff7a92" fill-opacity=".1" stroke="#ff7a92" stroke-width="1.3" opacity="0" style="filter:drop-shadow(0 0 6px #ff7a92)"/>
  <line x1="66" y1="252.0" x2="88" y2="252.0" stroke="#8f8cab" stroke-opacity=".5" stroke-dasharray="2 3"/>
  <text x="102" y="248" class="st-n" fill="#ff7a92">INFERENCE</text>
  <text x="182.60000000000002" y="248" class="st-d">running a model, billions of times a day</text>
  <text x="102" y="264" class="st-c">Bedrock · Vertex · Azure Foundry · Together · Fireworks · Baseten · vLLM</text>
  <rect x="88" y="296" width="580" height="46" rx="5" fill="#262b4a" stroke="#8f8cab" stroke-opacity=".55" stroke-width="1"/>
  <rect class="st-a st-l4" x="88" y="296" width="580" height="46" rx="5" fill="#6fcfc0" fill-opacity=".1" stroke="#6fcfc0" stroke-width="1.3" opacity="0" style="filter:drop-shadow(0 0 6px #6fcfc0)"/>
  <line x1="66" y1="319.0" x2="88" y2="319.0" stroke="#8f8cab" stroke-opacity=".5" stroke-dasharray="2 3"/>
  <text x="102" y="315" class="st-n" fill="#6fcfc0">CLOUD</text>
  <text x="153.0" y="315" class="st-d">renting out compute by the hour</text>
  <text x="102" y="331" class="st-c">AWS · Microsoft Azure · Google Cloud · Oracle · CoreWeave · Nebius · Lambda</text>
  <rect x="88" y="349" width="580" height="46" rx="5" fill="#262b4a" stroke="#8f8cab" stroke-opacity=".55" stroke-width="1"/>
  <rect class="st-a st-l5" x="88" y="349" width="580" height="46" rx="5" fill="#6fcfc0" fill-opacity=".1" stroke="#6fcfc0" stroke-width="1.3" opacity="0" style="filter:drop-shadow(0 0 6px #6fcfc0)"/>
  <line x1="66" y1="372.0" x2="88" y2="372.0" stroke="#8f8cab" stroke-opacity=".5" stroke-dasharray="2 3"/>
  <text x="102" y="368" class="st-n" fill="#6fcfc0">DATA CENTERS</text>
  <text x="204.8" y="368" class="st-d">buildings full of chips, plus power</text>
  <text x="102" y="384" class="st-c">Stargate · Crusoe · Equinix · Vertiv · GE Vernova · your local utility</text>
  <rect x="88" y="416" width="580" height="46" rx="5" fill="#262b4a" stroke="#8f8cab" stroke-opacity=".55" stroke-width="1"/>
  <rect class="st-a st-l6" x="88" y="416" width="580" height="46" rx="5" fill="#ffb15c" fill-opacity=".1" stroke="#ffb15c" stroke-width="1.3" opacity="0" style="filter:drop-shadow(0 0 6px #ffb15c)"/>
  <line x1="66" y1="439.0" x2="88" y2="439.0" stroke="#8f8cab" stroke-opacity=".5" stroke-dasharray="2 3"/>
  <text x="102" y="435" class="st-n" fill="#ffb15c">CHIPS + SYSTEMS</text>
  <text x="227.0" y="435" class="st-d">GPUs and accelerators, wired into racks</text>
  <text x="102" y="451" class="st-c">Nvidia · AMD · Google TPU · AWS Trainium · Broadcom · Arm · Synopsys</text>
  <rect x="88" y="469" width="580" height="46" rx="5" fill="#262b4a" stroke="#8f8cab" stroke-opacity=".55" stroke-width="1"/>
  <text x="102" y="488" class="st-n" fill="#ffb15c">MANUFACTURING</text>
  <text x="212.2" y="488" class="st-d">turning sand into chips</text>
  <text x="102" y="504" class="st-c">TSMC · Samsung · Intel · ASML · SK Hynix · Micron · Applied Materials</text>
  <line x1="22" y1="72" x2="22" y2="273" stroke="#ff7a92" stroke-width="1.4" stroke-opacity=".8"/>
  <text x="14" y="172.5" class="st-z" fill="#ff7a92" text-anchor="middle" transform="rotate(-90 14 172.5)">SOFTWARE</text>
  <line x1="22" y1="298" x2="22" y2="393" stroke="#6fcfc0" stroke-width="1.4" stroke-opacity=".8"/>
  <text x="14" y="345.5" class="st-z" fill="#6fcfc0" text-anchor="middle" transform="rotate(-90 14 345.5)">INFRA</text>
  <line x1="22" y1="418" x2="22" y2="513" stroke="#ffb15c" stroke-width="1.4" stroke-opacity=".8"/>
  <text x="14" y="465.5" class="st-z" fill="#ffb15c" text-anchor="middle" transform="rotate(-90 14 465.5)">HARDWARE</text>
  <rect class="st-a st-work" x="88" y="416" width="580" height="46" rx="5" fill="#ffb15c" fill-opacity=".16" stroke="#ffb15c" stroke-width="1.6" opacity="0" style="filter:drop-shadow(0 0 10px #ffb15c)"/>
  <line x1="66" y1="30" x2="66" y2="439.0" stroke="#8f8cab" stroke-opacity=".6" stroke-width="1.1"/>
  <circle cx="66" cy="30" r="11" fill="#2b3054" stroke="#f3ece2" stroke-width="1.1"/>
  <text x="66" y="33.5" text-anchor="middle" class="st-k" style="fill:#f3ece2;font-size:9px">you</text>
  <circle cx="96" cy="26" r="4" fill="#ff7a92"/><text x="106" y="29" class="st-k">your prompt travels down</text>
  <circle cx="96" cy="42" r="4" fill="#fff4e6"/><text x="106" y="45" class="st-k">the answer streams back up, one token at a time</text>
  <g class="st-pk"><circle class="st-a st-down" cx="66" cy="30" r="5" fill="#ff7a92" style="filter:drop-shadow(0 0 5px #ff7a92)"/><circle class="st-a st-up" cx="66" cy="30" r="5" fill="#fff4e6" opacity="0" style="filter:drop-shadow(0 0 5px #fff4e6)"/></g>
  <text x="62" y="495.0" text-anchor="end" class="st-k" style="font-size:8px;fill:#a9a6b8">built</text>
  <text x="62" y="505.0" text-anchor="end" class="st-k" style="font-size:8px;fill:#a9a6b8">earlier</text>
  <line x1="66" y1="469" x2="66" y2="515" stroke="#ffb15c" stroke-opacity=".5" stroke-dasharray="1 3"/>
</svg>

Read it two ways. **Bottom to top** is how AI gets built: you can't have a model without a data center, or a data center without chips. **Top to bottom** is what happens when you use it. Say I ask Cursor to fix a bug. My prompt goes down through the layers until it reaches a chip, the chip does the math, and the answer comes back up one word at a time. The fab isn't on that path. It made the chip months earlier.

The eight layers fall into three groups. **Hardware** is physical stuff made in factories. **Infrastructure** is buildings, power, and the business of renting them out. **Software** is the models and everything built on them. Let's start at the bottom.

## Hardware

### 1. Manufacturing: turning sand into chips

A modern AI chip has more than 100 billion transistors, each smaller than a virus. Only a few factories on Earth can make them. These factories are called **fabs**, and a leading-edge one costs over $20 billion to build.

- **TSMC** (Taiwan) makes nearly every advanced AI chip, for Nvidia, AMD, Apple, Google, and Amazon. It also handles **advanced packaging** (called CoWoS), which bonds the chip to its memory. Packaging capacity has been one of the tightest bottlenecks in all of AI.
- **Samsung** and **Intel** are the only other companies trying to make chips at the frontier. Both are behind TSMC.
- **ASML** (Netherlands) is the only company in the world that makes **EUV lithography machines**, which are needed to print the smallest features. Each one costs well over $150 million and ships in pieces across several cargo planes. No ASML, no frontier chips.
- **Applied Materials, Lam Research, Tokyo Electron, and KLA** make the rest of the fab equipment: deposition, etching, inspection.
- **SK Hynix, Samsung, and Micron** make **HBM** (high-bandwidth memory), the fast memory stacked next to every AI chip. This matters more than it sounds. When a model writes an answer, it usually waits on memory, not on math.

**In one line:** a few companies, mostly in Taiwan, Korea, and the Netherlands, can make what everything else in this post depends on.

### 2. Chips and systems: designing the engines

Most chip companies don't own factories. They're **fabless**. Nvidia designs a chip, and TSMC makes it. The design layer is where the famous names live.

- **Nvidia** makes the GPUs that most AI runs on (Hopper, then Blackwell, now Rubin). Its real moat is **CUDA**, the software that nearly every AI engineer learned on. Switching chips means rewriting years of tools. Nvidia also sells the networking that ties thousands of chips together.
- **AMD** is the main GPU challenger with its Instinct line. It's credible, and its customers are mostly companies that want a second supplier.
- **Custom chips (ASICs)** are made by big companies for their own needs. Examples are **Google's TPU**, **Amazon's Trainium**, Meta's MTIA, and Microsoft's Maia. **Broadcom** and **Marvell** help design many of them. OpenAI is building one with Broadcom. Anthropic trains on three chip families (TPU, Trainium, and Nvidia), so no single supplier has all the leverage.
- **Specialists** like **Cerebras** and **Groq** build chips just for fast inference.
- **Arm** licenses the CPU designs inside many of these systems. **Synopsys** and **Cadence** make the software that all chip designers use to design chips.

A chip alone doesn't do much anymore. Nvidia's GB200 NVL72 is a full rack where 72 GPUs act like one giant chip. Companies like **Foxconn, Supermicro, and Dell** assemble those racks, and **Arista** and **Broadcom** make the network switches that connect racks together.

**In one line:** Nvidia sells the engine, and the biggest buyers are all building their own so they can buy less from Nvidia.

## Infrastructure

### 3. Data centers and power: buildings full of chips

An AI data center is mostly a power and cooling problem. The biggest new ones are measured in **gigawatts**. One gigawatt is about the power used by a city of 750,000 homes. Chips run so hot they're cooled with liquid instead of air.

- The **hyperscalers** (Microsoft, Google, Amazon, Meta) build their own, and each one spends tens of billions a year on it.
- **Stargate** is the OpenAI, Oracle, and SoftBank effort to build gigawatt-scale campuses, starting in Abilene, Texas.
- **Crusoe**, **Equinix**, and **Digital Realty** build and run data centers for others.
- **Vertiv** and **Schneider Electric** make the cooling and power gear. **GE Vernova** makes the gas turbines. Utilities and nuclear deals are now part of AI strategy.

**In one line:** the scarcest thing in AI right now often isn't chips, it's electricity hooked up to a building.

### 4. Cloud: renting out compute

Almost nobody buys their own chips. They rent them by the hour.

- **AWS, Microsoft Azure, and Google Cloud** are the big three. **Oracle** became a major AI cloud thanks to its OpenAI deals.
- **Neoclouds** like **CoreWeave**, **Nebius**, **Lambda**, and **Crusoe** are newer clouds built just for AI. They often get the newest Nvidia chips first.

There are two jobs this compute does, and the difference matters:

| | Training | Inference |
|---|---|---|
| What it is | Building the model | Using the model |
| How often | Once per model, over months | Every time anyone sends a prompt |
| Shape | One giant job on tens of thousands of chips | Billions of small jobs |
| Who pays | The lab | Everyone who uses AI |

Training gets the headlines. Inference is where most of the long-term spending goes, because it grows with every user.

## Software

### 5. Inference: running the model

When you send a prompt, a server loads the model's weights onto chips. The model then predicts the answer **one token at a time** (a token is about three quarters of a word). Each token is a full pass through billions of numbers. Doing this fast and cheap for millions of people at once is its own field.

- **The labs serve their own models.** The Claude API and the OpenAI API are inference businesses.
- **Clouds resell them.** **Amazon Bedrock, Google Vertex AI, and Azure AI Foundry** let companies use Claude, Gemini, Llama, and others inside the cloud they already pay for.
- **Inference specialists** like **Together AI, Fireworks, Baseten, and Modal** run open-weight models, and often custom ones, faster and cheaper.
- **Serving software** like **vLLM** and **SGLang** (open source) and Nvidia's **TensorRT-LLM** handles the tricks: batching many users onto one chip, and caching repeated prompts.

The price of inference is quoted per **million tokens**, and it keeps falling fast for the same level of intelligence. That's why apps that were too expensive two years ago are viable now.

**In one line:** inference is the meter that runs every time AI is used.

### 6. Models: the brains

A model is a big file of numbers called **weights**, learned by reading a huge amount of text, code, and images. Training a frontier model costs hundreds of millions of dollars or more in compute alone, which is why only a handful of labs do it.

- **Closed models** (you can use them but can't download them): **Anthropic** (Claude), **OpenAI** (GPT), **Google DeepMind** (Gemini), **xAI** (Grok).
- **Open-weight models** (anyone can download and run them): **Meta** (Llama), **Mistral**, **DeepSeek**, **Alibaba** (Qwen), **Moonshot** (Kimi). Chinese labs lead much of the open-weight work.
- **Specialized models** do one thing well, like **ElevenLabs** for voice, **Runway** for video, and **Midjourney** for images.

Labs compete on intelligence, but also on speed, price, safety, and how well a model uses tools. That last one matters most for agents.

**In one line:** a few labs make the brains, and everyone above them rents those brains by the token.

### 7. Tooling: the glue

This is everything between "I can call a model" and "I have a product that works." It's less famous but it's where many apps succeed or fail. I wrote more about this in my [cheat sheet on harnesses and evals](cheat-sheet.html).

- **Connecting models to the world:** **MCP** (Model Context Protocol, from Anthropic and now an open standard) lets a model use tools and data. Frameworks like **LangChain** and **LlamaIndex** wire up steps.
- **Memory and search:** vector databases like **Pinecone** let a model find the right documents before it answers. This is called retrieval, or RAG.
- **Evals and monitoring:** **Braintrust**, **LangSmith**, and **Arize** test whether the AI is doing the right thing, before and after launch.
- **Training data:** **Scale AI**, **Surge**, and **Mercor** supply expert humans who write and grade the data that teaches models.

**In one line:** models are smart but forgetful and disconnected, and tooling fixes that.

### 8. Applications: what you actually touch

This is the busiest layer by far, with thousands of companies. A few groups:

- **Assistants:** **ChatGPT**, **Claude**, **Gemini**, Meta AI. Here the lab is also the app.
- **Coding:** **Cursor** (an AI code editor), **Claude Code**, **Cognition** (makers of Devin, an AI engineer, and owners of Windsurf), **GitHub Copilot**, **Replit**, **Lovable**. Coding is the first category where AI is clearly doing real work at scale.
- **Voice agents:** **HappyRobot** makes AI agents that make phone calls for freight and logistics, like booking trucks and checking on loads. **Bland AI** builds phone agents for enterprises. **Sierra** and **Decagon** run customer service.
- **Vertical AI:** **Harvey** for law, **Abridge** for doctors' notes, **Hebbia** for finance, **Glean** for searching inside a company, **Perplexity** for web search.

People used to dismiss these as "wrappers" around someone else's model. That misses where the value is. A good app owns the workflow, the data, and the customer. Cursor understands your whole codebase. HappyRobot plugs into a broker's systems. Some apps, Cursor included, now train their own models too, so the line between layers keeps blurring.

**In one line:** apps turn a general brain into a specific job someone will pay for.

## Follow the money

Each layer is a customer of the one below it. When I pay for Cursor, a slice of that eventually reaches a Dutch company that makes the machines that print chips.

<svg viewBox="0 0 680 150" xmlns="http://www.w3.org/2000/svg" data-wide role="img" aria-label="Money flows down the stack: you pay Cursor a subscription, Cursor buys tokens from Anthropic, Anthropic buys compute from AWS, AWS buys GPUs from Nvidia, Nvidia buys wafers from TSMC, TSMC buys EUV tools from ASML." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <style>
    .mf-n{font:600 11px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .mf-s{font:400 9px "IBM Plex Mono",ui-monospace,monospace;}
    .mf-b{font:400 9px "IBM Plex Mono",ui-monospace,monospace;fill:#c4c0cf;}
    .mf-f{font:italic 400 10px "IBM Plex Mono",ui-monospace,monospace;fill:#a9a6b8;}
    @keyframes mf-go{0%{transform:translateX(0);opacity:0}6%{opacity:1}94%{opacity:1}100%{transform:translateX(576px);opacity:0}}
    .mf-c{animation:mf-go 7s linear infinite;}
    @media (prefers-reduced-motion: reduce){.mf-c{animation:none;display:none;}}
  </style>
  <rect x="14" y="14" width="82" height="52" rx="5" fill="#262b4a" stroke="#ff7a92" stroke-opacity=".75" stroke-width="1.2"/>
  <text x="55.0" y="37" text-anchor="middle" class="mf-n">You</text>
  <text x="55.0" y="53" text-anchor="middle" class="mf-s" fill="#ff7a92">$20 a month</text>
  <rect x="110" y="14" width="82" height="52" rx="5" fill="#262b4a" stroke="#ff7a92" stroke-opacity=".75" stroke-width="1.2"/>
  <text x="151.0" y="37" text-anchor="middle" class="mf-n">Cursor</text>
  <text x="151.0" y="53" text-anchor="middle" class="mf-s" fill="#ff7a92">app</text>
  <rect x="206" y="14" width="82" height="52" rx="5" fill="#262b4a" stroke="#ff7a92" stroke-opacity=".75" stroke-width="1.2"/>
  <text x="247.0" y="37" text-anchor="middle" class="mf-n">Anthropic</text>
  <text x="247.0" y="53" text-anchor="middle" class="mf-s" fill="#ff7a92">model</text>
  <rect x="302" y="14" width="82" height="52" rx="5" fill="#262b4a" stroke="#6fcfc0" stroke-opacity=".75" stroke-width="1.2"/>
  <text x="343.0" y="37" text-anchor="middle" class="mf-n">AWS</text>
  <text x="343.0" y="53" text-anchor="middle" class="mf-s" fill="#6fcfc0">cloud</text>
  <rect x="398" y="14" width="82" height="52" rx="5" fill="#262b4a" stroke="#ffb15c" stroke-opacity=".75" stroke-width="1.2"/>
  <text x="439.0" y="37" text-anchor="middle" class="mf-n">Nvidia</text>
  <text x="439.0" y="53" text-anchor="middle" class="mf-s" fill="#ffb15c">chips</text>
  <rect x="494" y="14" width="82" height="52" rx="5" fill="#262b4a" stroke="#ffb15c" stroke-opacity=".75" stroke-width="1.2"/>
  <text x="535.0" y="37" text-anchor="middle" class="mf-n">TSMC</text>
  <text x="535.0" y="53" text-anchor="middle" class="mf-s" fill="#ffb15c">fab</text>
  <rect x="590" y="14" width="82" height="52" rx="5" fill="#262b4a" stroke="#ffb15c" stroke-opacity=".75" stroke-width="1.2"/>
  <text x="631.0" y="37" text-anchor="middle" class="mf-n">ASML</text>
  <text x="631.0" y="53" text-anchor="middle" class="mf-s" fill="#ffb15c">machines</text>
  <line x1="55.0" y1="90" x2="631.0" y2="90" stroke="#8f8cab" stroke-opacity=".6" stroke-width="1.1"/>
  <line x1="55.0" y1="66" x2="55.0" y2="90" stroke="#8f8cab" stroke-opacity=".5" stroke-dasharray="2 3"/>
  <line x1="151.0" y1="66" x2="151.0" y2="90" stroke="#8f8cab" stroke-opacity=".5" stroke-dasharray="2 3"/>
  <line x1="247.0" y1="66" x2="247.0" y2="90" stroke="#8f8cab" stroke-opacity=".5" stroke-dasharray="2 3"/>
  <line x1="343.0" y1="66" x2="343.0" y2="90" stroke="#8f8cab" stroke-opacity=".5" stroke-dasharray="2 3"/>
  <line x1="439.0" y1="66" x2="439.0" y2="90" stroke="#8f8cab" stroke-opacity=".5" stroke-dasharray="2 3"/>
  <line x1="535.0" y1="66" x2="535.0" y2="90" stroke="#8f8cab" stroke-opacity=".5" stroke-dasharray="2 3"/>
  <line x1="631.0" y1="66" x2="631.0" y2="90" stroke="#8f8cab" stroke-opacity=".5" stroke-dasharray="2 3"/>
  <text x="103.0" y="110" text-anchor="middle" class="mf-b">a subscription</text>
  <path d="M99.0 86 l6 4 l-6 4" fill="none" stroke="#8f8cab" stroke-width="1.1"/>
  <text x="199.0" y="110" text-anchor="middle" class="mf-b">tokens</text>
  <path d="M195.0 86 l6 4 l-6 4" fill="none" stroke="#8f8cab" stroke-width="1.1"/>
  <text x="295.0" y="110" text-anchor="middle" class="mf-b">compute</text>
  <path d="M291.0 86 l6 4 l-6 4" fill="none" stroke="#8f8cab" stroke-width="1.1"/>
  <text x="391.0" y="110" text-anchor="middle" class="mf-b">GPUs</text>
  <path d="M387.0 86 l6 4 l-6 4" fill="none" stroke="#8f8cab" stroke-width="1.1"/>
  <text x="487.0" y="110" text-anchor="middle" class="mf-b">wafers</text>
  <path d="M483.0 86 l6 4 l-6 4" fill="none" stroke="#8f8cab" stroke-width="1.1"/>
  <text x="583.0" y="110" text-anchor="middle" class="mf-b">EUV tools</text>
  <path d="M579.0 86 l6 4 l-6 4" fill="none" stroke="#8f8cab" stroke-width="1.1"/>
  <circle class="mf-c" cx="55.0" cy="90" r="4.5" fill="#ffb15c" style="animation-delay:0.0s;filter:drop-shadow(0 0 4px #ffb15c)"/>
  <circle class="mf-c" cx="55.0" cy="90" r="4.5" fill="#ffb15c" style="animation-delay:-1.75s;filter:drop-shadow(0 0 4px #ffb15c)"/>
  <circle class="mf-c" cx="55.0" cy="90" r="4.5" fill="#ffb15c" style="animation-delay:-3.5s;filter:drop-shadow(0 0 4px #ffb15c)"/>
  <circle class="mf-c" cx="55.0" cy="90" r="4.5" fill="#ffb15c" style="animation-delay:-5.25s;filter:drop-shadow(0 0 4px #ffb15c)"/>
  <text x="340.0" y="138" text-anchor="middle" class="mf-f">every layer is a customer of the layer below it</text>
</svg>

This explains a lot of the news. When app usage grows, labs need more inference. Labs sign huge cloud deals. Clouds order more GPUs. Nvidia books record revenue. TSMC builds new fabs. ASML sells more machines. The whole stack is one supply chain, and demand starts at the top with people like me typing prompts.

## Who plays where

The giants don't stay in one layer. They spread across several, so they depend less on anyone else.

<svg viewBox="0 0 680 360" xmlns="http://www.w3.org/2000/svg" data-wide role="img" aria-label="Who plays at which layer. Google, Amazon and Microsoft span chips, data centers, cloud, inference, models and apps. Meta spans chips, data centers, models and apps. Nvidia is chips first with smaller bets above. OpenAI and Anthropic are models, inference and apps, building into data centers. Cursor is apps with its own models. TSMC is fabs only." style="width:100%;height:auto;display:block;margin:2rem 0;">
  <style>
    .pl-h{font:600 9px "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.06em;}
    .pl-r{font:600 11px "IBM Plex Mono",ui-monospace,monospace;fill:#f3ece2;}
    .pl-l{font:400 9.5px "IBM Plex Mono",ui-monospace,monospace;fill:#c4c0cf;}
  </style>
  <text x="165.0" y="32" text-anchor="middle" class="pl-h" fill="#ffb15c">FABS</text>
  <text x="231.0" y="32" text-anchor="middle" class="pl-h" fill="#ffb15c">CHIPS</text>
  <text x="297.0" y="32" text-anchor="middle" class="pl-h" fill="#6fcfc0">DATA CTR</text>
  <text x="363.0" y="32" text-anchor="middle" class="pl-h" fill="#6fcfc0">CLOUD</text>
  <text x="429.0" y="32" text-anchor="middle" class="pl-h" fill="#ff7a92">INFERENCE</text>
  <text x="495.0" y="32" text-anchor="middle" class="pl-h" fill="#ff7a92">MODELS</text>
  <text x="561.0" y="32" text-anchor="middle" class="pl-h" fill="#ff7a92">TOOLING</text>
  <text x="627.0" y="32" text-anchor="middle" class="pl-h" fill="#ff7a92">APPS</text>
  <line x1="18" y1="42" x2="660" y2="42" stroke="#8f8cab" stroke-opacity=".4"/>
  <rect x="12" y="52.0" width="654" height="30" fill="#ffffff" fill-opacity=".025"/>
  <text x="18" y="71.0" class="pl-r">Google</text>
  <circle cx="165.0" cy="67.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="231.0" cy="67.0" r="7" fill="#ffb15c" fill-opacity=".9"/>
  <circle cx="297.0" cy="67.0" r="7" fill="#6fcfc0" fill-opacity=".9"/>
  <circle cx="363.0" cy="67.0" r="7" fill="#6fcfc0" fill-opacity=".9"/>
  <circle cx="429.0" cy="67.0" r="7" fill="#ff7a92" fill-opacity=".9"/>
  <circle cx="495.0" cy="67.0" r="7" fill="#ff7a92" fill-opacity=".9"/>
  <circle cx="561.0" cy="67.0" r="6.3" fill="none" stroke="#ff7a92" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="627.0" cy="67.0" r="7" fill="#ff7a92" fill-opacity=".9"/>
  <text x="18" y="101.0" class="pl-r">Amazon</text>
  <circle cx="165.0" cy="97.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="231.0" cy="97.0" r="7" fill="#ffb15c" fill-opacity=".9"/>
  <circle cx="297.0" cy="97.0" r="7" fill="#6fcfc0" fill-opacity=".9"/>
  <circle cx="363.0" cy="97.0" r="7" fill="#6fcfc0" fill-opacity=".9"/>
  <circle cx="429.0" cy="97.0" r="7" fill="#ff7a92" fill-opacity=".9"/>
  <circle cx="495.0" cy="97.0" r="6.3" fill="none" stroke="#ff7a92" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="561.0" cy="97.0" r="6.3" fill="none" stroke="#ff7a92" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="627.0" cy="97.0" r="6.3" fill="none" stroke="#ff7a92" stroke-width="1.4" stroke-opacity=".85"/>
  <rect x="12" y="112.0" width="654" height="30" fill="#ffffff" fill-opacity=".025"/>
  <text x="18" y="131.0" class="pl-r">Microsoft</text>
  <circle cx="165.0" cy="127.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="231.0" cy="127.0" r="6.3" fill="none" stroke="#ffb15c" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="297.0" cy="127.0" r="7" fill="#6fcfc0" fill-opacity=".9"/>
  <circle cx="363.0" cy="127.0" r="7" fill="#6fcfc0" fill-opacity=".9"/>
  <circle cx="429.0" cy="127.0" r="7" fill="#ff7a92" fill-opacity=".9"/>
  <circle cx="495.0" cy="127.0" r="6.3" fill="none" stroke="#ff7a92" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="561.0" cy="127.0" r="6.3" fill="none" stroke="#ff7a92" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="627.0" cy="127.0" r="7" fill="#ff7a92" fill-opacity=".9"/>
  <text x="18" y="161.0" class="pl-r">Meta</text>
  <circle cx="165.0" cy="157.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="231.0" cy="157.0" r="6.3" fill="none" stroke="#ffb15c" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="297.0" cy="157.0" r="7" fill="#6fcfc0" fill-opacity=".9"/>
  <circle cx="363.0" cy="157.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="429.0" cy="157.0" r="6.3" fill="none" stroke="#ff7a92" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="495.0" cy="157.0" r="7" fill="#ff7a92" fill-opacity=".9"/>
  <circle cx="561.0" cy="157.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="627.0" cy="157.0" r="7" fill="#ff7a92" fill-opacity=".9"/>
  <rect x="12" y="172.0" width="654" height="30" fill="#ffffff" fill-opacity=".025"/>
  <text x="18" y="191.0" class="pl-r">Nvidia</text>
  <circle cx="165.0" cy="187.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="231.0" cy="187.0" r="7" fill="#ffb15c" fill-opacity=".9"/>
  <circle cx="297.0" cy="187.0" r="6.3" fill="none" stroke="#6fcfc0" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="363.0" cy="187.0" r="6.3" fill="none" stroke="#6fcfc0" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="429.0" cy="187.0" r="6.3" fill="none" stroke="#ff7a92" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="495.0" cy="187.0" r="6.3" fill="none" stroke="#ff7a92" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="561.0" cy="187.0" r="6.3" fill="none" stroke="#ff7a92" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="627.0" cy="187.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <text x="18" y="221.0" class="pl-r">OpenAI</text>
  <circle cx="165.0" cy="217.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="231.0" cy="217.0" r="6.3" fill="none" stroke="#ffb15c" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="297.0" cy="217.0" r="6.3" fill="none" stroke="#6fcfc0" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="363.0" cy="217.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="429.0" cy="217.0" r="7" fill="#ff7a92" fill-opacity=".9"/>
  <circle cx="495.0" cy="217.0" r="7" fill="#ff7a92" fill-opacity=".9"/>
  <circle cx="561.0" cy="217.0" r="6.3" fill="none" stroke="#ff7a92" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="627.0" cy="217.0" r="7" fill="#ff7a92" fill-opacity=".9"/>
  <rect x="12" y="232.0" width="654" height="30" fill="#ffffff" fill-opacity=".025"/>
  <text x="18" y="251.0" class="pl-r">Anthropic</text>
  <circle cx="165.0" cy="247.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="231.0" cy="247.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="297.0" cy="247.0" r="6.3" fill="none" stroke="#6fcfc0" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="363.0" cy="247.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="429.0" cy="247.0" r="7" fill="#ff7a92" fill-opacity=".9"/>
  <circle cx="495.0" cy="247.0" r="7" fill="#ff7a92" fill-opacity=".9"/>
  <circle cx="561.0" cy="247.0" r="6.3" fill="none" stroke="#ff7a92" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="627.0" cy="247.0" r="7" fill="#ff7a92" fill-opacity=".9"/>
  <text x="18" y="281.0" class="pl-r">Cursor</text>
  <circle cx="165.0" cy="277.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="231.0" cy="277.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="297.0" cy="277.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="363.0" cy="277.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="429.0" cy="277.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="495.0" cy="277.0" r="6.3" fill="none" stroke="#ff7a92" stroke-width="1.4" stroke-opacity=".85"/>
  <circle cx="561.0" cy="277.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="627.0" cy="277.0" r="7" fill="#ff7a92" fill-opacity=".9"/>
  <rect x="12" y="292.0" width="654" height="30" fill="#ffffff" fill-opacity=".025"/>
  <text x="18" y="311.0" class="pl-r">TSMC</text>
  <circle cx="165.0" cy="307.0" r="7" fill="#ffb15c" fill-opacity=".9"/>
  <circle cx="231.0" cy="307.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="297.0" cy="307.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="363.0" cy="307.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="429.0" cy="307.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="495.0" cy="307.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="561.0" cy="307.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="627.0" cy="307.0" r="1.4" fill="#8f8cab" fill-opacity=".5"/>
  <circle cx="24" cy="343" r="6" fill="#f3ece2" fill-opacity=".85"/><text x="36" y="347" class="pl-l">core business</text>
  <circle cx="154" cy="343" r="5.5" fill="none" stroke="#f3ece2" stroke-width="1.3"/><text x="166" y="347" class="pl-l">building it, or a smaller bet</text>
</svg>

**Google** is the most complete. It designs its own chips, runs its own cloud, trains Gemini, and puts it in front of billions of users. **OpenAI** and **Anthropic** started as model labs and now build apps on top and data centers below. **Nvidia** is moving up into clouds and models. Startups mostly do the opposite: they pick one layer and go deep.

## Where the power sits

The most useful thing I learned making this: **the lower you go, the fewer companies there are.**

At the top there are thousands of AI apps, and a new one launches every day. There are about a dozen serious model labs, a handful of big clouds, one dominant GPU maker, one leading-edge fab, and one EUV machine maker. Those single-supplier spots are the **choke points**:

- **ASML** for EUV machines.
- **TSMC** for making and packaging advanced chips.
- **Nvidia** for GPUs, protected by CUDA.
- **SK Hynix** and peers for HBM memory.
- **Power**, which no company can manufacture fast enough.

Higher up, power comes from different things. Labs win on research talent and compute. Apps win on knowing a customer's job better than anyone. It's easier to start a company there, and harder to defend one.

## The whole stack on one card

1. **Manufacturing:** TSMC makes the chips, using ASML's machines and Hynix's memory.
2. **Chips + systems:** Nvidia designs most of them. Google, Amazon, and others design their own.
3. **Data centers:** buildings full of chips. The limit is power.
4. **Cloud:** AWS, Azure, Google Cloud, and neoclouds rent that compute by the hour.
5. **Inference:** running models for every prompt, priced per million tokens.
6. **Models:** Anthropic, OpenAI, Google, and a few others train the brains.
7. **Tooling:** MCP, retrieval, evals, and data. The glue that makes a model useful.
8. **Applications:** Cursor, Cognition, HappyRobot, Bland, and thousands more turn the brains into jobs.

The names will change fast. The shape probably won't. Next time I read an AI headline, the first question I'll ask is which layer it's about, and who sits above and below it.
