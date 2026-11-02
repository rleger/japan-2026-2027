# -*- coding: utf-8 -*-
"""Carnet v7 : contenu commun (couverture, sommaire, coup d'œil, carte, avant de partir, checklist par priorité, frise)."""

BOOKING = "https://www.booking.com/hotel/jp/{slug}.html?checkin={ci}&checkout={co}&group_adults=2&no_rooms=1"

def bk(slug, ci, co):
    return BOOKING.format(slug=slug, ci=ci, co=co)

COVER = dict(
    kicker="CARNET DE VOYAGE · LE TRAJET DU DEVIS ALLIBERT, PAR NOUS-MÊMES",
    title="Japon", subtitle="en hiver", jp="冬の日本", kanji="冬",
    dates="Du samedi 26 décembre 2026 au lundi 11 janvier 2027",
    line="Dix-sept jours et quatorze nuits au Japon, en train, en car, en voiture et à pied",
    stops=["Tokyo", "Matsumoto", "Takayama", "Shirakawa-gō", "Ise", "Kumano Kodo", "Nachi", "Kōya-san", "Osaka", "Kyoto", "Nara"],
    foot="Vols directs Air France réservés · version 7.0, 1er novembre 2026",
)

TOC_INTRO = {
    "read": [
        "Ce carnet suit l'itinéraire du devis Allibert du 29 octobre 2026, jour pour jour, avec les hébergements de leur tableau ou ceux que nous leur avons demandés à la place. Il permet de faire le même voyage par nous-mêmes si le devis ne se conclut pas, et sert de contrôle si nous le signons.",
        "La section « Ce que nous devons faire » liste tout, par ordre de priorité, avec les liens. Trois dates de vente sont à noter dans l'agenda : 30 novembre, 1er décembre, 9 décembre, à 2 h du matin heure française.",
        "Les noms d'hébergements sont des liens cliquables vers Booking, aux bonnes dates, pour deux adultes. Toutes les adresses ont une salle de bain privée, sauf mention contraire dans la fiche.",
        "Les pages 3 à 5, sans aucun prix, peuvent être partagées telles quelles.",
    ],
    "v7": "Version 7.0, construite le 1er novembre 2026 : hébergements revérifiés sur Booking ce jour, horaires des fêtes 2025-2026 à revérifier début décembre quand ceux de 2026-2027 seront publiés.",
}

