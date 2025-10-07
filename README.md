# Werkplaats 2

### Installatie

_Hieronder vind je de installatie-instructies voor het installeren en instellen van je app.
Om de app te runnen heb je de laatste python versie nodig of specifiek v3.13._

1. Clone de repo
   ```sh
   git clone https://github.com/Rac-Software-Development/wp2-2024-mvc-1c1-de-samengestelden.git
   ```
2. Voeg een python interpreter toe
3. In Pycharm klik "Install requirements" of in terminal:
   ```sh
   pip install -r requirements.txt
   ```
5. Run main.py in IDE of in terminal:
   ```sh
   python main.py
   ```

maar het ook handig om als je geen enviroment heeft kan je via de terminal een .env opstarten via de volgende commando's

  ```sh
   python3 -m .venv .venv
   ```

daarna voer je deze commando uit om de .env te activeren

  ```sh
   .\.venv\scripts\activate
   ```

wanner dat je deze omgeving heb geactiveerd kan je de requirements installeer door

   ```sh
   pip install -r requirements.txt
   ```

en daarna Run main.py in IDE of in terminal:

   ```sh
   python main.py
   ```

### users

| Username | Password | Role                                                                                                      |
|----------|----------|-----------------------------------------------------------------------------------------------------------|
| test     | test     | dit is een normale gebruiker rol, met deze rol heb je alleen toegang tot de tabladen questions en prompts |
| admin    | admin    | dit is een admin rol, met deze rol kan de admin wachtwoorden wijzigen en accounts toevoegen               |

### schermen

![image](https://github.com/user-attachments/assets/dbd0dc83-4e70-4015-80cd-43df97662fdc)

bij het starten van het applicatie kom je als eerste bij de login scherm terecht, hier kan je inloggen als de admin of
de test account.

wanneer je inlogt als gebruiker kom je op de vragen pagina terecht, hierop kan je de volgende acties doen: vragen
toevoegen, vragen bijwerken, vragen verwijderen, vragen filteren, vragen exporteren/importeren en per vraag de vragen
indexeren.
![image](https://github.com/user-attachments/assets/9564028d-e71e-4fc7-a869-c9158e0f68cd)

![image](https://github.com/user-attachments/assets/b468efca-353c-42c0-9d0d-8b81654a9b31)

bij deze knopje kom je terecht bij de Vraag indexeren naar taxonomie pagina, op deze vraag staan de informatie van deze
desbetreffende vraag, op deze pagina kan de gebruiker een voorstel genereren door een ai, daarnaast kan de gebruiker de
taxonomie selecteren op basis van de gegenereerde taxonomie.

![image](https://github.com/user-attachments/assets/c6a50e0b-f5fb-405a-9388-0bf523283466)

verder kan de gebruiker naar de tablad prompts gaan, daar kan de gebruiker informatie lezen over de prompts, de
statetieken lezen van de aantal keren de ai de goede taxonie heeft gegenereert en hoe vaak het niet goed heeft gedaan.
![image](https://github.com/user-attachments/assets/64743a49-b2b8-408f-89dc-e1a0d3c299f4)

wanneer een admin inlog wordt hij naar de admin panel gestuurd, hierop staat er een verschillende statetieken van de
vragen, de users en de prompts.
![image](https://github.com/user-attachments/assets/edad0df4-819d-4e1b-9428-84ac8819e32a)

verder kan de admin naar de user panel gaan, bij deze panel kan de admin gebruikers aanmaken, verwijderen, wachtwoord
wijzigen.

![image](https://github.com/user-attachments/assets/49ed5c4c-36cb-4907-a85a-609290f5787e)

Vraag indexeren naar taxonomie pagina
![image](https://github.com/user-attachments/assets/99e3c79e-3ccc-478b-bffa-5ee8e28b6dc3)

prompt details page
![image](https://github.com/user-attachments/assets/7b1e43e2-ed79-45c3-b486-5982687a757d)
je komt op deze pagina terecht wanner dat je op een id drukt van een prompt, op deze pagina wordt er een omschrijving
gegeven van de prompt en de succesrate van de prompt.

user details page
![image](https://github.com/user-attachments/assets/c19fffea-9c31-4d21-9017-06a69eb02dea)
je komt op deze pagina terecht wanner dat je op een id drukt van een user, op deze pagina wordt de username en de rol
weergegeven.

## trotse functionaliteiten

Een van de functionaliteiten waar we het meest trots op zijn, is het succesvol integreren van AI in het project en het
implementeren van CRUD-functionaliteiten, zoals het beheren van vragen en gebruikers. We zijn vooral trots op het
toepassen van CRUD, omdat dit een essentiële techniek is die in veel verschillende projecten wordt gebruikt. Het
beheersen ervan is daarom niet alleen waardevol, maar ook een belangrijke stap in onze ontwikkeling
