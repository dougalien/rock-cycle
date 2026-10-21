"""Content for the Rock Cycle explorer. Edit this file to tailor text to your course."""
from pathlib import Path
from urllib.parse import quote

COMMONS_FILE = "https://commons.wikimedia.org/wiki/File:"
COMMONS_PATH = "https://commons.wikimedia.org/wiki/Special:FilePath/"
PHOTO_DIR = Path(__file__).parent / "photos"    # built from "Rock Samples" by prepare_photos.py


def img_url(filename: str, width: int = 640) -> str:
    return f"{COMMONS_PATH}{quote(filename.replace(' ', '_'))}?width={width}"


def page_url(filename: str) -> str:
    return COMMONS_FILE + quote(filename.replace(" ", "_"))


# A rock has either `photos` (lab-sample photos: a list of (file in photos/, short label))
# or `file` + `license` (a Wikimedia Commons image). These helpers hide the difference.
def photo_count(rock: dict) -> int:
    return len(rock.get("photos", [None]))


def photo_label(rock: dict, n: int = 0) -> str:
    return rock["photos"][n][1] if rock.get("photos") else ""


def photo_src(rock: dict, n: int = 0, thumb: bool = False) -> str:
    """Path (lab photo) or URL (Wikimedia) to show for a rock. `thumb` gives the small version."""
    if rock.get("photos"):
        folder = PHOTO_DIR / "thumbs" if thumb else PHOTO_DIR
        return str(folder / rock["photos"][n][0])
    return img_url(rock["file"], 400 if thumb else 640)


def photo_caption(rock: dict, n: int = 0, with_label: bool = True) -> str:
    if rock.get("photos"):
        label = photo_label(rock, n)
        return f"{rock['name']} · lab sample" + (f": {label}" if with_label and label else "")
    return f"{rock['name']} · [{rock['license']} via Wikimedia Commons]({page_url(rock['file'])})"


# ---------------------------------------------------------------- rock types
GROUPS = {
    "Igneous": {
        "color": "#e4572e",
        "tagline": "Rock born from cooled magma or lava.",
        "intro": (
            "Igneous rocks form when molten rock cools and solidifies. The key question "
            "is *where* it cooled. Deep underground, cooling is slow, so crystals have "
            "time to grow large enough to see (**intrusive**, or *plutonic*). At the "
            "surface, lava cools fast, giving tiny crystals or even glass (**extrusive**, "
            "or *volcanic*)."
        ),
        "look_for": ["Interlocking crystals", "Crystal size (big = slow cooling)",
                     "Glassy shine or tiny gas bubbles", "No layers, no fossils"],
    },
    "Sedimentary": {
        "color": "#d4a24c",
        "tagline": "Rock built from pieces of other rocks, shells, or plants.",
        "intro": (
            "Sedimentary rocks form at or near Earth's surface. Sediment is weathered, "
            "transported, deposited, buried, and then **lithified** (turned to rock) by "
            "compaction and cementation. They are the rocks that most often hold "
            "**layers and fossils**, which makes them Earth's history books."
        ),
        "look_for": ["Layers (bedding)", "Rounded grains you can feel or see",
                     "Fossils or shell fragments", "Rock that scratches or crumbles easily"],
    },
    "Metamorphic": {
        "color": "#5b7db1",
        "tagline": "Rock changed, but not melted, by heat and pressure.",
        "intro": (
            "Metamorphic rocks start as any other rock (the **protolith**) and are "
            "transformed by heat, pressure, or hot fluids while staying solid. Minerals "
            "recrystallize and often line up into bands or sheets called **foliation**. "
            "If rock gets hot enough to melt, it has left metamorphism and become magma."
        ),
        "look_for": ["Banding or sparkly flat sheets (foliation)",
                     "Squashed or stretched grains", "Interlocking crystals, but aligned",
                     "Harder and denser than the original rock"],
    },
}

