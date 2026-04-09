import json, urllib.request, urllib.parse, time, ssl, os, sys

OUTPUT = r"c:\Users\guigu\Desktop\mtg_deck_desc"
ctx = ssl.create_default_context()

DECKS = {
    "Ayara": {
        "commander": "Ayara, First of Locthwain",
        "cards": [
            "Abhorrent Overlord","Balthor the Defiled","Blood Artist","Bloodghast",
            "Carrion Feeder","Crypt Ghast","Cult Conscript","Dire Fleet Ravager",
            "Dread Presence","Endrek Sahr, Master Breeder","Fleshbag Marauder",
            "Forsaken Miner","Gatekeeper of Malakir","Gravecrawler","Gravedigger",
            "Grave Titan","Gray Merchant of Asphodel","Gwenom, Remorseless",
            "Josu Vess, Lich Knight","Midnight Reaper","Mirkwood Bats",
            "Murderous Rider","Oathsworn Vampire","Ogre Slumlord","Phyrexian Rager",
            "Pitiless Plunderer","Plaguecrafter","Ravenous Chupacabra",
            "Reassembling Skeleton","Sheoldred, Whispering One","Shriekmaw",
            "Skeletal Changeling","Starscape Cleric","Twilight Diviner",
            "Zulaport Cutthroat",
            "Army of the Damned","Dread Return","Exsanguinate","Feed the Swarm",
            "Invoke Despair","Mutilate","Reanimate",
            "Dark Ritual","Go for the Throat","Soul Shatter","Vona's Hunger",
            "Aetherflux Reservoir","Arcane Signet","Ashnod's Altar",
            "Bontu's Monument","Charcoal Diamond","Mimic Vat","Mind Stone",
            "Skullclamp","Sol Ring","Vat of Rebirth","Wayfarer's Bauble",
            "Curse of Shallow Graves","Meathook Massacre II","Phyrexian Arena",
            "Phyrexian Reclamation","Sanguine Bond"
        ]
    },
    "Ellivere": {
        "commander": "Ellivere of the Wild Court",
        "cards": [
            "Argothian Enchantress","Aura Gnarlid","Celestial Ancient",
            "Eidolon of Countless Battles","Heliod's Pilgrim","Herald of the Pantheon",
            "Kor Spiritdancer","Mesa Enchantress","Satyr Enchanter",
            "Setessan Champion","Shalai, Voice of Plenty","Siona, Captain of the Pyleas",
            "Sram, Senior Edificer","Sythis, Harvest's Hand","Umbra Mystic",
            "Verduran Enchantress","Archon of Sun's Grace","Destiny Spinner",
            "Transcendent Envoy","Tuvasa the Sunlit","Yavimaya Enchantress",
            "Katilda, Dawnhart Martyr","Dragonlord Dromoka","Danitha Capashen, Paragon",
            "All That Glitters","Ancestral Mask","Angelic Destiny","Armadillo Cloak",
            "Battle Mastery","Bear Umbra","Daybreak Coronet","Ethereal Armor",
            "Flickering Ward","Gift of Paradise","Gryff's Boon","Holy Mantle",
            "Keen Sense","Mantle of the Ancients","On Serra's Wings",
            "Rancor","Sage's Reverie","Season of Growth","Shield of the Oversoul",
            "Shielded by Faith","Sigarda's Aid","Spirit Mantle","Smothering Tithe",
            "Snake Umbra","Spider Umbra","Staggering Insight","Unquestioned Authority",
            "Utopia Sprawl","Wild Growth",
            "Unfinished Business","Winds of Rath",
            "Path to Exile","Generous Gift",
            "Sol Ring","Arcane Signet"
        ]
    },
    "Hydra": {
        "commander": "Gargos, Vicious Watcher",
        "cards": [
            "Elvish Mystic","Fyndhorn Elves","Gyre Sage","Incubation Druid",
            "Llanowar Elves","Llanowar Tribe","Marwyn, the Nurturer",
            "Kalonian Hydra","Primordial Hydra","Hooded Hydra","Hydra Omnivore",
            "Lifeblood Hydra","Ulvenwald Hydra","Voracious Hydra","Genesis Hydra",
            "Managorger Hydra","Mistcutter Hydra","Oran-Rief Hydra",
            "Polukranos, World Eater","Protean Hydra","Savageborn Hydra",
            "Steelbane Hydra","Heroes' Bane","Hydra Broodmaster",
            "Hungering Hydra","Rishkar, Peema Renegade","Wildborn Preserver",
            "Beanstalk Giant","Whisperer of the Wilds","Nyxbloom Ancient",
            "Fertilid",
            "Cultivate","Kodama's Reach","Nature's Lore","Rishkar's Expertise",
            "Traverse the Outlands",
            "Solidarity of Heroes","Invigorating Surge","Snakeskin Veil",
            "Tamiyo's Safekeeping","Heroic Intervention","Inspiring Call",
            "Untamed Might","Aspect of Hydra","Momentous Fall","Ram Through",
            "Tyvar's Stand","Hunter's Prowess","Inscription of Abundance",
            "Hardened Scales","Hydra's Growth","Unbound Flourishing",
            "Zendikar Resurgent","Garruk's Uprising","Rancor",
            "Branching Evolution","Retreat to Kazandu","Evolutionary Escalation",
            "Greater Good",
            "Sol Ring","Swiftfoot Boots","Rhonas's Monument","The Great Henge"
        ]
    },
    "Jasper": {
        "commander": "Laughing Jasper Flint",
        "cards": [
            "Etali, Primal Storm","Gonti, Lord of Luxury","Gonti, Canny Acquisitor",
            "Brainstealer Dragon","Elder Brain","Grenzo, Havoc Raiser",
            "Thieving Amalgam","Dauthi Voidwalker","Dire Fleet Daredevil",
            "Dream Pillager","Grim Hireling","Hoskuld, Ravenous Butcher",
            "Karazikar, the Eye Tyrant","Mindclaw Shaman","Nightmare Unmaker",
            "Ogre Battlecaster","Plargg, Dean of Chaos","Ragavan, Nimble Pilferer",
            "Robber of the Rich","Tasha, the Witch Queen",
            "Fevered Suspicion","Ghastly Conscription","Heartless Conscription",
            "Xander's Pact","Sins of the Past","Knowledge Exploitation",
            "Praetor's Grasp","Acquire","Bribery","Reanimate","Beacon of Unrest",
            "Share the Spoils",
            "Bedevil","Chaos Warp","Hurl Through Hell","Outrageous Robbery",
            "Rakdos Charm","Thrilling Encore","Stunning Reversal",
            "Sol Ring","Arcane Signet","Chromatic Lantern","Commander's Sphere",
            "Darksteel Ingot","Fellwar Stone","Gilded Lotus","Rakdos Signet",
            "Talisman of Indulgence","Thran Dynamo","Whispersilk Cloak",
            "Swiftfoot Boots","Lightning Greaves","Mind Stone","Thought Vessel",
            "Hedron Archive","Worn Powerstone",
            "At Knifepoint","Cunning Rhetoric","Dead Man's Chest",
            "Stolen Strategy","Sticky Fingers","Minion's Return"
        ]
    },
    "Terra": {
        "commander": "Terra, Herald of Hope",
        "cards": [
            "Karmic Guide","Luminous Broodmoth","Puppeteer Clique",
            "Sun Titan","Solemn Simulacrum","Cavalier of Dawn","Cavalier of Night",
            "Combustible Gearhulk","Noxious Gearhulk","Cataclysmic Gearhulk",
            "Plaguecrafter","Fleshbag Marauder","Merciless Executioner",
            "Ravenous Chupacabra","Shriekmaw","Massacre Wurm","Siege-Gang Commander",
            "Murderous Redcap","Recruiter of the Guard","Imperial Recruiter",
            "Reveillark","Knight of the White Orchid","Burnished Hart",
            "Gray Merchant of Asphodel","Kokusho, the Evening Star",
            "Anger","Dockside Extortionist","Grim Haruspex","Midnight Reaper",
            "Archon of Cruelty","Blood Artist","Zulaport Cutthroat",
            "Fiend Hunter","Skullclamp","Syr Konrad, the Grim",
            "Pitiless Plunderer","Corpse Knight","Cruel Celebrant",
            "Elenda, the Dusk Rose","Vindictive Vampire","Butcher of Malakir",
            "Yawgmoth, Thran Physician","Vilis, Broker of Blood",
            "Mikaeus, the Unhallowed",
            "Buried Alive","Reanimate","Rise of the Dark Realms",
            "Ruinous Ultimatum","Victimize","Living Death","Unburial Rites",
            "Crackling Doom","Path to Exile","Swords to Plowshares",
            "Teferi's Protection",
            "Sol Ring","Arcane Signet","Orzhov Signet","Rakdos Signet",
            "Swiftfoot Boots","Boros Signet","Talisman of Conviction",
            "Goblin Bombardment"
        ]
    },
    "Suspend": {
        "commander": "Alaundo the Seer",
        "cards": [
            "Aphetto Alchemist","Kiora's Follower","Seeker of Skybreak",
            "Seedborn Muse","Thassa's Oracle","Psychosis Crawler",
            "Hullbreaker Horror","Fatestitcher","Vizier of Tumbling Sands",
            "Clever Conjurer","Kelpie Guide","Brinelin, the Moon Kraken",
            "Tidespout Tyrant","Teferi, Mage of Zhalfir","Jhoira of the Ghitu",
            "Rashmi, Eternities Crafter","Parcelbeast","Lonis, Cryptozoologist",
            "Sakashima of a Thousand Faces","Spark Double",
            "Ancestral Vision","Inspiring Refrain","Reality Strobe",
            "Cultivate","Farseek","Nature's Lore","Kodama's Reach",
            "Rampant Growth","Three Visits","Rift in Time",
            "Counterspell","Negate","Swan Song","Fierce Guardianship",
            "Brainstorm","Mystical Tutor","Cyclonic Rift",
            "Tamiyo's Safekeeping","Shore Up","Vitalize","Dramatic Reversal",
            "Beast Within","Krosan Grip","Growth Spiral",
            "Opt","Ponder","Preordain",
            "Freed from the Real","Intruder Alarm","Pemmin's Aura",
            "Quest for Renewal","Teferi's Ageless Insight","Utopia Sprawl",
            "Sol Ring","Arcane Signet","Simic Signet","Lotus Bloom",
            "Mox Tantalite","Sol Talisman","Thousand-Year Elixir",
            "Swiftfoot Boots","Lightning Greaves"
        ]
    },
    "Sidisi": {
        "commander": "Sidisi, Brood Tyrant",
        "cards": [
            "Stitcher's Supplier","Satyr Wayfinder","Golgari Grave-Troll",
            "Stinkweed Imp","Nyx Weaver",
            "Splinterfright","Syr Konrad, the Grim",
            "Mirkwood Bats","Meren of Clan Nel Toth","Muldrotha, the Gravetide",
            "Eternal Witness","Massacre Wurm","Thunderfoot Baloth",
            "Golgari Thug","Shambling Shell","Brawn","Wonder",
            "Filth","Nighthowler","Jarad, Golgari Lich Lord",
            "Lord of Extinction","Hogaak, Arisen Necropolis","Izoni, Thousand-Eyed",
            "World Shaper","Ramunap Excavator","The Gitrog Monster",
            "Lotleth Troll","Glowspore Shaman",
            "Skull Prophet","Altar of Dementia",
            "Deathrite Shaman","Spider Spawning",
            "Ghoultree","Boneyard Aberration",
            "Old Rutstein","Molderhulk","Nemesis of Mortals",
            "Kessig Cagebreakers","Winding Way","Mulch",
            "Dread Return","Life from the Loam",
            "Living Death","Victimize",
            "Gnaw to the Bone","Crawl from the Cellar",
            "Arcane Signet","Mesmeric Orb","Perpetual Timepiece","Sol Ring",
            "Hedge Shredder",
            "Awaken the Honored Dead","Crawling Infestation",
            "Insidious Roots","Phyrexian Reclamation"
        ]
    },
    "Ognis": {
        "commander": "Ognis, the Dragon's Lash",
        "cards": [
            "Birds of Paradise","Captain Lannery Storm","Crime Novelist",
            "Goldspan Dragon","Jolene, the Plunder Queen","Korvold, Fae-Cursed King",
            "Magda, Brazen Outlaw","Marionette Master","Mirkwood Bats","Xorn",
            "Tireless Provisioner","Kalain, Reclusive Painter","Professional Face-Breaker",
            "Mahadi, Emporium Master","Gala Greeters","Stimulus Package",
            "Academy Manufactor","Disciple of the Vault","Reckless Fireweaver",
            "Thundermaw Hellkite","Hellkite Charger","Etali, Primal Storm",
            "Purphoros, God of the Forge","Prosper, Tome-Bound",
            "Dockside Extortionist","Goblin Anarchomancer","Grand Warlord Radha",
            "Savage Ventmaw","Dragonborn Looter","Zhur-Taa Goblin",
            "Tendershoot Dryad","Juri, Master of the Revue",
            "Blood Money","Insurrection","Mass Mutiny","Mob Rule",
            "Song of Totentanz","Tempt with Vengeance","Cultivate",
            "Kodama's Reach","Nature's Lore","Krenko's Command",
            "Decimate","Jeska's Will",
            "Beast Within","Deadly Dispute","Gold Rush","Riveteers Charm",
            "Heroic Intervention","Big Score",
            "Sol Ring","Arcane Signet","Inspiring Statuary","Lightning Greaves",
            "Key to the City","Bootleggers' Stash","Talisman of Impulse",
            "Gruul Signet","Rakdos Signet",
            "Alchemist's Talent","Revel in Riches","Sticky Fingers"
        ]
    },
    "Neera": {
        "commander": "Neera, Wild Mage",
        "cards": [
            "Archmage Emeritus","Displacer Kitten","Guttersnipe",
            "Hullbreaker Horror","Kessig Flamebreather","Veyran, Voice of Duality",
            "Coruscation Mage","Talrand, Sky Summoner","Young Pyromancer",
            "Murmuring Mystic","Niv-Mizzet, Parun","Goblin Electromancer",
            "Baral, Chief of Compliance","Storm-Kiln Artist","Crackling Drake",
            "Metallurgic Summonings","Shark Typhoon",
            "Aminatou's Augury","Call Forth the Tempest","Mnemonic Deluge",
            "Ponder","Vandalblast","Preordain","Treasure Cruise",
            "Blasphemous Act","Expressive Iteration","Seize the Spoils",
            "Faithless Looting",
            "Brainstorm","Counterspell","Mystical Tutor","Swan Song",
            "Chaos Warp","Lightning Bolt","Negate","Fact or Fiction",
            "Dig Through Time","Frantic Search","Reality Shift",
            "Cyclonic Rift","Thrill of Possibility","Opt",
            "Rapid Hybridization","Unexpected Windfall",
            "Aetherflux Reservoir","Sol Ring","Arcane Signet","Izzet Signet",
            "Talisman of Creativity","Mind Stone","Thought Vessel",
            "Commander's Sphere","Cursed Mirror","Gilded Lotus",
            "Primal Amulet","Swiftfoot Boots",
            "As Foretold","Fiery Inscription","One with the Multiverse",
            "Propaganda","Thousand-Year Storm","Inventive Iteration"
        ]
    },
    "Nazgul": {
        "commander": "Lord of the Nazgul",
        "cards": [
            "Nazgul","Clever Impersonator","Mirrorhall Mimic",
            "Mockingbird","Sakashima of a Thousand Faces","Visage Bandit",
            "Archmage Emeritus","Hullbreaker Horror","Spark Double",
            "Phyrexian Metamorph","Phantasmal Image","Stunt Double",
            "Glasspool Mimic","Body Double","Evil Twin",
            "Changeling Outcast","Metallic Mimic","Unsettled Mariner",
            "Reflections of Littjara","Maskwood Nexus",
            "Wonder","Fallen Shinobi","Sheoldred, the Apocalypse",
            "Sauron, the Dark Lord",
            "Rite of Replication","Quasiduplicate","Irenicus's Vile Duplication",
            "Echoing Return","Victimize","Unearth","Dread Return",
            "Distant Melody","Kindred Dominance",
            "Ponder","Preordain","Agatha's Soul Cauldron",
            "Counterspell","Negate","Swan Song","See Double",
            "Cackling Counterpart","Cyclonic Rift","Brainstorm",
            "Deadly Rollick","Feed the Swarm","Go for the Throat",
            "Malicious Affliction","Pongify","Rapid Hybridization",
            "Dark Ritual","Tainted Pact",
            "Sol Ring","Arcane Signet","Dimir Signet","Fellwar Stone",
            "Talisman of Dominance","Winged Boots","Patchwork Banner",
            "Herald's Horn","Mind Stone","Thought Vessel",
            "Call of the Ring","Scroll of Isildur"
        ]
    },
    "Maarika": {
        "commander": "Maarika, Brutal Gladiator",
        "cards": [
            "Glistener Elf","Phyrexian Crusader","Skithiryx, the Blight Dragon",
            "Phyrexian Hydra","Putrefax","Ichor Rats","Plague Stinger",
            "Core Prowler","Hand of the Praetors",
            "Plague Myr","Septic Rats","Toxic Nim","Viridian Corrupter",
            "Halana and Alena, Partners","Forgotten Ancient",
            "Massacre Girl, Known Killer","Fynn, the Fangbearer",
            "Needle Specter","Phyrexian Swarmlord","Spinebiter",
            "Evolution Sage","Contaminant Grafter","Tyrranax Rex","Blight Mamba",
            "Flensermite","Necropede","Rot Wolf",
            "Chandra's Ignition","Gravitic Punch","Flesh // Blood",
            "Cultivate","Kodama's Reach","Nature's Lore",
            "Rishkar's Expertise","Traverse the Outlands",
            "Infectious Bite","Tainted Strike","Tyvar's Stand",
            "Soul's Fire","Heroic Intervention","Snakeskin Veil",
            "Golgari Charm","Return of the Wildspeaker",
            "Khalni Ambush","Ram Through",
            "Sol Ring","Arcane Signet","Grafted Exoskeleton",
            "Fiendlash","Infiltration Lens","Swiftfoot Boots","Lightning Greaves",
            "Glistening Oil","Phyresis","Rancor","Rhythm of the Wild",
            "Hardened Scales","Evolutionary Escalation","Bow of Nylea",
            "Unnatural Growth","Moldervine Reclamation"
        ]
    },
    "Kuja": {
        "commander": "Kuja, Genome Sorcerer",
        "cards": [
            "Guttersnipe","Coruscation Mage","Dark Confidant",
            "Gleeful Arsonist","Gogo, Mysidian Elder","Black Waltz No. 3",
            "Pinnacle Monk","Magus of the Wheel",
            "Boltwave","Mizzix's Mastery","Night's Whisper","Sign in Blood",
            "Faithless Looting","Wheel of Misfortune","Toxic Deluge",
            "Chain Lightning","Stitch Together","Dread Return",
            "Feed the Swarm","Damn",
            "Lightning Bolt","Shock","Go for the Throat","Chaos Warp",
            "Dark Ritual","Pyretic Ritual","Cabal Ritual","Seething Song",
            "Feign Death","Undying Malice","Supernatural Stamina",
            "Village Rites","Deadly Dispute","Thrill of Possibility",
            "Infernal Grasp","Hero's Downfall","Bedevil","Rakdos Charm",
            "Price of Progress","Flame Rift",
            "Lava Spike","Rift Bolt","Skullcrack","Stoke the Flames",
            "Fire Covenant","Searing Blood",
            "Sol Ring","Arcane Signet","Rakdos Signet",
            "Talisman of Indulgence","Mind Stone","Thought Vessel",
            "Fellwar Stone","Ruby Medallion","Jet Medallion",
            "Commander's Sphere","Cursed Mirror","Bender's Waterskin",
            "Arcane Bombardment","Collective Inferno","Fiery Inscription",
            "Quest for Pure Flame","Virtue of Courage"
        ]
    },
    "Gimli": {
        "commander": "Gimli, Mournful Avenger",
        "cards": [
            "Dragon Broodmother","Mycoloth","Tendershoot Dryad",
            "Dragonlair Spider","Writhing Chrysalis","Nest Invader",
            "Avenger of Zendikar","Goblin Instigator","Beetleback Chief",
            "Siege-Gang Commander","Endrek Sahr, Master Breeder",
            "Pia and Kiran Nalaar","Scute Swarm","Ogre Battledriver",
            "Purphoros, God of the Forge","Chancellor of the Forge",
            "Craterhoof Behemoth","Eldrazi Repurposer",
            "Hobgoblin Bandit Lord","Krenko, Mob Boss",
            "Mogg War Marshal","Esika's Chariot",
            "Song of Totentanz","Tempt with Vengeance","Pest Infestation",
            "Cultivate","Kodama's Reach","Nature's Lore",
            "Shamanic Revelation","Second Harvest","Dragon Fodder",
            "Fling","Temur Battle Rage","Kazuul's Fury",
            "Arachnogenesis","Heroic Intervention","Beast Within",
            "Chord of Calling","Worldly Tutor","Snakeskin Veil",
            "Harrow","Burn at the Stake",
            "Ashnod's Altar","Skullclamp","Embercleave",
            "Blade of the Bloodchief","Animation Module","Scepter of Celebration",
            "Sol Ring","Arcane Signet","Gruul Signet",
            "Swiftfoot Boots","Lightning Greaves","Phyrexian Altar",
            "Doubling Season","Goblin Bombardment","Impact Tremors",
            "Awakening Zone","Fecundity","Primal Vigor",
            "Rhythm of the Wild","Parallel Lives","Growing Rites of Itlimoc",
            "From Beyond"
        ]
    },
    "Cloud": {
        "commander": "Cloud, Ex-SOLDIER",
        "cards": [
            "Puresteel Paladin","Sram, Senior Edificer","Akiri, Fearless Voyager",
            "Armory Automaton","Bruenor Battlehammer","Danitha Capashen, Paragon",
            "Fervent Champion","Goblin Gaveleer","Halvar, God of Battle",
            "Kazuul's Toll Collector","Leonin Shikari","Nahiri, the Lithomancer",
            "Reyav, Master Smith","Stonehewer Giant","Stoneforge Mystic",
            "Syr Gwyn, Hero of Ashvale","Tiana, Ship's Caretaker",
            "Valduk, Keeper of the Flame","Wyleth, Soul of Steel",
            "Ardenn, Intrepid Archaeologist","Kemba, Kha Regent",
            "Sigarda's Aid","Barret, Captain of Avalanche",
            "Sephiroth, the One-Winged Angel","Red XIII, Desert Nanaki",
            "Yuffie, Materia Hunter","Zack Fair, SOLDIER First Class",
            "Austere Command","Hull Breach","Nature's Lore","Vandalblast",
            "Boros Charm","Chaos Warp","Clever Concealment","Path to Exile",
            "Swords to Plowshares","Heroic Intervention","Teferi's Protection",
            "Return of the Wildspeaker",
            "Bloodforged Battle-Axe","Champion's Helm","Conqueror's Flail",
            "Darksteel Plate","Lightning Greaves","Skullclamp",
            "Sword of the Animist","Nettlecyst","Hammer of Nazahn",
            "The Irencrag","Basilisk Collar","Masterwork of Ingenuity",
            "Mithril Coat","Mask of Memory","Swiftfoot Boots",
            "Sol Ring","Arcane Signet","Boros Signet","Gruul Signet",
            "Selesnya Signet","Talisman of Conviction","Talisman of Unity",
            "Commander's Sphere","Dowsing Dagger",
            "Forge Anew"
        ]
    },
}


