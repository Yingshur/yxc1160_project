
from app import db
from app.models import Emperor, Image, User, War, Architecture


hagia_sophia_description = (
    "\"Hagia Sophia, or 'Holy Wisdom,' is one of the world’s most innovative architectural marvels. The building, located in present-day Istanbul, Turkey, embodies a complex history of conversion, both within its walls and through its larger socio-political contexts. It takes on a multiplicity of cultural and religious identities, and despite being constructed thousands of years ago, its position is still not fixed. Recent events regarding its shift from a museum back to a practicing mosque has been the center of controversy and international attention, as well as proven the continuous, living nature of buildings and cultural monuments.\n\n"
    "Initially, Hagia Sophia was built as Constantinople’s central cathedral in the 4th century under emperor Constantius II, although its wooden roof led to it burning down. The church was reconstructed in the 5th century under Theodosius II, and this version’s wooden frame, too, led to its fiery demise. In 537 CE, the Byzantine emperor Justinian I rebuilt Hagia Sophia, and this structure stood the test of time and is the building that we know it as today. He felt it crucial to empower himself and his empire through the construction of Hagia Sophia and the city of Constnatinople as a whole. While it has structurally remained very similar to this 6th century version, it has also undergone multiple restorations and been subject to a changing of rulers, resulting in a variety of adaptations and subtracted or added elements. Constantinople was the imperial city of the Byzantine Empire and home of the Eastern Orthodox Church. During the Fourth Crusade in 1204, Constantinople was captured, and Hagia Sophia was converted to a Catholic church, although by 1261 it had been reinstated as an Orthodox church.\n\n"
    "The real fall of Constantinople occurred nearly 200 years later in 1453 with the arrival of the Ottoman sultan Mehmet II and the official demise of the Byzantine Empire. Mehmet II conquered the city, made Constantinople the new capital of the Ottoman Empire, and converted Hagia Sophia into a mosque. Instead of entirely destroying the building, as conquerors might typically do to assert their dominance, Mehmet II chose to keep the structural integrity of Hagia Sophia intact, essentially only adding fundamental Islamic elements that would solidify its role as a mosque. Mehmet II must have recognized the architectural innovation of the building and its value as an artistic feat.\n\n"
    "Conversion, still, is itself a political statement. In 1935, Kemal Ataturk, the founding father of the modern Republic of Turkey, elected to change Hagia Sophia from its role as an imperial mosque into a secular museum. For years it remained this way, until July of 2020 when the current president of Turkey, Recep Tayyip Erdoğan, decided to convert Hagia Sophia back into a mosque. This decision has been under fire from the international community and is seen as a loss of universal cultural heritage. Hagia Sophia has been subject to an always shifting religious, political, and cultural identity, and its recent conversion has proven that this identity is still in flux today.\n\n"
    "Hagia Sophia has been universally revered as an artistic and engineering marvel since its inception. The minds behind its design were engineer Isidore of Miletus and mathematician Anthemius of Tralles. The most striking and unique part of Hagia Sophia’s structural design is its dome, which gives off the impression that it is floating. One of the architectural challenges in constructing the church was connecting a dome, a shape with a round base, onto a structure with a square base. Isidore of Miletus and Anthemius of Tralles solved this problem by employing the pendentive, a rounded, triangular-shaped support that smoothly connects the drum of a dome to a columnar base. This innovation suspends the dome, overcoming the need for heavy supports that interfere with the rhythm and open space of the interior. Given Hagia Sophia’s massive scale, accomplishing this was a monumental feat of its own —although the dome is imperfect in shape due to spreading, the fact that it has stood the test of time speaks to the engineering prowess of the original architects.\n\n"
    "The employment of the dome has allowed for the incredibly light and airy interior of Hagia Sophia, as it is pierced at its base with many windows that allow for light to pour into the space from all directions, illuminating the gold mosaic decoration covering the ceilings and walls. Ekphraseis from visitors of Hagia Sophia in its peak condition, prior to the accumulation of dirt or weathering of age, have repeatedly noted its abundant radiance. Its longitudinal axis deviates from the traditional east-west orientation of Orthodox churches and is actually positioned in a line 33.5 degrees south of east. This decision allows for Hagia Sophia to have maximum light exposure, even on the shortest day of the year, and has been advantageous in illuminating the interior.\n\n"
    "Upon its initial building, Hagia Sophia featured no figural mosaics, as this period in time corresponded with Iconoclasm. After its passing, however, there was a resurgence in the importance of images in Christianity, and succeeding Byzantine emperors have had religious scenes included in the ceilings, arches, and walls of the church. In the apse, the focus of the building, there is an image of the virgin Mary known as the Theotokos Mosaic. Her position in the apse, which is situated right above a glowing row of windows, allows the viewer to understand she is the mediator for worship of her son, who sits on her lap. The gold surrounding her is illuminated, further emphasizing the connection of light as corresponding with divinity. Other mosaics depict portraits of emperors and their submission to Mary and Christ. Within each of the dome’s pendentives are also seraphim mosaics, which had been plastered over at some point during the Ottoman rule and were uncovered by the Swiss Fossati brothers during restoration in the 1840s.\n\n"
    "The decorative program of Hagia Sophia is also embedded within its structural supports—its floor, walls, and several of its columns are made from unique porphyry and polychrome marble. The origins of these materials are thought to be from specific Mediterranean quarries that had actually ceased their operations by the time of the building’s construction. This history has led scholars to believe that many of its Hagia Sophia’s elements are spoliated from distant places and other buildings, as well as their oft imperfect proportions from one another.\n\n"
    "When Mehmet the II initially conquered Constantinople in the 15th century, he chose to refashion the church into a mosque instead of destroying it outright, despite brutally ransacking the city as a whole. As previously mentioned, conversion itself is a subversive tool used to assert dominance. Mehmet used conversion to usurp power from both the Byzantine and Christian empires and while declaring the preeminence of his own religion and imperial power. Under centuries of Ottoman rule, additional Islamic elements like Arabic scriptures, minarets, and a prayer niche were added to Hagia Sophia. Figural representations are traditionally excluded from the Islamic visual language for reasons that parallel Iconoclasm; only God should possess the divine ability to conjure a perfect human form. Despite this custom, detailed drawings made of Hagia Sophia during its phase as a Muslim space of worship have shown that practically none of the Christian religious imagery was covered during a majority of Ottoman reign. This phenomenon has been considered the result of the link between important figures who play significant roles in both the Bible and the Quran.\n\n"
    "Since 1935, Hagia Sophia has been a secular museum that became Turkey’s most popular attraction. This decision was controversial in Turkey; members of the Turkish Republic considered this move empowering by opening themselves up to the world, while in contrast, conservatives and nationalists found this choice a form of surrender to the west and a stripping of Muslim identity. Time has shown that Hagia Sophia’s conversion to a museum has been an asset to Turkey, as well as to universal cultural heritage and global education.\n\n"
    "President Erdoğan’s 2020 decision to convert Hagia Sophia back into a mosque has marked a new era of controversy surrounding the building. Some have viewed this move as a kind of bluff or a performance of power, particularly in light of Erdoğan’s unpopularity. His tenure has not been well-received by much of the country, and the conversion decree has been considered a public concession to his nationalist base in exchange for continued support. UNESCO has explicitly expressed its disapproval of the decision, especially due to the fact that Erdoğan enacted it without consulting their leadership. President Erdoğan has stated his commitment to keep the building open to the public when not in prayer, in addition to only covering the interior Christian imagery when in session and drawing the curtains back otherwise. Perhaps this seems a compromise to President Erdoğan, but the choice of conversion itself as merely a political tool is a reflection of his insecurity and lack of power as a leader. For hundreds of years of Ottoman rule, these mosaics had been uncovered and untouched—how might Erdoğan defend his decision to change the interior space, despite his arguably more powerful predecessors opting not to?\n\n"
    "Hagia Sophia has experienced a plethora of cultural exchange and a variety of political and religious turnovers. Its history is unique and fascinating, and its role as a museum has been integral in elucidating its splendor—as an engineering marvel, an artefact, and a narrator of religion. In this way, we can view Hagia Sophia as a universally significant object whose history does not exclusively belong to Istanbul, but instead is a symbol of global dialogue. Its transformation might play a role in silencing this conversation. The controversy surrounding Hagia Sophia’s conversion reminds us of the living presence of cultural monuments, and why it is urgent that we continue to preserve and protect them.\""
)