ROCKS = [
    # ---- igneous
    dict(name="Granite", group="Igneous",
         photos=[("granite-1.jpg", "pink granite, close-up"), ("granite-2.jpg", "whole sample")],
         subtype="Intrusive (slow cooling)",
         texture="Coarse crystals you can see, interlocked, often pink, white, and black speckles.",
         made_of="Quartz, feldspar, plus dark mica or amphibole.",
         formed="Magma cooled slowly, kilometers underground. Slow cooling = big crystals.",
         seen="Mountain cores (Sierra Nevada, Yosemite), countertops, gravestones.",
         lab_tip="Count the different minerals you can see. Can you find the glassy gray quartz?",
         origin_note="Often exposed only after overlying rock erodes away."),
    dict(name="Diorite", group="Igneous",
         photos=[("diorite-1.jpg", "salt-and-pepper crystals"), ("diorite-2.jpg", "water-worn cobble")],
         subtype="Intrusive (slow cooling)",
         texture="Coarse, salt-and-pepper speckles: light and dark crystals in roughly equal amounts, "
                 "with little or no pink feldspar or obvious quartz.",
         made_of="Plagioclase feldspar and amphibole (hornblende), sometimes with biotite or pyroxene.",
         formed="Magma of in-between composition cooled slowly underground, "
                "falling between granite and gabbro in both color and chemistry.",
         seen="Magma chambers under volcanic arcs like the Andes and Cascades; ancient sculpture and building stone.",
         lab_tip="Line up granite, diorite, and gabbro. Granite is paler and pinker, gabbro is darker. Where does diorite fall?",
         origin_note="Its fast-cooling twin is andesite, the typical lava of subduction-zone volcanoes."),
    dict(name="Gabbro", group="Igneous",
         photos=[("gabbro-1.jpg", "coarse and dark"), ("gabbro-2.jpg", "whole sample")],
         subtype="Intrusive (slow cooling)",
         texture="Coarse crystals, dark colored. Looks like a dark cousin of granite.",
         made_of="Pyroxene and plagioclase feldspar, with little or no quartz.",
         formed="The slow-cooled, underground version of basalt (same chemistry, different texture).",
         seen="Deep oceanic crust, large intrusions.",
         lab_tip="Compare with basalt: same ingredients, but how does the texture differ, and why?",
         origin_note="Gabbro and basalt show that cooling *rate* controls texture."),
    dict(name="Basalt", group="Igneous",
         photos=[("basalt-1.jpg", "dense and fine-grained"), ("basalt-2.jpg", "vesicular (gas holes)")],
         subtype="Extrusive (fast cooling)",
         texture="Fine-grained, dark gray to black. Often has small holes (vesicles) from gas bubbles.",
         made_of="Pyroxene, plagioclase feldspar, sometimes olivine.",
         formed="Lava erupted and cooled quickly at the surface, too fast for visible crystals.",
         seen="Hawaii, Iceland, ocean floor (the most common rock of the oceanic crust).",
         lab_tip="Try to see individual crystals. If you can't, that's your fast-cooling clue.",
         origin_note="The ocean floor is almost entirely basalt."),
    dict(name="Obsidian", group="Igneous", photos=[("obsidian-1.jpg", "volcanic glass")],
         subtype="Extrusive (very fast cooling)",
         texture="Smooth volcanic glass with curved (conchoidal) fracture and sharp edges.",
         made_of="Silica-rich glass, with no time to form crystals.",
         formed="Silica-rich lava cooled so fast that atoms never organized into crystals.",
         seen="Edges of rhyolite lava flows; used for ancient tools and arrowheads.",
         lab_tip="Look at how it breaks. Curved, shell-like fractures like broken bottle glass.",
         origin_note="Technically a glass, not a mineral rock."),
    dict(name="Pumice", group="Igneous", file="Dacitic pumice (Holocene, Mt. St Helens).jpg", license="CC0",
         subtype="Extrusive (frothy)",
         texture="Light, frothy, full of bubbles. Some pieces float on water!",
         made_of="Volcanic glass foam.",
         formed="Gas-rich lava exploded out of a volcano and cooled into a froth.",
         seen="Explosive eruptions (Mt. St. Helens); used as an abrasive.",
         lab_tip="If your lab allows, test whether it floats. What does that say about its density?",
         origin_note="Rafts of floating pumice can drift across oceans for years."),
    dict(name="Tuff", group="Igneous",
         photos=[("tuff-1.jpg", "tan, with rock fragments"), ("tuff-2.jpg", "pale and porous")],
         subtype="Extrusive (pyroclastic: volcanic ash)",
         texture="Light tan to gray, rough and lumpy, gritty and porous, often with chunks of pumice "
                 "or other rock stuck in a fine ashy matrix.",
         made_of="Compacted and cemented volcanic ash, with pieces of pumice and other rock.",
         formed="An explosive eruption blasted out ash and fragments that settled, then were welded or cemented into rock.",
         seen="Around explosive volcanoes: Yellowstone, Bandelier in New Mexico; Roman catacombs; Easter Island statues.",
         lab_tip="It can look sedimentary. What clues (pumice bits, glassy ash, no rounded river pebbles) say it is volcanic?",
         origin_note="Tuff sits on the border between igneous and sedimentary: volcanic material that was "
                     "deposited and cemented, much like sediment."),
    # ---- sedimentary
    dict(name="Sandstone", group="Sedimentary",
         photos=[("sandstone-1.jpg", "gritty surface"), ("sandstone-2.jpg", "side view")],
         subtype="Clastic (made of grains)",
         texture="Gritty, made of cemented sand grains; often shows layers or cross-bedding.",
         made_of="Mostly quartz grains, cemented by silica, calcite, or iron oxide.",
         formed="Sand from beaches, rivers, or dunes was buried and cemented.",
         seen="Utah's red rock country, Zion, Arches; buildings.",
         lab_tip="Rub it. Do grains come off? A hand lens shows rounded, sand-sized grains.",
         origin_note="Rounder grains suggest the sand traveled farther."),
    dict(name="Shale", group="Sedimentary",
         photos=[("shale-1.jpg", "thin layers splitting apart"), ("shale-2.jpg", "layered edge, close-up")],
         subtype="Clastic (very fine grains)",
         texture="Smooth, thin splitting layers. Grains are too small to see.",
         made_of="Clay and silt-sized particles.",
         formed="Mud settled in calm water (lakes, deep sea) and was compressed.",
         seen="The most common sedimentary rock; often contains fossils.",
         lab_tip="Try to split it along its layers. Slate does this too, so compare the two.",
         origin_note="Shale is the protolith (starting rock) of slate."),
    dict(name="Limestone", group="Sedimentary", file="Shell limestone 4.jpg", license="CC BY-SA 4.0",
         subtype="Chemical / biochemical",
         texture="Varies from fine and smooth to fossil-packed; fizzes with weak acid.",
         made_of="Calcite (calcium carbonate), often from shells and coral.",
         formed="Calcite from marine organisms and seawater accumulated on warm shallow sea floors.",
         seen="Caves, Great Pyramids, Indiana, Florida, Yucatán.",
         lab_tip="The acid fizz test is the classic limestone ID. Why does it bubble?",
         origin_note="Much of it is made from the remains of living things."),
    dict(name="Conglomerate", group="Sedimentary",
         photos=[("conglomerate-1.jpg", "pebbles in a finer matrix"), ("conglomerate-2.jpg", "drill core with large clasts")],
         subtype="Clastic (very coarse)",
         texture="Rounded pebbles and cobbles cemented in a finer matrix.",
         made_of="Rounded gravel from many rock types.",
         formed="Fast, energetic water (a river or beach) rounded gravel before burial.",
         seen="Old river channels and beaches turned to stone.",
         lab_tip="Look at the pebbles. Which rock types can you recognize from other samples?",
         origin_note="Rounded = traveled. Angular pebbles make a *breccia* instead."),
    dict(name="Coal", group="Sedimentary", file="Coal bituminous.jpg", license="Public domain",
         subtype="Organic",
         texture="Black, lightweight, often with a dull to shiny, banded look.",
         made_of="Compressed, carbon-rich plant material.",
         formed="Swamp plants were buried, and heat and pressure drove off water and gas.",
         seen="Appalachia, Wyoming; fuel for power plants.",
         lab_tip="Notice how light it feels compared to other rocks of the same size.",
         origin_note="With more heat and pressure, coal progresses toward metamorphic anthracite."),
    # ---- metamorphic
    dict(name="Slate", group="Metamorphic",
         photos=[("slate-1.jpg", "flat sheet, edge view"), ("slate-2.jpg", "smooth top surface")],
         subtype="Foliated (low grade)",
         texture="Dense, fine-grained, splits into flat smooth sheets.",
         made_of="Microscopic clay-derived minerals (mica and chlorite).",
         formed="Shale gently squeezed and warmed; tiny minerals aligned.",
         seen="Roof tiles, old chalkboards, flooring.",
         lab_tip="Tap it. Slate often rings, while shale thuds. Compare their splitting.",
         origin_note="Low-grade: the first step up from shale."),
    dict(name="Schist", group="Metamorphic",
         photos=[("schist-1.jpg", "mica sheen and dark crystals"), ("schist-2.jpg", "another view")],
         subtype="Foliated (medium grade)",
         texture="Sparkly, wavy sheets of visible mica flakes; sometimes with garnet crystals.",
         made_of="Mica, quartz, and often garnet, staurolite, or kyanite.",
         formed="Mud-rich rock buried deeper, hotter, and squeezed harder than slate.",
         seen="Mountain belts (New England, Scottish Highlands, Manhattan's bedrock).",
         lab_tip="Tilt it in the light and watch the mica flash. Find any larger crystals.",
         origin_note="Manhattan's skyscrapers rest on schist."),
    dict(name="Gneiss", group="Metamorphic",
         photos=[("gneiss-1.jpg", "light and dark bands"), ("gneiss-2.jpg", "foliation, another sample")],
         subtype="Foliated (high grade)",
         texture="Coarse bands of light and dark minerals (pronounced 'nice').",
         made_of="Quartz and feldspar (light bands), biotite or amphibole (dark bands).",
         formed="High heat and pressure segregated minerals into stripes. Close to melting.",
         seen="Cores of ancient mountain ranges and continental shields.",
         lab_tip="Do the bands look straight, wavy, or folded? What does that say about the squeezing?",
         origin_note="Can come from granite, shale, or other rocks."),
    dict(name="Marble", group="Metamorphic", file="Statuarietto White Marble (Apuan Marble Formation, Tertiary metamorphism of Jurassic limestones; Carrara region, Italy) 6 (40899027645).jpg", license="CC BY 2.0",
         subtype="Non-foliated",
         texture="Interlocking calcite crystals that give a sugary, sparkly look. No bands.",
         made_of="Calcite (or dolomite). Still fizzes in acid.",
         formed="Limestone recrystallized under heat; fossils and layers are usually erased.",
         seen="Sculptures (Michelangelo's David), monuments, countertops.",
         lab_tip="Run the acid test and compare limestone with marble. Same chemistry, different texture.",
         origin_note="Limestone → marble: same composition, new crystals."),
    dict(name="Quartzite", group="Metamorphic", file="Quartzite 2 jpg.jpg", license="Public domain",
         subtype="Non-foliated",
         texture="Very hard, glassy-looking, fused quartz grains; breaks through grains, not around them.",
         made_of="Nearly pure quartz.",
         formed="Quartz sandstone was heated until its grains and cement fused together.",
         seen="Ridges and mountain tops (resists weathering); countertops.",
         lab_tip="In sandstone, grains pop out. In quartzite, the break cuts right through them.",
         origin_note="Sandstone → quartzite: same composition, fused texture."),
]

