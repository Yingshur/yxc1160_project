
from app import db
from app.models import Emperor, Image, User, War, Architecture, Literature, Artifact



andronicus_ii_bio = (
    "\"An intellectual and theologian rather than a statesman or soldier, Andronicus weakened Byzantium by reducing its land forces to a few thousand cavalry and infantry and eliminating the navy altogether, "
    "relying solely on a Genoese mercenary fleet. His lack of military initiative enabled the Ottoman Turks to gain control of nearly all of Anatolia by 1300, and his employment of Catalan mercenaries in 1304 ended disastrously, "
    "because the Catalans proved more inclined to pillage Byzantine cities than to fight the Turks. In the war between the Italian city-states of Venice and Genoa, Andronicus unwisely took sides, favouring Genoa, and suffered the wrath of the greatly superior Venetian navy.\n\n"
    "Internally, Andronicus’s reign was marked by a steady disintegration of centralized authority and increasing economic difficulties, although he did sponsor a revival of Byzantine art and culture and championed the independence of the Eastern Orthodox church. "
    "During his reign the great monastery complex at Mount Athos in Greece enjoyed its golden age.\n\n"
    "In 1328 Andronicus, after quarreling with his grandson—who would become Andronicus III—and excluding him from the succession, was deposed by him and entered a monastery.\""
)


saint_stephens_crown_description = (
    "\"Saint Stephen’s Crown, greatly venerated crown of Hungary, is the symbol of Hungarian nationhood, without which no sovereign was truly accepted by the Hungarian people. It is made from an 11th-century jeweled circlet of Byzantine style, augmented early in the 12th century by the addition of arches and an upper rim composed of alternate pointed and round-topped plaques of enameled gold. Small pendants hang on short chains on both sides and at the back.\n\n"
    "The cross on the top is crooked, because the screw hole in the knob it stands on was set at an angle, suggesting that originally it was not meant to occupy the top of the crown but to go on a sloping surface—possibly the curve of the foremost arch.\n\n"
    "The crown was given to a U.S. Army unit by a Hungarian honour guard to keep it from being seized by advancing Soviet troops after World War II. It remained in U.S. guardianship at Fort Knox until it was returned to Hungary in 1978.\""
)

isaac_ii_bio_detailed = (
    "\"In 1189 the Byzantine ruler was confronted with the Third Crusade, which, led by the Holy Roman emperor Frederick I Barbarossa, was passing through Byzantine territory. "
    "Isaac tried to protect himself by concluding a treaty with Saladin, the sultan of Egypt, but he was soon forced to assist Frederick. Isaac concluded the Treaty of Adrianople with Frederick in February 1190, and in the following month Frederick’s forces were transported across the Hellespont to Asia Minor.\n\n"
    "Free to turn his attention to the Balkans, Isaac restored Byzantine prestige by defeating Stefan Nemanja of Serbia (1190). With Hungarian help, he planned an expedition against the Bulgarians, assembling a Byzantine army for this purpose near the city of Cypsela in the spring of 1195. "
    "On April 8, however, he was suddenly overthrown by his brother, who imprisoned and blinded him and assumed the throne as Emperor Alexius III.\n\n"
    "In 1201 Isaac’s son Alexius made his way to Germany, where he succeeded in bringing about the diversion of the Fourth Crusade to Constantinople in order to restore his father to power. "
    "In July 1203 the Crusaders entered the city, and on August 1 Isaac, after eight years’ imprisonment, was crowned co-emperor with Alexius, who assumed the title Alexius IV. "
    "Friction between the Crusaders and the townspeople of Constantinople, however, led to a revolution in January 1204. The co-emperors were dethroned, Alexius IV was assassinated on February 8, 1204, and Isaac died several days later.\""
)