kleidion_description = (
    "\"A similarly stubborn refusal to give up when faced with apparently insurmountable physical obstacles was demonstrated by Basil II himself and his officers in the campaign of 1014. In the years preceding, the Roman strategy of attrition had worn down Bulgar resistance to such an extent that Samuel could no longer go on the offensive, but was limited to trying to prevent Byzantine incursions into his core territory and to preserve what lands and resources were still in his power. The Tsar’s strategy was to attempt to prevent the damaging raids mounted by Basil each year into these Macedonian heartlands. Campaigning generally began in May, and the raids usually involved imperial units pushing up from Serres in the south, through the pass of Rupel and along the ‘long plain’ (Campulungu, or ‘Kimbalonga’ in its Greek form) formed by the Strymon valley itself. Following well-established Bulgar practice, Samuel blocked many of the passes off with timber palisades and ditches, including the important pass at Kleidion (near the modern village of Kljuc), regularly employed by the imperial armies as they marched into Macedonia, despatching at the same time a diversionary attack against Thessaloniki by another route. The latter move was defeated by the local commander in the region, Theophylaktos Botaneiates, whose troops cut the Bulgar force to pieces. The attempt to block the pass also failed.\n\n"
    "Confronted by the high palisade erected by the Bulgars, the eastern Roman forces at first tried to storm the obstacle, but after sustaining disproportionate losses in the attempt, found that they would have to march a long way westwards or eastwards in order to circumvent the obstacle, which would have meant calling off the campaign for that year. One of Basil’s commanders, however, Niketas Xiphias, the commander of Philippoupolis, volunteered to lead a small force over the mountains in an attempt to find a way across and behind the enemy position. Basil’s forces maintained their position before the pass, launching a series of small-scale assaults to keep the Bulgars occupied, while Xiphias spent some time scouting the area on either side of the pass. Eventually he located a narrow and difficult track to the west of the pass, which led across mount Belasica, and at dawn on 29 July Xiphias’s small force fell on the rear lines of the Bulgar army with bloodcurdling yells. Order was never really established and, as panic gripped the Bulgar soldiers, the main imperial army under Basil, no longer faced by a determined and focused resistance from the palisade, were able to tear it down and begin the pursuit of their utterly disorganized foe. Many were killed, but the vast majority were surrounded and forced to surrender.\n\n"
    "This was Samuel’s last remaining army of any consequence, and its destruction effectively ended serious resistance. According to a slightly later source, some 15,000 prisoners were taken in all, and of these, Basil is supposed to have blinded all but one in every hundred, whom he left with one eye each to guide the rest back to Samuel. Whether the tale is true is hard to know, although there is probably some element of truth to it. At any rate, Samuel had a seizure or stroke of some kind when he saw what had happened to his soldiers, and died. Within the next four years Basil and his generals completed the subjugation of Bulgaria, and the Danube became once again the effective frontier of the Roman empire.\""
)