ROCK_BY_NAME = {r["name"]: r for r in ROCKS}

# --------------------------------------------------------------- the cycle
STATES = {
    "Magma": dict(
        title="Magma / Lava",
        color="#f08a24",
        blurb="You are molten rock, a hot mix of liquid, dissolved gas, and a few crystals, "
              "at roughly 700-1,300 °C. Underground you're called magma; erupted onto the surface, lava.",
        image=("Pāhoehoe Lava flow.JPG", "Pāhoehoe lava in Hawaii", "CC BY-SA 3.0"),
        rock_group=None,
    ),
    "Igneous": dict(
        title="Igneous Rock",
        color=GROUPS["Igneous"]["color"],
        blurb="You have cooled and crystallized. Slowly and deep down, you'd be coarse like granite. "
              "Quickly at the surface, you'd be fine or glassy like basalt or obsidian.",
        image=None, rock_group="Igneous",
    ),
    "Sediment": dict(
        title="Sediment",
        color="#b08d57",
        blurb="You are loose pieces: sand, silt, mud, gravel, shells, dissolved minerals. "
              "Water, wind, and ice carry you downhill and eventually drop you somewhere.",
        image=("Mississippi River Delta, Louisiana (MODIS 2016-01-01).jpg",
               "Mississippi River delta from space: sediment pouring into the Gulf of Mexico", "Public domain (NASA)"),
        rock_group=None,
    ),
    "Sedimentary": dict(
        title="Sedimentary Rock",
        color=GROUPS["Sedimentary"]["color"],
        blurb="Layer upon layer buried you, squeezing out water (compaction) while minerals "
              "glued your grains together (cementation). You're now rock, and maybe holding fossils.",
        image=None, rock_group="Sedimentary",
    ),
    "Metamorphic": dict(
        title="Metamorphic Rock",
        color=GROUPS["Metamorphic"]["color"],
        blurb="You were buried deep or caught in a collision zone. Heat and pressure rearranged "
              "your minerals without melting you. You may be banded, sheeted, or sparkly.",
        image=None, rock_group="Metamorphic",
    ),
}