michael_viii_bio_detailed = (
    "\"A scion of several former imperial families (Ducas, Angelus, Comnenus), Michael passed a rather uneventful boyhood, seemingly marked primarily by fantasies of himself recovering Constantinople from the Latins; he spent much of his youth living in the imperial palaces at Nicaea and Nicomedia.\"\n\n"
    "\"His remarkable resourcefulness and talent for intrigue were revealed early. At the age of 21 he was charged by the emperor John III Vatatzes of Nicaea with treasonous conduct against the state, a charge from which he extricated himself by the force of his wit. Later, on the death of the emperor Theodore II Lascaris in 1258, Michael was chosen regent for Theodore’s six-year-old son, John Lascaris. Gradually usurping more and more authority, Michael seized the throne and early in 1259 was crowned emperor after shunting aside and blinding the rightful heir, his charge, John. Faced with rebellion by Lascarid supporters in Asia Minor, Michael succeeded, in the eyes of many Greeks, in legitimating his rule by retaking Constantinople from the Latins. Whether as the result of Michael’s carefully planned ruse or of accident or both, the great city fell to his general in July 1261. Although the Greeks generally were exultant, a few realized that the centre of gravity had shifted from Asia Minor to Europe. In the long run this concern with Europe was to prove fateful, for it led to the neglect of the frontiers in the East and, with that neglect, eventually to the conquest and settlement of all of Asia Minor by the Turks.\"\n\n"
    "\"From the first, Michael’s hold on the throne was precarious, surrounded as it was on all sides by Latins desirous of restoring Latin rule. Especially active was Baldwin II of Courtenay, the last Latin emperor of Constantinople. In his maneuvers to recover his throne from Michael, Baldwin finally entered into a diplomatic and matrimonial alliance with a man who was the West’s ablest diplomat—in his machinations almost the equal of Michael himself—Charles of Anjou, brother of St. Louis of France. At papal invitation, Charles advanced into southern Italy, expelled the last representatives of the imperial house of Hohenstaufen, Manfred and Conradin, and then from Palermo and Naples almost at once fixed his gaze across the Balkans onto Constantinople. To quote a chronicler, 'he aspired to the monarchy of the world, hoping thereby to recreate the great empire of Julius Caesar by joining East and West.'\"\n\n"
    "\"In exchange for the papal promise to restrain Charles from attacking Constantinople, Michael promised to bring about religious union of the Greek church with Rome. That promise provoked the violent opposition of most of Michael’s own people, who opposed union on doctrinal grounds. Specifically, they objected to such parts of the Latin liturgy as the Filioque (statement of belief in the procession of the Holy Spirit from the Son and the Father) and the use of the azyme (unleavened bread). Perhaps more important, most of them refused to accept papal ecclesiastical supremacy, which they felt, however obscurely, would lead to restoration of Latin political domination and possibly even cultural assimilation to the Latins.\"\n\n"
    "\"Despite all the obstacles, union was nevertheless finally pronounced at the Second Council of Lyon in 1274. The Orthodox East was coerced into accepting union. Immediately after Michael’s death (1282), however, the Greek church declared the union invalid. The Greeks objected to the council on the grounds that not all the Eastern patriarchs or their representatives had been present, that no discussion of problems separating the two churches had taken place, and that no subsequent council had declared that of Lyon ecumenical. Nevertheless, for political reasons, Michael had struggled to maintain the union. But, when Charles of Anjou finally managed to enthrone his own candidate, Martin IV, as pope in 1281, Martin at once excommunicated Michael and at the same time pronounced Charles’s projected expedition against Byzantium a 'Holy Crusade' against the 'schismatic' Greeks. Included in the vast network of alliances erected by Charles to conquer the Greek East were not only Sicily, parts of Italy, Greek Lascarid dissidents, various Slavs of the Balkans, Baldwin, France, and Venice but also the papacy. Venice’s aim in particular was to recover the broad trading privileges it had exercised in the days of the Latin empire and to oust its arch foe, the Genoese, from the lucrative Greek markets.\"\n\n"
    "\"The diplomatic duel between Charles and Michael was intensified, with Charles striving unceasingly to prepare his troops and navy. He even launched an attack across the Adriatic on Berat (in modern Albania) under the French general Sully but was repulsed by Michael. What Michael had on his side—the result of his consummate diplomatic ability—was (for a time) the papal alliance, a secret agreement with the Hohenstaufen supporters in Sicily, the support of Genoa, and, most important, a secret alliance with the son-in-law of Manfred, King Peter III of Aragon. The denouement to this remarkable contest was the outbreak on March 30/31, 1282, of the Sicilian Vespers, the massacre of the French signaling the revolt against Charles. Byzantium was saved from a second occupation by the Latins.\"\n\n"
    "\"At his death, which occurred soon afterward, Michael thus left an intact empire to his son Andronicus II. But it cannot be denied that his policy of using ecclesiastical union to stave off Charles’s attack on his capital and the deep opposition that policy provoked among the Byzantine population established a fateful precedent for later Byzantine history. Moreover, by focusing his attention too exclusively on Europe, his policy helped lead to Ottoman occupation of all of Asia Minor and ultimately to the capture of Constantinople itself. Nevertheless, Michael’s positive accomplishments cannot be overlooked. He gave Byzantium two centuries more of life, began rebuilding the capital, and reestablished the University of Constantinople. His sponsorship of a general revival of learning led to the important Byzantine 'Renaissance' in the 14th and 15th centuries.\""
)


