import pygame
import sys
import json
import os
import random

pygame.init()

WIDTH, HEIGHT = 960, 640
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Campus Life RPG")
CLOCK = pygame.time.Clock()

SAVE_FILE = "campus_life_save.json"
TILE = 32
WORLD_W, WORLD_H = 90, 70

SKY = (152, 214, 255)
GRASS_A = (99, 178, 78)
GRASS_B = (90, 167, 70)
PATH_A = (188, 140, 88)
PATH_B = (173, 128, 78)
WATER_A = (81, 131, 221)
WATER_B = (66, 109, 196)
FENCE = (126, 88, 53)
TRUNK = (117, 83, 55)
LEAF_A = (56, 132, 62)
LEAF_B = (38, 97, 44)
WALL = (224, 210, 181)
WINDOW = (193, 229, 255)
HOME_ROOF = (63, 150, 135)
SCHOOL_ROOF = (180, 79, 79)
WORK_ROOF = (104, 95, 153)
CAFE_ROOF = (212, 141, 70)
LIB_ROOF = (110, 120, 140)
BLACK = (22, 24, 28)
WHITE = (245, 245, 240)
PANEL = (241, 228, 196)
PANEL_D = (210, 196, 160)
RED = (215, 86, 86)
GREEN = (76, 174, 92)
YELLOW = (235, 194, 72)
BLUE = (79, 128, 214)
PURPLE = (157, 111, 220)

HAIR = (76, 50, 24)
SKIN = (234, 214, 170)
SHIRT = (58, 124, 222)
PANTS = (62, 77, 115)

FONT = pygame.font.SysFont("consolas", 18)
BIG = pygame.font.SysFont("consolas", 28, bold=True)
SMALL = pygame.font.SysFont("consolas", 14)

EXAM_BANK = {
    "Math": [
        ("Derivative of x^2 ?", ["2x", "x", "x^2"], 0),
        ("2x + 8 = 12, x = ?", ["1", "2", "3"], 1),
        ("Integral of 1 dx ?", ["1", "x", "x^2"], 1),
        ("sin 90° = ?", ["0", "1", "-1"], 1),
        ("5! = ?", ["120", "60", "20"], 0),
        ("3^2 = ?", ["6", "9", "12"], 1),
    ],
    "Physics": [
        ("Unit of force?", ["Newton", "Joule", "Volt"], 0),
        ("Gravity on Earth ≈ ?", ["9.8 m/s²", "1 m/s²", "98 m/s²"], 0),
        ("Speed = distance / ?", ["time", "mass", "power"], 0),
        ("Light is fastest in?", ["glass", "water", "vacuum"], 2),
        ("Kinetic energy depends on speed?", ["Yes", "No", "Never"], 0),
        ("Current unit?", ["Ampere", "Watt", "Pascal"], 0),
    ],
    "English": [
        ("She ___ to class every day.", ["go", "goes", "going"], 1),
        ("Past tense of write?", ["writed", "written", "wrote"], 2),
        ("Synonym of easy?", ["simple", "angry", "late"], 0),
        ("Correct article: ___ hour", ["a", "an", "the"], 1),
        ("Plural of analysis?", ["analysises", "analyses", "analysises"], 1),
        ("Opposite of early?", ["late", "fast", "bright"], 0),
    ],
}

QUESTS = [
    {"title": "First Day", "desc": "Go to School and take your first exam.", "type": "exam", "target": 1},
    {"title": "Need Cash", "desc": "Work once to earn some money.", "type": "work", "target": 1},
    {"title": "Recharge", "desc": "Sleep at Home once.", "type": "home", "target": 1},
    {"title": "Campus Social", "desc": "Talk to 3 NPCs.", "type": "talk", "target": 3},
    {"title": "Smart Student", "desc": "Reach 60 Intelligence.", "type": "intel", "target": 60},
]

