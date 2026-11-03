# -*- coding: utf-8 -*-
"""Carnet v7, mode « avec Allibert » : ce qui change quand le voyage est organisé par Allibert Trekking (programme V2 du 2 novembre 2026)."""

KICKER = "CARNET DE VOYAGE · PROGRAMME ALLIBERT TREKKING, DEVIS DU 3 NOVEMBRE"
FOOT = "Vols directs Air France réservés par nous · devis Allibert n°2 du 3 novembre 2026 · guide version 7.2"

INTRO = ("Ce carnet suit le programme sur-mesure d'Allibert Trekking (devis n°2 du 3 novembre 2026, 4 045 € par personne hors vols et hors les deux nuits du Kumano, que nous réservons nous-mêmes au Kawayu Onsen Fujiya) : mêmes dates, mêmes étapes, "
         "les hôtels qu'ils ont confirmés. Allibert réserve les trains, les cars, la voiture, les hôtels, la journée guidée à Kyoto, et fournit le roadbook, le pocket wifi et une assistance 24 h/24. "
         "Ce que ce carnet ajoute, c'est le reste : les journées heure par heure, les adresses où manger, boire un café, se baigner, voir des appareils photo, et les plans B si quelque chose coince.")

# Ce qui est compris dans le devis Allibert (programme V2) et ce qui reste à notre charge
INCLUDED = dict(
    yes=[
        "Accueil à l'aéroport de Haneda le 27 décembre au soir par un représentant francophone, qui accompagne jusqu'à l'hôtel en transport public ; remise des documents et du pocket wifi illimité (pour deux, tout le séjour).",
        "Douze nuits d'hôtel avec petit-déjeuner (sauf le 27, arrivée tardive), le dîner à l'hôtel Urashima le 5 janvier. Les nuits des 3 et 4 janvier (Kumano) sont déduites du devis : nous les réservons nous-mêmes au Kawayu Onsen Fujiya.",
        "Les trains payables à l'avance : Azusa Tokyo → Matsumoto, Hida et Kintetsu vers Ise, Nankai depuis l'aéroport du Kansai, shinkansen Osaka → Kyoto, Nozomi Kyoto → Tokyo avec siège réservé. Une carte Icoca chargée de 5 000 yens (29 €) pour les métros et bus des villes.",
        "La voiture de location du 3 janvier (Ise) au 6 janvier (aéroport du Kansai), en aller simple, un conducteur inclus.",
        "Les cars Matsumoto → Takayama et Takayama ⇄ Shirakawa-gō : réservés par Allibert, mais à payer sur place (environ 40 € et 20 € par personne selon eux ; 25 € et 32 € selon les tarifs publics).",
        "La journée guidée à Kyoto le 7 janvier, avec un guide francophone.",
        "Le roadbook détaillé, la traduction du permis d'un conducteur, l'assistance 24 h/24 en français.",
    ],
    no=[
        "Les vols (réservés par nous : Air France, 3 431 € pour deux) et les trains Besançon ⇄ Paris.",
        "Les deux nuits du Kumano (3 et 4 janvier) : Kawayu Onsen Fujiya à réserver par nous, environ 520 à 580 € pour deux, dîners et petits-déjeuners compris.",
        "Les déjeuners et les dîners (sauf le 5 janvier), les boissons ; Allibert compte 8 à 12 € par repas, comptez plutôt 15 à 25 €.",
        "Les entrées des temples, musées, bains ; les cars de montagne (à régler sur place) ; le dîner du réveillon, à réserver par nous.",
        "La traduction du permis du second conducteur (70 € chez Japan Experience) et son ajout au contrat de location ; l'assurance annulation (option Allibert 4,45 %, ou 3,15 % en complément d'une carte bancaire).",
    ],
    todo="Au 3 novembre : devis valable jusqu'au 4 novembre, acompte de 35 % par carte à verser via le bulletin d'inscription ; Fujiya à réserver par nous tout de suite ; dîner du réveillon à réserver par nous ; cars réservés par Allibert mais payés sur place ; Nozomi avec siège réservé.",
)