# From each state: (process, destination, explanation)
MOVES = {
    "Magma": [
        ("Cool and crystallize", "Igneous",
         "Heat leaks away into the surrounding rock or the air. Crystals grow and interlock. "
         "Slow cooling gives big crystals; fast cooling gives small crystals or glass."),
    ],
    "Igneous": [
        ("Weather and erode at the surface", "Sediment",
         "Uplift and erosion expose you. Rain, ice, roots, and temperature swings break you down "
         "(physical weathering) or alter your minerals (chemical weathering). Then water, wind, or ice carry the pieces away."),
        ("Get buried and squeezed (heat + pressure)", "Metamorphic",
         "Plate motions push you deep, or magma bakes you from the side. You stay solid, "
         "but your minerals recrystallize into new, stable forms."),
        ("Get buried so deep you melt", "Magma",
         "In subduction zones or hot spots, temperatures climb until minerals start to melt. "
         "You become magma again, recycled."),
    ],
    "Sediment": [
        ("Get buried, compacted, and cemented (lithification)", "Sedimentary",
         "New layers pile on top. Weight squeezes out water and shrinks pore space, while minerals "
         "like calcite or silica precipitate between grains and glue them."),
        ("Keep traveling", "Sediment",
         "Rivers, waves, glaciers, and wind keep moving you. Grains round off and sort by size as they go. "
         "Maybe you're deposited a little farther downstream."),
    ],
    "Sedimentary": [
        ("Get uplifted, weathered, and eroded", "Sediment",
         "Tectonic uplift lifts you to the surface, where weathering begins again. "
         "Today's sandstone may be tomorrow's sand."),
        ("Get buried deeper (heat + pressure)", "Metamorphic",
         "Burial or mountain building raises your temperature and pressure. "
         "Shale → slate, limestone → marble, sandstone → quartzite."),
        ("Get carried down and melted", "Magma",
         "Subduction drags you into the hot mantle, where you melt."),
    ],
    "Metamorphic": [
        ("Get uplifted, weathered, and eroded", "Sediment",
         "Mountains rise, erosion strips away the rock above, and exposed metamorphic rock "
         "breaks down into sediment."),
        ("Get even hotter and more squeezed", "Metamorphic",
         "More heat and pressure can increase the metamorphic grade, for example slate → schist → gneiss."),
        ("Melt", "Magma",
         "If temperature goes beyond the melting point of your minerals, the rock melts "
         "and becomes magma."),
    ],
}