NPC_DIALOGUES = {
    "Ebrar": [
        [("Ebrar", "Deadlines this week look illegal."), ("Renas", "I just want to survive."), ("Ebrar", "Let's hit the library."), ("Renas", "Only after coffee.")],
        [("Ebrar", "How many tabs do you have open?"), ("Renas", "Too many."), ("Ebrar", "That's not studying."), ("Renas", "It's academic atmosphere.")],
        [("Ebrar", "If the UI looks clean, the project looks smarter."), ("Renas", "So design is academic magic?"), ("Ebrar", "Exactly."), ("Renas", "Love that.")],
    ],
    "Ilayda": [
        [("Ilayda", "Math felt easy today."), ("Renas", "That means the exam will be evil."), ("Ilayda", "Probably."), ("Renas", "Classic university move.")],
        [("Ilayda", "Physics is fine until the numbers show up."), ("Renas", "That's when my soul leaves."), ("Ilayda", "Very relatable."), ("Renas", "Deeply tragic.")],
        [("Ilayda", "We should add more features before the presentation."), ("Renas", "As long as they don't create ten bugs."), ("Ilayda", "No promises."), ("Renas", "Terrifying.")],
    ],
    "Barista": [
        [("Barista", "You look like you need caffeine and emotional support."), ("Renas", "One coffee, one miracle please."), ("Barista", "Coffee yes, miracle maybe.")],
        [("Barista", "Midterm week turns everyone into zombies."), ("Renas", "That explains the campus vibe."), ("Barista", "Coffee is carrying this university.")],
        [("Barista", "Students always say 'just one more semester'."), ("Renas", "That sentence is my whole degree."), ("Barista", "Respectfully terrifying.")],
    ],
    "Mert": [
        [("Mert", "I opened the slides and immediately got sleepy."), ("Renas", "That's an academic side effect."), ("Mert", "So it's not my fault?"), ("Renas", "You're a victim.")],
        [("Mert", "I said I'd start early this semester."), ("Renas", "And?"), ("Mert", "Then I kept being myself."), ("Renas", "A tragic character arc.")],
        [("Mert", "Group projects are trust issues with deadlines."), ("Renas", "That is painfully correct."), ("Mert", "I'm basically a philosopher."), ("Renas", "No, just sleep deprived.")],
    ],
}
NPC_INDEX = {"Ebrar": 0, "Ilayda": 0, "Barista": 0, "Mert": 0}


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def draw_text(surf, text, font, color, x, y, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surf.blit(img, rect)


def box(surf, rect, fill, border=BLACK, bw=3):
    pygame.draw.rect(surf, fill, rect)
    pygame.draw.rect(surf, border, rect, bw)


class DialogueBox:
    def __init__(self):
        self.text = "Move with WASD or arrows. Press E to interact."
        self.timer = 300

    def set(self, text, timer=260):
        self.text = text
        self.timer = timer

    def update(self):
        if self.timer > 0:
            self.timer -= 1

    def draw(self, surf):
        rect = pygame.Rect(12, HEIGHT - 96, WIDTH - 24, 84)
        box(surf, rect, PANEL)
        draw_text(surf, self.text, FONT, BLACK, rect.x + 16, rect.y + 16)
        draw_text(surf, "E interact | ENTER dialogue | F5 save | F9 load | TAB quests | Q relationships | G gift", SMALL, BLACK, rect.x + 16, rect.y + 50)


class StoryUI:
    def __init__(self):
        self.active = False
        self.lines = []
        self.i = 0

    def start(self, lines):
        self.lines = lines
        self.i = 0
        self.active = True

    def next(self):
        self.i += 1
        if self.i >= len(self.lines):
            self.active = False

    def current(self):
        if not self.active or not self.lines:
            return None
        return self.lines[self.i]

    def draw_face(self, surf, x, y, shirt_color, name):
        frame = pygame.Rect(x, y, 116, 116)
        box(surf, frame, PANEL_D)
        inner = pygame.Rect(x + 10, y + 10, 96, 96)
        box(surf, inner, PANEL)
        pygame.draw.rect(surf, shirt_color, (x + 34, y + 74, 48, 22))
        pygame.draw.rect(surf, SKIN, (x + 38, y + 26, 40, 36))
        pygame.draw.rect(surf, HAIR, (x + 34, y + 20, 48, 14))
        pygame.draw.rect(surf, HAIR, (x + 34, y + 30, 8, 12))
        pygame.draw.rect(surf, HAIR, (x + 74, y + 30, 8, 12))
        pygame.draw.rect(surf, BLACK, (x + 50, y + 40, 4, 4))
        pygame.draw.rect(surf, BLACK, (x + 64, y + 40, 4, 4))
        pygame.draw.rect(surf, (180, 120, 120), (x + 55, y + 53, 8, 3))
        draw_text(surf, name, SMALL, BLACK, x + 58, y + 101, center=True)

    def draw(self, surf):
        if not self.active:
            return

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surf.blit(overlay, (0, 0))

        panel = pygame.Rect(34, HEIGHT - 228, WIDTH - 68, 188)
        box(surf, panel, PANEL)

        speaker, text = self.current()
        colors = {
            "Ebrar": (212, 122, 168),
            "Ilayda": (145, 112, 228),
            "Barista": (198, 143, 82),
            "Mert": (92, 180, 130),
            "Renas": SHIRT,
        }

        if speaker == "Renas":
            self.draw_face(surf, panel.right - 138, panel.y + 24, SHIRT, "Renas")
        else:
            self.draw_face(surf, panel.x + 20, panel.y + 24, colors.get(speaker, SHIRT), speaker)
            self.draw_face(surf, panel.right - 138, panel.y + 24, SHIRT, "Renas")

        name_box = pygame.Rect(panel.x + 152, panel.y + 20, 170, 34)
        box(surf, name_box, PANEL_D)
        draw_text(surf, speaker, FONT, BLACK, name_box.centerx, name_box.centery, center=True)

        words = text.split()
        lines = []
        current = ""
        max_width = panel.w - 330
        for word in words:
            trial = current + (" " if current else "") + word
            if FONT.size(trial)[0] <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)

        for idx, line in enumerate(lines[:3]):
            draw_text(surf, line, FONT, BLACK, panel.x + 152, panel.y + 78 + idx * 28)

        hint = pygame.Rect(panel.right - 126, panel.bottom - 32, 96, 22)
        box(surf, hint, PANEL_D)
        draw_text(surf, "ENTER", SMALL, BLACK, hint.centerx, hint.centery, center=True)


