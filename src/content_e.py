# -*- coding: utf-8 -*-
"""Carnet v7, mode « avec Allibert » : ce qui change quand le voyage est organisé par Allibert Trekking (programme V2 du 2 novembre 2026)."""

KICKER = "CARNET DE VOYAGE · PROGRAMME ALLIBERT TREKKING, VERSION 2"
FOOT = "Vols directs Air France réservés par nous · programme Allibert V2 du 2 novembre 2026 · guide version 7.1"

INTRO = ("Ce carnet suit le programme sur-mesure d'Allibert Trekking (version 2 du 2 novembre 2026, 4 245 € par personne hors vols) : mêmes dates, mêmes étapes, "
         "les hôtels qu'ils ont confirmés. Allibert réserve les trains, les cars, la voiture, les hôtels, la journée guidée à Kyoto, et fournit le roadbook, le pocket wifi et une assistance 24 h/24. "
         "Ce que ce carnet ajoute, c'est le reste : les journées heure par heure, les adresses où manger, boire un café, se baigner, voir des appareils photo, et les plans B si quelque chose coince.")

# Ce qui est compris dans le devis Allibert (programme V2) et ce qui reste à notre charge
INCLUDED = dict(
    yes=[
        "Accueil à l'aéroport de Haneda le 27 décembre au soir, remise des documents et du pocket wifi illimité (pour deux, tout le séjour).",
        "Les 14 nuits d'hôtel avec petit-déjeuner (sauf le 27, arrivée tardive), le dîner à l'hôtel Urashima le 5 janvier.",
        "Les trains : Azusa Tokyo → Matsumoto, Hida et Kintetsu vers Ise, Nankai depuis l'aéroport du Kansai, Osaka → Kyoto, Nozomi Kyoto → Tokyo, et les trajets locaux prévus au programme (carte Icoca ou billets, selon le roadbook).",
        "La voiture de location du 3 janvier (Ise) au 6 janvier (aéroport du Kansai), en aller simple.",
        "La journée guidée à Kyoto le 7 janvier, avec un guide francophone.",
        "Le roadbook détaillé, la traduction du permis d'un conducteur, l'assistance 24 h/24 en français.",
    ],
    no=[
        "Les vols (réservés par nous : Air France, 3 431 € pour deux) et les trains Besançon ⇄ Paris.",
        "Les déjeuners et les dîners (sauf le 5 janvier), les boissons.",
        "Les entrées des temples, musées, bains ; les cars de montagne du 31 décembre et du 1er janvier s'ils restent « à régler sur place » (à confirmer avec Camille).",
        "La traduction du permis du second conducteur (70 € chez Japan Experience), l'assurance annulation si l'on ne passe pas par la leur.",
        "Le supplément Kawayu Onsen Fujiya à la place de J-Hoppers, si Allibert accepte de le réserver (environ 520 € les deux nuits, dîners compris).",
    ],
    todo="Points encore ouverts au 2 novembre : Yunomine (Fujiya ou J-Hoppers), les cars de montagne, le restaurant du réveillon, la réservation de siège du Nozomi du 9 janvier.",
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
    kumano=[("Kawayu Onsen Fujiya (ou J-Hoppers Kumano Yunomine)", "2 nuits, 3 et 4 janvier", "Kawayu, Hongū-chō, Tanabe, Wakayama", "Kawayu Onsen Fujiya", "https://www.fuziya.co.jp/",
             "Notre demande à Allibert : ryokan au bord de la rivière chaude de Kawayu, chambres avec bain et toilettes, bains extérieurs sur la rivière, dîner et petit-déjeuner, parking. Yunomine est à 10 min de voiture. Si Allibert maintient J-Hoppers Kumano Yunomine Guesthouse (au bord de la rivière de Yunomine, sanitaires communs, trois bains privatisables, cuisine commune, pas de dîner) : courses à Shingū le 3 avant de monter."),
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
            ("Tout de suite", "Répondre à Camille et envoyer les passeports",
             "Copies des passeports, et nos réponses : Fujiya à Kawayu plutôt que J-Hoppers (dîners compris, nous prenons le surcoût), Experience Ise en twin, aucun régime, Gyu-Suke pour le réveillon (qui réserve, et à quelle heure ?), cars de montagne compris ou non, siège réservé dans le Nozomi du 9 janvier.", "B"),
            ("À réception", "Devis n°2 et bulletin d'inscription",
             "Vérifier que le devis reprend bien les hôtels de la V2 (eph, Experience Ise, Fujiya ou J-Hoppers, Urashima avec dîner, The Gate), la voiture en aller simple avec pneus hiver et deux conducteurs, le pocket wifi, la journée guidée à Kyoto. Signer et verser l'acompte : les hôtels de Takayama ne sont bloqués qu'après.", "B"),
            ("Cette semaine", "Traduction du permis du second conducteur",
             "Allibert ne traduit qu'un permis. Pour pouvoir conduire à deux : <a href=\"https://japan-experience.com/transportation/driving-licence-translation\">Japan Experience, traduction officielle</a>, 70 €, environ 12 jours, livraison à domicile. Le permis international français ne sert à rien au Japon.", "B"),
            ("Cette semaine", "Assurance annulation et rapatriement",
             "Regarder ce que couvre la carte bancaire (annulation, rapatriement, bagages, franchise de la voiture de location) avant d'accepter ou non l'assurance proposée dans le bulletin d'inscription.", "I"),
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
            ("Mi-décembre", "Dîner du réveillon à Takayama",
             "Si Allibert ne réserve pas Gyu-Suke, le faire nous-mêmes par l'hôtel eph ou par téléphone ; viser 18 h ou 18 h 30 pour être au temple Hida Kokubun-ji vers 23 h 30 pour la cloche de la nuit. En secours, Ajikura Tengoku (yakiniku, sans réservation, s'y présenter à 17 h).", "I"),
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
             "eph Takayama ferme sa réception à 20 h ; Fujiya ou J-Hoppers servent le dîner à heure fixe ou attendent une arrivée avant 18 h ; Urashima check-in 15 h. Allibert transmet en général, mais un mot de confirmation ne coûte rien.", "U"),
        ]),
    ],
    [
        ("5", "Sur place", "les rendez-vous à ne pas manquer", [
            ("27 déc.", "Haneda, 19 h 55", "Accueil Allibert à la sortie des arrivées du terminal 3, remise des documents et du pocket wifi. Retirer des yens au 7-Eleven avant de partir.", "B"),
            ("30 déc.", "Azusa de Shinjuku", "Quais 9 et 10 des express Chūō, au sud de la gare ; 20 min de marge, valises dans l'espace derrière la dernière rangée. Chambre rendue le matin, valises reprises vers 15 h.", "I"),
            ("31 déc.", "Car de Matsumoto", "Terminal de bus face à la gare, 15 min avant le départ, valises en soute. Le soir, Gyu-Suke puis Hida Kokubun-ji vers 23 h 30 pour la cloche.", "I"),
            ("3 janv.", "Naikū à l'aube, puis la voiture", "Naikū avant 7 h (ouvert jour et nuit pendant les fêtes), retour à l'hôtel, prise de la voiture à l'heure indiquée par le roadbook : permis, traductions, pneus hiver, carte ETC, état des lieux en photos. Plein et courses à Shingū.", "B"),
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
        ("LE BULLETIN D'INSCRIPTION", "Tant qu'il n'est pas signé, les hôtels de Takayama (31 décembre) ne sont pas bloqués : c'est le point le plus tendu du voyage."),
        ("LE SECOND PERMIS", "Allibert ne traduit qu'un permis. Douze jours de délai chez Japan Experience : à commander cette semaine pour conduire à deux."),
        ("YUNOMINE", "Fujiya (Kawayu, dîners compris) ou J-Hoppers (Yunomine, sans dîner) : la réponse de Camille décide des courses à faire à Shingū le 3."),
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
                      "Si l'auberge ne sert pas de dîner (J-Hoppers), faire aussi les courses du soir à Shingū. Prévenir de l'heure d'arrivée."],
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
    "NOUVEL AN": "Du 29 décembre au 3 janvier, musées, administrations et beaucoup de restaurants ferment ; les sanctuaires sont bondés. Konbini, grandes gares et restaurants d'hôtel restent ouverts. Le 31 au soir à Takayama (Gyu-Suke) et les 3 et 4 au Kumano (demi-pension à Fujiya, ou courses si J-Hoppers), les dîners sont à régler avant de partir.",
    "ARRIVÉE ET DÉPART": "Le 27, accueil Allibert à Haneda (terminal 3) puis train Keikyū, 45 min jusqu'à Akihabara. Visit Japan Web fournit un seul QR code, à montrer à l'immigration puis à la douane. Le 10 janvier, depuis le Mitsui Garden, 45 min jusqu'au terminal 3 par la ligne Ōedo (Daimon) puis Keikyū direct ; être à l'aéroport 3 h avant le vol.",
}

BEFORE_BOXES = [
    ("AVEC ALLIBERT",
     "<p>Programme sur-mesure V2 du 2 novembre 2026, conseillère Camille de Farcy (+33 5 34 44 55 73). Compris : hôtels avec petits-déjeuners, trains, voiture en aller simple, journée guidée à Kyoto, pocket wifi, accueil à Haneda, roadbook, assistance 24 h/24 en français.</p>"
     "<p>Non compris : vols et TGV (à nous), repas sauf le dîner du 5 janvier, entrées et bains, cars de montagne si « à régler sur place », traduction du second permis.</p>"),
    ("LE PROGRAMME EN UNE LIGNE",
     "<p>Tokyo 27 au 30 décembre ; Matsumoto le 30 ; Takayama les 31 et 1er avec Shirakawa-gō ; Ise le 2 ; voiture du 3 au 6 : Kumano (Kawayu ou Yunomine), Nachi et Kii-Katsuura, Kōya-san ; Osaka le 6 ; Kyoto les 7 et 8 avec Nara ; Tokyo le 9 ; vol le 10 au soir.</p>"
     "<p>Dix-sept jours, quatorze nuits, environ 60 km de marche en tout, quatre jours de voiture.</p>"),
]

BRIEF_OVERRIDES = {
    "Point d'attention": "Allibert réserve trains, cars (à confirmer), voiture et hôtels ; restent à nous le bulletin d'inscription à signer vite (Takayama), la traduction du second permis, le TGV du retour, et les dîners des jours où rien n'est compris.",
    "Hébergements": "Hôtels de ville bien tenus (Nohga, Dormy Inn, eph, Richmond, Mitsui Garden, The Gate), un ryokan ou une guesthouse au bord de la rivière chaude du Kumano, et un grand hôtel de bains face à la mer à Kii-Katsuura, dîner compris.",
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
    ("Hébergements : Booking.com, relevés du 1er novembre 2026 pour deux adultes aux dates du voyage ; les prix changent chaque jour. ", ""),
]