# --------------------------------------------------------------- other pages
PROCESSES = [
    ("Weathering", "Breaking rock down in place.",
     "**Physical** weathering cracks rock apart (frost wedging, root growth, temperature swings). "
     "**Chemical** weathering changes minerals (rain slowly dissolves limestone; iron rusts). "
     "Neither involves movement of the pieces."),
    ("Erosion & transport", "Moving the pieces.",
     "Water, wind, ice, and gravity carry sediment. Longer trips mean rounder, smaller, better-sorted grains."),
    ("Deposition", "Dropping the load.",
     "When a river slows, wind dies down, or a glacier melts, sediment settles out. Layers build up in deltas, "
     "lakes, beaches, dunes, and the deep sea."),
    ("Lithification", "Turning sediment into rock.",
     "**Compaction** squeezes grains together; **cementation** glues them with minerals carried in groundwater."),
    ("Metamorphism", "Changing rock without melting it.",
     "Heat (from magma or depth), pressure (from burial or collisions), and hot fluids cause minerals to "
     "recrystallize and align."),
    ("Melting", "Making magma.",
     "Rock melts when temperature rises, pressure drops, or water is added (as in subduction zones). "
     "Melting is partial, so the magma has a different composition than the rock it came from."),
    ("Crystallization", "Making igneous rock.",
     "As magma or lava cools, atoms organize into mineral crystals. Cooling rate sets crystal size."),
    ("Uplift", "Raising rock to the surface.",
     "Plate tectonics lifts mountains and exposes deep rock. It is the quiet engine that keeps the cycle "
     "going, because without uplift, erosion would run out of rock."),
]