OVERVIEW = dict(
    kicker="EN UN COUP D'ŒIL",
    title="Tokyo, les Alpes, la péninsule de Kii, Kyoto",
    intro="Dix-sept jours à deux, du 26 décembre 2026 au 11 janvier 2027. Tokyo pour commencer ; les Alpes japonaises sous la neige pour le Nouvel An, "
          "Matsumoto, Takayama et le village de Shirakawa-gō ; puis le grand sanctuaire d'Ise, quatre jours de voiture sur la péninsule de Kii, le Kumano Kodo à pied, "
          "la cascade de Nachi et le mont Kōya ; enfin Osaka, Kyoto, Nara, et une dernière journée à Tokyo.",
    rows=[
        ("26 déc.", "Départ", "", "TGV vers Paris, vol direct Air France de nuit.", False),
        ("27 au 30 déc.", "Tokyo", "3", "Arrivée le 27 au soir. Asakusa, Yanaka, sanctuaire Meiji, Shibuya ; Kamakura en option. Le 30 en fin d'après-midi, l'express Azusa pour Matsumoto.", False),
        ("30 déc.", "Matsumoto", "1", "Nuit-étape à l'entrée des Alpes : rue Nawate, soba, bain d'hôtel.", True),
        ("31 déc. et 1er janv.", "Takayama", "2", "Car par le col d'Abō, la vieille ville, le réveillon ; le 1er, Shirakawa-gō sous la neige en car.", True),
        ("2 janv.", "Ise", "1", "Express Hida et Kintetsu, 4 h 30. Arrivée 12 h 30, le Gekū puis Okage Yokochō.", True),
        ("3 et 4 janv.", "Kumano Kodo", "2", "Le Naikū à l'aube, voiture prise à Ise, route de la côte, Hongū, Yunomine. Le 4, Hosshinmon-ōji vers Hongū à pied, bain à Tsuboyu.", True),
        ("5 janv.", "Nachi", "1", "Daimon-zaka, sanctuaire et cascade de Nachi ; nuit face à la mer à Kii-Katsuura, bains dans les grottes.", True),
        ("6 janv.", "Kōya-san, Osaka", "1", "Route de montagne, Okunoin et le Garan, voiture rendue à l'aéroport du Kansai, soirée à Dōtonbori.", True),
        ("7 et 8 janv.", "Kyoto et Nara", "2", "Fushimi Inari, Higashiyama, Gion ; Nara et ses cerfs.", False),
        ("9 janv.", "Tokyo", "1", "Matin à Kyoto, marché de Nishiki, shinkansen, nuit à Gaienmae.", False),
        ("10 janv.", "Retour", "", "Journée à Tokyo, vol direct Air France à 22 h 55.", False),
        ("11 janv.", "Arrivée", "", "Paris à 5 h 50, TGV, à la maison en fin de matinée.", False),
    ],
    brief=[
        ("Le Nouvel An", "Réveillon à Takayama, premier jour de l'année à Shirakawa-gō, hatsumōde au sanctuaire d'Ise le 3 à l'aube."),
        ("Marches", "Kumano Kodo (10 km), Daimon-zaka et Nachi, Okunoin, Fushimi Inari, Nara. Des étapes de 5 à 10 km, sans difficulté technique."),
        ("Hébergements", "Hôtels de ville, un ryokan ou une maison au Kumano, un grand hôtel de bains face à la mer, un hôtel de caractère à Osaka."),
        ("Transports", "Trains et cars jusqu'à Ise, puis quatre jours de voiture sur la péninsule de Kii ; les valises suivent partout."),
        ("Point d'attention", "Le Nozomi du 9 janvier (tout réservé ce week-end-là) et la traduction du permis se réservent tout de suite ; Azusa, cars de montagne et Hida ont leur date de vente en décembre."),
    ],
)

MAP_PAGE = dict(
    kicker="L'ITINÉRAIRE", image="map_overview.png",
    title="De Tokyo à Tokyo, par les Alpes et la péninsule de Kii",
    caption="Numéros : ordre des étapes de nuit. En rouge, les quatre jours de voiture. Cercles dorés : étapes communes avec le carnet v6. Carte établie pour ce carnet ; côtes et relief Natural Earth.",
    cols=[
        ("LE RYTHME", "On marche le matin, quand la lumière est belle et les sites encore vides ; la nuit tombe vers 17 h. Trois nuits à Tokyo, deux à Takayama, deux au Kumano, deux à Kyoto ; le reste en étapes d'une nuit, dans l'ordre du devis Allibert."),
        ("LES NUITS", "Des hôtels de ville bien tenus, un ryokan ou une maison au bord de la rivière chaude du Kumano, un hôtel de bains creusé dans la falaise à Katsuura, un hôtel de caractère à Osaka, et le choix, partout, entre l'adresse d'Allibert et celle que nous préférons."),
        ("LA TABLE", "Soba de Matsumoto, bœuf de Hida à Takayama, udon et tekone-zushi d'Ise, mehari-zushi des pèlerins, thon de Katsuura, cuisine des moines à Kōya-san, les comptoirs d'Osaka et le marché de Nishiki."),
    ],
)

