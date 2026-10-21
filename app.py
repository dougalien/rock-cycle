"""The Rock Cycle: an exploration-style guide for introductory geology students.

Run with:  streamlit run app.py
"""
import random

import streamlit as st

import dougalien_brand as brand

from rock_data import (BIG_IDEAS, GLOSSARY, GROUPS, MOVES, PROCESSES, ROCK_BY_NAME,
                       ROCKS, STATES, img_url, photo_caption, photo_count, photo_label,
                       photo_src)

st.set_page_config(page_title="Explore the Rock Cycle", page_icon=brand.page_icon("🪨"), layout="wide")
brand.apply_branding()

PAGES = ["🏠 Welcome", "🔄 The Big Picture", "🖼️ Rock Gallery", "🧭 Take a Journey",
         "🔍 Rock Detective", "📖 Glossary"]

TIMESCALE = {
    "Igneous": "Lava can solidify in hours to years; magma deep underground takes thousands to millions of years.",
    "Sediment": "Weathering and erosion take thousands to millions of years.",
    "Sedimentary": "Burial and lithification take thousands to millions of years.",
    "Metamorphic": "Metamorphism usually takes millions of years.",
    "Magma": "Melting happens over millions of years, as rock is carried to depth.",
}

REFLECTIONS = [
    "Where on Earth might this be happening right now?",
    "What would you expect to see in a rock formed this way?",
    "Which force is doing the work here: the Sun and water, or Earth's internal heat?",
    "Could this rock have gone a different way? Which path would you try next time?",
    "How would a geologist tell this rock apart from the one you started with?",
]


# ------------------------------------------------------------------ helpers
def show_rock_image(rock, n=0, thumb=False, with_label=True):
    st.image(photo_src(rock, n, thumb), width="stretch")
    st.caption(photo_caption(rock, n, with_label))


def show_rock_photos(rock):
    """All photos of a rock: one image, or a tab per photo."""
    if photo_count(rock) == 1:
        show_rock_image(rock)
        return
    labels = [f"Photo {i + 1}: {photo_label(rock, i)}" if photo_label(rock, i) else f"Photo {i + 1}"
              for i in range(photo_count(rock))]
    for i, tab in enumerate(st.tabs(labels)):
        with tab:
            show_rock_image(rock, i, with_label=False)


def cycle_dot(highlight=None):
    def node(key, label, fill):
        pen = "3" if key == highlight else "1"
        color = "#111111" if key == highlight else "#666666"
        label = label.replace("|", "\\n")   # "|" marks a line break (no backslashes allowed inside f-string braces before Python 3.12)
        return (f'{key} [label="{label}", fillcolor="{fill}", color="{color}", penwidth={pen}];')

    return f"""
    digraph {{
      rankdir=LR; bgcolor="transparent"; nodesep=0.7; ranksep=1.0;
      node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=14, fontcolor="white", margin="0.25,0.15"];
      edge [fontname="Helvetica", fontsize=11, color="#777777", fontcolor="#999999"];
      {node("Magma", "Magma / Lava", STATES["Magma"]["color"])}
      {node("Igneous", "Igneous|Rock", STATES["Igneous"]["color"])}
      {node("Sediment", "Sediment", STATES["Sediment"]["color"])}
      {node("Sedimentary", "Sedimentary|Rock", STATES["Sedimentary"]["color"])}
      {node("Metamorphic", "Metamorphic|Rock", STATES["Metamorphic"]["color"])}
      Magma -> Igneous [label="cooling &\\ncrystallization"];
      Igneous -> Sediment [label="weathering,\\nerosion"];
      Sediment -> Sedimentary [label="compaction &\\ncementation"];
      Sedimentary -> Metamorphic [label="heat & pressure"];
      Igneous -> Metamorphic [label="heat & pressure"];
      Metamorphic -> Magma [label="melting"];
      Sedimentary -> Magma [label="melting", style=dashed];
      Igneous -> Magma [label="remelting", style=dashed];
      Sedimentary -> Sediment [label="uplift, weathering", style=dashed];
      Metamorphic -> Sediment [label="uplift, weathering", style=dashed];
    }}
    """


