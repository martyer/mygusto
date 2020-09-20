important_tags = ['Schweiz', 'Sommer', 'Frühling', 'Herbst', 'Winter', 'Vegetarisch', 'Europa', 'Fleisch/Fisch',
                  'Nordamerika', 'Fingerfood', 'Pizza', 'Salat', 'Familienrezepte', 'Mexiko', 'Gesunde Rezepte',
                  'Italien', 'Suppe', 'Pasta', 'Wähen, Quiches, Tartes', 'Vegan', 'Brot', 'Auflauf/Gratin', 'Glace',
                  'Grossbritannien', 'Asien', 'Wok', 'Mittelamerika und Karibik', 'Burger', 'Risotto', 'Afrika',
                  'Kuchen', 'Guetzli', 'Eintöpfe', 'Wild', 'Nordafrika', 'Root', 'Frankreich', 'Vietnam', 'Südafrika',
                  'Australien', 'Spanien', 'Orient', 'Torte', 'Österreich', 'Balkan', 'Skandinavien', 'Griechenland',
                  'Deutschland', 'Japan', 'Smoothie', 'Thailand', 'Fusion', 'Südamerika']


def make_one_hot_vector(recipe):
    one_hot = [0] * 53
    tags = recipe['_source']['tags']
    for tag_name in important_tags:
        values = [tag['name'] for tag in tags if tag['type'] == tag_name]
        for value in values:
            one_hot[important_tags.index(value)] = 1
    return one_hot