def fetch_json(url, data=None, method=None):
    headers = {
        "User-Agent": "MTGDeckDesc/1.0",
        "Accept": "application/json",
    }
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(
            url, data=body,
            headers={**headers, "Content-Type": "application/json"},
            method=method or "POST",
        )
    else:
        req = urllib.request.Request(url, headers=headers, method=method or "GET")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"    HTTP {e.code}: {url[:80]}")
        try:
            print(f"    {e.read().decode('utf-8', errors='replace')[:200]}")
        except:
            pass
        return None
    except Exception as e:
        print(f"    Error: {e}")
        return None


# ── STEP 1: Scryfall ─────────────────────────────────────────
print("=" * 60)
print("STEP 1: Fetching card oracle text from Scryfall")
print("=" * 60)

all_unique = set()
for d in DECKS.values():
    all_unique.add(d["commander"])
    all_unique.update(d["cards"])

card_list = sorted(all_unique)
print(f"  Total unique cards: {len(card_list)}")

scryfall = {}
not_found = []

for i in range(0, len(card_list), 75):
    batch = card_list[i : i + 75]
    identifiers = [{"name": n} for n in batch]
    bn = i // 75 + 1
    tb = (len(card_list) - 1) // 75 + 1
    print(f"  Batch {bn}/{tb}: {len(batch)} cards...")
    result = fetch_json(
        "https://api.scryfall.com/cards/collection", {"identifiers": identifiers}
    )
    if result:
        for card in result.get("data", []):
            cname = card.get("name", "")
            oracle = card.get("oracle_text", "")
            if not oracle and "card_faces" in card:
                oracle = " // ".join(
                    f.get("oracle_text", "") for f in card["card_faces"]
                )
            scryfall[cname] = {
                "oracle_text": oracle,
                "mana_cost": card.get("mana_cost", ""),
                "type_line": card.get("type_line", ""),
                "cmc": card.get("cmc", 0),
                "keywords": card.get("keywords", []),
            }
        for nf in result.get("not_found", []):
            not_found.append(nf.get("name", str(nf)))
    time.sleep(0.12)