# ------------------------------------------------------------------- pages
def page_welcome():
    st.title("🪨 Explore the Rock Cycle")
    st.markdown(
        "Rocks are not permanent. Over millions of years, every rock is slowly being "
        "**made, broken, buried, cooked, melted, and made again**. This app is a place to "
        "wander through that story at your own pace. There are no grades and no quizzes, "
        "just things to look at and questions to think about."
    )
    c1, c2 = st.columns([3, 2])
    with c1:
        st.subheader("How to use this app")
        st.markdown(
            "- **🔄 The Big Picture**: see the whole cycle and what drives it.\n"
            f"- **🖼️ Rock Gallery**: meet {len(ROCKS)} common rocks, with photos and what to look for in lab.\n"
            "- **🧭 Take a Journey**: *become* a rock and choose your own path through the cycle.\n"
            "- **🔍 Rock Detective**: describe what you see in a sample and find candidates.\n"
            "- **📖 Glossary**: quick definitions.\n\n"
            "Use it alongside lecture and lab: look up the rocks you handled, then follow one on a journey."
        )
        st.info("Tip: start with **Take a Journey** if you like stories, or the **Gallery** if you like to look first.")
    with c2:
        for g, info in GROUPS.items():
            st.markdown(
                f"<div style='border-left:8px solid {info['color']};padding:6px 12px;margin-bottom:10px;"
                f"background:rgba(128,128,128,0.08)'><b>{g}</b><br>{info['tagline']}</div>",
                unsafe_allow_html=True)
    st.divider()
    cols = st.columns(3)
    for col, name in zip(cols, ["Granite", "Sandstone", "Gneiss"]):
        with col:
            show_rock_image(ROCK_BY_NAME[name], thumb=True)


def page_big_picture():
    st.title("🔄 The Big Picture")
    st.markdown(
        "Here is the whole cycle. **Solid arrows** are the classic loop; **dashed arrows** are the "
        "shortcuts that show it isn't one fixed circle. Almost any rock can go almost any direction."
    )
    st.graphviz_chart(cycle_dot(), width="stretch")

    st.subheader("Big ideas")
    for idea in BIG_IDEAS:
        st.markdown(f"- {idea}")

    st.subheader("Explore the processes")
    st.caption("Open any process to read more.")
    for name, short, long in PROCESSES:
        with st.expander(f"**{name}**: {short}"):
            st.markdown(long)

    st.subheader("Two engines, one cycle")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### ☀️ Surface engine\nSun, water, wind, ice and gravity break rock down, "
                    "move it, and build layers.")
        s = STATES["Sediment"]["image"]
        st.image(img_url(s[0]), caption=f"{s[1]} ({s[2]})", width="stretch")
    with c2:
        st.markdown("#### 🌋 Interior engine\nEarth's internal heat drives plate tectonics, volcanism, "
                    "metamorphism, and melting.")
        s = STATES["Magma"]["image"]
        st.image(img_url(s[0]), caption=f"{s[1]} ({s[2]})", width="stretch")


def page_gallery():
    st.title("🖼️ Rock Gallery")
    st.markdown("Pick a rock family, then a rock. Compare how **texture** reveals **how a rock formed**.")
    group = st.radio("Rock family", list(GROUPS), horizontal=True)
    info = GROUPS[group]
    st.markdown(f"<h4 style='color:{info['color']}'>{info['tagline']}</h4>", unsafe_allow_html=True)
    st.markdown(info["intro"])
    with st.expander("What to look for in this family"):
        for item in info["look_for"]:
            st.markdown(f"- {item}")

    rocks = [r for r in ROCKS if r["group"] == group]
    name = st.radio("Choose a rock", [r["name"] for r in rocks], horizontal=True, key=f"pick_{group}")
    rock = ROCK_BY_NAME[name]

    c1, c2 = st.columns([1, 1])
    with c1:
        show_rock_photos(rock)
    with c2:
        st.subheader(rock["name"])
        st.caption(rock["subtype"])
        st.markdown(f"**What it looks like:** {rock['texture']}")
        st.markdown(f"**Made of:** {rock['made_of']}")
        st.markdown(f"**How it formed:** {rock['formed']}")
        st.markdown(f"**Where you've seen it:** {rock['seen']}")
        st.success(f"🔬 **In the lab:** {rock['lab_tip']}")
        st.markdown(f"💡 *{rock['origin_note']}*")

    with st.expander("Compare all rocks in this family side by side"):
        per_row = 5
        for start in range(0, len(rocks), per_row):
            cols = st.columns(per_row)
            for col, r in zip(cols, rocks[start:start + per_row]):
                with col:
                    st.image(photo_src(r, thumb=True), caption=r["name"], width="stretch")