basil_i_bio = (
    "\"Basil came of a peasant family that had settled in Macedonia, perhaps of Armenian origin. He was a handsome and physically powerful man who gained employment in influential official circles in Constantinople and was fortunate enough to attract the imperial eye of the reigning emperor, Michael III. After rapid promotion he became chief equerry, then chamberlain, and finally, in 866, coemperor with Michael. Quick to sense opposition, he forestalled the emperor’s uncle, the powerful Caesar Bardas, by murdering him (866) and followed this by killing his own patron, Michael, who had begun to show signs of withdrawing his favour (867).\n\n"
    "From the mid-9th century onward, the Byzantines had taken the offensive in the agelong struggle between Christian and Muslim on the eastern borders of Asia Minor. Basil continued the attacks made during Michael III’s reign against the Arabs and their allies, the Paulicians, and had some success. Raids across the eastern frontier into the Euphrates region continued, though Basil did not manage to take the key city of Melitene. But the dangerous heretical Paulicians on the borders of the Armenian province in Asia Minor were crushed by 872, largely owing to the efforts of Basil’s son-in-law Christopher.\n\n"
    "In Cilicia, in southeast Asia Minor, the advance against the emir of Tarsus succeeded under the gifted general Nicephorus Phocas the Elder. Though Constantinople had lost much of its former naval supremacy in the Mediterranean, it still had an effective fleet. Cyprus appears to have been regained for several years.\n\n"
    "Basil’s plans for Italy involved him in negotiations with the Frankish emperor Louis II, the great-grandson of Charlemagne. The Byzantine position in southern Italy was strengthened with the help of the Lombard duchy of Benevento, and the campaigns of Nicephorus Phocas the Elder did much to consolidate this. The region was organized into the provinces of Calabria and Langobardia. But key cities in Sicily, such as Syracuse in 878, still continued to fall into Muslim hands, an indication of the strength of Arab forces in the Mediterranean.\n\n"
    "Another arm of Byzantine policy was the attempt to establish some measure of control over the Slavs in the Balkans. Closely allied to this was the delicate question of ecclesiastical relations between Constantinople and Rome. During Basil I’s reign, the young Bulgar state accepted the ecclesiastical jurisdiction of Constantinople (870). This had significant results both for the Balkan principalities and for the Orthodox Church, as well as greatly strengthening Byzantine influence in the south Slav world. Basil had inherited a quarrel between Photius and Ignatius as to which was to be patriarch of Constantinople. This had international implications, since appeals had been made to Rome. Immediately on his accession, Basil attempted to win support at home and to conciliate Rome by reinstating the deposed patriarch Ignatius and excommunicating Photius. Eventually, Photius was restored by Basil on the death of Ignatius (877) and recognized by Rome in 879. Contrary to the belief that used to be held, no “second schism” occurred. Basil successfully resolved the tension between liberal and strict Byzantine churchmen and managed to maintain a show of peace between East and West despite Rome’s displeasure at the marked extension of imperial influence in the new Balkan principalities.\n\n"
    "Toward the end of his life, Basil seemed to suffer fits of derangement, and he was cruelly biased against his son Leo. Basil died on the hunting field. The 11th-century historian Psellus wrote of his dynasty as “more blessed by God than any other family known to me, though rooted in murder and bloodshed.” But Macedonian historians were understandably biased in favour of the existing dynasty, to the detriment of the rulers it had supplanted. Recent historical research has raised the stature of Basil’s predecessor, Michael III, and his regents. It is now generally agreed that the “new age” in Byzantine history began with Michael III in 842 and not with the Macedonian dynasty in 867. Basil’s policies were largely determined, both at home and abroad, by factors not of his own making.\""
)