# Hôtels du programme V2, par chapitre : (nom, adresse, requête Google Maps, site, notes)
HOTELS = dict(
    tokyo=[("Nohga Hotel Akihabara Tokyo", "3 nuits, 27 au 30 décembre", "3-10-11 Sotokanda, Chiyoda-ku, Tokyo", "Nohga Hotel Akihabara Tokyo", "https://nohgahotel.com/akihabara/",
            "Hôtel design à Akihabara, à 6 min de la gare JR Akihabara et 4 min du métro Suehirochō (ligne Ginza) ; petit-déjeuner 7 h à 10 h à la Pizzeria & Bar Nohga (focaccia au feu de bois, œufs). Depuis Haneda : Keikyū jusqu'à Shinagawa puis Yamanote, 45 min. Salle de sport ; demander une chambre en étage pour le calme.")],
    alpes=[("Dormy Inn Matsumoto", "1 nuit, 30 décembre", "2-2-1 Fukashi, Matsumoto, Nagano", "Dormy Inn Matsumoto Natural Hot Spring", "https://www.dormy-hotels.com/dormyinn/hotels/matsumoto/",
            "À 4 min à pied de la gare, sortie côté château. Bains de source naturelle au 9e étage (bain extérieur, sauna), et le « yonaki soba », bol de ramen offert vers 21 h 30. Petit-déjeuner buffet avec soba de Shinshū."),
           ("eph TAKAYAMA", "2 nuits, 31 décembre et 1er janvier", "5-13-17 Hanasatomachi, Takayama, Gifu", "eph TAKAYAMA", "https://www.eph-takayama.com/",
            "Hôtel récent à 1 min de la gare (sortie est) et 2 min de la gare routière. Toutes les chambres ont une salle de bain avec baignoire profonde en hinoki et douche à part. Pas de dîner ; petit-déjeuner compris dans le programme. Attention : réception de 7 h à 20 h, check-in jusqu'à 21 h, pas d'arrivée tardive."),
           ("Experience Ise Miyamachi Hotel", "1 nuit, 2 janvier (chambre twin)", "Miyamachi, Ise, Mie", "Experience Ise Miyamachi Hotel", "",
            "Petit hôtel récent à 10 min à pied de la gare d'Ise-shi, parking. Chambre twin (deux lits). Le Gekū est à 10 min à pied, le Naikū en bus 51 ou 55 depuis la gare.")],
    kumano=[("Kawayu Onsen Fujiya", "2 nuits, 3 et 4 janvier, réservées par nous", "1452 Kawayu, Hongū-chō, Tanabe, Wakayama", "Kawayu Onsen Fujiya", "https://www.fuziya.co.jp/",
             "Hors devis Allibert, réservé par nous (Booking, environ 520 à 580 € les deux nuits, dîner et petit-déjeuner compris, chambre avec bain et toilettes). Ryokan au bord de la rivière chaude de Kawayu, bains extérieurs sur la berge, le Sennin-buro (bain creusé dans la rivière, gratuit, décembre à février) devant la porte, parking. Yunomine, Tsuboyu et le départ du Dainichi-goe sont à 10 min de voiture (4 km) ; le Hongū Taisha à 5 km. Arrivée avant 18 h pour le dîner, prévenir de l'heure."),
            ("Hotel Urashima", "1 nuit, 5 janvier, chambre japonaise (Nagisakan), dîner compris", "1165-2 Katsuura, Nachikatsuura, Wakayama", "Hotel Urashima Nachikatsuura", "https://www.hotelurashima.co.jp/",
             "Grand hôtel de bains des années 1970 sur sa presqu'île : voiture au parking de l'hôtel à Tenman, navette, puis bateau-tortue de 5 min depuis le port. Bains dans les grottes Bōkidō (5 h à 10 h, 13 h à 23 h) et Genbudō. Dîner-buffet avec découpe de thon. Check-in 15 h, départ 10 h.")],
    koya=[("The Gate Hotel Osaka by Hulic", "1 nuit, 6 janvier", "3-12-14 Minamisenba, Chūō-ku, Osaka", "The Gate Hotel Osaka by Hulic", "https://www.gate-hotel.jp/osaka/",
           "Ouvert en juin 2026, à 1 min de la station Shinsaibashi (ligne Midōsuji) et 13 min à pied de Namba, où arrive le Nankai de l'aéroport. Terrasse-bar au 28e étage, salle de sport. Dōtonbori est à 10 min à pied.")],
    kyoto=[("Richmond Hotel Premier Kyoto Ekimae", "2 nuits, 7 et 8 janvier", "565-3 Kitafudōdō-chō, Shimogyō-ku, Kyoto", "Richmond Hotel Premier Kyoto Ekimae", "https://richmondhotel.jp/kyoto-ekimae/",
            "Hôtel très bien tenu à 5 min à pied de la sortie centrale (nord) de la gare de Kyoto, pratique pour le train de Nara le 8 et le shinkansen le 9. Check-in 14 h, check-out 11 h ; la réception garde les valises.")],
    retour=[("Mitsui Garden Hotel Jingūgaien Tokyo Premier", "1 nuit, 9 janvier", "11-3 Kasumigaoka-machi, Shinjuku-ku, Tokyo", "Mitsui Garden Hotel Jingu Gaien Tokyo Premier", "https://www.gardenhotels.co.jp/jingugaien-tokyo-premier/",
             "Face au stade national, à 1 min de la station Kokuritsu-Kyōgijō (ligne Ōedo) et 5 min de Sendagaya (JR). Grand bain public, chambres avec balcon. Le sanctuaire Meiji et Harajuku sont à 15 min à pied, Haneda à 45 min (Ōedo jusqu'à Daimon puis Keikyū direct).")],
)

