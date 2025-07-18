
from app import db
from app.models import Emperor, Image, User
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
        {'username': 'Chen', 'email': 'chenyingshu1234@gmail.com', 'role': 'Admin', 'pw': 'Chenxh1031!'},
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
            'dynasty': "Macedonian"

        },
        {
            'title': 'Leo VI "the Wise"',
            'in_greek': 'Λέων ΣΤʹ ὁ Σοφός',
            'birth': '866, Constantinople',
            'death': '11 May 912',
            'reign': '886–912',
            'life': leo_vi_bio,
            'dynasty': "Macedonian"
        },
        {
            'title': 'Alexander',
            'in_greek': 'Ἀλέξανδρος',
            'birth': '870, Constantinople',
            'death': '6 June 913',
            'reign': '912–913',
            'life': alexander_bio,
            'dynasty': "Macedonian"
        }
    ]

    for e in emperors:
        emperor = Emperor(**e)
        db.session.add(emperor)

    images = [
        {
            'filename': 'Basil I',
            'url': '/static/images/macedonians/Basil_I.png',
            'caption':'Portrait from the illuminated manuscript Paris Gregory',
            'emperor_title': 'Basil I "the Macedonian"'
        },
        {
            'filename': 'Leo VI',
            'url': '/static/images/macedonians/Leo_VI.jpg',
            'caption': 'Mosaic Portrait in Hagia Sophia',
            'emperor_title': 'Leo VI "the Wise"'
        },
        {
            'filename': 'Alexander',
            'url': '/static/images/macedonians/Alexandros.jpg',
            'caption': 'Mosaic Portrait in Hagia Sophia',
            'emperor_title': 'Alexander'
        }
    ]

    for i in images:
        image = Image(**i)
        db.session.add(image)

    db.session.commit()