leo_vi_bio = (
    "\"Leo was the son of Basil I the Macedonian, who had begun the codification, and his second wife, Eudocia Ingerina. Made coemperor in 870, Leo succeeded to the throne on his father’s death. His foreign policy was directed mainly against the Arabs and the Bulgars. The able commander Nicephorus Phocas the Elder was recalled from his successful campaigns against the Lombards in south Italy to assist in the Balkans. After this Byzantium met with reverses in the West: Sicily was lost to the Arabs in 902, Thessalonica was sacked by Leo of Tripoli, and the Aegean was open to constant attack from Arab pirates. Steps were taken to strengthen the Byzantine navy, which successfully attacked the Arab fleet in the Aegean in 908. But the naval expedition of 911–912 was defeated by Leo of Tripoli. Byzantium’s enemy to the north was Simeon, the Bulgar ruler. Hostilities arose out of a trade dispute in 894, and the Byzantines, aided by the Magyars of the Danube-Dnieper region, forced Simeon to agree to a truce. With the help of the nomadic Pechenegs, however, Simeon in 896 took revenge on the Byzantines, forcing them to pay an annual tribute to the Bulgars.\n\n"
    "During Leo’s reign the Russian prince Oleg sailed to Constantinople and in 907 obtained a treaty regulating the position of Russian merchants in Byzantium, which was formally ratified in 911. Because of his anxiety for a male heir Leo married four times, thus incurring the censure of the church.\n\n"
    "Educated by the patriarch Photius, Leo was more scholar than soldier. In addition to completing the canon of laws, he wrote several decrees (novels) on a wide range of ecclesiastical and secular problems. He also wrote a funeral panegyric on his father, liturgical poems, sermons and orations, secular poetry, and military treatises. Leo’s image is in a mosaic over the central door of Hagia Sophia.\""
)

alexander_bio = (
    "\"Alexander was crowned co-emperor with his brother Leo VI in 879 after the death of their elder brother, Constantine, but he remained inactive in state affairs until after Leo’s death in May 912. Sending Leo VI’s fourth wife, Zoe, to a nunnery, he replaced Leo’s advisers and reinstated the deposed patriarch, Nicholas Mysticus.\n\n"
    "Alexander’s refusal to pay the annual tribute owed to the Bulgars by the treaty of 896 precipitated war with Symeon, their powerful and aggressive king. Alexander declared his nephew, Leo’s young son, later Constantine VII, his heir to the Byzantine throne and was co-regent with him for several months.\""
)