BEFORE = dict(
    kicker="PRÉPARER", title="Avant de partir",
    boxes=[
        ("LES VOLS",
         "<p><b>Aller, samedi 26 décembre.</b> Air France AF274, Paris-Charles-de-Gaulle à 22 h 20, arrivée à Tokyo Haneda le dimanche 27 à 19 h 55. Vol direct, 13 h 35.</p>"
         "<p><b>Retour, dimanche 10 janvier.</b> Air France AF279, Haneda à 22 h 55, arrivée à Paris le lundi 11 à 5 h 50. Vol direct, 14 h 55.</p>"
         "<p><b>Réservés</b> en classe économique avec l'option siège large, 3 431 € pour deux. Il reste à régler le train du 26 décembre vers Paris : une seule place obtenue sur le TGV direct, la seconde est à trouver (voir checklist).</p>"),
        ("L'HIVER LÀ-BAS",
         "<p>5 à 10 °C à Tokyo, Kyoto et sur la côte de Kii ; -5 à 2 °C à Matsumoto, Takayama et Shirakawa-gō, où la neige est quasi certaine début janvier ; 0 à 5 °C à Kōya-san, verglas possible. La nuit tombe vers 17 h : on marche tôt, ce qui évite aussi la foule. Ciel souvent clair et sec sur la côte pacifique.</p>"),
        ("À RÉSERVER TÔT",
         "<ul><li><b>Cette semaine :</b> les deux nuits de Takayama (31 décembre et 1er janvier), le Kumano, la traduction du permis, la voiture.</li>"
         "<li><b>Trois dates de vente :</b> 30 novembre (Azusa du 30 décembre), 1er décembre (cars de montagne), 2 décembre (Hida du 2 janvier, au guichet), à 2 h du matin en France ; le Nozomi du 9 janvier se réserve dès maintenant sur smartEX.</li>"
         "<li>Le détail, dans l'ordre, est dans « Ce que nous devons faire », pages suivantes.</li></ul>"),
        ("LA VOITURE",
         "<p>Du 3 janvier à Ise au 6 janvier à l'aéroport du Kansai. Le permis international français n'est pas reconnu au Japon : il faut le permis français et sa traduction japonaise officielle, impossible à obtenir de la JAF depuis l'étranger, donc par un service en ligne (Japan Experience, 70 € par conducteur, 12 jours). Deux traductions si vous voulez conduire tous les deux.</p>"),
    ],
    foot="Prix et disponibilités vérifiés le 1er novembre 2026 : chaque hébergement proposé était libre aux dates indiquées sur Booking.com. Les prix de fin décembre évoluent vite : Nohga Tokyo est passé de 900 à 1 061 € et Koto no Yume de 655 à 809 € en trois jours. Taux : 175 yens pour 1 €.",
)

CHECK_INTRO = dict(
    kicker="NE RIEN RATER", title="Ce que nous devons faire, par priorité",
    intro="Tout ce qu'il faut réserver ou préparer, du plus urgent au plus simple, avec les liens. Les lignes rouges sont les points bloquants : sans eux, une étape tombe. "
          "Les ventes de train et de car ouvrent un mois avant le jour du voyage, à 10 h au Japon, soit 2 h du matin en France.",
    blocks=[
        ("LE NOUVEL AN À TAKAYAMA", "Le point le plus tendu du voyage : Camille (Allibert) parlait d'une seule chambre restante dans leur adresse. eph TAKAYAMA et Koto no Yume étaient disponibles le 1er novembre, à réserver avant tout le reste."),
        ("LE PERMIS", "Sans traduction japonaise, pas de voiture, et sans voiture le Kumano et Kōya-san deviennent des journées de bus. Douze jours de délai : à commander cette semaine."),
        ("LES CARS DU 31 ET DU 1ER", "Allibert les laisse « à régler sur place ». Le 31 décembre, le car direct Matsumoto → Takayama peut être complet : le réserver le 1er décembre à l'ouverture."),
        ("LE TGV DU 26 DÉCEMBRE", "Une seule place obtenue pour Paris. Deuxième place, autre train avec correspondance, ou voiture jusqu'à Roissy : à régler maintenant."),
    ],
)