print(f"\n  Found: {len(scryfall)} / {len(card_list)} cards")
if not_found:
    print(f"  Not found ({len(not_found)}):")
    for nf in not_found:
        print(f"    - {nf}")


# ── STEP 2: Commander Spellbook ───────────────────────────────
print("\n" + "=" * 60)
print("STEP 2: Commander Spellbook combos")
print("=" * 60)

spellbook = {}
for name, deck in DECKS.items():
    cmd = deck["commander"]
    deck_set = set(c.lower() for c in [cmd] + deck["cards"])
    print(f"\n  [{name}] {cmd}")

    q = urllib.parse.quote(f'card:"{cmd}"')
    url = f"https://backend.commanderspellbook.com/variants/?q={q}&limit=50&format=json"
    result = fetch_json(url)

    combos = []
    if result:
        results_list = result.get("results", [])
        if not isinstance(results_list, list):
            results_list = []
        for combo in results_list:
            uses = combo.get("uses", [])
            combo_cards = []
            for u in uses:
                if isinstance(u, dict):
                    c = u.get("card", {})
                    cn = c.get("name", "") if isinstance(c, dict) else str(c)
                    combo_cards.append(cn)
            produces = combo.get("produces", [])
            prod_names = []
            for p in produces:
                if isinstance(p, dict):
                    feat = p.get("feature", {})
                    prod_names.append(
                        feat.get("name", "") if isinstance(feat, dict) else str(feat)
                    )
            desc = combo.get("description", "")
            in_deck = sum(1 for c in combo_cards if c.lower() in deck_set)
            combos.append({
                "cards": combo_cards,
                "produces": prod_names,
                "description": str(desc)[:500],
                "cards_in_deck": in_deck,
                "total_cards": len(combo_cards),
            })

    combos.sort(key=lambda c: (c["cards_in_deck"] / max(c["total_cards"], 1), c["cards_in_deck"]), reverse=True)
    relevant = [c for c in combos if c["total_cards"] > 0 and c["cards_in_deck"] >= c["total_cards"] - 1][:15]
    spellbook[name] = relevant if relevant else combos[:10]
    nr = len(relevant)
    print(f"    {len(combos)} total, {nr} relevant")
    for c in (relevant or combos)[:3]:
        print(f"      {' + '.join(c['cards'][:4])} => {', '.join(c['produces'][:3])}")
    time.sleep(0.25)