class EffectText:
    def __init__(self, text, color):
        self.text = text
        self.color = color
        self.life = 100

    def update(self):
        self.life -= 1


class Quiz:
    def __init__(self):
        self.active = False
        self.subject = ""
        self.questions = []
        self.index = 0
        self.score = 0

    def start(self, subject):
        self.active = True
        self.subject = subject
        self.questions = random.sample(EXAM_BANK[subject], 3)
        self.index = 0
        self.score = 0

    def answer(self, idx):
        if not self.active:
            return None
        q = self.questions[self.index]
        if idx == q[2]:
            self.score += 1
        self.index += 1
        if self.index >= 3:
            self.active = False
            return self.score
        return None

    def draw(self, surf):
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 150))
        surf.blit(shade, (0, 0))

        rect = pygame.Rect(135, 85, 690, 440)
        box(surf, rect, PANEL)
        draw_text(surf, f"{self.subject} Exam", BIG, BLACK, rect.centerx, 125, True)

        q = self.questions[self.index]
        draw_text(surf, f"Question {self.index + 1}/3", FONT, BLACK, rect.x + 28, 170)
        draw_text(surf, q[0], FONT, BLACK, rect.x + 28, 220)

        for i, opt in enumerate(q[1]):
            orect = pygame.Rect(rect.x + 32, 280 + i * 72, rect.w - 64, 52)
            box(surf, orect, PANEL_D)
            draw_text(surf, f"{i + 1}) {opt}", FONT, BLACK, orect.x + 14, orect.y + 14)

        draw_text(surf, "Press 1 / 2 / 3", SMALL, BLACK, rect.centerx, rect.bottom - 28, True)


class NPC:
    def __init__(self, x, y, name, lines, shirt_color, gift_pref):
        self.x = x
        self.y = y
        self.name = name
        self.lines = lines
        self.i = 0
        self.shirt_color = shirt_color
        self.friendship = 0
        self.gift_pref = gift_pref

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, 24, 34)

    def talk(self):
        line = self.lines[self.i]
        self.i = (self.i + 1) % len(self.lines)
        return f"{self.name}: {line}"

    def give_gift(self, gift):
        if gift == self.gift_pref:
            self.friendship = clamp(self.friendship + 8, 0, 100)
            return f"{self.name} loved the {gift}!"
        self.friendship = clamp(self.friendship + 2, 0, 100)
        return f"{self.name} accepted the {gift}."

    def draw(self, surf, cam_x, cam_y):
        px = self.x - cam_x
        py = self.y - cam_y
        pygame.draw.rect(surf, SKIN, (px + 6, py, 12, 10))
        pygame.draw.rect(surf, HAIR, (px + 4, py, 16, 4))
        pygame.draw.rect(surf, self.shirt_color, (px + 4, py + 10, 16, 12))
        pygame.draw.rect(surf, PANTS, (px + 5, py + 22, 6, 12))
        pygame.draw.rect(surf, PANTS, (px + 13, py + 22, 6, 12))
        pygame.draw.rect(surf, BLACK, (px + 8, py + 4, 2, 2))
        pygame.draw.rect(surf, BLACK, (px + 14, py + 4, 2, 2))
        draw_text(surf, self.name, SMALL, BLACK, px - 6, py - 14)


class Building:
    def __init__(self, rect, roof_color, label, kind):
        self.rect = rect
        self.roof_color = roof_color
        self.label = label
        self.kind = kind


