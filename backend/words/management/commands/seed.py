from django.core.management.base import BaseCommand
from words.models import Word, Paragraph

PARAGRAPHS = [
    (
        "forests",
        "Forests cover about one-third of the Earth's land surface and are home to more than "
        "half of the world's terrestrial species. They regulate the climate by absorbing carbon "
        "dioxide and releasing oxygen through the process of photosynthesis. The canopy layer, "
        "formed by the tallest trees, filters sunlight and creates a humid microclimate beneath "
        "it. Fallen leaves and decaying matter enrich the soil, sustaining a complex web of "
        "organisms from fungi to insects.",
    ),
    (
        "solar system",
        "The solar system consists of the Sun and the eight planets that orbit around it, along "
        "with moons, asteroids, and comets. Gravity is the invisible force that keeps every "
        "planet locked in its elliptical path around the Sun. The inner planets — Mercury, "
        "Venus, Earth, and Mars — are rocky and dense, while the outer planets are massive gas "
        "giants. Scientists continue to explore the outer edges of the solar system, where the "
        "Voyager probes have now traveled beyond the heliopause.",
    ),
]

WORDS = [
    # --- Paragraph 1: Forests & Ecosystems ---
    (
        "forests",
        "Large areas of land covered densely with trees and undergrowth.",
        "Forests are home to countless species of animals and plants.",
    ),
    (
        "cover",
        "To extend over or spread across a surface or area.",
        "Dark clouds began to cover the sky before the storm.",
    ),
    (
        "about",
        "Approximately; used to express an estimate or rough figure.",
        "The hike takes about three hours to complete.",
    ),
    (
        "one",
        "The number 1; a single unit or entity.",
        "One tree can absorb several kilograms of carbon dioxide per year.",
    ),
    (
        "third",
        "Constituting number three in a sequence; one of three equal parts.",
        "A third of the planet's fresh water is locked in glaciers.",
    ),
    (
        "earth",
        "The planet on which we live; the world.",
        "Earth is the only known planet to support life.",
    ),
    (
        "land",
        "The solid part of the Earth's surface as distinct from sea or water.",
        "Fertile land is essential for growing crops.",
    ),
    (
        "surface",
        "The outermost or uppermost layer of something.",
        "The surface of Mars is covered in iron oxide dust.",
    ),
    (
        "are",
        "Second person singular present and first, second, third person plural of 'be'.",
        "These plants are native to tropical regions.",
    ),
    (
        "home",
        "The natural environment or habitat of an animal or plant.",
        "The rainforest is home to millions of species.",
    ),
    (
        "more",
        "A greater or additional amount or degree.",
        "More research is needed to understand deep-sea ecosystems.",
    ),
    (
        "than",
        "Used to introduce the second element in a comparison.",
        "The Amazon is larger than any other rainforest on Earth.",
    ),
    (
        "half",
        "One of two equal or corresponding parts into which something is divided.",
        "Half of all known species live in tropical forests.",
    ),
    (
        "world",
        "The Earth together with all its countries and peoples.",
        "The world depends on forests for clean air and water.",
    ),
    (
        "terrestrial",
        "Of, on, or relating to the Earth or dry land (as opposed to water or air).",
        "Terrestrial ecosystems include forests, grasslands, and deserts.",
    ),
    (
        "species",
        "A group of living organisms that share common characteristics and can interbreed.",
        "Many species of birds migrate thousands of miles each year.",
    ),
    (
        "they",
        "Used to refer to two or more people or things previously mentioned.",
        "They found new species in the unexplored jungle.",
    ),
    (
        "regulate",
        "To control or maintain something at a desired level.",
        "The liver helps regulate the body's chemical balance.",
    ),
    (
        "climate",
        "The long-term pattern of weather in a particular area.",
        "A changing climate threatens many ecosystems around the world.",
    ),
    (
        "by",
        "Through the means or agency of; performed by.",
        "The river was crossed by a narrow wooden bridge.",
    ),
    (
        "absorbing",
        "Taking in or soaking up energy, liquid, or another substance.",
        "The sponge is absorbing all the water from the spill.",
    ),
    (
        "carbon",
        "A chemical element found in all living organisms, symbol C.",
        "Carbon is the backbone of all organic molecules.",
    ),
    (
        "dioxide",
        "A compound consisting of two oxygen atoms bonded to one other atom.",
        "Carbon dioxide is a greenhouse gas released by burning fossil fuels.",
    ),
    (
        "releasing",
        "Allowing a substance or energy to escape or be emitted.",
        "The volcano was releasing large amounts of sulfur dioxide.",
    ),
    (
        "oxygen",
        "A colorless, odorless gas that most living organisms need to breathe.",
        "Oxygen makes up about 21 percent of the Earth's atmosphere.",
    ),
    (
        "through",
        "Moving in one side and out of the other side of an opening.",
        "Light passed through the glass and formed a rainbow on the wall.",
    ),
    (
        "process",
        "A series of actions or steps taken to achieve a result.",
        "Digestion is a complex process involving many organs.",
    ),
    (
        "photosynthesis",
        "The process by which green plants use sunlight to convert carbon dioxide and water into food.",
        "Photosynthesis is the foundation of almost all food chains on Earth.",
    ),
    (
        "canopy",
        "The uppermost layer of a forest, formed by the crowns of the tallest trees.",
        "Many birds spend their entire lives in the forest canopy.",
    ),
    (
        "layer",
        "A sheet, coating, or thickness of material covering a surface.",
        "A layer of ice covers the lake every winter.",
    ),
    (
        "formed",
        "Brought into existence or given shape.",
        "The mountains were formed by tectonic activity millions of years ago.",
    ),
    (
        "tallest",
        "Of the greatest height; superlative of tall.",
        "The tallest tree ever recorded was a coastal redwood in California.",
    ),
    (
        "trees",
        "Tall plants with a wooden trunk, branches, and leaves.",
        "Trees provide shade, shelter, and food for many animals.",
    ),
    (
        "filters",
        "Passes a substance through a device to remove unwanted material.",
        "The kidneys filter waste products from the blood.",
    ),
    (
        "sunlight",
        "Light from the Sun that reaches the Earth's surface.",
        "Sunlight is essential for vitamin D production in the human body.",
    ),
    (
        "creates",
        "Brings something into existence.",
        "Evaporation creates clouds that eventually release rain.",
    ),
    (
        "humid",
        "Marked by a relatively high level of water vapor in the air.",
        "The jungle was humid and warm throughout the year.",
    ),
    (
        "microclimate",
        "The climate of a very small or restricted area, differing from the surrounding climate.",
        "A dense hedge can create a sheltered microclimate in a garden.",
    ),
    (
        "beneath",
        "Extending or directly below something.",
        "The river flowed quietly beneath the old stone bridge.",
    ),
    (
        "fallen",
        "Having dropped or come down from a higher position.",
        "Fallen branches covered the path after the storm.",
    ),
    (
        "leaves",
        "The flat, typically green parts of a plant that grow from a stem or branch.",
        "In autumn, leaves change color before falling to the ground.",
    ),
    (
        "decaying",
        "Rotting or decomposing through biological processes.",
        "Decaying wood provides nutrients and shelter for many insects.",
    ),
    (
        "matter",
        "Physical substance that occupies space and has mass.",
        "All matter is made up of atoms.",
    ),
    (
        "enrich",
        "To improve the quality or value of something by adding something beneficial.",
        "Compost can enrich poor soil and help plants grow.",
    ),
    (
        "soil",
        "The upper layer of earth in which plants grow.",
        "Rich soil contains minerals, water, air, and organic material.",
    ),
    (
        "sustaining",
        "Keeping something going over time; providing nourishment.",
        "The river is sustaining the wildlife in the surrounding area.",
    ),
    (
        "complex",
        "Consisting of many different and connected parts; not simple.",
        "The human brain is an incredibly complex organ.",
    ),
    (
        "web",
        "A network of fine threads or interconnected elements.",
        "A spider's web can be stronger than steel of the same thickness.",
    ),
    (
        "organisms",
        "Individual living things, such as animals, plants, or bacteria.",
        "Microorganisms in the soil help break down dead matter.",
    ),
    (
        "fungi",
        "A kingdom of organisms that includes mushrooms, molds, and yeasts.",
        "Fungi play a critical role in decomposing organic material.",
    ),
    (
        "insects",
        "Small invertebrate animals with six legs and typically one or two pairs of wings.",
        "Insects are the most diverse group of animals on Earth.",
    ),
    # --- Paragraph 2: The Solar System ---
    (
        "solar",
        "Of or relating to the Sun.",
        "Solar energy is a clean and renewable source of power.",
    ),
    (
        "system",
        "A set of connected things or parts forming a complex whole.",
        "The immune system defends the body against infection.",
    ),
    (
        "consists",
        "Is composed or made up of.",
        "Water consists of hydrogen and oxygen atoms.",
    ),
    (
        "sun",
        "The star at the center of our solar system.",
        "The Sun provides the energy that drives Earth's weather and climate.",
    ),
    (
        "eight",
        "The number 8; one more than seven.",
        "There are eight planets in our solar system.",
    ),
    (
        "planets",
        "Large celestial bodies that orbit a star.",
        "The planets in our solar system vary greatly in size and composition.",
    ),
    (
        "orbit",
        "To move in a curved path around a star, planet, or moon.",
        "The Moon takes about 27 days to orbit the Earth.",
    ),
    (
        "around",
        "Located or situated on every side of something.",
        "The children gathered around the campfire to stay warm.",
    ),
    (
        "along",
        "Moving or extending parallel to something else.",
        "We walked along the riverbank until we reached the bridge.",
    ),
    (
        "with",
        "Accompanied by or in the company of.",
        "She went to the market with her younger brother.",
    ),
    (
        "moons",
        "Natural satellites that orbit a planet.",
        "Jupiter has dozens of moons, some larger than Mercury.",
    ),
    (
        "asteroids",
        "Small rocky bodies orbiting the Sun, mainly between Mars and Jupiter.",
        "Asteroids are remnants from the early formation of the solar system.",
    ),
    (
        "comets",
        "Icy bodies that release gas or dust as they travel near the Sun.",
        "Comets develop bright tails when they pass close to the Sun.",
    ),
    (
        "gravity",
        "The natural force that attracts objects with mass toward one another.",
        "Gravity keeps the Moon in orbit around the Earth.",
    ),
    (
        "invisible",
        "Unable to be seen; not visible to the naked eye.",
        "Radio waves are invisible but carry signals across vast distances.",
    ),
    (
        "force",
        "A push or pull that changes the motion or shape of an object.",
        "The force of the wind knocked down several trees during the storm.",
    ),
    (
        "keeps",
        "Causes something to remain in a specified state or position.",
        "A thermostat keeps the room temperature constant.",
    ),
    (
        "every",
        "Each individual or item in a group without exception.",
        "Every cell in the human body contains DNA.",
    ),
    (
        "planet",
        "A large, rounded celestial body orbiting a star.",
        "Saturn is the only planet with rings visible from Earth with binoculars.",
    ),
    (
        "locked",
        "Fixed or secured so as to prevent movement.",
        "The gears were locked in place, preventing the machine from running.",
    ),
    (
        "its",
        "Belonging to or associated with a thing previously mentioned.",
        "The tree shed its leaves as winter approached.",
    ),
    (
        "elliptical",
        "Having the shape of an ellipse; oval.",
        "Planets travel in elliptical orbits rather than perfect circles.",
    ),
    (
        "path",
        "A route or course taken to reach a destination.",
        "The spacecraft followed a precise path toward the distant planet.",
    ),
    (
        "inner",
        "Situated inside or further toward the center.",
        "The inner layers of the Earth are extremely hot.",
    ),
    (
        "mercury",
        "The smallest planet in the solar system and closest to the Sun.",
        "Mercury has no atmosphere to protect it from temperature extremes.",
    ),
    (
        "venus",
        "The second planet from the Sun, known for its thick atmosphere and extreme heat.",
        "Venus is the hottest planet in the solar system despite not being the closest to the Sun.",
    ),
    (
        "mars",
        "The fourth planet from the Sun, known as the Red Planet.",
        "Mars has the tallest volcano in the solar system, Olympus Mons.",
    ),
    (
        "rocky",
        "Consisting of or full of rock; resembling rock in hardness.",
        "The rocky coastline made it difficult to land a boat.",
    ),
    (
        "dense",
        "Having a high density; closely compacted in substance.",
        "Lead is a very dense metal that sinks quickly in water.",
    ),
    (
        "while",
        "During the time that; at the same time as.",
        "While some animals hibernate in winter, others migrate south.",
    ),
    (
        "outer",
        "Situated further from the center or inside.",
        "The outer planets of the solar system are composed mostly of gas.",
    ),
    (
        "massive",
        "Large and heavy; of great size and weight.",
        "A massive asteroid struck Earth 66 million years ago.",
    ),
    (
        "gas",
        "A substance in a state in which it expands to fill the container it is in.",
        "Hydrogen is the lightest gas known to exist.",
    ),
    (
        "giants",
        "Things that are very large in size or importance.",
        "The gas giants in our solar system have no solid surface.",
    ),
    (
        "scientists",
        "People who study or have expert knowledge in a natural or physical science.",
        "Scientists use telescopes to observe distant galaxies.",
    ),
    (
        "continue",
        "To persist in doing something without stopping.",
        "Researchers continue to search for signs of life on Mars.",
    ),
    (
        "explore",
        "To travel through an unfamiliar area in order to learn about it.",
        "Rovers explore the Martian surface collecting data and samples.",
    ),
    (
        "edges",
        "The outermost parts or limits of an area.",
        "At the edges of the solar system, the Sun appears as a bright star.",
    ),
    (
        "where",
        "In, at, or to which place or position.",
        "Scientists study the areas where rivers meet the ocean.",
    ),
    (
        "voyager",
        "A long journey, especially by sea or in space.",
        "The Voyager probes were launched in 1977 and are still sending data.",
    ),
    (
        "probes",
        "Unmanned spacecraft used to explore space and transmit data.",
        "Space probes have visited every planet in the solar system.",
    ),
    (
        "have",
        "Used with a past participle to form perfect tenses.",
        "Scientists have discovered thousands of exoplanets in recent years.",
    ),
    (
        "now",
        "At the present time or moment.",
        "The rover is now transmitting images from the surface of Mars.",
    ),
    (
        "traveled",
        "Journeyed from one place to another, often over a long distance.",
        "The probe has traveled billions of kilometers since its launch.",
    ),
    (
        "beyond",
        "At or to a greater distance than something.",
        "Little is known about what lies beyond the edge of the observable universe.",
    ),
    (
        "heliopause",
        "The boundary of the heliosphere, where the solar wind meets interstellar space.",
        "Voyager 1 crossed the heliopause in 2012, entering interstellar space.",
    ),
]


class Command(BaseCommand):
    help = "Seeds the database with sample paragraphs and words."

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding paragraphs...")
        for label, text in PARAGRAPHS:
            _, created = Paragraph.objects.get_or_create(text=text)
            if created:
                self.stdout.write(f"  Created paragraph: {label}")
            else:
                self.stdout.write(f"  Skipped (exists): {label}")

        self.stdout.write("\nSeeding words...")
        for text, definition, example in WORDS:
            _, created = Word.objects.get_or_create(
                text=text,
                defaults={"definition": definition, "example": example},
            )
            if created:
                self.stdout.write(f"  Created word: {text}")
            else:
                self.stdout.write(f"  Skipped (exists): {text}")

        self.stdout.write(self.style.SUCCESS("\nDone. Database seeded successfully."))