BIG_IDEAS = [
    "**It's a cycle, not a ladder.** Any rock type can become any other, and rocks can also skip steps or loop back.",
    "**Plate tectonics drives it.** Uplift, burial, and melting happen mostly at plate boundaries.",
    "**The sun and water drive the surface half.** Weathering, erosion, and deposition run on solar energy and gravity.",
    "**Earth's interior heat drives the deep half.** Metamorphism and melting run on geothermal energy.",
    "**It's slow.** Typical steps take thousands to millions of years. A full loop can take hundreds of millions.",
    "**Rocks keep a record.** Texture and minerals tell you how a rock formed: your lab observations are real detective work.",
]

GLOSSARY = {
    "Cementation": "Minerals precipitating between grains and gluing them together.",
    "Clastic": "Made of broken fragments (clasts) of earlier rocks.",
    "Compaction": "Squeezing of sediment under the weight of overlying layers.",
    "Crystal": "Orderly, repeating atomic arrangement of a mineral.",
    "Extrusive": "Igneous rock cooled at the surface (volcanic). Fine grained or glassy.",
    "Foliation": "Parallel alignment of minerals into layers or sheets in metamorphic rock.",
    "Intrusive": "Igneous rock cooled underground (plutonic). Coarse grained.",
    "Lithification": "The overall process of turning loose sediment into rock.",
    "Magma / Lava": "Molten rock underground / on the surface.",
    "Metamorphic grade": "How intense the metamorphism was. Low (slate) to high (gneiss).",
    "Mineral": "A naturally occurring, solid, inorganic crystal with a defined chemistry.",
    "Protolith": "The original rock before metamorphism.",
    "Sediment": "Loose particles from weathered rock, shells, or plants.",
    "Vesicle": "A small hole left by a gas bubble in volcanic rock.",
    "Weathering": "Breakdown of rock at Earth's surface.",
}