# Chaque page : liste de (numéro, titre, sous-titre, items) ; item : (date, titre, détail, niveau B/I/U)
CHECK_PAGES = [
    [
        ("1", "Cette semaine", "ce qui bloque le voyage", [
            ("Avant le 8 nov.", "Décider : Allibert ou par nous-mêmes",
             "Attendre la réponse de Camille au mail du 29 octobre (prix par poste, hébergements ajustés). Si le devis revient vers 11 000 € avec de vrais ryokan, signer ; sinon, dérouler cette liste. Dans les deux cas, traduction du second permis et Nozomi sont à faire par nous.", "B"),
            ("Tout de suite", "Takayama, 31 décembre et 1er janvier",
             "<a href=\"" + bk("eph-takayama", "2026-12-31", "2027-01-02") + "\">eph TAKAYAMA</a> (505 €, salle de bain, 4 min de la gare) ou <a href=\"" + bk("oyado-koto-no-yume", "2026-12-31", "2027-01-02") + "\">Oyado Koto no Yume</a> (809 €, ryokan, demander une twin avec bain). Annulation gratuite à vérifier au moment de réserver ; prendre l'une des deux dès maintenant, quitte à changer.", "B"),
            ("Tout de suite", "Traduction du permis de conduire, pour les deux conducteurs",
             "<a href=\"https://japan-experience.com/transportation/driving-licence-translation\">Japan Experience, traduction officielle</a> : 70 € par permis, environ 12 jours, livraison à domicile. Scanner le permis recto verso après paiement. La JAF ne traite pas les demandes depuis l'étranger ; le permis international français ne sert à rien au Japon.", "B"),
            ("Tout de suite", "Voiture du 3 au 6 janvier, Ise vers l'aéroport du Kansai",
             "<a href=\"https://rent.toyota.co.jp/eng/\">Toyota Rent a Car</a> (agence de la gare d'Ise-shi, retour à l'aéroport du Kansai, aller simple) ou <a href=\"https://www2.tocoo.jp/en/\">ToCoo!</a> pour comparer. Agence Toyota Ise (Kawasaki 2-11-6, 7 min de la gare, 8 h à 20 h) ou Times (face à la gare) ; retour à Toyota Kansai Airport (Aeroplaza, ferme à 20 h). Compacte, environ 270 € pour 3 jours plus l'aller simple entre préfectures (60 à 100 €, montant donné par le simulateur), pneus hiver (« studless », à réserver), carte ETC (330 yens, par téléphone), deux conducteurs. Le moteur ne propose que les créneaux où l'agence est ouverte : c'est le test du 3 janvier.", "B"),
            ("Tout de suite", "Kumano, 3 et 4 janvier, avec les dîners",
             "<a href=\"" + bk("kawakyu-onsen-fujiya", "2027-01-03", "2027-01-05") + "\">Kawayu Onsen Fujiya</a> (579 € les 2 nuits, ryokan, bains sur la rivière ; vérifier que la formule inclut dîner et petit-déjeuner), ou <a href=\"" + bk("entire-building-for-private-use-convenient-for-walking-the-kumano-kodo-and-sight", "2027-01-03", "2027-01-05") + "\">Guesthouse Kumano Iori</a> (284 €, maison entière à Ukegawa, sans repas), ou <a href=\"" + bk("minshuku-sumiya", "2027-01-03", "2027-01-05") + "\">Minshuku Sumiya</a> (254 €, repas compris, sanitaires communs). Détail dans le chapitre Kumano.", "B"),
            ("Tout de suite", "Shinkansen Nozomi, Kyoto → Tokyo, 9 janvier vers 15 h",
             "<a href=\"https://smart-ex.jp/en/\">smartEX</a> accepte les réservations un an à l'avance (siège confirmé un mois avant) et JR Central a rendu tous les Nozomi « tout réservés » du 9 au 11 janvier 2027 : réserver maintenant, 13 970 yens (80 €) par personne, siège côté E (Fuji à gauche), modification gratuite ; grosse valise : siège « espace bagage » en dernière rangée, même prix.", "B"),
            ("Tout de suite", "TGV Besançon et Paris du 26 décembre : la deuxième place",
             "<a href=\"https://www.sncf-connect.com/\">SNCF Connect</a> : surveiller le TGV direct (des places se libèrent), sinon TER vers Dijon ou Belfort-Montbéliard puis TGV, en arrivant à Roissy avant 18 h 30. Dernier recours : voiture jusqu'à Roissy (4 h 30) et parking longue durée.", "B"),
        ]),
    ],
    [
        ("2", "Dans la foulée", "les autres nuits, par ordre de tension", [
            ("Cette semaine", "Matsumoto, 30 décembre",
             "<a href=\"" + bk("dormy-inn-matsumoto", "2026-12-30", "2026-12-31") + "\">Dormy Inn Matsumoto</a> (120 €, bain de source, ramen gratuit le soir) ou <a href=\"" + bk("tian-ran-wen-quan-aduminotang-yu-su-ye-nai-song-ben", "2026-12-30", "2026-12-31") + "\">Onyado Nono Matsumoto</a> (143 €, onsen, note 9,0), tous deux à 5 min de la gare.", "I"),
            ("Cette semaine", "Ise, 2 janvier",
             "<a href=\"" + bk("experience-ise-miyamachi", "2027-01-02", "2027-01-03") + "\">Experience Ise Miyamachi Hotel</a> (259 €, 10 min à pied de la gare, parking) plutôt que <a href=\"" + bk("comfort-ise", "2027-01-02", "2027-01-03") + "\">Comfort Hotel ERA Ise</a> (179 €). Demander un parking si la voiture est prise la veille au soir.", "I"),
            ("Cette semaine", "Kii-Katsuura, 5 janvier",
             "<a href=\"" + bk("urashima", "2027-01-05", "2027-01-06") + "\">Hotel Urashima</a> (142 € sans repas, 260 à 285 € avec dîner-buffet et petit-déjeuner ; chambre japonaise non fumeur dans le bâtiment Nagisakan, formule repas à choisir sur la fiche). Parking de l'hôtel à Tenman, navette puis bateau.", "I"),
            ("Cette semaine", "Tokyo, du 27 au 30 décembre",
             "<a href=\"" + bk("the-kanzashi-tokyo-asakusa", "2026-12-27", "2026-12-30") + "\">The Kanzashi Asakusa</a> (431 €) ou <a href=\"" + bk("nohga-akihabara-tokyo", "2026-12-27", "2026-12-30") + "\">Nohga Akihabara</a>, l'adresse d'Allibert (1 061 €) ; autres choix dans le chapitre Tokyo. Réception ouverte le 30 pour garder les valises jusqu'à 16 h.", "I"),
            ("Cette semaine", "Osaka le 6, Kyoto les 7 et 8, Tokyo le 9",
             "<a href=\"" + bk("the-gate-osaka-by-hulic", "2027-01-06", "2027-01-07") + "\">The Gate Hotel Osaka</a> (231 €) ; <a href=\"" + bk("m-39-s-est-nanajo", "2027-01-07", "2027-01-09") + "\">Wander Kyoto Nanajo</a> (96 €) ou <a href=\"" + bk("richmond-hotel-premier-kyoto-ekimae", "2027-01-07", "2027-01-09") + "\">Richmond Premier Kyoto Ekimae</a> (292 €) ; <a href=\"" + bk("mitsui-garden-jingugaien-tokyo-premier", "2027-01-09", "2027-01-10") + "\">Mitsui Garden Jingugaien</a> (251 €). Tous avec annulation gratuite à vérifier.", "I"),
            ("Dès la décision", "Libérer les réservations du carnet v6",
             "Annuler Rengejoin (Kōya-san, 31 décembre, gratuit jusqu'au 17 décembre, sur Booking) et retirer la demande chez Oyado Daikichi à Tsumago (30 décembre) par un mail de deux lignes.", "I"),
            ("Mi-novembre", "Dîner du 31 décembre à Takayama",
             "Ni eph ni Koto no Yume ne servent de dîner (petit-déjeuner en option chez les deux). Demander à l'hôtel de réserver une table de bœuf de Hida (Kyoya, Maruaki, Kyoshi), ou se présenter à 17 h chez Ajikura Tengoku (yakiniku, 2 min de la gare, sans réservation) ; aucune source ne confirme les ouvertures du 31 au soir, l'hôtel saura. En dernier recours, toshikoshi soba à emporter et konbini.", "I"),
        ]),
        ("3", "Les ventes à date fixe", "2 h du matin en France", [
            ("30 nov., 2 h", "Express Azusa 37, Shinjuku 16 h 00 → Matsumoto 18 h 29, 30 décembre",
             "<a href=\"https://www.eki-net.com/en/jreast-train-reservation/Top/Index\">JR-EAST Train Reservation (Ekinet)</a> : compte créé avant, carte enregistrée (certaines cartes françaises sont refusées, en tester deux) ; toutes places réservées, 6 730 yens (38 €) par personne. Billet retiré au distributeur de places réservées de Shinjuku avec le QR code ou la carte, 15 min de marge.", "B"),
            ("1er déc., 2 h", "Car Matsumoto → Takayama du 31 décembre, et cars de Shirakawa-gō du 1er janvier",
             "<a href=\"https://www.highwaybus.com/gp/index\">highwaybus.com</a> (Alpico, ouvre dès 4 h au Japon, 20 h en France la veille) pour Matsumoto 7 h 40 → Takayama 10 h 13, 4 400 yens (25 €) par personne, paiement sous 5 jours ; <a href=\"https://japanbusonline.com/en\">Japan Bus Online</a> ou <a href=\"https://www.nouhibus.co.jp/english/\">Nohi Bus</a> pour Takayama 8 h 20 → Shirakawa-gō et retour 14 h 45 ou 15 h 45, 2 800 yens (16 €) l'aller. Vérifier début décembre les grilles d'hiver.", "B"),
            ("2 déc., 2 h", "Express Hida 4, Takayama 8 h 00 → Nagoya 10 h 34, 2 janvier",
             "Pas de vente en ligne en anglais pour le Hida (smartEX ne couvre que le shinkansen, Ekinet que JR East) : achat au guichet JR de la gare de Tokyo le 28 décembre, 6 540 yens (37 €) par personne, tout réservé du 25 décembre au 5 janvier. Puis Kintetsu Nagoya → Ise-shi, 3 080 yens (18 €) : <a href=\"https://www.kintetsu.co.jp/gyoumu/ticket/e-ticket/vs/en/index.html\">e-ticket Kintetsu en anglais</a> dès le 2 décembre, ou distributeur le jour même.", "I"),
            ("9 déc., 0 h", "Confirmation du siège Nozomi",
             "Si la réservation smartEX a été faite (priorité 1), le siège est confirmé par mail un mois avant le départ, à 8 h au Japon ; vérifier le mail et le numéro de voiture. Sinon, c'est la date d'ouverture classique de la vente.", "U"),
        ]),
    ],
    [
        ("4", "En novembre, sans date fixe", "comptes, papiers, téléphone", [
            ("Avant le 25 nov.", "Créer les comptes de réservation",
             "Ekinet (JR East), highwaybus.com, Japan Bus Online, Kintetsu, Toyota Rent a Car (smartEX est déjà fait avec le Nozomi) : cinq minutes chacun, carte bancaire testée. Noter les identifiants dans le carnet.", "I"),
            ("Novembre", "Horaires de fêtes 2026-2027",
             "Dès leur publication (début décembre) : cars Alpico et Nohi des 31 décembre et 1er janvier, grille d'hiver du bus Ryūjin (Yunomine 8 h 00 → Hosshinmon-ōji 8 h 37 le 4 janvier, <a href=\"https://www.ryujinbus.com/\">ryujinbus.com</a> ou <a href=\"https://www.tb-kumano.jp/en/\">Kumano Tourism Bureau</a>, qui répond en anglais), restrictions de circulation à Ise (<a href=\"https://www.rakurakuise.jp/\">rakurakuise.jp</a>, fin décembre), ouvertures du Nouvel An à Shirakawa-gō (<a href=\"https://shirakawa-go.gr.jp/\">shirakawa-go.gr.jp</a>, mi-décembre).", "I"),
            ("Novembre", "eSIM de données",
             "<a href=\"https://cellulardata.ubigi.com/\">Ubigi</a> ou <a href=\"https://www.airalo.com/japan-esim\">Airalo</a>, forfait illimité ou 20 Go pour 16 jours, 30 à 50 € par personne, installée en France, activée à l'atterrissage. Indispensable pour Google Maps en voiture.", "U"),
            ("Novembre", "Assurance et banque",
             "Vérifier ce que couvre la carte bancaire (annulation, rapatriement, bagages, voiture de location : franchise et exclusions). Prévenir la banque, faire relever les plafonds de retrait et de paiement, partir avec deux cartes.", "I"),
            ("Novembre", "Urashima : formule avec dîner",
             "Choisir sur Booking la chambre Nagisakan avec dîner et petit-déjeuner (buffet ou kaiseki) : le port de Katsuura a peu de restaurants ouverts le soir en janvier.", "U"),
        ]),
        ("5", "Dans les deux semaines avant le départ", "", [
            ("Mi-décembre", "Visit Japan Web", "<a href=\"https://www.vjw.digital.go.jp/\">Remplir en ligne</a> immigration et douane : un seul QR code, à présenter deux fois à Haneda. Capture d'écran.", "I"),
            ("Mi-décembre", "Passeports et permis", "Passeports valides pendant tout le séjour ; permis français et traductions dans le même étui, avec une photocopie dans la valise.", "I"),
            ("Mi-décembre", "Suica dans le téléphone, cartes hors ligne", "Suica ajoutée au portefeuille (recharge testée en France) ; cartes Google Maps de Tokyo, des Alpes, de la péninsule de Kii, de Kyoto et d'Osaka téléchargées hors ligne ; app Safety Tips.", "U"),
            ("Mi-décembre", "Prévenir les hôtels", "Arrivées tardives : Tokyo le 27 vers 21 h 30, Matsumoto le 30 vers 19 h, Osaka le 6 vers 18 h 45. Demander à l'hôtel de Tokyo de garder les valises le 30 jusqu'à 16 h.", "I"),
            ("Mi-décembre", "Équipement", "Adaptateurs type A, batterie externe, câble allume-cigare, petits crampons, bâtons, pharmacie, chaussures de marche imperméables, bonnet et gants pour les Alpes.", "U"),
            ("Mi-décembre", "Tables et billets d'entrée", "Shibuya Sky au coucher du soleil (créneau à réserver) ; un dîner kaiseki ou kappō à Kyoto le 8 (TableCheck, Omakase) ; horaires de marée inutiles cette fois, pas de Miyajima.", "U"),
        ]),
    ],
    [
        ("6", "Sur place", "les gestes à ne pas oublier", [
            ("27 déc.", "Yens et Suica", "Retirer 60 000 yens (340 €) au distributeur 7-Eleven de Haneda ; recharger la Suica. Espèces pour les auberges, les bus de campagne, les temples et les stations-service.", "I"),
            ("28 déc.", "Guichet JR de la gare de Tokyo", "Acheter le Hida 4 du 2 janvier (places réservées), vérifier l'Azusa du 30 et retirer le Nozomi du 9 si besoin ; demander les horaires de fêtes. Guichet Midori no madoguchi, enseigne verte, personnel anglophone.", "I"),
            ("30 déc.", "Départ de Tokyo", "Valises reprises à l'hôtel vers 15 h 30, Shinjuku 20 min avant l'Azusa ; dîner à Matsumoto en arrivant, rue Nawate.", "U"),
            ("31 déc.", "Terminal de bus de Matsumoto", "Face à la gare, 15 min avant le car, numéro de réservation ; valises en soute. À Takayama, hôtel à 5 min de la gare routière.", "I"),
            ("2 janv.", "Nagoya, changement de gare", "Hida aux quais JR à 10 h 34, puis gare Kintetsu-Nagoya par le niveau inférieur, 10 min ; e-ticket Kintetsu sur le téléphone ou billet au distributeur, places réservées.", "U"),
            ("3 janv.", "Prise de la voiture", "Permis, traduction, passeport ; état des lieux photographié, pneus hiver vérifiés, carte ETC, GPS en anglais ; plein à Shingū avant Hongū (dernière station avant la montagne).", "B"),
            ("5 et 6 janv.", "Plein et restitution", "Plein à Shingū le 5 ou à Hashimoto le 6 (reçu à garder) ; restitution à l'agence de l'aéroport du Kansai avant la fermeture, navette vers le terminal, train Nankai.", "I"),
            ("9 janv.", "Valises et Nozomi", "Valises reprises à l'hôtel de Kyoto vers 14 h 15, portillons du shinkansen côté sud de la gare, 15 min de marge.", "U"),
        ]),
    ],
]