# Checklist en mode Allibert : (numéro, titre, sous-titre, items (date, titre, détail html, niveau B/I/U))
CHECK_PAGES = [
    [
        ("1", "Cette semaine", "boucler avec Allibert", [
            ("Avant le 4 nov.", "Bulletin d'inscription et acompte de 35 %",
             "Le devis n°2 (4 045 € par personne hors vols, 18 € de frais) n'est valable que jusqu'au 4 novembre. Signer le bulletin numérique, payer l'acompte par carte, confirmer l'adresse postale (25 rue du Petit Charmont, 25000 Besançon). Allibert confirme ensuite la disponibilité de chaque prestation, ou propose une alternative, ou rembourse l'acompte. Demander par écrit la liste nominative des hôtels (Nohga, Dormy Inn, eph Takayama, Experience Ise twin, Urashima chambre japonaise avec dîner, The Gate, Richmond, Mitsui Garden) : la page du devis dit « donnés à titre indicatif ».", "B"),
            ("Aujourd'hui", "Réserver Kawayu Onsen Fujiya, 3 et 4 janvier",
             "Hors devis, à faire par nous : <a href=\"https://www.booking.com/hotel/jp/kawakyu-onsen-fujiya.html?checkin=2027-01-03&checkout=2027-01-05&group_adults=2&no_rooms=1\">Booking, Kawayu Onsen Fujiya</a> (579 € les deux nuits le 1er novembre), chambre avec bain et toilettes, formule dîner et petit-déjeuner, annulation gratuite si possible. Envoyer la confirmation à Camille pour le roadbook.", "B"),
            ("Cette semaine", "Traduction du permis du second conducteur",
             "Allibert ne traduit qu'un permis. Pour pouvoir conduire à deux : <a href=\"https://japan-experience.com/transportation/driving-licence-translation\">Japan Experience, traduction officielle</a>, 70 €, environ 12 jours, livraison à domicile. Le permis international français ne sert à rien au Japon.", "B"),
            ("Avec le bulletin", "Assurance annulation et rapatriement",
             "Options Allibert : contrat Tranquillité 4,45 % du voyage (environ 360 €), ou 3,15 % en complément des garanties d'une carte bancaire haut de gamme (environ 255 €). Vérifier d'abord ce que couvre la carte (annulation, rapatriement, franchise de la voiture) avant de cocher.", "I"),
            ("Cette semaine", "Second conducteur sur la voiture",
             "Le devis inclut un seul conducteur. Pour conduire à deux : traduction du second permis, et demander à Camille d'ajouter un conducteur au contrat (quelques centaines de yens par jour chez Toyota), ou le faire au comptoir le 3 janvier.", "I"),
        ]),
        ("2", "Dès l'ouverture des ventes", "le TGV du retour", [
            ("Vers mi-novembre", "TGV Paris → Besançon du 11 janvier",
             "<a href=\"https://www.sncf-connect.com/\">SNCF Connect</a> : arrivée du vol à 5 h 50 à Roissy ; viser un TGV direct depuis l'aéroport Charles-de-Gaulle 2 vers 9 h ou 10 h, en tarif modifiable, au cas où le vol prenne du retard. Lundi hors vacances scolaires : il y aura de la place.", "I"),
        ]),
    ],
    [
        ("3", "En novembre et décembre", "ce qui ne dépend pas d'Allibert", [
            ("Novembre", "La carte Suica dans l'iPhone",
             "App Cartes, ajouter une carte de transport Suica, recharger par Apple Pay (tester avec deux cartes bancaires, certaines Visa françaises sont refusées). Elle paie métro, trains locaux, bus, konbini, consignes. Allibert fournit peut-être une carte Icoca physique : les deux coexistent sans problème.", "I"),
            ("Novembre", "Shibuya Sky, si l'on veut la vue le 29",
             "<a href=\"https://www.shibuya-scramble-square.com/sky/\">Billets en ligne</a> avec créneau horaire ; les créneaux du coucher du soleil partent plusieurs jours avant. Optionnel.", "U"),
            ("Novembre", "Banque et argent",
             "Prévenir la banque, relever les plafonds de retrait et de paiement, partir avec deux cartes. Prévoir environ 60 000 yens (340 €) d'espèces pour les jours de campagne, retirés au 7-Eleven de Haneda puis en route.", "I"),
            ("Novembre", "Équipement d'hiver",
             "Petits crampons pour les rues gelées de Takayama et Shirakawa-gō, chaussures imperméables, bonnet, gants fins pour les photos ; bâtons pliants pour le Kumano Kodo (pierres humides) ; serviette fine et sac pour les bains ; carte SD et batteries de rechange (le froid vide les batteries).", "U"),
            ("Début décembre", "Demander à Camille les horaires de fêtes confirmés",
             "Cars Alpico et Nohi des 31 décembre et 1er janvier (grille d'hiver publiée début décembre), bus Ryūjin de Yunomine vers Hosshinmon-ōji le 4 janvier (8 h 00 dans la grille de septembre 2026), restrictions de circulation à Ise les 2 et 3 janvier. Le roadbook devrait tout contenir ; vérifier ces trois points.", "I"),
            ("Fin novembre", "Dîner du réveillon à Takayama, à réserver par nous",
             "Allibert ne le réserve pas. Gyu-Suke (yakiniku de bœuf de Hida maturé, 80 m de la gare, 0577-57-8293) : réservation par <a href=\"https://savorjapan.com/0031549237/\">Savor Japan</a> ou via l'hôtel eph ; viser 18 h ou 18 h 30 pour être au temple Hida Kokubun-ji vers 23 h 30 pour la cloche. Son ouverture le 31 au soir n'est pas confirmée : plans B, Maruaki (ouvert le 31) ou Ajikura Tengoku (sans réservation, à 17 h).", "I"),
        ]),
        ("4", "Deux semaines avant", "papiers et téléphone", [
            ("Dès le 12 déc.", "Visit Japan Web",
             "<a href=\"https://www.vjw.digital.go.jp/\">vjw.digital.go.jp</a> : passeport, vol AF274, hôtel du 27 (Nohga). Un seul QR code pour l'immigration et la douane, en capture d'écran.", "B"),
            ("Mi-décembre", "Documents Allibert",
             "Roadbook, vouchers d'hôtels, billets ou e-tickets de train, contrat de location de voiture, numéro d'assistance 24 h/24 : tout en PDF sur les deux téléphones, et une version papier dans le bagage cabine.", "B"),
            ("Mi-décembre", "Passeports et permis",
             "Passeports valides pour tout le séjour (pas de visa pour les Français, 90 jours). Permis français originaux et les deux traductions japonaises, dans le bagage cabine avec les passeports.", "B"),
            ("Mi-décembre", "Téléphone",
             "Google Maps avec les cartes hors ligne de Tokyo, des Alpes, de la péninsule de Kii, de Kyoto ; Japan Travel by Navitime pour les horaires ; DeepL ou Google Traduction hors ligne ; ce carnet dans Fichiers ou sur l'écran d'accueil. Le pocket wifi d'Allibert est remis à Haneda : pas besoin d'eSIM.", "I"),
            ("Mi-décembre", "Prévenir les hôtels de l'heure d'arrivée",
             "eph Takayama ferme sa réception à 20 h ; le Fujiya sert le dîner à heure fixe et attend une arrivée avant 18 h ; Urashima check-in 15 h. Allibert transmet en général, mais un mot de confirmation ne coûte rien.", "U"),
        ]),
    ],
    [
        ("5", "Sur place", "les rendez-vous à ne pas manquer", [
            ("27 déc.", "Haneda, 19 h 55", "Accueil Allibert à la sortie des arrivées du terminal 3, remise des documents et du pocket wifi. Retirer des yens au 7-Eleven avant de partir.", "B"),
            ("30 déc.", "Azusa de Shinjuku", "Quais 9 et 10 des express Chūō, au sud de la gare ; 20 min de marge, valises dans l'espace derrière la dernière rangée. Chambre rendue le matin, valises reprises vers 15 h.", "I"),
            ("31 déc.", "Car de Matsumoto", "Terminal de bus face à la gare, 15 min avant le départ, valises en soute. Le soir, Gyu-Suke puis Hida Kokubun-ji vers 23 h 30 pour la cloche.", "I"),
            ("3 janv.", "Naikū à l'aube, puis la voiture", "Naikū avant 7 h (ouvert jour et nuit pendant les fêtes), retour à l'hôtel, prise de la voiture à l'heure indiquée par le roadbook : permis, traductions, second conducteur, pneus hiver, carte ETC, état des lieux en photos. Plein à Shingū ; dîner au Fujiya, arrivée avant 18 h.", "B"),
            ("4 janv.", "Bus de 8 h 00 vers Hosshinmon-ōji", "Depuis l'arrêt Yunomine Onsen (ou Kawayu, avec changement à Hongū Taisha-mae) ; sinon taxi commandé la veille par l'auberge. Bentō demandé la veille.", "I"),
            ("6 janv.", "Kōya-san, voiture rendue avant 20 h", "Quitter Kōya-san à 16 h 30 au plus tard ; plein à Hashimoto, reçu à garder ; agence Toyota de l'Aeroplaza, à 3 min du terminal 1. Puis Nankai jusqu'à Namba.", "B"),
            ("9 janv.", "Nozomi de Kyoto", "Portillons du shinkansen côté sud de la gare (Hachijō), 15 min de marge ; descendre à Shinagawa pour un seul changement vers l'hôtel.", "I"),
            ("10 janv.", "Haneda, terminal 3", "Partir de l'hôtel vers 18 h 30 (Ōedo jusqu'à Daimon, puis Keikyū direct, 45 min), être au terminal 3 h avant le vol de 22 h 55. Pocket wifi à rendre selon les consignes d'Allibert (boîte prépayée ou comptoir).", "B"),
        ]),
    ],
]