constantine_x_bio = (
    "\"Constantine’s accession was a triumph for the civil aristocracy and was unfortunate in that he proved an incapable emperor. "
    "He reduced the army and neglected the frontier defenses at a time when the Seljuq Turks were pressing into the eastern provinces; "
    "consequently, the sultan Alp Arslan overran Armenia (1064–65) and attacked Caesarea (1067). In 1064 the Hungarians occupied Belgrade, "
    "and the Pechenegs (Patzinaks) and Uzes (Kumans) crossed the Danube River and ravaged the Balkan provinces, penetrating into Greece. "
    "In Italy, the Normans were rapidly conquering the last remnants of the Byzantine possessions.\""
)

alexios_i_bio = (
    "\"The third son of John Comnenus and a nephew of Isaac I (emperor 1057–59), Alexius came from a distinguished Byzantine landed family "
    "and was one of the military magnates who had long urged more effective defense measures, particularly against the Turks’ encroaching on "
    "Byzantine provinces in eastern and central Anatolia. From 1068 to 1081 he gave able military service during the short reigns of Romanus IV, "
    "Michael VII, and Nicephorus III. Then, with the support of his brother Isaac and his mother, the formidable Anna Dalassena, and with that "
    "of the powerful Ducas family, to which his wife, Irene, belonged, he seized the Byzantine throne from Nicephorus III.\n\n"
    "Alexius was crowned on April 4, 1081. After more than 50 years of ineffective or short-lived rulers, Alexius, in the words of Anna Comnena, "
    "his daughter and biographer, found the empire 'at its last gasp,' but his military ability and diplomatic gifts enabled him to retrieve the "
    "situation. He drove back the south Italian Normans, headed by Robert Guiscard, who were invading western Greece (1081–82). This victory was "
    "achieved with Venetian naval help, bought at the cost of granting Venice extensive trading privileges in the Byzantine Empire. In 1091 he "
    "defeated the Pechenegs, Turkic nomads who had been continually surging over the Danube River into the Balkans. Alexius halted the further "
    "encroachment of the Seljuq Turks, who had already established the sultanate of Rūm (or Konya) in central Anatolia. He made agreements with "
    "Sulaymān ibn Qutalmïsh of Konya (1081) and subsequently with his son Qïlïch Arslan (1093), as well as with other Muslim rulers on Byzantium’s "
    "eastern border.\n\n"
    "At home, Alexius’s policy of strengthening the central authority and building up professional military and naval forces resulted in increased "
    "Byzantine strength in western and southern Anatolia and eastern Mediterranean waters. But he was unable or unwilling to limit the considerable "
    "powers of the landed magnates who had threatened the unity of the empire in the past. Indeed, he strengthened their position by further concessions, "
    "and he had to reward services, military and otherwise, by granting fiscal rights over specified areas. This method, which was to be increasingly "
    "employed by his successors, inevitably weakened central revenues and imperial authority. He repressed heresy and maintained the traditional imperial "
    "role of protecting the Eastern Orthodox church, but he did not hesitate to seize ecclesiastical treasure when in financial need. He was subsequently "
    "called to account for this by the church.\n\n"
    "To later generations Alexius appeared as the ruler who pulled the empire together at a crucial time, thus enabling it to survive until 1204, and in "
    "part until 1453, but modern scholars tend to regard him, together with his successors John II (reigned 1118–43) and Manuel I (reigned 1143–80), as having "
    "effected only stopgap measures. Judgments of Alexius must be tempered by allowing for the extent to which he was handicapped by the inherited internal "
    "weaknesses of the Byzantine state and, even more, by the series of crises precipitated by the western European Crusaders from 1097 onward. The Crusading "
    "movement, motivated partly by a desire to recapture the holy city of Jerusalem, partly by the hope of acquiring new territory, increasingly encroached on "
    "Byzantine preserves and frustrated Alexius’s foreign policy, which was primarily directed toward the reestablishment of imperial authority in Anatolia. "
    "His relations with Muslim powers were disrupted on occasion, and former valued Byzantine possessions, such as Antioch, passed into the hands of arrogant "
    "Western princelings, who even introduced Latin Christianity in place of Greek. Thus, it was during Alexius’s reign that the last phase of the clash between "
    "the Latin West and the Greek East was inaugurated. He did regain some control over western Anatolia; he also advanced into the southeast Taurus region, "
    "securing much of the fertile coastal plain around Adana and Tarsus, as well as penetrating farther south along the Syrian coast. But neither Alexius nor "
    "succeeding Comnenian emperors were able to establish permanent control over the Latin Crusader principalities. Nor was the Byzantine Empire immune from "
    "further Norman attacks on its western islands and provinces—as in 1107–08, when Alexius successfully repulsed Bohemond I of Antioch’s assault on Avlona in "
    "western Greece. Continual Latin (particularly Norman) attacks, constant thrusts from Muslim principalities, the rising power of Hungary and the Balkan "
    "principalities—all conspired to surround Byzantium with potentially hostile forces. Even Alexius’s diplomacy, whatever its apparent success, could not "
    "avert the continual erosion that ultimately led to the Ottoman conquest.\""
)