# Frise du voyage : (date, étape, nuit, jalons, journée en voiture). Jalon : (icône, texte, genre) ; genre t = transport, w = marche, r = voiture, k = valises.
TIMELINE = dict(
    kicker="LA FRISE DU VOYAGE", title="Dix-sept jours en un regard",
    intro="Chaque ligne, une journée : où l'on dort, comment on se déplace, ce que l'on marche. Les journées sur fond sable sont celles de la voiture de location, du 3 au 6 janvier ; les valises suivent tout le voyage.",
    legend_bp="journées en voiture",
    rows=[
        ("26 déc.", "Besançon, Paris, vol de nuit", "en vol", [("train", "TGV, 3 h", "t"), ("plane", "AF274 à 22 h 20, 13 h 35 de vol", "t")], False),
        ("27 déc.", "Tokyo", "Tokyo", [("plane", "Haneda à 19 h 55", "t"), ("train", "Keikyū, 40 min", "t"), ("bag", "valises roulées jusqu'à l'hôtel", "k")], False),
        ("28 déc.", "Le vieux Tokyo", "Tokyo", [("walk", "10 km, Asakusa, Yanaka", "w"), ("train", "guichet JR : billets", "t")], False),
        ("29 déc.", "Tokyo moderne, ou Kamakura", "Tokyo", [("train", "Kamakura, 1 h (option)", "t"), ("walk", "5 à 8 km", "w")], False),
        ("30 déc.", "Tokyo, puis les Alpes", "Matsumoto", [("walk", "matinée à Tokyo", "w"), ("train", "Azusa 16 h, 2 h 30", "t")], False),
        ("31 déc.", "Takayama, le réveillon", "Takayama", [("bus", "car, 2 h 30", "t"), ("walk", "vieille ville, 5 km", "w")], False),
        ("1er janv.", "Shirakawa-gō", "Takayama", [("bus", "car, 50 min chaque sens", "t"), ("walk", "village et point de vue, 4 km", "w")], False),
        ("2 janv.", "Vers Ise", "Ise", [("train", "Hida 2 h 34, Kintetsu 1 h 20", "t"), ("walk", "Gekū, Okage Yokochō, 4 km", "w")], False),
        ("3 janv.", "Naikū à l'aube, route de la côte", "Yunomine", [("walk", "Naikū, 3 km", "w"), ("car", "Ise → Yunomine, 200 km, 3 h 30", "r")], True),
        ("4 janv.", "Kumano Kodo", "Yunomine", [("bus", "30 min", "t"), ("walk", "10 km, 4 h 30, bains", "w")], True),
        ("5 janv.", "Nachi, Katsuura", "Kii-Katsuura", [("car", "60 km, 1 h 30", "r"), ("walk", "Daimon-zaka, Nachi, 3 km", "w")], True),
        ("6 janv.", "Kōya-san, puis Osaka", "Osaka", [("car", "Kōya 3 h, aéroport 1 h 45", "r"), ("walk", "Okunoin, Garan, 5 km", "w"), ("train", "Nankai, 45 min", "t")], True),
        ("7 janv.", "Fushimi Inari, Higashiyama", "Kyoto", [("train", "Osaka → Kyoto, 30 min", "t"), ("walk", "10 km", "w")], False),
        ("8 janv.", "Nara", "Kyoto", [("train", "JR, 45 min", "t"), ("walk", "8 à 10 km", "w")], False),
        ("9 janv.", "Kyoto, shinkansen, Tokyo", "Tokyo", [("walk", "Nishiki, 4 km", "w"), ("train", "Nozomi 15 h, 2 h 15", "t")], False),
        ("10 janv.", "Tokyo, envol", "en vol", [("walk", "6 à 8 km", "w"), ("train", "Haneda, 40 min", "t"), ("plane", "AF279 à 22 h 55", "t")], False),
        ("11 janv.", "Paris, Besançon", "à la maison", [("plane", "CDG à 5 h 50", "t"), ("train", "TGV, 3 h", "t")], False),
    ],
    legend=[("train", "train, shinkansen", "t"), ("bus", "car, bus", "t"), ("car", "voiture de location", "r"), ("plane", "avion", "t"), ("walk", "marche", "w"), ("bag", "valises avec vous", "k")],
)