CHECK_INTRO = dict(
    kicker="NE RIEN RATER", title="Ce qui reste à faire, par priorité",
    intro="Allibert réserve l'essentiel. Voici ce qui dépend encore de nous, du plus urgent au plus simple, puis les rendez-vous à ne pas manquer sur place.",
    blocks=[
        ("LE BULLETIN D'INSCRIPTION", "Devis valable jusqu'au 4 novembre ; tant que l'acompte n'est pas versé, rien n'est réservé, et Takayama le 31 décembre est le point le plus tendu."),
        ("LE SECOND PERMIS", "Allibert ne traduit qu'un permis. Douze jours de délai chez Japan Experience : à commander cette semaine pour conduire à deux."),
        ("LE FUJIYA", "Les deux nuits du Kumano sont sorties du devis : c'est à nous de réserver le Kawayu Onsen Fujiya, et vite, il restait peu de chambres le 1er novembre."),
        ("LE TGV DU 11 JANVIER", "Pas encore en vente ; prendre un billet modifiable depuis l'aéroport vers 9 h ou 10 h dès l'ouverture."),
    ],
)

BUDGET = dict(
    kicker="COMBIEN ÇA COÛTE", title="Budget pour deux, avec Allibert",
    intro="Le programme V2 à 4 245 € par personne hors vols, plus nos vols, et ce qui reste à payer sur place. Les repas non compris sont estimés à 45 € par jour et par personne, moins quand un dîner est compris.",
    col0="Poste, pour deux", col1="Montant", col2="Qui paie",
    rows=[
        ("Programme Allibert V2, hors vols (hôtels, trains, voiture, guide, wifi, assistance)", "8 490 €", "Allibert"),
        ("Vols Air France aller-retour, éco siège large", "3 431 €", "réservés"),
        ("TGV Besançon et Paris, aller et retour", "250 €", "nous"),
        ("Supplément Fujiya à la place de J-Hoppers (si accepté)", "≈ 300 €", "nous"),
        ("Traduction du second permis", "70 €", "nous"),
        ("Cars de montagne, si non compris", "120 €", "sur place"),
        ("Repas non compris (13 déjeuners, 13 dîners)", "≈ 1 100 €", "sur place"),
        ("Entrées, bains, carburant et péages en plus, petites dépenses", "≈ 400 €", "sur place"),
    ],
    total=("Total estimé pour deux", "≈ 14 200 €"),
    note="Pour mémoire, le même voyage organisé par nous-mêmes revenait à environ 9 300 € tout compris (carnet v7.0) : l'écart, environ 4 900 €, paie le roadbook, le guide de Kyoto, l'accueil, le wifi, l'assistance, et surtout le fait de ne pas gérer une quinzaine de réservations à distance.",
)