john_ii_komnenos_bio = (
    "\"A son of Emperor Alexius I Comnenus and Irene Ducas, John kept an austere court and spent most of his reign with his troops. "
    "He canceled Venetian trading privileges granted by his father but was forced to restore them after the Venetians launched a fleet against him. "
    "He thwarted Pecheneg, Hungarian, and Serbian threats during the 1120s, and in 1130 he allied himself with the German emperor Lothar II (III) against the Norman king Roger II of Sicily.\n\n"
    "In the later part of his reign John focused his activities on the East. In 1135 he defeated the Danishmend emirate of Melitene. "
    "Two years later he reconquered all of Cilicia from the kingdom of Lower Armenia and later forced Raymond of Poitiers, prince of Antioch, to recognize Byzantine suzerainty. "
    "Though John and Raymond formed an alliance against the Turkish Atabegs of Syria, their campaigns were not particularly successful. "
    "In 1143 John returned to press his claims to Antioch. He died following a hunting accident after naming his fourth son, Manuel I, to succeed him.\""
)


madrid_skylitzes_description = (
    "\"The Madrid Skylitzes (Biblioteca Nacional, vitr.26-2) is a twelfth-century illustrated manuscript of John Skylitzes’ historical chronicle, the *Synopsis Historion*. It narrates the history of the Byzantine Empire from 811 to 1057, covering the reigns of emperors from Nikephoros I to Michael VI.\n\n"
    "What makes the Madrid Skylitzes exceptional is that it is the only surviving illustrated manuscript of a Greek chronicle. Containing 574 vivid miniatures, it provides visual insights into nearly every aspect of Byzantine life—naval expeditions, sieges, court rituals, religious ceremonies, dreams, and even rare depictions such as conjoined twins. These images enrich and complicate the relationship between text and image, narrative and illustration.\n\n"
    "Produced in Norman Sicily, the manuscript is a product of cultural confluence. Its Greek text, copied in a Latin and Arabic-speaking context, opens up questions about the manuscript’s intended audience, its function, and the transmission of Byzantine historical memory in the multicultural environment of twelfth-century Sicily.\n\n"
    "The manuscript has become the centerpiece of an international scholarly effort. A multimedia edition is in development, combining critical commentary on text, imagery, captions, and narrative structure. Dr. Bente Bjornholt at the University of Sussex is constructing a detailed image database, categorizing iconographic features, styles, and colors for public access. Meanwhile, the textual commentary is being led by Associate Professor Roger Scott at the University of Melbourne, in collaboration with scholars from Melbourne and Manitoba, ensuring a comprehensive scholarly resource for future study.\""
)



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

    },
        {
            'title': 'Constantine X Doukas',
            'in_greek': 'Κωνσταντῖνος Ι΄ Δούκας',
            'birth': 'c. 1006, Constantinople',
            'death': '23 May 1067, Constantinople',
            'reign': '1059–1067',
            'life': constantine_x_bio,
            'dynasty': 'Doukas',
            'reign_start': 1059,
            'ascent_to_power': 'Appointment',
            'references': 'Encyclopaedia Britannica (n.d.). Constantine X Ducas | Byzantine emperor. [online] Available at: https://www.britannica.com/biography/Constantine-X-Ducas [Accessed 4 Aug. 2025].'
        }
        , {
        'title': 'Alexios I Komnenos',
        'in_greek': 'Ἀλέξιος Αʹ Κομνηνός',
        'birth': 'c. 1057, Constantinople',
        'death': '15 August 1118, Constantinople',
        'reign': '1081–1118',
        'life': alexios_i_bio,
        'dynasty': 'Komnenos',
        'reign_start': 1081,
        'ascent_to_power': 'Coup d\'état',
        'references': 'The Editors of Encyclopædia Britannica (n.d.). Alexius I Comnenus | Byzantine emperor. [online] Available at: https://www.britannica.com/biography/Alexius-I-Comnenus [Accessed 4 Aug. 2025].'
    },
        {
            'title': 'Michael VIII Palaiologus',
            'in_greek': 'Μιχαὴλ ΗʹΠαλαιολόγος',
            'birth': '1224 or 1225, Empire of Nicaea',
            'death': '11 December 1282, Thrace',
            'reign': '1259–1282',
            'life': michael_viii_bio_detailed,
            'dynasty': 'Palaiologos',
            'reign_start': 1259,
            'ascent_to_power': 'Coup d\'état',
            'references': 'The Editors of Encyclopædia Britannica (n.d.). MichaelVIII Palaiologus | Byzantine emperor. [online] Available at: https://www.britannica.com/biography/Michael‑VIII‑Palaeologus [Accessed 4 Aug.2025].'
        },
        {
            'title': 'Isaac II Angelos',
            'in_greek': 'Ἰσαάκιος Βʹ Ἄγγελος',
            'birth': 'September 1156, Constantinople',
            'death': 'January 1204, Constantinople',
            'reign': '1185–1195, 1203–1204',
            'life': isaac_ii_bio_detailed,
            'dynasty': 'Angelos',
            'reign_start': 1185,
            'ascent_to_power': 'Civil War',
            'references': 'Encyclopædia Britannica (n.d.) Isaac II Angelus | Byzantine emperor. Available at: https://www.britannica.com/biography/Isaac-II-Angelus (Accessed: 5 August 2025).'
        },
       {
        'title': 'John II Komnenos',
        'in_greek': 'Ἰωάννης Βʹ Κομνηνός',
        'birth': '13 September 1087, Constantinople',
        'death': '8 April 1143, Cilicia',
        'reign': '1118–1143',
        'life': john_ii_komnenos_bio,
        'dynasty': 'Komnenos',
        'reign_start': 1118,
        'ascent_to_power': 'Hereditary Succession',
    'references': 'The Editors of Encyclopædia Britannica (n.d.) John II Comnenus | Byzantine emperor. Available at: https://www.britannica.com/biography/John-II-Comnenus (Accessed: 5 August 2025).'
    },
        {
        'title': 'Andronikos II Palaiologos',
        'in_greek': 'Ἀνδρόνικος Δούκας Ἄγγελος Κομνηνὸς Παλαιολόγος',
        'birth': '25 March 1259 (Nicaea / Constantinople)',
        'death': '13 February 1332, Constantinople',
        'reign': '1282–1328',
        'life': andronicus_ii_bio,
        'dynasty': 'Palaiologos',
        'reign_start': 1282,
        'ascent_to_power': 'Hereditary Succession',
        'references': 'The Editors of Encyclopædia Britannica (n.d.) Andronikos II Palaiologus | Byzantine emperor. Available at: https://www.britannica.com/biography/Andronicus‑II‑Palaeologus (Accessed: 5 August 2025).'
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
            'filename': 'Constantine X Doukas',
            'url': '/static/images/Constantine_X_full_portrait.jpg',
            'caption': 'Portrait of Constantine X Doukas',
            'emperor_id': 4
        },
        {
            'filename': 'Alexios I Komnenos',
            'url': '/static/images/Alexios_I_Komnenos.jpg',
            'caption': 'Portrait of Alexios I Komnenos',
            'emperor_id': 5
        },
        {
            'filename': 'Michael VIII Palaiologos',
            'url': '/static/images/Miniature_of_Michael_VIII.png',
            'caption': 'Portrait of Michael VIII Palaiologos',
            'emperor_id': 6
        },
        {
            'filename': 'Isaac II Angelos',
            'url': '/static/images/144_-_Isaac_II_Angelos_(Mutinensis_-_color).png',
            'caption': 'Portrait of Isaac II Angelos',
            'emperor_id': 7
        },
        {
            'filename': 'John II Komnenos',
            'url': '/static/images/Jean_II_Comnene.jpg',
            'caption': 'Portrait of John II Komnenos',
            'emperor_id': 8
        },
        {
            'filename': 'Andronikos II',
            'url': '/static/images/Miniature_of_Andronikos_II.png',
            'caption': 'Portrait of Andronikos II',
            'emperor_id': 9
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
        ,
        {
            'filename': 'Madrid Skylitzes',
            'url': '/static/images/culture/manuscript_1.jpg',
            'caption': 'The defeat of George I of Georgia by Basil II',
            'literature_id': 1
        },
        {
            'filename': 'Holy Crown of Hungary',
            'url': '/static/images/culture/Hungarian_Parliament_002_-_Flickr_-_granada_turnier.jpg',
            'caption': 'Holy Crown of Hungary, crafted in Constantinople',
            'artifact_id': 1
        },
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

    literature_items = [
        {
            'title': "Madrid Skylitzes",
            'in_greek': "Σύνοψις Ἱστοριῶν",
            'author': "John Skylitzes",
            'year_completed': '12ths century',
            'current_location': "National Library of Spain, Madrid",
            'genre': "Chronicle",
            'description': madrid_skylitzes_description,
            'references': "Sussex Centre for Byzantine Cultural History. 2025. The Madrid Skylitzes Project. University of Sussex. Available at: https://www.sussex.ac.uk/byzantine/research/skylitzes [Accessed 25 July 2025]."
        }
    ]

    for item in literature_items:
        entry = Literature(**item)
        db.session.add(entry)





    artifact_items = [
        {
            'title': "Holy Crown of Hungary",
            'in_greek': "Szent Korona",
            'year_completed': '1070s',
            'current_location': "Hungarian Parliament, Budapest",
            'description': saint_stephens_crown_description,
            'references': "Encyclopaedia Britannica. (n.d.). Saint Stephen’s Crown. [online] Available at: https://www.britannica.com/topic/Saint-Stephens-Crown [Accessed 31 Jul. 2025]."
        }
    ]

    for item in artifact_items:
        entry = Artifact(**item)
        db.session.add(entry)

    db.session.commit()
