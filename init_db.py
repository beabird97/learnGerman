from app import app, db
from models import User, Word, Verb, UserProgress

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()

        # Check if users already exist
        if User.query.first() is None:
            # Create users
            users = [
                User(username='sam', password='sam'),
                User(username='sheryl', password='sheryl'),
                User(username='chris', password='chris')
            ]
            for user in users:
                db.session.add(user)

            # Commit users first to get their IDs
            db.session.commit()

            # Now create initial progress entries
            for user in users:
                progress = UserProgress(user_id=user.id)
                db.session.add(progress)

            # 100 common German nouns
            words = [
                ('Mann', 'man', 'der'), ('Frau', 'woman', 'die'), ('Kind', 'child', 'das'),
                ('Haus', 'house', 'das'), ('Auto', 'car', 'das'), ('Stadt', 'city', 'die'),
                ('Land', 'country', 'das'), ('Welt', 'world', 'die'), ('Leben', 'life', 'das'),
                ('Jahr', 'year', 'das'), ('Tag', 'day', 'der'), ('Zeit', 'time', 'die'),
                ('Arbeit', 'work', 'die'), ('Familie', 'family', 'die'), ('Freund', 'friend', 'der'),
                ('Schule', 'school', 'die'), ('Buch', 'book', 'das'), ('Tür', 'door', 'die'),
                ('Fenster', 'window', 'das'), ('Tisch', 'table', 'der'), ('Stuhl', 'chair', 'der'),
                ('Hand', 'hand', 'die'), ('Kopf', 'head', 'der'), ('Auge', 'eye', 'das'),
                ('Wasser', 'water', 'das'), ('Brot', 'bread', 'das'), ('Geld', 'money', 'das'),
                ('Name', 'name', 'der'), ('Weg', 'way', 'der'), ('Raum', 'room', 'der'),
                ('Mutter', 'mother', 'die'), ('Vater', 'father', 'der'), ('Bruder', 'brother', 'der'),
                ('Schwester', 'sister', 'die'), ('Sohn', 'son', 'der'), ('Tochter', 'daughter', 'die'),
                ('Hund', 'dog', 'der'), ('Katze', 'cat', 'die'), ('Fisch', 'fish', 'der'),
                ('Vogel', 'bird', 'der'), ('Baum', 'tree', 'der'), ('Blume', 'flower', 'die'),
                ('Garten', 'garden', 'der'), ('Straße', 'street', 'die'), ('Platz', 'place', 'der'),
                ('Kirche', 'church', 'die'), ('Geschäft', 'store', 'das'), ('Markt', 'market', 'der'),
                ('Restaurant', 'restaurant', 'das'), ('Hotel', 'hotel', 'das'), ('Bank', 'bank', 'die'),
                ('Post', 'post office', 'die'), ('Flughafen', 'airport', 'der'), ('Bahnhof', 'train station', 'der'),
                ('Bus', 'bus', 'der'), ('Zug', 'train', 'der'), ('Fahrrad', 'bicycle', 'das'),
                ('Telefon', 'telephone', 'das'), ('Computer', 'computer', 'der'), ('Brief', 'letter', 'der'),
                ('Zeitung', 'newspaper', 'die'), ('Musik', 'music', 'die'), ('Bild', 'picture', 'das'),
                ('Film', 'film', 'der'), ('Spiel', 'game', 'das'), ('Sport', 'sport', 'der'),
                ('Fußball', 'soccer', 'der'), ('Essen', 'food', 'das'), ('Getränk', 'drink', 'das'),
                ('Kaffee', 'coffee', 'der'), ('Tee', 'tea', 'der'), ('Milch', 'milk', 'die'),
                ('Bier', 'beer', 'das'), ('Wein', 'wine', 'der'), ('Apfel', 'apple', 'der'),
                ('Ei', 'egg', 'das'), ('Käse', 'cheese', 'der'), ('Fleisch', 'meat', 'das'),
                ('Gemüse', 'vegetable', 'das'), ('Salat', 'salad', 'der'), ('Suppe', 'soup', 'die'),
                ('Kuchen', 'cake', 'der'), ('Schokolade', 'chocolate', 'die'), ('Zucker', 'sugar', 'der'),
                ('Salz', 'salt', 'das'), ('Pfeffer', 'pepper', 'der'), ('Messer', 'knife', 'das'),
                ('Gabel', 'fork', 'die'), ('Löffel', 'spoon', 'der'), ('Tasse', 'cup', 'die'),
                ('Glas', 'glass', 'das'), ('Teller', 'plate', 'der'), ('Flasche', 'bottle', 'die'),
                ('Hemd', 'shirt', 'das'), ('Hose', 'pants', 'die'), ('Kleid', 'dress', 'das'),
                ('Schuh', 'shoe', 'der'), ('Hut', 'hat', 'der'), ('Tasche', 'bag', 'die'),
                ('Uhr', 'clock', 'die'), ('Woche', 'week', 'die'), ('Monat', 'month', 'der'),
                ('Minute', 'minute', 'die'), ('Stunde', 'hour', 'die'), ('Nacht', 'night', 'die')
            ]

            for german, english, article in words:
                word = Word(german=german, english=english, article=article)
                db.session.add(word)

            # 30 common German verbs with present tense conjugations
            verbs = [
                ('sein', 'to be', 'bin', 'bist', 'ist', 'sind', 'seid', 'sind'),
                ('haben', 'to have', 'habe', 'hast', 'hat', 'haben', 'habt', 'haben'),
                ('werden', 'to become', 'werde', 'wirst', 'wird', 'werden', 'werdet', 'werden'),
                ('können', 'can/to be able to', 'kann', 'kannst', 'kann', 'können', 'könnt', 'können'),
                ('müssen', 'must/to have to', 'muss', 'musst', 'muss', 'müssen', 'müsst', 'müssen'),
                ('sagen', 'to say', 'sage', 'sagst', 'sagt', 'sagen', 'sagt', 'sagen'),
                ('machen', 'to do/make', 'mache', 'machst', 'macht', 'machen', 'macht', 'machen'),
                ('geben', 'to give', 'gebe', 'gibst', 'gibt', 'geben', 'gebt', 'geben'),
                ('kommen', 'to come', 'komme', 'kommst', 'kommt', 'kommen', 'kommt', 'kommen'),
                ('wollen', 'to want', 'will', 'willst', 'will', 'wollen', 'wollt', 'wollen'),
                ('gehen', 'to go', 'gehe', 'gehst', 'geht', 'gehen', 'geht', 'gehen'),
                ('wissen', 'to know', 'weiß', 'weißt', 'weiß', 'wissen', 'wisst', 'wissen'),
                ('sehen', 'to see', 'sehe', 'siehst', 'sieht', 'sehen', 'seht', 'sehen'),
                ('lassen', 'to let/leave', 'lasse', 'lässt', 'lässt', 'lassen', 'lasst', 'lassen'),
                ('stehen', 'to stand', 'stehe', 'stehst', 'steht', 'stehen', 'steht', 'stehen'),
                ('finden', 'to find', 'finde', 'findest', 'findet', 'finden', 'findet', 'finden'),
                ('nehmen', 'to take', 'nehme', 'nimmst', 'nimmt', 'nehmen', 'nehmt', 'nehmen'),
                ('tun', 'to do', 'tue', 'tust', 'tut', 'tun', 'tut', 'tun'),
                ('heißen', 'to be called', 'heiße', 'heißt', 'heißt', 'heißen', 'heißt', 'heißen'),
                ('denken', 'to think', 'denke', 'denkst', 'denkt', 'denken', 'denkt', 'denken'),
                ('sprechen', 'to speak', 'spreche', 'sprichst', 'spricht', 'sprechen', 'sprecht', 'sprechen'),
                ('bringen', 'to bring', 'bringe', 'bringst', 'bringt', 'bringen', 'bringt', 'bringen'),
                ('leben', 'to live', 'lebe', 'lebst', 'lebt', 'leben', 'lebt', 'leben'),
                ('fahren', 'to drive', 'fahre', 'fährst', 'fährt', 'fahren', 'fahrt', 'fahren'),
                ('laufen', 'to run/walk', 'laufe', 'läufst', 'läuft', 'laufen', 'lauft', 'laufen'),
                ('arbeiten', 'to work', 'arbeite', 'arbeitest', 'arbeitet', 'arbeiten', 'arbeitet', 'arbeiten'),
                ('lernen', 'to learn', 'lerne', 'lernst', 'lernt', 'lernen', 'lernt', 'lernen'),
                ('spielen', 'to play', 'spiele', 'spielst', 'spielt', 'spielen', 'spielt', 'spielen'),
                ('lieben', 'to love', 'liebe', 'liebst', 'liebt', 'lieben', 'liebt', 'lieben'),
                ('kaufen', 'to buy', 'kaufe', 'kaufst', 'kauft', 'kaufen', 'kauft', 'kaufen')
            ]

            for infinitive, english, ich, du, er, wir, ihr, sie in verbs:
                verb = Verb(
                    infinitive=infinitive,
                    english=english,
                    ich=ich,
                    du=du,
                    er_sie_es=er,
                    wir=wir,
                    ihr=ihr,
                    sie_Sie=sie
                )
                db.session.add(verb)

            db.session.commit()
            print("Database initialized successfully!")
        else:
            print("Database already initialized.")

if __name__ == '__main__':
    init_database()