def reset_db():
    db.drop_all()
    db.create_all()

    users = [
        {'username': 'Chen', 'email': 'chenyingshu1234@gmail.com', 'role': 'Admin', 'pw': 'Chenxh1031!', 'user_type': 'Autocrat'},
        {'username': 'Chen1', 'email': 'chenryan715@gmail.com', 'pw': 'Chenxh1031!'},
    ]

    for u in users:
        pw = u.pop('pw')
        user = User(**u)
        user.set_password(pw)
        db.session.add(user)

    emperors = [
        {
            'title': 'Basil I "the Macedonian"',
            'in_greek': 'Βασίλειος Αʹ ὁ Μακεδών',
            'birth': '826-835?, Thrace',
            'death': 'August 29 886',
            'reign': '867-886',
            'life': basil_i_bio,
            'dynasty': "Macedonian",
            'reign_start': 867,
            'ascent_to_power': 'Hereditary succession',
            'references': 'Hussey, J.M. (n.d.). Basil I | Byzantine emperor. [online] Encyclopedia Britannica. Available at: https://www.britannica.com/biography/Basil-I-Byzantine-emperor.'
        },
        {
            'title': 'Leo VI "the Wise"',
            'in_greek': 'Λέων ΣΤʹ ὁ Σοφός',
            'birth': '866, Constantinople',
            'death': '11 May 912',
            'reign': '886–912',
            'life': leo_vi_bio,
            'dynasty': "Macedonian",
            'reign_start': 886,
            'ascent_to_power': 'Hereditary succession',
            'references': 'The Editors of Encyclopædia Britannica (n.d.). Leo IV | Byzantine emperor. [online] Encyclopedia Britannica. Available at: https://www.britannica.com/biography/Leo-IV.'

        },
        {
            'title': 'Alexander',
            'in_greek': 'Ἀλέξανδρος',
            'birth': '870, Constantinople',
            'death': '6 June 913',
            'reign': '912–913',
            'life': alexander_bio,
            'dynasty': "Macedonian",
            'reign_start': 912,
            'ascent_to_power': 'Hereditary succession',
            'references': 'The Editors of Encyclopædia Britannica (1998). Alexander | Byzantine Empire, Eastern Roman Empire, Reformer. [online] Encyclopedia Britannica. Available at: https://www.britannica.com/biography/Alexander-Byzantine-emperor [Accessed 2 Jun. 2025].'

    }
    ]

    for e in emperors:
        emperor = Emperor(**e)
        db.session.add(emperor)

    wars = [
        {
            'title': "Battle of Kleidion",
            'start_year': 1014,
            'dates': "29 July 1014",
            'location': "Belasitsa Mountains, near Klyuch (modern Bulgaria)",
            'latitude': 41.3667,
            'longitude': 23.0167,
            'dynasty': "Macedonian",
            'war_name': "Byzantine–Bulgarian Wars",
            'war_type': "Foreign War",
            'result': "Roman Victory",
            'roman_commanders': "Basil II, Niketas Xiphias, Theophylaktos Botaneiates",
            'enemy_commanders': "Tsar Samuel of Bulgaria",
            'roman_strength': "Unknown; likely imperial field army with support from Philippoupolis",
            'enemy_strength': "Approx. 15,000 men",
            'roman_loss': "Moderate losses during frontal assault; minimal afterward",
            'enemy_loss': "Heavy; most of 15,000 captured and allegedly blinded",
            'description': kleidion_description,
            'references': 'Haldon, J., 2008. The Byzantine Wars. The History Press.'
        }
    ]
    for war_data in wars:
        war = War(**war_data)
        db.session.add(war)



    images = [
        {
            'filename': 'Basil I',
            'url': '/static/images/macedonians/Basil_I.png',
            'caption':'Portrait from the illuminated manuscript Paris Gregory',
            'emperor_id': 1
        },
        {
            'filename': 'Leo VI',
            'url': '/static/images/macedonians/Leo_VI.jpg',
            'caption': 'Mosaic Portrait in Hagia Sophia',
            'emperor_id': 2
        },
        {
            'filename': 'Alexander',
            'url': '/static/images/macedonians/Alexandros.jpg',
            'caption': 'Mosaic Portrait in Hagia Sophia',
            'emperor_id': 3
        },
        {
            'filename': 'Battle of Kleidon',
            'url': '/static/images/wars/Basil_win.jpg',
            'caption': 'Basil II defeats the Bulgarian Tsar',
            'war_id': 1
        },
        {
            'filename': 'Hagia Sophia',
            'url': '/static/images/culture/Hagia_Sophia.jpg',
            'caption': 'Hagia Sophia, February 2024',
            'architecture_id': 1
        }
    ]

    for i in images:
        image = Image(**i)
        db.session.add(image)

    buildings = [
        {
            'title': "Hagia Sophia",
            'in_greek': "Ἁγία Σοφία",
            'construction_completed': 360,
            'architectural_style': "Early Byzantine",
            'current_status': "Converted into a Mosque",
            'location': "Constantinople",
            'latitude' : 41.0086,
            'longitude': 28.9802,
            'building_type': "Ecclesiastical Building",
            'description': hagia_sophia_description,
            'references': "Harvard University. (n.d.). Hagia Sophia. Whose Culture? Retrieved July 25, 2025, from https://whoseculture.hsites.harvard.edu/hagia-sophia"
        }
    ]

    for building_data in buildings:
        building = Architecture(**building_data)
        db.session.add(building)


    db.session.commit()
