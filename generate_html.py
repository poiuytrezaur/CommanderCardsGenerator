#!/usr/bin/env python3
"""Generate the French deck_cards.html from template."""

html = r'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fiches Commander — Collection de Decks</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Alegreya:ital,wght@0,400;0,700;1,400&display=swap');

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: #1a1a2e;
    font-family: 'Alegreya', Georgia, serif;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 4mm;
    padding: 5mm;
  }

  @page {
    size: A4 portrait;
    margin: 8mm;
  }

  @media print {
    body {
      background: white;
      gap: 1mm;
      padding: 0;
    }
    .card { break-inside: avoid; }
  }

  .card {
    width: 63mm;
    height: 88mm;
    border-radius: 3mm;
    overflow: hidden;
    position: relative;
    display: flex;
    flex-direction: column;
    box-shadow: 0 2px 8px rgba(0,0,0,0.6);
    flex-shrink: 0;
  }

  .card-border {
    position: absolute;
    inset: 0;
    border-radius: 3mm;
    border: 1.2mm solid rgba(255,255,255,0.15);
    pointer-events: none;
    z-index: 10;
  }

  .card-header {
    position: relative;
    height: 22mm;
    overflow: hidden;
    flex-shrink: 0;
  }

  .card-header img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    filter: brightness(0.85) saturate(1.1);
  }

  .card-header::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 10mm;
    background: linear-gradient(transparent, var(--card-bg));
    z-index: 1;
  }

  .card-name-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 2;
    padding: 0 2mm 0.5mm 2mm;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
  }

  .commander-name {
    font-family: 'Cinzel', serif;
    font-weight: 700;
    font-size: 8.5pt;
    color: #fff;
    text-shadow: 0 1px 3px rgba(0,0,0,0.9), 0 0 6px rgba(0,0,0,0.5);
    line-height: 1.1;
    max-width: 80%;
  }

  .mana-pips {
    display: flex;
    gap: 0.5mm;
    flex-shrink: 0;
  }

  .mana-pip {
    width: 3.5mm;
    height: 3.5mm;
    border-radius: 50%;
    border: 0.3mm solid rgba(0,0,0,0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 6.5pt;
    font-weight: 900;
    text-shadow: 0 0.5px 1px rgba(0,0,0,0.3);
    box-shadow: inset 0 1px 2px rgba(255,255,255,0.3), 0 1px 2px rgba(0,0,0,0.4);
  }

  .pip-W { background: radial-gradient(circle at 30% 30%, #fff9e6, #f0d860); color: #6b5c1f; }
  .pip-U { background: radial-gradient(circle at 30% 30%, #4fa8d8, #0a4f8a); color: #c8e4f8; }
  .pip-B { background: radial-gradient(circle at 30% 30%, #555, #1a1a1a); color: #bbb; }
  .pip-R { background: radial-gradient(circle at 30% 30%, #f06040, #a01020); color: #ffddc8; }
  .pip-G { background: radial-gradient(circle at 30% 30%, #50b060, #1a6030); color: #d0f0c8; }

  .card-body {
    flex: 1;
    background: var(--card-bg);
    padding: 1.5mm 2mm 1mm 2mm;
    display: flex;
    flex-direction: column;
    gap: 0.6mm;
    overflow: hidden;
  }

  .section-label {
    font-family: 'Cinzel', serif;
    font-size: 6.5pt;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.2mm;
    border-bottom: 0.2mm solid var(--accent-dim);
    padding-bottom: 0.3mm;
    margin-bottom: 0.2mm;
    line-height: 1;
  }

  .strategy-text {
    font-size: 6.5pt;
    color: var(--text);
    line-height: 1.2;
  }

  .combos-list {
    font-size: 6pt;
    color: var(--text);
    line-height: 1.15;
    list-style: none;
  }

  .combos-list li {
    padding-left: 2mm;
    position: relative;
    margin-bottom: 0.2mm;
  }

  .combos-list li::before {
    content: '\2694';
    position: absolute;
    left: 0;
    font-size: 5pt;
    color: var(--accent);
  }

  .keywords-line {
    font-size: 5.5pt;
    color: var(--text-dim);
    line-height: 1.15;
    font-style: italic;
  }

  .keywords-line strong {
    color: var(--accent);
    font-style: normal;
    font-size: 5.5pt;
  }

  .mana-curve-section {
    margin-top: auto;
    flex-shrink: 0;
    padding: 0.5mm 1mm;
  }

  .mana-curve {
    display: flex;
    align-items: flex-end;
    gap: 0.5mm;
    height: 10mm;
    padding-top: 0.5mm;
  }

  .mana-bar-group {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
    justify-content: flex-end;
  }

  .mana-bar {
    width: 100%;
    background: var(--accent);
    border-radius: 0.3mm 0.3mm 0 0;
    min-height: 0;
    opacity: 0.75;
  }

  .mana-bar-label {
    font-size: 5pt;
    color: var(--text-dim);
    line-height: 1;
    margin-top: 0.2mm;
  }

  .mana-bar-count {
    font-size: 4.5pt;
    color: var(--text-dim);
    line-height: 1;
    margin-bottom: 0.1mm;
  }

  .avg-mv {
    font-size: 5pt;
    color: var(--text-dim);
    text-align: right;
    line-height: 1;
    margin-top: 0.2mm;
  }

  .glossary-body {
    flex: 1;
    background: var(--card-bg);
    padding: 2mm;
    overflow: hidden;
  }

  .glossary-title {
    font-family: 'Cinzel', serif;
    font-size: 8pt;
    color: var(--accent);
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 0.3mm;
    margin-bottom: 1.5mm;
  }

  .glossary-item {
    font-size: 5.5pt;
    color: var(--text);
    line-height: 1.3;
    margin-bottom: 0.4mm;
  }

  .glossary-item strong {
    color: var(--accent);
    font-size: 6pt;
  }
</style>
</head>
<body>
<script>
const decks = [
  {
    commander: "Ayara, First of Locthwain",
    colors: ["B"],
    bg: "linear-gradient(160deg, #1c1020 0%, #25152a 40%, #1a1020 100%)",
    accent: "#b48ead",
    accentDim: "rgba(180,142,173,0.25)",
    text: "#d8ccd8",
    textDim: "#8a7a8a",
    strategy: "Aristocrates mono-noir. Chaque cr\u00e9ature noire qui d\u00e9barque draine 1 PV via Ayara. Sacrifiez, ressuscitez, re-sacrifiez \u2014 vos adversaires fondent comme neige au soleil pendant que vous sirotez leur essence vitale.",
    combos: [
      "Saccageur impitoyable + Autel d\u2019Ashnod + cr\u00e9ature r\u00e9cursive \u2192 \u221e mana & drain",
      "Rampeur des tombes + Saccageur impitoyable + Bouffeur de charogne \u2192 \u221e mort",
      "Marchand gris d\u2019Asphodel + haute d\u00e9votion \u2192 swing de vie massif",
      "Exsanguination / R\u00e9servoir d\u2019Aetherflux comme finisseurs"
    ],
    keywords: "Contact mortel \u00b7 Vol \u00b7 Menace \u00b7 Lien de vie",
    curve: [0, 11, 14, 13, 12, 8, 1, 3],
    avgMv: 3.13
  },
  {
    commander: "Ellivere of the Wild Court",
    colors: ["G", "W"],
    bg: "linear-gradient(160deg, #1a2418 0%, #22301a 40%, #1c2816 100%)",
    accent: "#a3be8c",
    accentDim: "rgba(163,190,140,0.25)",
    text: "#d4dcc8",
    textDim: "#7a8a70",
    strategy: "Voltron Enchantresse. Empilez les auras, piochez \u00e0 n\u2019en plus finir gr\u00e2ce aux enchanteresses. Le r\u00f4le Vertueux d\u2019Ellivere donne l\u2019\u00e9vasion pour achever au commandant. Les auras ne sont pas des autocollants, c\u2019est un art de vivre.",
    combos: [
      "Armure \u00e9th\u00e9r\u00e9e / Tout ce qui brille \u2192 puissance massive",
      "Manteau d\u2019esprit + Masque ancestral \u2192 l\u00e9tal imblocable",
      "Vents de Rath \u2192 nettoyage unilat\u00e9ral (garde les enchant\u00e9s)",
      "Manteau des anciens \u2192 r\u00e9cup\u00e8re toutes les auras du cimeti\u00e8re"
    ],
    keywords: "Vol \u00b7 Constellation \u00b7 Lien de vie \u00b7 Pi\u00e9tinement",
    curve: [0, 9, 22, 16, 10, 4, 0, 1],
    avgMv: 2.71
  },
  {
    commander: "Gargos, Vicious Watcher",
    colors: ["G"],
    bg: "linear-gradient(160deg, #0e200e 0%, #183018 40%, #0e200e 100%)",
    accent: "#5faa4f",
    accentDim: "rgba(95,170,79,0.25)",
    text: "#c8dcc0",
    textDim: "#6a8a5a",
    strategy: "Rampez fort, castez des Hydres XXL \u00e0 prix r\u00e9duit gr\u00e2ce \u00e0 Gargos. Ciblez vos propres Hydres pour d\u00e9clencher des combats gratuits. Vos serpents \u00e0 47 t\u00eates adorent faire la causette aux cr\u00e9atures adverses.",
    combos: [
      "Gargos + sort de ciblage \u2192 combat gratuit comme removal",
      "Floraison d\u00e9brid\u00e9e \u2192 double les sorts X",
      "Hydre kalonienne \u2192 double les marqueurs +1/+1 \u00e0 l\u2019attaque",
      "\u00c9cailles endurcies + hydres \u00e0 marqueurs \u2192 bonus partout"
    ],
    keywords: "Pi\u00e9tinement \u00b7 Port\u00e9e \u00b7 Garde \u00b7 Combat",
    curve: [0, 12, 20, 18, 4, 3, 4, 1],
    avgMv: 2.71
  },
  {
    commander: "Laughing Jasper Flint",
    colors: ["B", "R"],
    bg: "linear-gradient(160deg, #201010 0%, #2a1515 40%, #1a0e0e 100%)",
    accent: "#bf616a",
    accentDim: "rgba(191,97,106,0.25)",
    text: "#d8c8c8",
    textDim: "#8a6a6a",
    strategy: "Exilez les cartes des mains adverses avec Jasper, puis castez-les vous-m\u00eame. D\u2019autres cr\u00e9atures volent depuis les biblioth\u00e8ques et cimeti\u00e8res. Pourquoi construire un deck quand on peut emprunter les v\u00f4tres ?",
    combos: [
      "Jasper + Cape de soie susurrante \u2192 exile fiable de la main",
      "Etali, Temp\u00eate primordiale \u2192 vol en cascade \u00e0 l\u2019attaque",
      "Suspicion fi\u00e9vreuse \u2192 vol massif + d\u00e9g\u00e2ts",
      "Vol scandaleux \u2192 exil de 8 cartes adverses"
    ],
    keywords: "Contact mortel \u00b7 Vol \u00b7 Menace \u00b7 Tr\u00e9sor",
    curve: [1, 4, 19, 12, 10, 4, 4, 8],
    avgMv: 3.55
  },
  {
    commander: "Terra, Herald of Hope",
    colors: ["W", "B", "R"],
    bg: "linear-gradient(160deg, #201518 0%, #2a1820 40%, #1a1015 100%)",
    accent: "#d08770",
    accentDim: "rgba(208,135,112,0.25)",
    text: "#d8d0cc",
    textDim: "#8a7a70",
    strategy: "R\u00e9animateur Mardu. Remplissez le cimeti\u00e8re de bombes, Terra les ram\u00e8ne au bercail. Boucles sacrifice + r\u00e9cursion ad nauseam. Le cimeti\u00e8re c\u2019est pas la fin \u2014 c\u2019est la salle d\u2019attente.",
    combos: [
      "Celes + Bombardement des gobelins \u2192 \u221e arriv\u00e9es & d\u00e9parts",
      "Phal\u00e8ne pondeuse lumineuse + Bombardement des gobelins \u2192 \u221e boucle",
      "Squall + Peur de rater + Bombardement \u2192 quasi-\u221e d\u00e9g\u00e2ts",
      "Ascension des royaumes sombres \u2192 r\u00e9anime TOUS les cimeti\u00e8res"
    ],
    keywords: "Vol \u00b7 Initiative \u00b7 Lien de vie \u00b7 Recyclage \u00b7 Meule",
    curve: [0, 7, 16, 15, 13, 5, 2, 4],
    avgMv: 3.27
  },
  {
    commander: "Alaundo the Seer",
    colors: ["U", "G"],
    bg: "linear-gradient(160deg, #0e1a1e 0%, #102828 40%, #0e1a1e 100%)",
    accent: "#88c0d0",
    accentDim: "rgba(136,192,208,0.25)",
    text: "#c8dce0",
    textDim: "#6a8a8e",
    strategy: "Tapez Alaundo pour piocher et exiler avec des marqueurs temps, puis castez tout gratos. Effets de d\u00e9gagement = activations infinies. Le temps est relatif, surtout quand vous le supprimez.",
    combos: [
      "Lib\u00e9r\u00e9 du r\u00e9el / Aura de Pemmin + Alaundo \u2192 \u221e activations",
      "Ioreth + d\u00e9gageur (Kiora / Vizir / Guide) \u2192 \u221e mana & pioche",
      "Oracle de Thassa \u2192 victoire apr\u00e8s biblio vide",
      "Muse n\u00e9e-des-graines \u2192 d\u00e9gagement tour de chaque joueur"
    ],
    keywords: "Suspension \u00b7 Recyclage \u00b7 Mue \u00b7 Regard",
    curve: [4, 14, 22, 17, 2, 5, 2, 1],
    avgMv: 2.40
  },
  {
    commander: "Sidisi, Brood Tyrant",
    colors: ["B", "G", "U"],
    bg: "linear-gradient(160deg, #101a18 0%, #152520 40%, #101a18 100%)",
    accent: "#8fbcbb",
    accentDim: "rgba(143,188,187,0.25)",
    text: "#c8d8d6",
    textDim: "#6a8a88",
    strategy: "Auto-meule pour spawner des zombies avec Sidisi. +60 cr\u00e9atures au deck pour maximiser les triggers. Votre cimeti\u00e8re EST votre seconde main. Le recyclage : bon pour la plan\u00e8te, mortel pour vos adversaires.",
    combos: [
      "Orbe mesm\u00e9rienne + d\u00e9gagement \u2192 meule massive + zombies",
      "Mort vivante \u2192 r\u00e9surrection en masse du cimeti\u00e8re",
      "Syr Konrad + auto-meule \u2192 drain \u00e0 toute la table",
      "Drague (Troll du Golgari) \u2192 triggers de meule r\u00e9p\u00e9t\u00e9s"
    ],
    keywords: "Meule \u00b7 Drague \u00b7 Vol \u00b7 Recyclage",
    curve: [0, 7, 20, 17, 9, 6, 4, 0],
    avgMv: 2.98
  },
  {
    commander: "Ognis, the Dragon's Lash",
    colors: ["B", "R", "G"],
    bg: "linear-gradient(160deg, #1a1510 0%, #2a1e14 40%, #1a1510 100%)",
    accent: "#ebcb8b",
    accentDim: "rgba(235,203,139,0.25)",
    text: "#d8d4c8",
    textDim: "#8a8468",
    strategy: "Attaquez avec des cr\u00e9atures c\u00e9l\u00e9rit\u00e9, r\u00e9coltez des tr\u00e9sors via Ognis. Les tr\u00e9sors financent synergies artefacts et victoire alternative. L\u2019argent ne fait pas le bonheur, mais il gagne la partie.",
    combos: [
      "Revel in Riches + 10 tr\u00e9sors \u2192 condition de victoire alternative",
      "Ma\u00eetre marionnettiste + sacrifice de tr\u00e9sors \u2192 drain massif",
      "Planque de contrebandiers \u2192 les terrains produisent des tr\u00e9sors",
      "Insurrection / Loi de la foule \u2192 volez toutes les cr\u00e9atures"
    ],
    keywords: "C\u00e9l\u00e9rit\u00e9 \u00b7 Vol \u00b7 Pi\u00e9tinement \u00b7 Tr\u00e9sor \u00b7 Initiative",
    curve: [0, 9, 20, 13, 7, 7, 4, 2],
    avgMv: 3.06
  },
  {
    commander: "Neera, Wild Mage",
    colors: ["U", "R"],
    bg: "linear-gradient(160deg, #14101e 0%, #1e1528 40%, #14101e 100%)",
    accent: "#b48ead",
    accentDim: "rgba(180,142,173,0.25)",
    text: "#d0c8d8",
    textDim: "#7a6a8a",
    strategy: "Castez un sort \u00e0 1 mana, Neera le polymorphe en bombe de 9 mana. Manipulez le dessus de la biblio pour contr\u00f4ler le r\u00e9sultat. Loterie magique, sauf que vous avez marqu\u00e9 les cartes.",
    combos: [
      "Horreur brisecoque + Anneau solaire \u2192 \u221e mana & compteur d\u2019orage",
      "R\u00e9servoir d\u2019Aetherflux + temp\u00eate de sorts \u2192 laser 50 d\u00e9g\u00e2ts",
      "D\u00e9luge mn\u00e9monique \u2192 copie un gros sort 3 fois",
      "Veyran + triggers de sorts \u2192 d\u00e9g\u00e2ts et effets doubl\u00e9s"
    ],
    keywords: "Vol \u00b7 Regard \u00b7 Cascade \u00b7 Annihilateur",
    curve: [0, 13, 15, 11, 6, 4, 3, 10],
    avgMv: 3.47
  },
  {
    commander: "Lord of the Nazg\u00fbl",
    colors: ["U", "B"],
    bg: "linear-gradient(160deg, #10101a 0%, #181825 40%, #10101a 100%)",
    accent: "#81a1c1",
    accentDim: "rgba(129,161,193,0.25)",
    text: "#c8d0d8",
    textDim: "#6a7a8a",
    strategy: "Tribal Nazg\u00fbl avec 9 copies qui grossissent \u00e0 chaque arriv\u00e9e de spectre. Clonez-les pour multiplier les triggers \u2014 chaque copie booste toutes les autres. Un Anneau pour les dominer tous.",
    combos: [
      "Horreur brisecoque + Anneau solaire \u2192 \u221e mana & orage",
      "Rite de R\u00e9plication sur Nazg\u00fbl \u2192 5 copies, tous boost\u00e9s",
      "Retour en \u00e9cho \u2192 ram\u00e8ne TOUS les Nazg\u00fbl du cimeti\u00e8re",
      "Appel de l\u2019Anneau \u2192 pioche constante + tentation de l\u2019Anneau"
    ],
    keywords: "Contact mortel \u00b7 Changelin \u00b7 Flash \u00b7 Regard",
    curve: [0, 12, 14, 20, 13, 4, 1, 1],
    avgMv: 2.85
  },
  {
    commander: "Maarika, Brutal Gladiator",
    colors: ["B", "R", "G"],
    bg: "linear-gradient(160deg, #1a1210 0%, #261818 40%, #1a1210 100%)",
    accent: "#a3be8c",
    accentDim: "rgba(163,190,140,0.25)",
    text: "#d0d0c8",
    textDim: "#7a7a68",
    strategy: "Voltron Infection. Collez un Exosquelette greff\u00e9 sur Maarika = d\u00e9g\u00e2ts d\u2019infection au commandant. Maarika combat quand elle inflige des d\u00e9g\u00e2ts exc\u00e9dentaires. Chandra\u2019s Ignition + infection = table empoisonn\u00e9e. Th\u00e9rapeutique, promis.",
    combos: [
      "Exosquelette greff\u00e9 + Maarika \u2192 infection au commandant",
      "Ignition de Chandra sur cr\u00e9ature infect\u00e9e \u2192 empoisonne la table",
      "Frappe corrompue + haute puissance \u2192 infection surprise l\u00e9tale",
      "Fouet de la furie + combats \u2192 d\u00e9g\u00e2ts doubl\u00e9s"
    ],
    keywords: "Infection \u00b7 Initiative \u00b7 Pi\u00e9tinement \u00b7 Combat",
    curve: [0, 10, 16, 17, 9, 6, 3, 1],
    avgMv: 2.97
  },
  {
    commander: "Kuja, Genome Sorcerer",
    colors: ["B", "R"],
    bg: "linear-gradient(160deg, #1e1018 0%, #281420 40%, #1e1018 100%)",
    accent: "#bf616a",
    accentDim: "rgba(191,97,106,0.25)",
    text: "#d8c8d0",
    textDim: "#8a6a78",
    strategy: "Spellslinger br\u00fblant. \u00c9ph\u00e9m\u00e8res et rituels pas chers d\u00e9clenchent tokens et d\u00e9g\u00e2ts de Kuja. Arcane Bombardment = sorts exponentiels chaque tour. Mizzix\u2019s Mastery overload\u00e9 = tout le cimeti\u00e8re rejou\u00e9. Le feu, c\u2019est beau.",
    combos: [
      "Bombardement arcanique + sorts en masse \u2192 casts exponentiels",
      "Qu\u00eate de la Flamme Pure \u2192 double TOUS les d\u00e9g\u00e2ts",
      "Ma\u00eetrise de Mizzix overload\u00e9 \u2192 replay du cimeti\u00e8re entier",
      "Tripier + cha\u00eene de sorts pas chers \u2192 burn rapide"
    ],
    keywords: "Convocation \u00b7 Regard \u00b7 Contact mortel \u00b7 Overload",
    curve: [0, 13, 27, 13, 6, 2, 1, 0],
    avgMv: 2.35
  },
  {
    commander: "Gimli, Mournful Avenger",
    colors: ["R", "G"],
    bg: "linear-gradient(160deg, #1a1810 0%, #251e12 40%, #1a1810 100%)",
    accent: "#d08770",
    accentDim: "rgba(208,135,112,0.25)",
    text: "#d8d4c8",
    textDim: "#8a8068",
    strategy: "Sacrifice de tokens. Cr\u00e9ez des vagues de jetons, sacrifiez-les pour gonfler Gimli en +1/+1. Doubling Season multiplie tout. Puis Fling un Gimli de 35/35 au visage. Petit nain, gros d\u00e9g\u00e2ts.",
    combos: [
      "Fosse de l\u2019engeance + Saison de d\u00e9doublement + Autel d\u2019Ashnod \u2192 \u221e tokens & mana",
      "Lame du chef de sang + Module d\u2019animation + Autel d\u2019Ashnod \u2192 \u221e mort & mana",
      "Fling / Fureur de Kazuul \u2192 d\u00e9g\u00e2ts directs l\u00e9taux avec un Gimli \u00e9norme",
      "Tremblements d\u2019impact + tokens en masse \u2192 burn direct"
    ],
    keywords: "Port\u00e9e \u00b7 Pi\u00e9tinement \u00b7 D\u00e9vorer \u00b7 Recyclage",
    curve: [0, 12, 19, 11, 7, 8, 3, 2],
    avgMv: 2.95
  },
  {
    commander: "Cloud, Ex-SOLDIER",
    colors: ["W", "R", "G"],
    bg: "linear-gradient(160deg, #181a10 0%, #222412 40%, #181a10 100%)",
    accent: "#ebcb8b",
    accentDim: "rgba(235,203,139,0.25)",
    text: "#d8d8c8",
    textDim: "#8a8a68",
    strategy: "Voltron \u00c9quipement. Armez Cloud jusqu\u2019aux dents \u00e0 co\u00fbt r\u00e9duit. Puresteel Paladin = \u00e9quipement gratuit, Sram = pioche par arme. Un Cloud bien charg\u00e9, c\u2019est comme un tank avec une \u00e9p\u00e9e Buster.",
    combos: [
      "Paladin puracier + ma\u00eetrise m\u00e9tal \u2192 co\u00fbt d\u2019\u00e9quipement gratuit",
      "Sram + sorts d\u2019\u00e9quipement \u2192 moteur de pioche",
      "Hache de sang forg\u00e9e \u2192 armes qui se multiplient \u00e0 chaque frappe",
      "Cuirasse de sombracier + Fl\u00e9au du conqu\u00e9rant \u2192 frappes prot\u00e9g\u00e9es"
    ],
    keywords: "C\u00e9l\u00e9rit\u00e9 \u00b7 Double initiative \u00b7 Vigilance \u00b7 Vol",
    curve: [1, 11, 20, 19, 7, 2, 2, 1],
    avgMv: 2.62
  }
];

const glossaryKeywords = [
  { fr: "Vol", desc: "Ne peut \u00eatre bloqu\u00e9 que par vol ou port\u00e9e" },
  { fr: "Pi\u00e9tinement", desc: "D\u00e9g\u00e2ts exc\u00e9dentaires inflig\u00e9s au joueur" },
  { fr: "C\u00e9l\u00e9rit\u00e9", desc: "Peut attaquer et s\u2019engager imm\u00e9diatement" },
  { fr: "Contact mortel", desc: "Toute blessure \u00e0 une cr\u00e9ature est mortelle" },
  { fr: "Lien de vie", desc: "D\u00e9g\u00e2ts inflig\u00e9s = gain de vie" },
  { fr: "Menace", desc: "Bloqu\u00e9 par 2 cr\u00e9atures minimum" },
  { fr: "Initiative", desc: "Inflige ses blessures de combat en premier" },
  { fr: "Double initiative", desc: "Blessures en premier ET normalement" },
  { fr: "Infection", desc: "Marqueurs -1/-1 aux cr\u00e9atures, poison aux joueurs" },
  { fr: "Garde", desc: "Adversaire paie un co\u00fbt extra pour cibler" },
  { fr: "Changelin", desc: "Poss\u00e8de tous les types de cr\u00e9ature" },
  { fr: "Cascade", desc: "Exile jusqu\u2019\u00e0 trouver un sort moins cher, lancez-le gratis" },
  { fr: "Suspension", desc: "Exil\u00e9 avec marqueurs temps, lanc\u00e9 quand il n\u2019y en a plus" },
  { fr: "Drague", desc: "Au lieu de piocher, meulez pour le ramener" },
  { fr: "Meule", desc: "Mettez des cartes du dessus au cimeti\u00e8re" },
  { fr: "Recyclage", desc: "D\u00e9faussez + payez pour piocher une carte" },
  { fr: "Regard", desc: "Regardez le dessus, mettez dessus ou dessous" },
  { fr: "Port\u00e9e", desc: "Peut bloquer les cr\u00e9atures avec le vol" },
  { fr: "Flash", desc: "Peut \u00eatre lanc\u00e9 \u00e0 tout moment" },
  { fr: "Vigilance", desc: "Attaquer n\u2019engage pas cette cr\u00e9ature" },
  { fr: "Constellation", desc: "Se d\u00e9clenche quand un enchantement arrive" },
  { fr: "Convocation", desc: "Engagez des cr\u00e9atures pour aider \u00e0 payer" },
];

const pipLetters = { W: 'W', U: 'U', B: 'B', R: 'R', G: 'G' };

function renderCard(deck) {
  const maxCurve = Math.max(...deck.curve);
  const curveHTML = deck.curve.map((count, i) => {
    const pct = maxCurve > 0 ? (count / maxCurve) * 80 : 0;
    return `
      <div class="mana-bar-group">
        <span class="mana-bar-count">${count > 0 ? count : ''}</span>
        <div class="mana-bar" style="height:${pct}%"></div>
        <span class="mana-bar-label">${i}</span>
      </div>`;
  }).join('');

  const pipsHTML = deck.colors.map(c =>
    `<span class="mana-pip pip-${c}">${pipLetters[c]}</span>`
  ).join('');

  const combosHTML = deck.combos.map(c =>
    `<li>${c}</li>`
  ).join('');

  return `
    <div class="card" style="--card-bg:${deck.bg};--accent:${deck.accent};--accent-dim:${deck.accentDim};--text:${deck.text};--text-dim:${deck.textDim}">
      <div class="card-border"></div>
      <div class="card-header">
        <img data-commander="${deck.commander}" alt="${deck.commander}" loading="lazy">
        <div class="card-name-bar">
          <span class="commander-name">${deck.commander}</span>
          <span class="mana-pips">${pipsHTML}</span>
        </div>
      </div>
      <div class="card-body">
        <div class="section-label">Strat\u00e9gie</div>
        <div class="strategy-text">${deck.strategy}</div>
        <div class="section-label">Lignes de Victoire</div>
        <ul class="combos-list">${combosHTML}</ul>
        <div class="keywords-line"><strong>Mots-cl\u00e9s :</strong> ${deck.keywords}</div>
        <div class="mana-curve-section">
          <div class="section-label">Courbe de Mana</div>
          <div class="mana-curve">${curveHTML}</div>
          <div class="avg-mv">Moy. ${deck.avgMv.toFixed(2)}</div>
        </div>
      </div>
    </div>`;
}

function renderGlossary() {
  const half = Math.ceil(glossaryKeywords.length / 2);
  const cards = [0, 1].map(page => {
    const slice = page === 0
      ? glossaryKeywords.slice(0, half)
      : glossaryKeywords.slice(half);
    const itemsHTML = slice.map(k =>
      `<div class="glossary-item"><strong>${k.fr}</strong> \u2014 ${k.desc}</div>`
    ).join('');
    return `
      <div class="card" style="--card-bg:linear-gradient(160deg,#151520 0%,#1a1a2a 40%,#151520 100%);--accent:#d4a76a;--accent-dim:rgba(212,167,106,0.25);--text:#d0ccc0;--text-dim:#8a8678">
        <div class="card-border"></div>
        <div class="glossary-body">
          <div class="glossary-title">\ud83d\udcd6 Glossaire${page === 1 ? ' (suite)' : ''}</div>
          ${itemsHTML}
        </div>
      </div>`;
  });
  return cards.join('');
}

document.body.innerHTML = decks.map(renderCard).join('') + renderGlossary();

// Fetch art from Scryfall JSON API
document.querySelectorAll('img[data-commander]').forEach(async img => {
  const name = img.dataset.commander;
  try {
    const resp = await fetch(`https://api.scryfall.com/cards/named?fuzzy=${encodeURIComponent(name)}`);
    if (!resp.ok) return;
    const data = await resp.json();
    const uri = data.image_uris?.art_crop
      ?? data.card_faces?.[0]?.image_uris?.art_crop;
    if (uri) img.src = uri;
  } catch (e) { /* network failure */ }
});
</script>
</body>
</html>'''

with open('deck_cards.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Written {len(html)} bytes to deck_cards.html")