def init_journey(start):
    st.session_state.journey = [dict(state=start, rock=None, via=None)]
    st.session_state.journey_seed = random.randint(0, 10_000)


def page_journey():
    st.title("🧭 Take a Journey")
    st.markdown("Become a rock. At each step, choose what happens next. There is no right answer, "
                "and the same rock can end up in very different places. Try several journeys!")

    if "journey" not in st.session_state:
        start = st.selectbox("Where do you want to start?", list(STATES),
                             format_func=lambda k: STATES[k]["title"], index=0)
        if st.button("Begin journey ▶", type="primary"):
            init_journey(start)
            st.rerun()
        st.graphviz_chart(cycle_dot(), width="stretch")
        return

    journey = st.session_state.journey
    step = journey[-1]
    key = step["state"]
    state = STATES[key]

    # choose / remember an example rock for rock states
    if state["rock_group"] and step["rock"] is None:
        step["rock"] = random.Random(st.session_state.journey_seed + len(journey)).choice(
            [r["name"] for r in ROCKS if r["group"] == state["rock_group"]])

    left, right = st.columns([3, 2])
    with left:
        st.markdown(f"### Step {len(journey)}: you are {state['title']}")
        if step["via"]:
            st.caption(f"Because you: {step['via']}")
        st.markdown(f"<div style='border-left:8px solid {state['color']};padding:8px 14px;"
                    f"background:rgba(128,128,128,0.08)'>{state['blurb']}</div>", unsafe_allow_html=True)
        if step["rock"]:
            options = [r["name"] for r in ROCKS if r["group"] == state["rock_group"]]
            step["rock"] = st.selectbox("Which rock do you picture yourself as?", options,
                                        index=options.index(step["rock"]), key=f"rock_{len(journey)}")
            rock = ROCK_BY_NAME[step["rock"]]
            st.markdown(f"**{rock['name']}:** {rock['formed']}")
            st.caption(f"Look for: {rock['texture']}")
        if len(journey) > 1:
            st.caption("⏳ " + TIMESCALE[key])

        st.markdown("#### What happens next?")
        for i, (process, dest, why) in enumerate(MOVES[key]):
            with st.container(border=True):
                st.markdown(f"**{process}** → *{STATES[dest]['title']}*")
                st.caption(why)
                if st.button("Choose this", key=f"mv_{len(journey)}_{i}"):
                    journey.append(dict(state=dest, rock=None, via=process))
                    st.rerun()
        st.info("🤔 " + REFLECTIONS[(len(journey) + st.session_state.journey_seed) % len(REFLECTIONS)])

    with right:
        if step["rock"]:
            show_rock_image(ROCK_BY_NAME[step["rock"]])
        elif state["image"]:
            fn, cap, lic = state["image"]
            st.image(img_url(fn), caption=f"{cap} ({lic})", width="stretch")
        st.graphviz_chart(cycle_dot(highlight=key), width="stretch")

    st.divider()
    st.subheader("Your journey so far")
    log = []
    for n, s in enumerate(journey, 1):
        label = STATES[s["state"]]["title"] + (f" ({s['rock']})" if s["rock"] else "")
        log.append(f"{n}. {label}" + (f"  ← {s['via']}" if s["via"] else ""))
    st.markdown("\n".join(f"- {l}" for l in log))
    c1, c2, c3 = st.columns(3)
    if c1.button("⬅️ Undo last step", disabled=len(journey) < 2):
        journey.pop()
        st.rerun()
    if c2.button("🔁 Start a new journey"):
        del st.session_state.journey
        st.rerun()
    c3.download_button("💾 Save journey (text)", "\n".join(log), file_name="my_rock_journey.txt")


