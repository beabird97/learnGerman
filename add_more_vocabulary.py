from app import app, db
from models import Word, Verb

def add_vocabulary():
    with app.app_context():
        # Additional nouns with articles
        new_nouns = [
            # People & Family
            ("der", "Vater", "father"),
            ("die", "Mutter", "mother"),
            ("der", "Bruder", "brother"),
            ("die", "Schwester", "sister"),
            ("der", "Sohn", "son"),
            ("die", "Tochter", "daughter"),
            ("der", "Freund", "friend (male)"),
            ("die", "Freundin", "friend (female)"),
            ("der", "Lehrer", "teacher (male)"),
            ("die", "Lehrerin", "teacher (female)"),
            ("der", "Arzt", "doctor (male)"),
            ("die", "Ärztin", "doctor (female)"),
            ("der", "Student", "student (male)"),
            ("die", "Studentin", "student (female)"),
            ("das", "Baby", "baby"),
            ("der", "Junge", "boy"),
            ("das", "Mädchen", "girl"),

            # House & Home
            ("die", "Wohnung", "apartment"),
            ("das", "Zimmer", "room"),
            ("die", "Küche", "kitchen"),
            ("das", "Bad", "bathroom"),
            ("das", "Schlafzimmer", "bedroom"),
            ("das", "Wohnzimmer", "living room"),
            ("die", "Tür", "door"),
            ("das", "Fenster", "window"),
            ("der", "Tisch", "table"),
            ("der", "Stuhl", "chair"),
            ("das", "Bett", "bed"),
            ("der", "Schrank", "closet"),
            ("die", "Lampe", "lamp"),
            ("der", "Teppich", "carpet"),
            ("die", "Wand", "wall"),
            ("die", "Decke", "ceiling"),
            ("der", "Boden", "floor"),

            # Food & Drink
            ("das", "Brot", "bread"),
            ("die", "Butter", "butter"),
            ("der", "Käse", "cheese"),
            ("die", "Milch", "milk"),
            ("das", "Wasser", "water"),
            ("der", "Kaffee", "coffee"),
            ("der", "Tee", "tea"),
            ("das", "Bier", "beer"),
            ("der", "Wein", "wine"),
            ("der", "Saft", "juice"),
            ("das", "Fleisch", "meat"),
            ("der", "Fisch", "fish"),
            ("das", "Gemüse", "vegetable"),
            ("das", "Obst", "fruit"),
            ("der", "Apfel", "apple"),
            ("die", "Banane", "banana"),
            ("die", "Orange", "orange"),
            ("die", "Kartoffel", "potato"),
            ("die", "Tomate", "tomato"),
            ("der", "Salat", "salad"),
            ("die", "Suppe", "soup"),
            ("der", "Kuchen", "cake"),
            ("das", "Ei", "egg"),
            ("der", "Reis", "rice"),
            ("die", "Nudel", "noodle"),

            # Transportation
            ("der", "Zug", "train"),
            ("der", "Bus", "bus"),
            ("das", "Flugzeug", "airplane"),
            ("das", "Fahrrad", "bicycle"),
            ("das", "Motorrad", "motorcycle"),
            ("das", "Schiff", "ship"),
            ("die", "Straße", "street"),
            ("der", "Weg", "way/path"),
            ("die", "Brücke", "bridge"),
            ("der", "Bahnhof", "train station"),
            ("der", "Flughafen", "airport"),

            # Nature
            ("der", "Baum", "tree"),
            ("die", "Blume", "flower"),
            ("der", "Berg", "mountain"),
            ("der", "Fluss", "river"),
            ("der", "See", "lake"),
            ("das", "Meer", "sea"),
            ("der", "Wald", "forest"),
            ("der", "Himmel", "sky"),
            ("die", "Sonne", "sun"),
            ("der", "Mond", "moon"),
            ("der", "Stern", "star"),
            ("die", "Wolke", "cloud"),
            ("der", "Regen", "rain"),
            ("der", "Schnee", "snow"),
            ("der", "Wind", "wind"),
            ("das", "Wetter", "weather"),

            # Time
            ("die", "Zeit", "time"),
            ("der", "Tag", "day"),
            ("die", "Nacht", "night"),
            ("die", "Woche", "week"),
            ("der", "Monat", "month"),
            ("die", "Stunde", "hour"),
            ("die", "Minute", "minute"),
            ("die", "Sekunde", "second"),
            ("der", "Morgen", "morning"),
            ("der", "Abend", "evening"),
            ("der", "Mittag", "noon"),
            ("die", "Mitternacht", "midnight"),

            # Body
            ("der", "Kopf", "head"),
            ("das", "Auge", "eye"),
            ("das", "Ohr", "ear"),
            ("die", "Nase", "nose"),
            ("der", "Mund", "mouth"),
            ("die", "Hand", "hand"),
            ("der", "Fuß", "foot"),
            ("das", "Bein", "leg"),
            ("der", "Arm", "arm"),
            ("das", "Herz", "heart"),
            ("der", "Körper", "body"),
            ("der", "Finger", "finger"),
            ("das", "Haar", "hair"),

            # Clothing
            ("das", "Hemd", "shirt"),
            ("die", "Hose", "pants"),
            ("das", "Kleid", "dress"),
            ("der", "Rock", "skirt"),
            ("die", "Jacke", "jacket"),
            ("der", "Mantel", "coat"),
            ("der", "Hut", "hat"),
            ("der", "Schuh", "shoe"),
            ("die", "Socke", "sock"),
            ("die", "Tasche", "bag/pocket"),

            # School & Work
            ("die", "Schule", "school"),
            ("die", "Universität", "university"),
            ("das", "Büro", "office"),
            ("das", "Buch", "book"),
            ("das", "Heft", "notebook"),
            ("der", "Stift", "pen"),
            ("der", "Bleistift", "pencil"),
            ("das", "Papier", "paper"),
            ("der", "Computer", "computer"),
            ("das", "Telefon", "telephone"),
            ("das", "Handy", "cell phone"),
            ("die", "Arbeit", "work"),
            ("der", "Beruf", "profession"),

            # City & Buildings
            ("das", "Geschäft", "store"),
            ("der", "Laden", "shop"),
            ("das", "Restaurant", "restaurant"),
            ("das", "Café", "cafe"),
            ("das", "Hotel", "hotel"),
            ("das", "Krankenhaus", "hospital"),
            ("die", "Kirche", "church"),
            ("das", "Museum", "museum"),
            ("das", "Theater", "theater"),
            ("das", "Kino", "cinema"),
            ("die", "Post", "post office"),
            ("die", "Bank", "bank"),
            ("der", "Park", "park"),
            ("der", "Platz", "square/place"),

            # Abstract Concepts
            ("die", "Liebe", "love"),
            ("die", "Freude", "joy"),
            ("die", "Angst", "fear"),
            ("die", "Hoffnung", "hope"),
            ("die", "Wahrheit", "truth"),
            ("die", "Frage", "question"),
            ("die", "Antwort", "answer"),
            ("das", "Problem", "problem"),
            ("die", "Lösung", "solution"),
            ("die", "Idee", "idea"),
            ("der", "Gedanke", "thought"),
            ("das", "Glück", "happiness/luck"),
            ("die", "Gesundheit", "health"),
            ("die", "Kraft", "strength/power"),

            # Numbers & Money
            ("die", "Zahl", "number"),
            ("das", "Geld", "money"),
            ("der", "Euro", "euro"),
            ("der", "Preis", "price"),

            # Colors & Qualities
            ("die", "Farbe", "color"),
            ("die", "Größe", "size"),
            ("die", "Form", "shape"),

            # Communication
            ("die", "Sprache", "language"),
            ("das", "Wort", "word"),
            ("der", "Satz", "sentence"),
            ("der", "Brief", "letter"),
            ("die", "Nachricht", "message"),
            ("das", "Gespräch", "conversation"),

            # Animals
            ("der", "Hund", "dog"),
            ("die", "Katze", "cat"),
            ("das", "Pferd", "horse"),
            ("die", "Kuh", "cow"),
            ("das", "Schwein", "pig"),
            ("das", "Schaf", "sheep"),
            ("der", "Vogel", "bird"),
            ("der", "Fisch", "fish (animal)"),
            ("die", "Maus", "mouse"),

            # Entertainment
            ("die", "Musik", "music"),
            ("das", "Lied", "song"),
            ("der", "Film", "film/movie"),
            ("das", "Spiel", "game"),
            ("der", "Sport", "sport"),
            ("das", "Hobby", "hobby"),

            # Miscellaneous
            ("die", "Sache", "thing"),
            ("das", "Ding", "thing/object"),
            ("der", "Name", "name"),
            ("die", "Seite", "side/page"),
            ("der", "Teil", "part"),
            ("das", "Stück", "piece"),
            ("die", "Art", "kind/type"),
            ("die", "Weise", "way/manner"),
            ("der", "Grund", "reason/ground"),
            ("das", "Ende", "end"),
            ("der", "Anfang", "beginning"),
        ]

        # Additional verbs with conjugations
        new_verbs = [
            # Common verbs
            ("gehen", "go", "gehe", "gehst", "geht", "gehen", "geht", "gehen"),
            ("kommen", "come", "komme", "kommst", "kommt", "kommen", "kommt", "kommen"),
            ("sehen", "see", "sehe", "siehst", "sieht", "sehen", "seht", "sehen"),
            ("nehmen", "take", "nehme", "nimmst", "nimmt", "nehmen", "nehmt", "nehmen"),
            ("geben", "give", "gebe", "gibst", "gibt", "geben", "gebt", "geben"),
            ("wissen", "know", "weiß", "weißt", "weiß", "wissen", "wisst", "wissen"),
            ("denken", "think", "denke", "denkst", "denkt", "denken", "denkt", "denken"),
            ("machen", "make/do", "mache", "machst", "macht", "machen", "macht", "machen"),
            ("sagen", "say", "sage", "sagst", "sagt", "sagen", "sagt", "sagen"),
            ("können", "can/be able to", "kann", "kannst", "kann", "können", "könnt", "können"),
            ("müssen", "must/have to", "muss", "musst", "muss", "müssen", "müsst", "müssen"),
            ("wollen", "want", "will", "willst", "will", "wollen", "wollt", "wollen"),
            ("sollen", "should", "soll", "sollst", "soll", "sollen", "sollt", "sollen"),
            ("dürfen", "may/be allowed", "darf", "darfst", "darf", "dürfen", "dürft", "dürfen"),
            ("mögen", "like", "mag", "magst", "mag", "mögen", "mögt", "mögen"),
            ("werden", "become", "werde", "wirst", "wird", "werden", "werdet", "werden"),

            # Action verbs
            ("essen", "eat", "esse", "isst", "isst", "essen", "esst", "essen"),
            ("trinken", "drink", "trinke", "trinkst", "trinkt", "trinken", "trinkt", "trinken"),
            ("schlafen", "sleep", "schlafe", "schläfst", "schläft", "schlafen", "schlaft", "schlafen"),
            ("lesen", "read", "lese", "liest", "liest", "lesen", "lest", "lesen"),
            ("schreiben", "write", "schreibe", "schreibst", "schreibt", "schreiben", "schreibt", "schreiben"),
            ("sprechen", "speak", "spreche", "sprichst", "spricht", "sprechen", "sprecht", "sprechen"),
            ("hören", "hear", "höre", "hörst", "hört", "hören", "hört", "hören"),
            ("verstehen", "understand", "verstehe", "verstehst", "versteht", "verstehen", "versteht", "verstehen"),
            ("kaufen", "buy", "kaufe", "kaufst", "kauft", "kaufen", "kauft", "kaufen"),
            ("verkaufen", "sell", "verkaufe", "verkaufst", "verkauft", "verkaufen", "verkauft", "verkaufen"),

            # Movement verbs
            ("laufen", "run/walk", "laufe", "läufst", "läuft", "laufen", "lauft", "laufen"),
            ("fahren", "drive/go", "fahre", "fährst", "fährt", "fahren", "fahrt", "fahren"),
            ("fliegen", "fly", "fliege", "fliegst", "fliegt", "fliegen", "fliegt", "fliegen"),
            ("schwimmen", "swim", "schwimme", "schwimmst", "schwimmt", "schwimmen", "schwimmt", "schwimmen"),
            ("springen", "jump", "springe", "springst", "springt", "springen", "springt", "springen"),
            ("stehen", "stand", "stehe", "stehst", "steht", "stehen", "steht", "stehen"),
            ("sitzen", "sit", "sitze", "sitzt", "sitzt", "sitzen", "sitzt", "sitzen"),
            ("liegen", "lie", "liege", "liegst", "liegt", "liegen", "liegt", "liegen"),

            # Communication verbs
            ("fragen", "ask", "frage", "fragst", "fragt", "fragen", "fragt", "fragen"),
            ("antworten", "answer", "antworte", "antwortest", "antwortet", "antworten", "antwortet", "antworten"),
            ("rufen", "call", "rufe", "rufst", "ruft", "rufen", "ruft", "rufen"),
            ("erzählen", "tell", "erzähle", "erzählst", "erzählt", "erzählen", "erzählt", "erzählen"),

            # Mental/Emotional verbs
            ("lieben", "love", "liebe", "liebst", "liebt", "lieben", "liebt", "lieben"),
            ("hassen", "hate", "hasse", "hasst", "hasst", "hassen", "hasst", "hassen"),
            ("fühlen", "feel", "fühle", "fühlst", "fühlt", "fühlen", "fühlt", "fühlen"),
            ("glauben", "believe", "glaube", "glaubst", "glaubt", "glauben", "glaubt", "glauben"),
            ("hoffen", "hope", "hoffe", "hoffst", "hofft", "hoffen", "hofft", "hoffen"),
            ("wünschen", "wish", "wünsche", "wünschst", "wünscht", "wünschen", "wünscht", "wünschen"),

            # Work/Activity verbs
            ("arbeiten", "work", "arbeite", "arbeitest", "arbeitet", "arbeiten", "arbeitet", "arbeiten"),
            ("lernen", "learn", "lerne", "lernst", "lernt", "lernen", "lernt", "lernen"),
            ("lehren", "teach", "lehre", "lehrst", "lehrt", "lehren", "lehrt", "lehren"),
            ("spielen", "play", "spiele", "spielst", "spielt", "spielen", "spielt", "spielen"),
            ("üben", "practice", "übe", "übst", "übt", "üben", "übt", "üben"),
            ("beginnen", "begin", "beginne", "beginnst", "beginnt", "beginnen", "beginnt", "beginnen"),
            ("enden", "end", "ende", "endest", "endet", "enden", "endet", "enden"),
            ("helfen", "help", "helfe", "hilfst", "hilft", "helfen", "helft", "helfen"),
            ("suchen", "search", "suche", "suchst", "sucht", "suchen", "sucht", "suchen"),
            ("finden", "find", "finde", "findest", "findet", "finden", "findet", "finden"),

            # Change/Action verbs
            ("öffnen", "open", "öffne", "öffnest", "öffnet", "öffnen", "öffnet", "öffnen"),
            ("schließen", "close", "schließe", "schließt", "schließt", "schließen", "schließt", "schließen"),
            ("bringen", "bring", "bringe", "bringst", "bringt", "bringen", "bringt", "bringen"),
            ("holen", "fetch/get", "hole", "holst", "holt", "holen", "holt", "holen"),
            ("legen", "lay/put", "lege", "legst", "legt", "legen", "legt", "legen"),
            ("stellen", "put/place", "stelle", "stellst", "stellt", "stellen", "stellt", "stellen"),
            ("zeigen", "show", "zeige", "zeigst", "zeigt", "zeigen", "zeigt", "zeigen"),
            ("tragen", "carry/wear", "trage", "trägst", "trägt", "tragen", "tragt", "tragen"),
            ("werfen", "throw", "werfe", "wirfst", "wirft", "werfen", "werft", "werfen"),
            ("ziehen", "pull", "ziehe", "ziehst", "zieht", "ziehen", "zieht", "ziehen"),

            # Daily life verbs
            ("wohnen", "live/reside", "wohne", "wohnst", "wohnt", "wohnen", "wohnt", "wohnen"),
            ("kochen", "cook", "koche", "kochst", "kocht", "kochen", "kocht", "kochen"),
            ("putzen", "clean", "putze", "putzt", "putzt", "putzen", "putzt", "putzen"),
            ("waschen", "wash", "wasche", "wäschst", "wäscht", "waschen", "wascht", "waschen"),
            ("zahlen", "pay", "zahle", "zahlst", "zahlt", "zahlen", "zahlt", "zahlen"),
            ("kosten", "cost", "koste", "kostest", "kostet", "kosten", "kostet", "kosten"),
            ("brauchen", "need", "brauche", "brauchst", "braucht", "brauchen", "braucht", "brauchen"),
            ("benutzen", "use", "benutze", "benutzt", "benutzt", "benutzen", "benutzt", "benutzen"),
        ]

        print("Adding nouns...")
        added_nouns = 0
        for article, german, english in new_nouns:
            # Check if word already exists
            existing = Word.query.filter_by(german=german).first()
            if not existing:
                word = Word(article=article, german=german, english=english)
                db.session.add(word)
                added_nouns += 1

        db.session.commit()
        print(f"✓ Added {added_nouns} new nouns")

        print("\nAdding verbs...")
        added_verbs = 0
        for infinitive, english, ich, du, er_sie_es, wir, ihr, sie_Sie in new_verbs:
            # Check if verb already exists
            existing = Verb.query.filter_by(infinitive=infinitive).first()
            if not existing:
                verb = Verb(
                    infinitive=infinitive,
                    english=english,
                    ich=ich,
                    du=du,
                    er_sie_es=er_sie_es,
                    wir=wir,
                    ihr=ihr,
                    sie_Sie=sie_Sie
                )
                db.session.add(verb)
                added_verbs += 1

        db.session.commit()
        print(f"✓ Added {added_verbs} new verbs")

        # Final counts
        total_words = Word.query.count()
        total_verbs = Verb.query.count()

        print(f"\n✓ Database updated!")
        print(f"Total nouns: {total_words}")
        print(f"Total verbs: {total_verbs}")

        # Show article distribution
        der_count = Word.query.filter_by(article='der').count()
        die_count = Word.query.filter_by(article='die').count()
        das_count = Word.query.filter_by(article='das').count()

        print(f"\nArticle distribution:")
        print(f"  der: {der_count}")
        print(f"  die: {die_count}")
        print(f"  das: {das_count}")

if __name__ == '__main__':
    add_vocabulary()