# Texte de remplacement des blocs « pratique » qui parlaient de réserver par nous-mêmes
PRATIQUE_OVERRIDES = {
    ("tokyo", "26"): ["Allibert n'intervient qu'à partir de Haneda : le TGV et le vol sont à nous. Ajouter une carte Suica dans l'app Cartes de l'iPhone avant le départ.",
                      "Permis français, les deux traductions japonaises et les documents Allibert dans le bagage cabine, avec les passeports."],
    ("tokyo", "27"): ["Un représentant d'Allibert attend à la sortie des arrivées du terminal 3 : documents, roadbook, pocket wifi. Retirer des yens au 7-Eleven de l'aéroport avant de partir : auberges, bus de campagne, temples et petites tables ne prennent souvent que les espèces."],
    ("tokyo", "30"): ["Billets de l'Azusa fournis par Allibert (roadbook) ; toutes places réservées, espace valises derrière la dernière rangée.",
                      "À Shinjuku, les quais 9 et 10 des express Chūō sont au sud de la gare : 20 min de marge, la gare est immense."],
    ("alpes", "31"): ["Car Alpico : vérifier avec Camille s'il est réservé par Allibert ou « à régler sur place » ; dans ce cas, le réserver le 1er décembre à l'ouverture sur highwaybus.com (4 400 yens, 25 €, par personne).",
                      "Il fait -5 à 0 °C : les rues de Takayama sont déneigées mais glissantes le soir ; petits crampons utiles pour la promenade de Higashiyama.",
                      "Valises en soute du car ; l'hôtel les garde si la chambre n'est pas prête (check-in 15 h)."],
    ("alpes", "1<sup>er</sup>"): ["Cars Nohi : départs réservés 8 h 20 et 9 h 35, retours 14 h 45 et 15 h 45 (à confirmer avec Allibert, ou à réserver sur japanbusonline.com) ; départs sans réservation 8 h 50 et 10 h 50, retours 13 h 15, 15 h 15, 16 h 15.",
                                  "Neige au sol presque certaine : chaussures imperméables, crampons, bonnet. Ne pas marcher sous les avant-toits, la neige en tombe par paquets.",
                                  "Ouvertures du Nouvel An publiées mi-décembre sur shirakawa-go.gr.jp ; le village lui-même se visite librement."],
    ("alpes", "2"): ["Hida et Kintetsu fournis par Allibert, places réservées (le Hida est tout réservé du 25 décembre au 5 janvier). Le 2 janvier est un jour de retours : ne pas rater le Hida de 8 h 00.",
                     "À Nagoya, le Kintetsu part de la gare Kintetsu-Nagoya, dans le même bâtiment, 10 min à pied par le niveau inférieur.",
                     "Ise les 2 et 3 janvier : pic du hatsumōde ; les sanctuaires restent ouverts jour et nuit jusqu'au 5 au soir (pratique 2025-26) ; on y va à pied et en bus."],
    ("kumano", "3"): ["Ise le 3 janvier : avenues des sanctuaires fermées aux voitures, sortie d'autoroute Ise-nishi fermée de 8 h 45 à 15 h 30 (pratique 2025-26) ; cela ne gêne pas, on quitte la ville vers le sud depuis la gare.",
                      "Voiture : l'agence et l'heure sont dans le roadbook ; vérifier pneus hiver, carte ETC, les deux conducteurs inscrits, et photographier la carrosserie. Le plein à Shingū, les stations sont rares et ferment tôt dans la vallée.",
                      "Le Fujiya sert le dîner à heure fixe : arriver avant 18 h, prévenir de l'heure. Le Sennin-buro, bain dans la rivière, est devant l'hôtel, maillot à prévoir."],
    ("koya", "6"): ["Kōya-san en janvier : -4 °C la nuit, 3 °C le jour, verglas possible sur les routes d'accès ; la voiture a des pneus hiver (demandés à Allibert).",
                    "Kongōbu-ji et Garan : 8 h 30 à 17 h (dernière entrée 16 h 30) ; Reihōkan 9 h à 17 h, fermé pendant les fêtes (dates 2027 à vérifier) ; Okunoin libre à toute heure, Tōrō-dō de 6 h à 17 h.",
                    "Péages : environ 1 800 yens (10 €) avec la carte ETC, pont de l'aéroport compris. Plein avant l'autoroute, à Hashimoto ; l'agence demande le reçu. Nankai : billets fournis par Allibert ou à prendre au distributeur (970 yens, 6 €, sans supplément)."],
    ("retour", "9"): ["Nozomi fourni par Allibert : JR Central a rendu tous les Nozomi « tout réservés » du 9 au 11 janvier 2027, vérifier que le billet porte bien un numéro de voiture et de siège. Siège côté E pour le Fuji.",
                      "Valise de plus de 160 cm (longueur, largeur et hauteur additionnées) : siège avec espace bagage, dernière rangée de la voiture."],
}

COINCE_OVERRIDES = {
    ("tokyo", "30"): "Azusa manqué : un Azusa par heure jusqu'à 19 h, appeler l'assistance Allibert pour le changement de billet ; en dernier recours, car Keiō depuis Busta Shinjuku, 3 h 15.",
    ("alpes", "31"): "Car complet ou supprimé par la neige : départs suivants 9 h 55, 10 h 55, 11 h 55, 13 h 05 ; par le sud, express Shinano vers Nagoya puis Hida vers Takayama, 5 h 30. Prévenir l'assistance Allibert, qui refait les billets.",
    ("alpes", "2"): "Hida raté ou complet : le Hida 6 de 9 h 36, Ise vers 14 h ; appeler l'assistance pour le changement. Trains Kintetsu bondés le 2 janvier : la ligne JR Mie offre une seconde voie.",
    ("retour", "9"): "Shinkansen perturbé par la neige vers Sekigahara (10 à 30 min de retard possibles) : la soirée à Tokyo est de toute façon libre. Train manqué : le billet Nozomi se reporte sur le suivant au guichet, places assises selon disponibilité.",
}

# Infos pratiques réécrites pour le mode Allibert (par titre) ; les autres sont reprises telles quelles
PRACTICAL_OVERRIDES = {
    "TRAINS": "Tous les trains du programme sont réservés par Allibert et remis dans le roadbook (billets papier ou e-tickets à retirer au distributeur avec un code). Azusa, Hida et Nozomi sont tout réservés pendant les fêtes : garder les billets sous la main, le contrôleur passe. Les trajets locaux non prévus (Kamakura le 29, Nara le 8) se paient avec la Suica ou la carte Icoca fournie.",
    "CARS": "Matsumoto → Takayama le 31 décembre et Takayama ⇄ Shirakawa-gō le 1er janvier : à confirmer avec Allibert, réservés par eux ou « à régler sur place ». Dans le second cas, les réserver nous-mêmes un mois avant (highwaybus.com pour Alpico, Japan Bus Online pour Nohi) : le car du 31 au matin peut être complet.",
    "VOITURE": "Réservée par Allibert : prise à Ise le 3 janvier au matin, rendue à l'aéroport du Kansai le 6 avant 20 h, aller simple, pneus hiver et carte ETC demandés, deux conducteurs. Permis français et traduction japonaise officielle obligatoires pour chaque conducteur (Allibert en fournit une, la seconde est à commander). Conduite à gauche, routes de montagne étroites, nuit à 17 h : on roule de jour. Photographier la carrosserie à la prise et au retour.",
    "TÉLÉPHONE": "Allibert remet à Haneda un pocket wifi illimité pour deux, à garder chargé (batterie externe) : il remplace l'eSIM. Google Maps en voiture, Google Traduction en mode appareil photo pour les menus et les panneaux. Télécharger quand même les cartes hors ligne des Alpes et du Kumano, où le réseau est inégal.",
    "NOUVEL AN": "Du 29 décembre au 3 janvier, musées, administrations et beaucoup de restaurants ferment ; les sanctuaires sont bondés. Konbini, grandes gares et restaurants d'hôtel restent ouverts. Le 31 au soir à Takayama (Gyu-Suke, à réserver par nous) et les 3 et 4 au Kumano (demi-pension au Fujiya), les dîners sont réglés avant de partir.",
    "ARRIVÉE ET DÉPART": "Le 27, accueil Allibert à Haneda (terminal 3) puis train Keikyū, 45 min jusqu'à Akihabara. Visit Japan Web fournit un seul QR code, à montrer à l'immigration puis à la douane. Le 10 janvier, depuis le Mitsui Garden, 45 min jusqu'au terminal 3 par la ligne Ōedo (Daimon) puis Keikyū direct ; être à l'aéroport 3 h avant le vol.",
}