# Observations -> which rocks they point to
CLUES = {
    "I can see interlocking crystals": ["Granite", "Diorite", "Gabbro", "Marble", "Quartzite", "Schist", "Gneiss"],
    "The crystals are big and not lined up": ["Granite", "Diorite", "Gabbro"],
    "Salt-and-pepper speckles of light and dark crystals": ["Diorite", "Granite", "Gabbro"],
    "Lumpy and gritty, with bits of pumice or rock in a fine ashy matrix": ["Tuff", "Conglomerate"],
    "Light and dark minerals are in bands": ["Gneiss"],
    "Shiny mica flakes in wavy sheets": ["Schist", "Slate"],
    "Splits into thin flat sheets": ["Slate", "Shale", "Schist"],
    "Made of cemented sand-sized grains": ["Sandstone", "Quartzite"],
    "Rounded pebbles in a finer matrix": ["Conglomerate"],
    "Grains too fine to see": ["Shale", "Slate", "Basalt", "Obsidian"],
    "Glassy, breaks with curved surfaces": ["Obsidian"],
    "Full of holes or frothy": ["Pumice", "Basalt", "Tuff"],
    "Very light, might float": ["Pumice"],
    "Dark gray or black": ["Basalt", "Gabbro", "Coal", "Obsidian", "Slate"],
    "Fizzes with weak acid": ["Limestone", "Marble"],
    "Contains fossils or shells": ["Limestone", "Shale", "Sandstone", "Coal"],
    "Sugary, sparkly, no bands": ["Marble", "Quartzite"],
    "Extremely hard, breaks through the grains": ["Quartzite"],
    "Black, lightweight, can smudge": ["Coal"],
}


def page_detective():
    st.title("🔍 Rock Detective")
    st.markdown("Describe what you observe in a hand sample and see which rocks fit. "
                "This is a **thinking aid**, not an answer key. Real samples vary, so always confirm "
                "with your hand lens, acid, and your instructor.")
    picked = st.multiselect("What do you observe?", list(CLUES))
    if not picked:
        st.info("Choose one or more observations above to see candidate rocks.")
        return
    score = {}
    for obs in picked:
        for r in CLUES[obs]:
            score.setdefault(r, []).append(obs)
    ranked = sorted(score.items(), key=lambda kv: -len(kv[1]))[:4]
    st.subheader("Best matches")
    cols = st.columns(len(ranked))
    for col, (name, hits) in zip(cols, ranked):
        rock = ROCK_BY_NAME[name]
        with col:
            st.image(photo_src(rock, thumb=True), width="stretch")
            st.markdown(f"**{name}** · {rock['group']}")
            st.caption(f"Matches {len(hits)} of your {len(picked)} observations")
            for h in hits:
                st.markdown(f"- ✓ {h}")
            st.caption(f"Formed: {rock['formed']}")
    groups = {ROCK_BY_NAME[n]["group"] for n, _ in ranked}
    if len(groups) > 1:
        st.warning("Your matches span more than one rock family. What further test or observation "
                   "would help you decide between them? (Try texture: crystals, grains, or layers?)")


def page_glossary():
    st.title("📖 Glossary")
    q = st.text_input("Filter terms").lower()
    for term, definition in GLOSSARY.items():
        if q in term.lower() or q in definition.lower():
            st.markdown(f"**{term}**: {definition}")


# -------------------------------------------------------------------- main
st.sidebar.title("🪨 Rock Cycle")
page = st.sidebar.radio("Navigate", PAGES, label_visibility="collapsed")
st.sidebar.caption("Rock photos: lab samples, plus Wikimedia Commons (public domain / Creative Commons) "
                   "where noted. Click a Wikimedia caption for the source and license.")

{"🏠 Welcome": page_welcome, "🔄 The Big Picture": page_big_picture, "🖼️ Rock Gallery": page_gallery,
 "🧭 Take a Journey": page_journey, "🔍 Rock Detective": page_detective,
 "📖 Glossary": page_glossary}[page]()

