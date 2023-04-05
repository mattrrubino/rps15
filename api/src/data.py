MOVES = [
    "rock", "fire", "scissors", "snake", "human",
    "tree", "wolf", "sponge", "paper", "air", "water",
    "dragon", "devil", "lightning", "gun",
]

VERBS = {
    "rock": {"fire": "pounds out", "tree": "blocks growth of", "default": "crushes"},
    "fire": {"scissors": "melts", "default": "burns"},
    "scissors": {"air": "swish through", "tree": "carve", "default": "cut"},
    "snake": {"human": "bites", "wolf": "bites", "sponge": "swallows", "tree": "nests in", "paper": "nests in", "air": "breathes", "water": "drinks"},
    "human": {"tree": "plants", "wolf": "tames", "sponge": "cleans with", "paper": "writes", "air": "breathes", "water": "drinks", "dragon": "slays"},
    "tree": {"sponge": "outlives", "paper": "becomes", "air": "produces", "water": "drinks", "devil": "imprisons", "default": "shelters"},
    "wolf": {"air": "breathes", "water": "drinks", "dragon": "outruns", "lightning": "outruns", "devil": "bites", "default": "chews up"},
    "sponge": {"paper": "soaks", "air": "uses", "water": "absorbs", "gun": "cleans", "lightning": "conducts", "default": "cleanses"},
    "paper": {"air": "fans", "rock": "covers", "water": "floats on", "gun": "outlaws", "lightning": "defines", "default": "rebukes"},
    "air": {"fire": "blows out", "rock": "erodes", "water": "evaporates", "devil": "chokes", "gun": "tarnishes", "dragon": "freezes", "lightning": "creates"},
    "water": {"rock": "erodes", "fire": "puts out", "scissors": "rusts", "gun": "rusts", "lightning": "conducts", "default": "drowns"},
    "dragon": {"devil": "commands", "lightning": "breathes", "fire": "breathes", "rock": "rests on", "snake": "spawns", "default": "is immune to"},
    "devil": {"rock": "hurls", "fire": "breathes", "lightning": "casts", "snakes": "eats", "human": "possesses", "default": "is immune to"},
    "lightning": {"gun": "melts", "scissors": "melts", "rock": "splits", "tree": "splits", "fire": "starts", "defautl": "strikes"},
    "gun": {"rock": "targets", "tree": "targets", "fire": "targets", "scissors": "outclasses", "default": "shoots"},
}