BEFORE_BOXES = [
    ("AVEC ALLIBERT",
     "<p>Devis n°2 du 3 novembre 2026 (T7J40LQCQ000D002), conseillère Camille de Farcy (+33 5 34 44 55 73, c.de-farcy@allibert-trekking.com). Compris : 12 nuits avec petits-déjeuners, trains, voiture en aller simple (un conducteur), journée guidée à Kyoto, pocket wifi, carte Icoca 5 000 yens, accueil à Haneda, roadbook, assistance 24 h/24 en français. 4 045 € par personne hors vols.</p>"
     "<p>Non compris : vols et TGV, les deux nuits du Kumano (Fujiya, réservées par nous), repas sauf le dîner du 5 janvier, entrées et bains, cars de montagne (réservés, payés sur place), dîner du réveillon, traduction du second permis, assurance.</p>"),
    ("LE PROGRAMME EN UNE LIGNE",
     "<p>Tokyo 27 au 30 décembre ; Matsumoto le 30 ; Takayama les 31 et 1er avec Shirakawa-gō ; Ise le 2 ; voiture du 3 au 6 : Kumano (Kawayu ou Yunomine), Nachi et Kii-Katsuura, Kōya-san ; Osaka le 6 ; Kyoto les 7 et 8 avec Nara ; Tokyo le 9 ; vol le 10 au soir.</p>"
     "<p>Dix-sept jours, quatorze nuits, environ 60 km de marche en tout, quatre jours de voiture.</p>"),
]

BRIEF_OVERRIDES = {
    "Point d'attention": "Allibert réserve trains, cars, voiture et hôtels ; restent à nous le bulletin et l'acompte avant le 4 novembre, le Fujiya à réserver tout de suite, le dîner du réveillon, la traduction du second permis, le TGV du retour.",
    "Hébergements": "Hôtels de ville bien tenus (Nohga, Dormy Inn, eph, Richmond, Mitsui Garden, The Gate), le ryokan Fujiya au bord de la rivière chaude de Kawayu (réservé par nous, dîners compris), et un grand hôtel de bains face à la mer à Kii-Katsuura, dîner compris.",
}

PRACTICAL_EXTRA = [
    ("COURSE À PIED", "Une option de course d'une heure au plus est donnée à chaque étape dans l'onglet Adresses (filtre « Course »). Au Japon, courir tôt est facile et sûr : le jour se lève vers 6 h 50 fin décembre, les parcs ouvrent souvent avant, les konbini sont là pour l'eau. Trottoirs à gauche, on ne traverse pas au rouge même sans voiture. Sur les sentiers (Takayama, Kumano, Kōya-san, Kyoto) : frontale, petits crampons si neige ou verglas, téléphone chargé, et prévenir Claudie de l'heure de retour. Les ours hibernent en janvier dans le Kii, mais les clochettes des locaux ne coûtent rien. Ne pas oublier la serviette : les hôtels d'affaires ont un grand bain, et le Mitsui Garden, Dormy Inn, eph (baignoire) et les ryokan permettent de se laver après."),
]

# Nuit par date (clé = index dans HOTELS[chapitre])
HOTEL_BY_DATE = {
    "2026-12-27": ("tokyo", 0), "2026-12-28": ("tokyo", 0), "2026-12-29": ("tokyo", 0),
    "2026-12-30": ("alpes", 0), "2026-12-31": ("alpes", 1), "2027-01-01": ("alpes", 1), "2027-01-02": ("alpes", 2),
    "2027-01-03": ("kumano", 0), "2027-01-04": ("kumano", 0), "2027-01-05": ("kumano", 1),
    "2027-01-06": ("koya", 0), "2027-01-07": ("kyoto", 0), "2027-01-08": ("kyoto", 0), "2027-01-09": ("retour", 0),
}
NIGHT_OTHER = {"2026-12-26": "Nuit dans l'avion, AF274 Paris → Tokyo", "2027-01-10": "Nuit dans l'avion, AF279 Tokyo → Paris"}

# Phrases du carnet « par nous-mêmes » à neutraliser en mode Allibert
TEXT_FIXES = [
    ("Passage par la gare de Tokyo : au guichet JR, acheter ou vérifier les billets de train de tout le voyage (voir checklist).", "Si l'envie vient, passage par la gare de Tokyo pour repérer les quais et les consignes ; les billets de train sont dans le roadbook Allibert."),
    ("réservé d'avance (beaucoup de restaurants ferment ce soir-là, voir checklist)", "réservé d'avance : Gyu-Suke, à 80 m de la gare, ou une autre table de bœuf de Hida (beaucoup de restaurants ferment ce soir-là)"),
    (", voir checklist)", ")"),
    ("(voir checklist)", ""),
    ("Yunomine, Kawayu ou Ukegawa", "Kawayu Onsen, ryokan Fujiya"),
    ("Ise → Yunomine : 210 km, 4 h avec les arrêts", "Ise → Kawayu : 210 km, 4 h avec les arrêts"),
    ("puis la route de la côte jusqu'à Yunomine", "puis la route de la côte jusqu'à Kawayu"),
    ("Arrivée à Yunomine vers 15 h 30, voiture au parking de l'auberge ou du village. Premier bain, dîner au ryokan (ou, en maison entière, dîner préparé avec les courses de Shingū), et le silence du hameau, où la vapeur de la source monte dans la nuit.", "Arrivée au Fujiya, à Kawayu, vers 15 h 30, voiture au parking du ryokan. Premier bain sur la berge de l'Ōtō, ou dans le Sennin-buro creusé dans la rivière, dîner au ryokan, et le silence de la vallée, où la vapeur monte de l'eau dans la nuit."),
    ("Yunomine Onsen → Hosshinmon-ōji", "Kawayu (ou Yunomine) → Hosshinmon-ōji"),
    ("Retour à l'auberge pour le dîner : à pied à Yunomine, en voiture laissée la veille ou en bus pour Kawayu et Ukegawa.", "Retour au Fujiya pour le dîner : bus de Yunomine vers Kawayu (changement à Hongū), taxi, ou la voiture si elle a été laissée à Hongū le matin."),
    ("à pied (Yunomine) ; bus, taxi ou voiture récupérée (Kawayu, Ukegawa)", "bus via Hongū, taxi, ou voiture récupérée à Hongū"),
    ("Hébergements : Booking.com, relevés du 1er novembre 2026 pour deux adultes aux dates du voyage ; les prix changent chaque jour. ", ""),
]

