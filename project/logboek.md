# Logboek Introductieproject

Dit logboek documenteert voortgang, keuzes, problemen en reflecties tijdens het project. Gebruik het sjabloon hieronder voor elke afgeronde eenheid werk.

## Sjabloon (kopieer voor nieuwe entries)
```
## DAG MAAND JAAR UURMINUUT
Korte maar volledige beschrijving van wat je gedaan hebt (>20 woorden) en vooral waarom je het zo hebt aangepakt. Beschrijf verwachtingen vs resultaat, problemen en hypotheses, en wat je volgende acties zijn.
- Doel: ...
- Resultaat: ...
- Problemen & hypotheses: ...
- Volgende acties: ...
```

---

## 7 December 2025 1335
Project gestart. Ik heb de projectfolder aangemaakt en het logboekbestand toegevoegd.
Ik ga nu beginnen met de Blackjack-tutorial te volgen op Youtube.

## 7 December 2025 1442
Ben begonnen de tutorial te volgen en heb de bestand blackjack.py aangemaakt in mijn projectfolder. Ik heb het pygame-venster correct kunnen openen en de basis van de game loop werkt. Ik begrijp nog niet alles, zoals deepcopy, maar ik heb dit opgezocht en uitleg gekregen. Tot nu toe voelt alles duidelijk en ik ben klaar om verder te bouwen aan het spel.

## 7 December 2025 1541
Ik heb nu een functie toegevoegd die de knoppen en het scoreboard op het scherm tekent. de "DEAL HAND", "HIT ME", "STAND" knoppen verschijnen afhankelijk van de staat van het spel (active of niet). Ook heb ik win/loss/draw records toegevoegd en een tweede font toegevoegd om de tekst duidelijk op verschillende groottes te tonen. Ik begin te begrijpen hoe pygame rechthoeken tekent en hoe knoppen visueel worden weergegeven. Dit voelde als een duidelijke stap vooruit.

## 7 December 2025 1622
Ik heb variabelen toegevoegd voor de spelerhand, dealerhand, het deck en de spelstatus. Ook heb ik de DEAL HAND-knop actief gemaakt: wanneer je erop klikt wordt het spel gestart, het deck opnieuw aangemaakt en alle handen leeggemaakt. Zo begint elke ronde in een volledig nieuwe, schone toestand.

## 7 December 2025 1724
Ik heb een functie deal_cards() toegevoegd waarmee de speler en dealer kaarten uit het deck kunnen trekken. Ook heb ik de initial deal geïmplementeerd: zodra je op DEAL HAND klikt, krijgen speler en dealer elk twee kaarten en wordt het deck en de handen opnieuw ingesteld. Hierdoor kan elke ronde correct en schoon beginnen met echte kaarten.

## 7 December 2025 1810
Ik heb een functie draw_cards() toegevoegd waarmee de kaarten van de speler en dealer visueel op het scherm worden getoond. De eerste kaart van de dealer blijft verborgen zolang de speler nog speelt (???), en wordt pas zichtbaar als reveal_dealer = True wordt gezet. Hierdoor kan het spel nu echt visueel gespeeld worden en is de basis gelegd voor verdere acties zoals hit of stand.

## 8 December 2025 1153
Vandaag heb ik eindelijk de scoreberekening toegevoegd, inclusief hoe Azen moeten tellen. Ook toont het spel nu netjes de scores op het scherm. De dealer speelt nu automatisch verder tot hij 17 heeft. Het spel begint hierdoor echt op blackjack te lijken.

## 8 December 2025 1228
ik heb de HIT- en STAND-knoppen werkend gemaakt. Met hand_active kan de speler nu alleen kaarten nemen tijdens zijn beurt, en bij STAND wordt de dealerkaart onthuld. De basis van de game-flow werkt nu zoals in echt Blackjack.

## 8 December 2025 1321
Ik heb de results-lijst toegevoegd om berichten voor verschillende uitkomsten van het spel op te slaan, en de variabele outcome om het resultaat van de huidige hand bij te houden. Daarnaast heb ik de functie check_endgame() gemaakt, die automatisch controleert of de speler gebust is, gewonnen, verloren of gelijk gespeeld heeft, en de records-lijst hierop aanpast. Ook heb ik de DEAL HAND-knop toegevoegd en de functionaliteit ervan geïmplementeerd in de event-lus, zodat het klikken erop een nieuw spel start, de beginhanden van speler en dealer worden gedeeld en alle noodzakelijke spelvariabelen worden gereset. Dit zorgt ervoor dat het spel correct van ronde naar ronde verloopt.

## 9 December 2025 1157
Ik heb de volledige tutorial afgewerkt en ga een aparte commit maken met een duidelijke boodschap dat de tutorial is afgerond. Dit vormt nu een duidelijk eindpunt van het basisproject, zodat ik vanaf hier kan beginnen aan mijn eigen uitbreidingen.