# ── STEP 3: EDHREC combo pages ────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3: EDHREC combo pages (via web fetch)")
print("=" * 60)

# We'll save EDHREC URLs for the user to check, and also try the EDHREC JSON API
edhrec_combos = {}
for name, deck in DECKS.items():
    cmd = deck["commander"]
    # Build EDHREC slug: lowercase, replace spaces/commas/apostrophes
    slug = cmd.lower()
    for ch in [",", "'", "'"]:
        slug = slug.replace(ch, "")
    slug = slug.replace(" ", "-")
    # Remove double dashes
    while "--" in slug:
        slug = slug.replace("--", "-")
    slug = slug.strip("-")

    url = f"https://json.edhrec.com/pages/combos/{slug}.json"
    print(f"\n  [{name}] {url}")
    result = fetch_json(url)

    combos_list = []
    if result:
        # EDHREC combos endpoint
        card_lists = result.get("cardlists", [])
        for cl in card_lists:
            if cl.get("tag", "") in ("combos", "newcombos", "topcombos"):
                for item in cl.get("cardviews", []):
                    combo_names = [c.get("name", "") for c in item.get("cards", [])]
                    combo_desc = item.get("description", "")
                    combos_list.append({
                        "cards": combo_names,
                        "description": combo_desc[:500],
                    })
        # Also check container format
        containers = result.get("container", {})
        if isinstance(containers, dict):
            json_dict = containers.get("json_dict", {})
            if isinstance(json_dict, dict):
                combos_data = json_dict.get("cardlists", [])
                for cl in combos_data:
                    for item in cl.get("cardviews", []):
                        combo_names = [c.get("name", "") for c in item.get("cards", [])]
                        combo_desc = item.get("description", "")
                        combos_list.append({
                            "cards": combo_names,
                            "description": combo_desc[:500],
                        })

    edhrec_combos[name] = combos_list
    print(f"    Found {len(combos_list)} combos from EDHREC")
    for c in combos_list[:3]:
        print(f"      {' + '.join(c['cards'][:4])}")
    time.sleep(0.3)