class Player:
    def __init__(self):
        self.x = 420
        self.y = 360
        self.w = 24
        self.h = 34
        self.frame = 0
        self.anim = 0
        self.dir = "down"
        self.inventory = {"coffee": 1, "snack": 1, "book": 0}

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, keys, blocked):
        dx = 0
        dy = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 3
            self.dir = "left"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 3
            self.dir = "right"
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 3
            self.dir = "up"
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 3
            self.dir = "down"

        if dx and dy:
            dx *= 0.7071
            dy *= 0.7071

        nx = self.x + dx
        ny = self.y + dy
        rx = pygame.Rect(int(nx), int(self.y), self.w, self.h)
        ry = pygame.Rect(int(self.x), int(ny), self.w, self.h)

        if not any(rx.colliderect(b) for b in blocked):
            self.x = clamp(nx, 0, WORLD_W * TILE - self.w)
        if not any(ry.colliderect(b) for b in blocked):
            self.y = clamp(ny, 0, WORLD_H * TILE - self.h)

        if dx or dy:
            self.anim += 1
            if self.anim >= 10:
                self.anim = 0
                self.frame = 1 - self.frame

    def draw(self, surf, cam_x, cam_y):
        px = int(self.x - cam_x)
        py = int(self.y - cam_y)
        step = 1 if self.frame else 0
        pygame.draw.rect(surf, SKIN, (px + 6, py, 12, 10))
        pygame.draw.rect(surf, HAIR, (px + 4, py, 16, 4))
        pygame.draw.rect(surf, SHIRT, (px + 4, py + 10, 16, 12))
        pygame.draw.rect(surf, PANTS, (px + 5, py + 22, 6, 12 - step))
        pygame.draw.rect(surf, PANTS, (px + 13, py + 22 + step, 6, 12 - step))
        pygame.draw.rect(surf, BLACK, (px + 8, py + 4, 2, 2))
        pygame.draw.rect(surf, BLACK, (px + 14, py + 4, 2, 2))


