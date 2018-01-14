from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CategoryItem

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Category 1
category1 = Category(name="Science Fiction")
session.add(category1)
session.commit()

categoryItem1 = CategoryItem(
    name="Foundation and Empire",
    description="Foundation and Empire is the story of first contact"
                "between the two Foundations of Hari Seldon by Isaac Asimov",
    category=category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(
    name="Valis",
    description="Part science fiction, part theological detective story in"
                "which God plays both the missing person and the perpetrator "
                "of the ultimate crime by Philip K Dick",
    category=category1)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(
    name="The Man in the High Castle",
    description="This is an alternate history of America. The Nazis and "
                "Japanese won World War Two and America is split between"
                " the two powers by Philip Dick",
    category=category1)
session.add(categoryItem3)
session.commit()


# Category 2
category1 = Category(name="Classics")
session.add(category1)
session.commit()

categoryItem1 = CategoryItem(
    name="1984",
    description="Totalitarian world which demands absolute obedience and"
                " controls people through the all-seeing telescreens and the"
                " watchful eye of Big Brother by George Orwell",
    category=category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(
    name="A Christmas Carol",
    description="Tells the story of Ebenezer Scrooge, an old miser who is "
                "visited by the ghost of his former business partner Jacob "
                "Marley and the Ghosts of Christmas Past by Charles Dickens",
    category=category1)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(
    name="Lord of the Flies",
    description="A plane crashes on an uninhabited island and the only "
                "survivors, a group of schoolboys",
    category=category1)
session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(
    name="The Trouble with Goats and Sheep",
    description="Part whodunnit, part coming of age, this is a gripping "
                "debut about the secrets behind every door",
    category=category1)
session.add(categoryItem4)
session.commit()


# Category 3
category1 = Category(name="Historical")
session.add(category1)
session.commit()

categoryItem1 = CategoryItem(
    name="Fools and Mortals",
    description="Shakespeare dreams of a glittering career in one of the "
                "London playhouses, a world dominated by his older brother,"
                " William by Bernard Cornwell",
    category=category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(
    name="Daughters of the Night Sky",
    description="Russia, 1941. Katya Ivanova is a young pilot in a far-flung"
                " military academy in the Ural Mountains by Aimie K. Runyan",
    category=category1)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(
    name="The Last Tudor",
    description="Jane Grey was queen of England for nine days. Popular"
                " historical fiction at its finest, immaculately researched"
                " and superbly told by Philippa Gregory",
    category=category1)
session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(
    name="The Tiger's Prey",
    description="The Malabar coast is full of dangers: greedy tradesmen,"
                " fearless pirates, and men full of vengeance. But for a "
                "Courtney, the greatest danger might just be his own family "
                "by Wilbur Smith",
    category=category1)
session.add(categoryItem4)
session.commit()

categoryItem5 = CategoryItem(
    name="Orphan Girl",
    description="Lorinda is only a child when tragedy deprives her of her "
                "true family and, sent to live with her aunt in her boarding "
                "house, she grows up desperately craving affection by "
                "Maggie Hope",
    category=category1)
session.add(categoryItem5)
session.commit()


# Category 4
category1 = Category(name="Horror")
session.add(category1)
session.commit()

categoryItem1 = CategoryItem(
    name="Necronomicon: The Best Weird Tales of H.P. Lovecraft",
    description="H.P. Lovecraft's tales of the tentacled Elder God Cthulhu"
                " and his pantheon of alien deities ",
    category=category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(
    name="The Outsider",
    description="When an eleven-year-old boy is found murdered, forensic "
                "evidence and reliable eyewitnesses undeniably point to the "
                "town's popular Little League coach by Stephen King",
    category=category1)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(
    name="Sleeping Beauties",
    description="All around the world, something is happening to women when"
                " they fall asleep; they become shrouded in a cocoon-like "
                "gauze by Stephen King",
    category=category1)
session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(
    name="Dr Jekyll and Mr Hyde",
    description="In seeking to discover his inner self, the brilliant Dr "
                "Jekyll discovers a monster by Robert Louis Stevenson",
    category=category1)
session.add(categoryItem4)
session.commit()

categoryItem5 = CategoryItem(
    name="The Night Circus",
    description="The circus arrives without warning. No announcements precede"
                " it. It is simply there, when yesterday it was not by "
                "Erin Morgenstern",
    category=category1)
session.add(categoryItem5)
session.commit()

categoryItem6 = CategoryItem(
    name="The Daylight War",
    description="The DAYLIGHT WAR is book three of the Demon Cycle, pulling "
                "the reader into a world of demons, darkness and heroes"
                " by Peter V. Brett",
    category=category1)
session.add(categoryItem6)
session.commit()

# Category 5
category1 = Category(name="Psychology")
session.add(category1)
session.commit()

categoryItem1 = CategoryItem(
    name="The Dalai Lama's Cat",
    description="Dalai Lama's cat discovers how instead of trying to change "
                "the world, changing the way we experience the world is the"
                " key to true contentment by David Michie",
    category=category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(
    name="The Unconsoled",
    description="Ishiguro's extraordinary and original study of a man whose "
                "life has accelerated beyond his control was met on "
                "publication by consternation, vilification - and the highest"
                " praise by Kazuo Ishiguro",
    category=category1)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(
    name="The Red Book: Liber Novus",
    description="The Red Book, much like the handcrafted -Books of Hours- "
                "from the Middle Ages, is unique. Both in terms of its place"
                " in Jung's development and as a work of art, its publication"
                " is a landmark by C. G. Jung ",
    category=category1)
session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(
    name="Psychology",
    description="Now in its fifth edition, the ever popular Psychology is a"
                " comprehensive and lively introduction to the fascinating "
                "study of the subject by G Neil Martin",
    category=category1)
session.add(categoryItem4)
session.commit()

categoryItem5 = CategoryItem(
    name="Dream Psychology: Psychoanalysis for Beginners",
    description="Sigmund Freud's classic book for non-professionals describing"
                " the psychoanalysis of dreams and exploring the meaning of "
                "dreams by Sigmund Freud's",
    category=category1)
session.add(categoryItem5)
session.commit()

categoryItem6 = CategoryItem(
    name="The Power Of Your Subconscious Mind",
    description="This book will give you the key to the most awesome power "
                "within your reach by Joseph Murphy",
    category=category1)
session.add(categoryItem6)
session.commit()

categoryItem7 = CategoryItem(
    name="The Critique of Pure Reason",
    description="The Critique of Pure Reason, published by Immanuel Kant in "
                "1781, is one of the most complex structures and the most "
                "significant of modern philosophy by Immanuel Kant",
    category=category1)
session.add(categoryItem7)
session.commit()


# Category 6
category1 = Category(name="Religion")
session.add(category1)
session.commit()

categoryItem1 = CategoryItem(
    name="A Monk's Guide to a Clean House and Mind",
    description="In this Japanese bestseller a Buddhist monk explains the "
                "traditional meditative techniques that will help cleanse"
                " not only your house - but your soul by Shoukei Matsumoto",
    category=category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(
    name="The Book of Joy",
    description="Dalai Lama and Archbishop Desmond Tutu, share their wisdom "
                "in this uplifting book",
    category=category1)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(
    name="Unshakeable",
    description="In this daily devotional Christine Caine encourages you to "
                "find confidence to live as the person God created you to be "
                "by Christine Caine ",
    category=category1)
session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(
    name="A History of Judaism",
    description="Judaism is by some distance the oldest of the three Abrahamic"
                " religions by Martin Goodman",
    category=category1)
session.add(categoryItem4)
session.commit()


# Category 7
category1 = Category(name="Scientific")
session.add(category1)
session.commit()

categoryItem1 = CategoryItem(
    name="Astrophysics for People in a Hurry",
    description="Tyson has told the story of our Universe magnificently in"
                " these 12 short chapters",
    category=category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(
    name="A Brief History Of Time: From Big Bang To Black Holes",
    description="Was there a beginning of time? Could time run backwards?"
                " Is the universe infinite or does it have boundaries? ",
    category=category1)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(
    name="Relativity: The Special and the General Theory",
    description="2010 Reprint of 1920 First English Edition.",
    category=category1)
session.add(categoryItem3)
session.commit()


# Category 8
category1 = Category(name="Biography")
session.add(category1)
session.commit()

categoryItem1 = CategoryItem(
    name="My Inventions: and Other Writings",
    description="The Croatian-American inventor recounts the story of his "
                "life, from his schooling and work in Europe to his "
                "collaboration with Thomas Edison, discovery of the rotary "
                "magnetic field, and development of the alternating-current "
                "induction motor by Nicola Tesla",
    category=category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(
    name="Leonardo Da Vinci",
    description="Infinitely curious, easily distracted, vain and vegetarian, "
    "Leonardo is brought to vivid life in this accomplished biography",
    category=category1)
session.add(categoryItem2)
session.commit()


print "added menu items!"