# Lieu du jour (pour le soleil et la météo) : date -> (nom, lat, lon)
DAY_PLACE = {
    "2026-12-26": ("Paris", 49.01, 2.55), "2026-12-27": ("Tokyo", 35.70, 139.77), "2026-12-28": ("Tokyo", 35.70, 139.77), "2026-12-29": ("Tokyo", 35.70, 139.77),
    "2026-12-30": ("Matsumoto", 36.24, 137.97), "2026-12-31": ("Takayama", 36.14, 137.25), "2027-01-01": ("Shirakawa-gō", 36.26, 136.91), "2027-01-02": ("Ise", 34.49, 136.71),
    "2027-01-03": ("Kumano, Hongū", 33.84, 135.77), "2027-01-04": ("Kumano, Hongū", 33.84, 135.77), "2027-01-05": ("Nachi, Kii-Katsuura", 33.62, 135.94), "2027-01-06": ("Kōya-san", 34.21, 135.59),
    "2027-01-07": ("Kyoto", 35.00, 135.77), "2027-01-08": ("Nara", 34.68, 135.84), "2027-01-09": ("Kyoto, Tokyo", 35.00, 135.77), "2027-01-10": ("Tokyo", 35.68, 139.71), "2027-01-11": ("Paris", 49.01, 2.55),
}
CAR_DAYS = {"2027-01-03", "2027-01-04", "2027-01-05", "2027-01-06"}
MOUNTAIN_DAYS = {"2026-12-30", "2026-12-31", "2027-01-01", "2027-01-02", "2027-01-03", "2027-01-04", "2027-01-05", "2027-01-06"}

# Noms et adresses en japonais, à montrer au chauffeur (clé = nom d'hôtel tel que dans HOTELS)
HOTELS_JP = {
    "Nohga Hotel Akihabara Tokyo": "ノーガホテル秋葉原東京　東京都千代田区外神田3-10-11",
    "Dormy Inn Matsumoto": "ドーミーイン松本　長野県松本市深志2-2-1",
    "eph TAKAYAMA": "エフ高山（eph TAKAYAMA）　岐阜県高山市花里町5-13-17",
    "Experience Ise Miyamachi Hotel": "Experience Ise Miyamachi Hotel　三重県伊勢市宮町（伊勢市駅から徒歩10分）",
    "Kawayu Onsen Fujiya": "川湯温泉 冨士屋　和歌山県田辺市本宮町川湯1452",
    "Hotel Urashima": "ホテル浦島　和歌山県東牟婁郡那智勝浦町勝浦1165-2",
    "The Gate Hotel Osaka by Hulic": "ザ・ゲートホテル大阪 by HULIC　大阪市中央区南船場3-12-14",
    "Richmond Hotel Premier Kyoto Ekimae": "リッチモンドホテルプレミア京都駅前　京都市下京区北不動堂町565-3",
    "Mitsui Garden Hotel Jingūgaien Tokyo Premier": "三井ガーデンホテル神宮外苑の杜プレミア　東京都新宿区霞ヶ丘町11-3",
}

# Météo, routes, webcams : liens par journée de montagne ou de voiture
WEATHER_LINKS = {
    "2026-12-30": [("JMA, prévisions Nagano", "https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=200000")],
    "2026-12-31": [("JMA, prévisions Gifu (Hida)", "https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=210000"), ("Alpico, info trafic des cars", "https://www.alpico.co.jp/traffic/express/matsumoto_takayama/")],
    "2027-01-01": [("JMA, prévisions Gifu (Hida)", "https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=210000"), ("Webcams de Shirakawa-gō (recherche)", "https://www.google.com/search?q=白川郷+ライブカメラ"), ("Nohi Bus, info trafic", "https://www.nouhibus.co.jp/")],
    "2027-01-02": [("JMA, prévisions Mie", "https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=240000")],
    "2027-01-03": [("JMA, prévisions Mie", "https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=240000"), ("JMA, prévisions Wakayama", "https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=300000"), ("Routes de Wakayama, fermetures en temps réel", "https://www.wakayamaken.geocloud.jp/mp/7"), ("Restrictions de circulation à Ise (Nouvel An)", "https://www.rakurakuise.jp/")],
    "2027-01-04": [("JMA, prévisions Wakayama", "https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=300000"), ("Kumano Travel, état des sentiers", "https://www.tb-kumano.jp/en/")],
    "2027-01-05": [("JMA, prévisions Wakayama", "https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=300000"), ("Routes de Wakayama, fermetures en temps réel", "https://www.wakayamaken.geocloud.jp/mp/7")],
    "2027-01-06": [("JMA, prévisions Wakayama (Kōya-san)", "https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=300000"), ("Routes de Wakayama, fermetures en temps réel", "https://www.wakayamaken.geocloud.jp/mp/7"), ("Webcams de Kōya-san (recherche)", "https://www.google.com/search?q=高野山+ライブカメラ"), ("JARTIC, info routes (japonais)", "https://www.jartic.or.jp/")],
}