class Game:
    def __init__(self):
        self.player = Player()
        self.dialog = DialogueBox()
        self.story = StoryUI()
        self.quiz = Quiz()
        self.effects = []

        self.day = 1
        self.hour = 8
        self.energy = 80
        self.money = 60
        self.intel = 40
        self.gpa = 2.0
        self.study_hours = 0

        self.subjects = ["Math", "Physics", "English"]
        self.subject_index = 0
        self.exam_ready = True

        self.show_quests = False
        self.show_rels = False

        self.exam_taken = 0
        self.work_done = 0
        self.home_used = 0
        self.talk_count = 0
        self.time_counter = 0

        self.buildings = [
            Building(pygame.Rect(14 * TILE, 10 * TILE, 6 * TILE, 5 * TILE), HOME_ROOF, "HOME", "home"),
            Building(pygame.Rect(34 * TILE, 12 * TILE, 8 * TILE, 6 * TILE), SCHOOL_ROOF, "SCHOOL", "school"),
            Building(pygame.Rect(54 * TILE, 34 * TILE, 7 * TILE, 5 * TILE), WORK_ROOF, "WORK", "work"),
            Building(pygame.Rect(24 * TILE, 31 * TILE, 6 * TILE, 4 * TILE), CAFE_ROOF, "CAFE", "cafe"),
            Building(pygame.Rect(42 * TILE, 28 * TILE, 7 * TILE, 5 * TILE), LIB_ROOF, "LIBRARY", "library"),
        ]
        self.home, self.school, self.work, self.cafe, self.library = [b.rect for b in self.buildings]
        self.pond = pygame.Rect(8 * TILE, 34 * TILE, 8 * TILE, 5 * TILE)

        self.npcs = [
            NPC(26 * TILE, 16 * TILE, "Ebrar", [
                "A clean UI makes everything look smarter.",
                "Go to School if you want GPA.",
                "Cafe is nice when you're tired."
            ], (212, 122, 168), "coffee"),
            NPC(46 * TILE, 27 * TILE, "Ilayda", [
                "Math is easy today. Don't panic.",
                "Library gives extra intelligence.",
                "Work helps, but don't burn out."
            ], (145, 112, 228), "book"),
            NPC(20 * TILE, 34 * TILE, "Barista", [
                "Coffee is 10 money and +12 energy.",
                "Snacks are cheap and useful.",
                "Everyone looks dead during finals."
            ], (198, 143, 82), "snack"),
            NPC(58 * TILE, 22 * TILE, "Mert", [
                "I only study the night before.",
                "Physics lab destroyed me.",
                "Did you save the game?"
            ], (92, 180, 130), "snack"),
        ]
            def calculate_exam_result(self):
    score = self.study_hours * 0.5 + self.intel * 0.5

    if score >= 80:
        self.gpa += 0.3
        result = "Great result!"
    elif score >= 50:
        self.gpa += 0.1
        result = "Passed."
    else:
        self.gpa -= 0.2
        result = "Failed."

    self.study_hours = 0
    return result
        def study(self):
    self.study_hours += 5
    self.energy -= 5
    self.dialog.set("You studied. +5 knowledge")

        self.blocked = [self.pond]
        self.blocked += [b.rect for b in self.buildings]
        self.blocked += [
            pygame.Rect(22 * TILE, 7 * TILE, 2 * TILE, 8 * TILE),
            pygame.Rect(47 * TILE, 35 * TILE, 3 * TILE, 6 * TILE),
        ]

        self.load()

    def save(self):
        data = {
            "x": self.player.x,
            "y": self.player.y,
            "day": self.day,
            "hour": self.hour,
            "energy": self.energy,
            "money": self.money,
            "intel": self.intel,
            "gpa": self.gpa,
            "subject_index": self.subject_index,
            "exam_ready": self.exam_ready,
            "exam_taken": self.exam_taken,
            "work_done": self.work_done,
            "home_used": self.home_used,
            "talk_count": self.talk_count,
            "inventory": self.player.inventory,
            "friendships": {n.name: n.friendship for n in self.npcs},
        }
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
        self.dialog.set("Game saved.")

    def load(self):
        if not os.path.exists(SAVE_FILE):
            return
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.player.x = data.get("x", self.player.x)
            self.player.y = data.get("y", self.player.y)
            self.day = data.get("day", self.day)
            self.hour = data.get("hour", self.hour)
            self.energy = data.get("energy", self.energy)
            self.money = data.get("money", self.money)
            self.intel = data.get("intel", self.intel)
            self.gpa = data.get("gpa", self.gpa)
            self.subject_index = data.get("subject_index", self.subject_index)
            self.exam_ready = data.get("exam_ready", self.exam_ready)
            self.exam_taken = data.get("exam_taken", self.exam_taken)
            self.work_done = data.get("work_done", self.work_done)
            self.home_used = data.get("home_used", self.home_used)
            self.talk_count = data.get("talk_count", self.talk_count)
            self.player.inventory = data.get("inventory", self.player.inventory)
            fr = data.get("friendships", {})
            for n in self.npcs:
                n.friendship = fr.get(n.name, 0)
            self.dialog.set("Save loaded.")
        except Exception:
            self.dialog.set("Save could not be loaded.")

    def add_effect(self, text, color):
        self.effects.append(EffectText(text, color))

    def advance_time(self, hours=1):
        self.hour += hours
        while self.hour >= 24:
            self.hour -= 24
            self.day += 1
            self.exam_ready = True
        if self.hour >= 23 or self.hour < 7:
            self.dialog.set("It's late. Better go home soon.")

    def do_sleep(self):
        self.energy = 100
        self.hour = 8
        self.day += 1
        self.exam_ready = True
        self.home_used += 1
        self.dialog.set("You slept and started a new day.")
        self.add_effect("Energy full", GREEN)

    def handle_quiz_result(self, score):
        self.exam_taken += 1
        if score == 3:
            self.gpa = min(4.0, self.gpa + 0.35)
            self.intel = clamp(self.intel + 6, 0, 100)
            self.dialog.set("Perfect exam. GPA increased a lot.")
            self.add_effect("GPA +0.35", GREEN)
        elif score == 2:
            self.gpa = min(4.0, self.gpa + 0.18)
            self.dialog.set("Good exam. GPA increased.")
            self.add_effect("GPA +0.18", GREEN)
        else:
            self.gpa = max(0.0, self.gpa - 0.10)
            self.dialog.set("Bad exam. GPA decreased.")
            self.add_effect("GPA -0.10", RED)

        self.energy = clamp(self.energy - 10, 0, 100)
        self.advance_time(2)

    def get_quest_progress(self, q):
        t = q["type"]
        if t == "exam":
            return self.exam_taken
        if t == "work":
            return self.work_done
        if t == "home":
            return self.home_used
        if t == "talk":
            return self.talk_count
        if t == "intel":
            return self.intel
        return 0

    def interact_npc(self, npc):
        self.talk_count += 1
        npc.friendship = clamp(npc.friendship + 1, 0, 100)
        self.dialog.set(npc.talk())

        if npc.name in NPC_DIALOGUES:
            idx = NPC_INDEX[npc.name]
            self.story.start(NPC_DIALOGUES[npc.name][idx])
            NPC_INDEX[npc.name] = (idx + 1) % len(NPC_DIALOGUES[npc.name])

    def interact_building(self, kind):
        if kind == "home":
            self.do_sleep()
            return

        if kind == "work":
            if self.energy < 10:
                self.dialog.set("Too tired to work. Go rest first.")
                return
            earn = random.randint(18, 30)
            self.money += earn
            self.energy = clamp(self.energy - 12, 0, 100)
            self.work_done += 1
            self.dialog.set("Shift completed.")
            self.add_effect(f"Money +{earn}", YELLOW)
            self.add_effect("Energy -12", RED)
            self.advance_time(3)
            return

        if kind == "school":
            if self.exam_ready:
                subject = self.subjects[self.subject_index]
                self.subject_index = (self.subject_index + 1) % len(self.subjects)
                self.quiz.start(subject)
                self.exam_ready = False
                self.dialog.set(f"{subject} exam started.")
            else:
                gain = random.randint(4, 7)
                self.intel = clamp(self.intel + gain, 0, 100)
                self.energy = clamp(self.energy - 8, 0, 100)
                self.dialog.set("You attended class.")
                self.add_effect(f"Intel +{gain}", BLUE)
                self.add_effect("Energy -8", RED)
                self.advance_time(2)
            return

        if kind == "library":
            gain = random.randint(6, 10)
            self.intel = clamp(self.intel + gain, 0, 100)
            self.energy = clamp(self.energy - 6, 0, 100)
            self.player.inventory["book"] += 1
            self.dialog.set("You studied quietly at the library.")
            self.add_effect(f"Intel +{gain}", BLUE)
            self.add_effect("Book +1", GREEN)
            self.advance_time(2)
            return

        if kind == "cafe":
            if self.money >= 10:
                self.money -= 10
                self.energy = clamp(self.energy + 12, 0, 100)
                self.player.inventory["coffee"] += 1
                self.player.inventory["snack"] += 1
                self.dialog.set("You bought coffee and a snack.")
                self.add_effect("Energy +12", GREEN)
                self.add_effect("Coffee +1", YELLOW)
                self.advance_time(1)
            else:
                self.dialog.set("Not enough money for cafe items.")

    def interact(self):
        if self.story.active:
            return

        prect = self.player.rect.inflate(20, 20)
        for npc in self.npcs:
            if prect.colliderect(npc.rect):
                self.interact_npc(npc)
                return
        for b in self.buildings:
            if prect.colliderect(b.rect):
                self.interact_building(b.kind)
                return

    def try_gift(self):
        if self.story.active:
            return

        prect = self.player.rect.inflate(20, 20)
        target = None
        for npc in self.npcs:
            if prect.colliderect(npc.rect):
                target = npc
                break

        if not target:
            self.dialog.set("Stand near an NPC to give a gift.")
            return

        for item in ["coffee", "snack", "book"]:
            if self.player.inventory.get(item, 0) > 0:
                self.player.inventory[item] -= 1
                self.dialog.set(target.give_gift(item))
                self.add_effect(f"Gift: {item}", PURPLE)
                return

        self.dialog.set("You have no gifts to give.")
    def update(self):

    keys = pygame.key.get_pressed()
    self.time_counter += 1

    if self.time_counter >= 300:
        self.time_counter = 0
        self.advance_time(1)

        keys = pygame.key.get_pressed()
    self.time_counter += 1

    if self.time_counter >= 300:
        self.time_counter = 0
        self.advance_time(1)

    if keys[pygame.K_s]:
        self.study()


    if not self.quiz.active and not self.story.active and not self.show_quests and not self.show_rels:
        self.player.update(keys, self.blocked)

    self.dialog.update()

    for eff in self.effects[:]:
        eff.update()
        if eff.life <= 0:
            self.effects.remove(eff)

    
    def draw_tree(self, surf, wx, wy, cam_x, cam_y):
        px, py = wx - cam_x, wy - cam_y
        pygame.draw.rect(surf, TRUNK, (px + 10, py + 24, 12, 18))
        pygame.draw.circle(surf, LEAF_B, (px + 16, py + 16), 16)
        pygame.draw.circle(surf, LEAF_A, (px + 8, py + 14), 13)
        pygame.draw.circle(surf, LEAF_A, (px + 22, py + 14), 13)
        pygame.draw.circle(surf, LEAF_A, (px + 15, py + 8), 12)

    def draw_ground(self, surf, cam_x, cam_y):
        for y in range(WORLD_H):
            for x in range(WORLD_W):
                px = x * TILE - cam_x
                py = y * TILE - cam_y
                c = GRASS_A if (x + y) % 2 == 0 else GRASS_B
                pygame.draw.rect(surf, c, (px, py, TILE, TILE))
                pygame.draw.rect(surf, (120, 190, 94), (px + 4, py + 5, 2, 2))
                pygame.draw.rect(surf, (120, 190, 94), (px + 19, py + 14, 2, 2))
                pygame.draw.rect(surf, (120, 190, 94), (px + 26, py + 25, 2, 2))

        for y in range(self.pond.y // TILE, self.pond.bottom // TILE):
            for x in range(self.pond.x // TILE, self.pond.right // TILE):
                px = x * TILE - cam_x
                py = y * TILE - cam_y
                c = WATER_A if (x + y) % 2 == 0 else WATER_B
                pygame.draw.rect(surf, c, (px, py, TILE, TILE))
                pygame.draw.rect(surf, (156, 203, 255), (px + 6, py + 8, 8, 2))
                pygame.draw.rect(surf, (156, 203, 255), (px + 18, py + 18, 6, 2))

        paths = [
            pygame.Rect(16 * TILE, 12 * TILE, 26 * TILE, 2 * TILE),
            pygame.Rect(18 * TILE, 14 * TILE, 2 * TILE, 23 * TILE),
            pygame.Rect(38 * TILE, 14 * TILE, 2 * TILE, 23 * TILE),
            pygame.Rect(20 * TILE, 35 * TILE, 19 * TILE, 2 * TILE),
            pygame.Rect(29 * TILE, 31 * TILE, 9 * TILE, 2 * TILE),
        ]
        for p in paths:
            for y in range(p.y // TILE, p.bottom // TILE):
                for x in range(p.x // TILE, p.right // TILE):
                    px = x * TILE - cam_x
                    py = y * TILE - cam_y
                    c = PATH_A if (x + y) % 2 == 0 else PATH_B
                    pygame.draw.rect(surf, c, (px, py, TILE, TILE))
                    pygame.draw.rect(surf, (150, 108, 63), (px + 3, py + 6, 3, 3))
                    pygame.draw.rect(surf, (150, 108, 63), (px + 22, py + 15, 3, 3))

    def draw_building(self, surf, b, cam_x, cam_y):
        r = pygame.Rect(b.rect.x - cam_x, b.rect.y - cam_y, b.rect.w, b.rect.h)
        roof_shadow = pygame.Rect(r.x - 8, r.y - 8, r.w + 16, 12)
        pygame.draw.rect(surf, (80, 70, 70), roof_shadow)
        roof = pygame.Rect(r.x - 8, r.y - 14, r.w + 16, 18)
        box(surf, roof, b.roof_color)
        box(surf, r, WALL)

        door = pygame.Rect(r.centerx - 10, r.bottom - 24, 20, 24)
        box(surf, door, (122, 82, 52))
        pygame.draw.rect(surf, (200, 160, 120), (door.x + 14, door.y + 11, 2, 2))

        win_count = max(1, r.w // 64)
        for i in range(win_count):
            wx = r.x + 14 + i * 30
            if wx + 18 < r.right - 12:
                rect = pygame.Rect(wx, r.y + 18, 18, 18)
                box(surf, rect, WINDOW, bw=2)
                pygame.draw.line(surf, BLACK, (wx + 9, r.y + 20), (wx + 9, r.y + 34), 1)
                pygame.draw.line(surf, BLACK, (wx + 2, r.y + 27), (wx + 16, r.y + 27), 1)

        sign = pygame.Rect(r.centerx - 42, r.y + 46, 84, 20)
        box(surf, sign, PANEL)
        draw_text(surf, b.label, SMALL, BLACK, sign.centerx, sign.centery, center=True)
        draw_text(surf, "E", SMALL, BLACK, r.centerx, r.y + 76, True)

    def draw_fences(self, surf, cam_x, cam_y):
        for x in range(8, 17):
            px = x * TILE - cam_x
            py = 29 * TILE - cam_y
            pygame.draw.rect(surf, FENCE, (px, py, TILE, 6))
            pygame.draw.rect(surf, FENCE, (px + 4, py - 8, 6, 18))
        for y in range(29, 38):
            px = 8 * TILE - cam_x
            py = y * TILE - cam_y
            pygame.draw.rect(surf, FENCE, (px, py, 6, TILE))
            pygame.draw.rect(surf, FENCE, (px - 8, py + 4, 18, 6))

    def draw_world(self, surf, cam_x, cam_y):
        surf.fill(SKY)
        self.draw_ground(surf, cam_x, cam_y)

        for fx, fy, col in [(18, 18, (255, 210, 90)), (21, 21, (255, 140, 170)), (27, 18, (180, 150, 255)), (60, 31, (255, 140, 170)), (63, 34, (255, 210, 90))]:
            px = fx * TILE - cam_x + 10
            py = fy * TILE - cam_y + 10
            pygame.draw.rect(surf, (65, 140, 70), (px + 3, py + 6, 2, 6))
            pygame.draw.rect(surf, col, (px, py, 8, 8))

        for tx, ty in [(9, 8), (12, 10), (49, 10), (53, 12), (62, 16), (14, 43), (26, 38), (44, 42), (69, 25), (72, 28)]:
            self.draw_tree(surf, tx * TILE, ty * TILE, cam_x, cam_y)

        self.draw_fences(surf, cam_x, cam_y)

        for b in self.buildings:
            self.draw_building(surf, b, cam_x, cam_y)

        for npc in self.npcs:
            npc.draw(surf, cam_x, cam_y)

        self.player.draw(surf, cam_x, cam_y)

    def draw_ui(self, surf):
        top = pygame.Rect(0, 0, WIDTH, 92)
        box(surf, top, PANEL)

        draw_text(surf, f"Day: {self.day}", FONT, BLACK, 12, 10)
        draw_text(surf, f"Time: {self.hour}:00", FONT, BLACK, 92, 10)
        draw_text(surf, f"Energy: {self.energy}", FONT, BLACK, 214, 10)
        draw_text(surf, f"Intel: {self.intel}", FONT, BLACK, 374, 10)
        draw_text(surf, f"Money: {self.money}", FONT, BLACK, 500, 10)
        draw_text(surf, f"GPA: {self.gpa:.2f}", FONT, BLACK, 646, 10)

        inv = f"Inv C:{self.player.inventory['coffee']} S:{self.player.inventory['snack']} B:{self.player.inventory['book']}"
        chip = pygame.Rect(12, 42, 250, 22)
        box(surf, chip, PANEL_D)
        draw_text(surf, inv, SMALL, BLACK, chip.x + 8, chip.y + 4)

        draw_text(surf, "Campus Life RPG", SMALL, BLACK, WIDTH - 140, 10)

        for i, eff in enumerate(self.effects[-4:]):
            draw_text(surf, eff.text, SMALL, eff.color, WIDTH - 180, 34 + i * 14)

        self.dialog.draw(surf)

    def draw_quests_panel(self, surf):
        if not self.show_quests:
            return
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 130))
        surf.blit(shade, (0, 0))

        rect = pygame.Rect(130, 80, 700, 460)
        box(surf, rect, PANEL)
        draw_text(surf, "Quests", BIG, BLACK, rect.centerx, rect.y + 34, True)

        y = rect.y + 80
        for q in QUESTS:
            prog = self.get_quest_progress(q)
            done = prog >= q["target"]
            color = GREEN if done else BLACK
            draw_text(surf, q["title"], FONT, color, rect.x + 24, y)
            draw_text(surf, q["desc"], SMALL, BLACK, rect.x + 24, y + 24)
            draw_text(surf, f"{prog}/{q['target']}", SMALL, color, rect.right - 90, y + 10)
            y += 72

        draw_text(surf, "TAB to close", SMALL, BLACK, rect.centerx, rect.bottom - 24, True)

    def draw_relationships_panel(self, surf):
        if not self.show_rels:
            return
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 130))
        surf.blit(shade, (0, 0))

        rect = pygame.Rect(190, 90, 580, 420)
        box(surf, rect, PANEL)
        draw_text(surf, "Relationships", BIG, BLACK, rect.centerx, rect.y + 34, True)

        y = rect.y + 90
        for n in self.npcs:
            draw_text(surf, n.name, FONT, BLACK, rect.x + 26, y)
            bar_bg = pygame.Rect(rect.x + 140, y + 4, 300, 18)
            bar_fg = pygame.Rect(rect.x + 140, y + 4, int(300 * (n.friendship / 100)), 18)
            box(surf, bar_bg, PANEL_D, bw=2)
            pygame.draw.rect(surf, PURPLE, bar_fg)
            pygame.draw.rect(surf, BLACK, bar_fg, 2)
            draw_text(surf, f"{n.friendship}/100", SMALL, BLACK, rect.right - 92, y + 2)
            y += 60

        draw_text(surf, "Q to close", SMALL, BLACK, rect.centerx, rect.bottom - 24, True)

   def draw(self, surf):
    cam_x = clamp(int(self.player.x - WIDTH // 2), 0, WORLD_W * TILE - WIDTH)
    cam_y = clamp(int(self.player.y - HEIGHT // 2), 0, WORLD_H * TILE - HEIGHT)

    self.draw_world(surf, cam_x, cam_y)
    self.draw_ui(surf)

    if self.hour >= 18 or self.hour < 6:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 30, 60, 70))
        surf.blit(overlay, (0, 0))

    if self.quiz.active:
        self.quiz.draw(surf)

    self.draw_quests_panel(surf)
    self.draw_relationships_panel(surf)

    if self.story.active:
        self.story.draw(surf)


def main():
    game = Game()
    running = True

    while running:
        CLOCK.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save()
                running = False

            elif event.type == pygame.KEYDOWN:
                if game.story.active:
                    if event.key == pygame.K_RETURN:
                        game.story.next()

                elif game.quiz.active:
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        result = game.quiz.answer(int(event.unicode) - 1)
                        if result is not None:
                            game.handle_quiz_result(result)

                else:
                    if event.key == pygame.K_e:
                        game.interact()
                    elif event.key == pygame.K_F5:
                        game.save()
                    elif event.key == pygame.K_F9:
                        game.load()
                    elif event.key == pygame.K_TAB:
                        game.show_quests = not game.show_quests
                        game.show_rels = False
                    elif event.key == pygame.K_q:
                        game.show_rels = not game.show_rels
                        game.show_quests = False
                    elif event.key == pygame.K_g:
                        game.try_gift()

        game.update()
        game.draw(SCREEN)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