# ── SAVE ──────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SAVING")
print("=" * 60)

with open(os.path.join(OUTPUT, "scryfall_data.json"), "w", encoding="utf-8") as f:
    json.dump(scryfall, f, indent=2, ensure_ascii=False)
print(f"  scryfall_data.json ({len(scryfall)} cards)")

with open(os.path.join(OUTPUT, "spellbook_combos.json"), "w", encoding="utf-8") as f:
    json.dump(spellbook, f, indent=2, ensure_ascii=False)
t1 = sum(len(v) for v in spellbook.values())
print(f"  spellbook_combos.json ({t1} combos)")

with open(os.path.join(OUTPUT, "edhrec_combos.json"), "w", encoding="utf-8") as f:
    json.dump(edhrec_combos, f, indent=2, ensure_ascii=False)
t2 = sum(len(v) for v in edhrec_combos.values())
print(f"  edhrec_combos.json ({t2} combos)")

# Combined analysis
deck_analysis = {}
for name, deck in DECKS.items():
    non_land = []
    for cn in sorted(set(deck["cards"])):
        sf = scryfall.get(cn, {})
        tl = sf.get("type_line", "")
        if "Land" in tl:
            continue
        non_land.append({
            "name": cn,
            "type": tl,
            "oracle": sf.get("oracle_text", ""),
            "cmc": sf.get("cmc", 0),
            "keywords": sf.get("keywords", []),
        })
    deck_analysis[name] = {
        "commander": deck["commander"],
        "commander_oracle": scryfall.get(deck["commander"], {}).get("oracle_text", ""),
        "card_count": len(deck["cards"]),
        "non_land_cards": non_land,
        "combos_spellbook": spellbook.get(name, []),
        "combos_edhrec": edhrec_combos.get(name, []),
    }

with open(os.path.join(OUTPUT, "deck_analysis.json"), "w", encoding="utf-8") as f:
    json.dump(deck_analysis, f, indent=2, ensure_ascii=False)
print(f"  deck_analysis.json")

print("\nDone!")