# Papiers : champs à remplir (clé, libellé, valeur par défaut)
PAPERS_FIELDS = [
    ("vol_aller", "Vol aller", "AF274, Paris CDG 22 h 20 → Haneda 19 h 55 (27 déc.)"),
    ("vol_retour", "Vol retour", "AF279, Haneda 22 h 55 (10 janv.) → Paris CDG 5 h 50"),
    ("pnr", "Référence Air France (PNR)", ""),
    ("allibert_dossier", "Dossier Allibert (n° et conseillère)", "Devis T7J4, Camille de Farcy, +33 5 34 44 55 73"),
    ("assistance", "Assistance Allibert 24 h/24 (numéro du roadbook)", ""),
    ("agence_locale", "Agence locale au Japon (nom, téléphone)", ""),
    ("voiture", "Voiture de location (loueur, n° de réservation, plaque)", "Prise à Ise le 3 janv., rendue à l'aéroport du Kansai le 6 avant 20 h"),
    ("assurance", "Assurance voyage (contrat, téléphone)", ""),
    ("banque", "Banque, opposition carte (téléphone)", ""),
    ("ambassade", "Ambassade de France à Tokyo", "4-11-44 Minami-Azabu, Minato-ku ; +81 3 5798 6000 ; urgences 119 (ambulance), 110 (police)"),
    ("wifi", "Pocket wifi (identifiants, consigne de retour)", ""),
    ("tgv", "TGV Besançon ⇄ Paris (références)", ""),
]

PHRASES = [
    ("Bonjour / Bonsoir", "こんにちは / こんばんは", "konnichiwa / konbanwa"),
    ("Merci beaucoup", "ありがとうございます", "arigatō gozaimasu"),
    ("Excusez-moi (pour appeler, s'excuser)", "すみません", "sumimasen"),
    ("Deux personnes, sans réservation", "予約なしで、二人です", "yoyaku nashi de, futari desu"),
    ("Nous avons une réservation au nom de Léger", "レジェで予約しています", "Rejē de yoyaku shite imasu"),
    ("L'addition, s'il vous plaît", "お会計お願いします", "okaikei onegaishimasu"),
    ("Carte bancaire, c'est possible ?", "カードは使えますか", "kādo wa tsukaemasu ka"),
    ("Pas d'allergie, nous mangeons de tout", "アレルギーはありません。何でも食べます", "arerugī wa arimasen, nandemo tabemasu"),
    ("Une recommandation du chef, s'il vous plaît", "おすすめをお願いします", "osusume o onegaishimasu"),
    ("Où est la gare / l'arrêt de bus ?", "駅 / バス停はどこですか", "eki / basutei wa doko desu ka"),
    ("Ce bus va à Hosshinmon-ōji ?", "このバスは発心門王子に行きますか", "kono basu wa Hosshinmon-ōji ni ikimasu ka"),
    ("Le plein, ordinaire, s'il vous plaît", "レギュラー満タンでお願いします", "regyurā mantan de onegaishimasu"),
    ("Pneus hiver, c'est bien équipé ?", "スタッドレスタイヤですか", "sutaddoresu taiya desu ka"),
    ("Pouvons-nous laisser les bagages ?", "荷物を預かってもらえますか", "nimotsu o azukatte moraemasu ka"),
    ("À quelle heure est le dîner / le petit-déjeuner ?", "夕食 / 朝食は何時ですか", "yūshoku / chōshoku wa nanji desu ka"),
    ("Le bain est ouvert jusqu'à quelle heure ?", "お風呂は何時までですか", "ofuro wa nanji made desu ka"),
    ("Un bain privé, c'est possible ?", "貸切風呂はありますか", "kashikiri-buro wa arimasu ka"),
    ("Je ne parle pas japonais, anglais ?", "日本語が話せません。英語は大丈夫ですか", "nihongo ga hanasemasen, eigo wa daijōbu desu ka"),
    ("Pouvez-vous écrire ici, s'il vous plaît ?", "ここに書いてもらえますか", "koko ni kaite moraemasu ka"),
    ("Jusqu'à cet hôtel, s'il vous plaît (taxi)", "このホテルまでお願いします", "kono hoteru made onegaishimasu"),
    ("C'est délicieux", "おいしいです", "oishii desu"),
    ("Au revoir / Merci pour le repas", "さようなら / ごちそうさまでした", "sayōnara / gochisōsama deshita"),
]

NUMBERS = [
    ("Urgences", "119 ambulance et pompiers, 110 police (anglais possible, parler lentement)"),
    ("Japan Visitor Hotline (JNTO, 24 h/24, anglais)", "050 3816 2787"),
    ("Ambassade de France à Tokyo", "+81 3 5798 6000"),
    ("Allibert, assistance 24 h/24", "numéro dans le roadbook, à recopier dans Papiers"),
    ("Kumano Travel (Tanabe), anglais", "+81 739 34 5599"),
    ("Nohi Bus, Takayama", "+81 577 32 1688"),
    ("JR East, infoline anglais", "+81 50 2016 1603"),
    ("Objets perdus dans un taxi ou un train", "demander à l'hôtel d'appeler la compagnie ; garder les reçus"),
]

PACK = [
    "Passeports (validité OK), copies dans Papiers", "Permis français et les deux traductions japonaises", "Roadbook et vouchers Allibert (PDF + papier)", "Billets AF, TGV, QR Visit Japan Web en capture",
    "Cartes bancaires (deux), un peu de yens si possible", "Téléphones chargés, câbles, batterie externe, adaptateur type A", "Chaussures de marche ou de trail, petits crampons, bâtons pliants",
    "Doudoune légère, polaire, coupe-vent, bonnet, gants fins", "Serviette fine et sac pour les bains, maillot (Sennin-buro)", "Petite pharmacie", "Appareils photo, cartes, batteries, chargeurs", "Lunettes de soleil (neige), crème", "Sac à dos de journée",
]
MORNING = [
    "Passeports et portefeuille", "Pocket wifi chargé et dans le sac", "Billets ou roadbook du jour", "Téléphones et batterie externe chargés", "Cartes hors ligne du jour téléchargées",
    "Bouteille d'eau, en-cas", "Rien d'oublié dans la chambre (chargeurs, bain, coffre)", "Heure du prochain train ou car vérifiée",
]
