"""Tower Defense em Pygame com níveis, modo infinito, torres e evoluções."""

import math
import random
from dataclasses import dataclass

import pygame


WIDTH, HEIGHT = 1100, 700
MAP_WIDTH, MAP_HEIGHT = 850, 620
FPS = 60
PATH_WIDTH = 58

WHITE = (241, 246, 249)
PANEL = (22, 34, 44)
PANEL_LIGHT = (38, 55, 67)
BLUE = (46, 119, 190)
GREEN = (67, 151, 75)
RED = (207, 66, 55)
GOLD = (242, 190, 65)
DISABLED = (82, 94, 105)

LEVELS = {
    "facil": {
        "name": "Bosque Tranquilo", "subtitle": "Fácil · 10 ondas",
        "waves": 10, "lives": 20, "money": 220, "difficulty": 0.85,
        "grass": (78, 145, 64),
        "path": [(-25, 100), (180, 100), (180, 280), (410, 280),
                 (410, 130), (650, 130), (650, 480), (875, 480)],
    },
    "medio": {
        "name": "Desfiladeiro", "subtitle": "Médio · 15 ondas",
        "waves": 15, "lives": 15, "money": 180, "difficulty": 1.0,
        "grass": (126, 122, 67),
        "path": [(-25, 80), (145, 80), (145, 235), (350, 235),
                 (350, 80), (570, 80), (570, 350), (320, 350),
                 (320, 530), (875, 530)],
    },
    "dificil": {
        "name": "Terras Vulcânicas", "subtitle": "Difícil · 20 ondas",
        "waves": 20, "lives": 10, "money": 155, "difficulty": 1.25,
        "grass": (92, 66, 58),
        "path": [(-25, 105), (220, 105), (220, 235), (80, 235),
                 (80, 410), (430, 410), (430, 155), (700, 155),
                 (700, 500), (875, 500)],
    },
    "infinito": {
        "name": "Cerco Infinito", "subtitle": "Sem limite · Recorde",
        "waves": None, "lives": 15, "money": 200, "difficulty": 1.05,
        "grass": (65, 112, 91),
        "path": [(-25, 95), (170, 95), (170, 255), (390, 255),
                 (390, 100), (630, 100), (630, 390), (465, 390),
                 (465, 535), (875, 535)],
    },
    "gelo": {
        "name": "Reino Gelado", "subtitle": "Médio · 16 ondas",
        "waves": 16, "lives": 14, "money": 185, "difficulty": 1.05,
        "grass": (104, 145, 157),
        "path": [(-25, 115), (245, 115), (245, 270), (90, 270),
                 (90, 485), (480, 485), (480, 195), (700, 195),
                 (700, 510), (875, 510)],
    },
    "deserto": {
        "name": "Dunas Perdidas", "subtitle": "Difícil · 18 ondas",
        "waves": 18, "lives": 12, "money": 170, "difficulty": 1.16,
        "grass": (174, 142, 76),
        "path": [(-25, 85), (285, 85), (285, 205), (115, 205),
                 (115, 390), (565, 390), (565, 155), (735, 155),
                 (735, 520), (875, 520)],
    },
    "labirinto": {
        "name": "Labirinto Real", "subtitle": "Extremo · 25 ondas",
        "waves": 25, "lives": 8, "money": 145, "difficulty": 1.38,
        "grass": (77, 82, 93),
        "path": [(-25, 70), (190, 70), (190, 180), (60, 180),
                 (60, 310), (350, 310), (350, 125), (560, 125),
                 (560, 440), (300, 440), (300, 550), (875, 550)],
    },
}

TOWER_TYPES = {
    "arqueira": {
        "name": "Arqueira", "cost": 55, "damage": 15, "range": 125,
        "delay": 0.48, "colour": (74, 152, 80), "shot": (255, 230, 120),
        "description": "Rápida e equilibrada",
    },
    "canhao": {
        "name": "Canhão", "cost": 90, "damage": 38, "range": 112,
        "delay": 1.25, "colour": (83, 91, 102), "shot": (255, 128, 55),
        "splash": 55, "description": "Dano em área",
    },
    "gelo": {
        "name": "Gelo", "cost": 75, "damage": 8, "range": 120,
        "delay": 0.75, "colour": (71, 166, 205), "shot": (160, 235, 255),
        "slow": 0.58, "description": "Abranda inimigos",
    },
    "laser": {
        "name": "Laser", "cost": 125, "damage": 30, "range": 150,
        "delay": 0.72, "colour": (170, 72, 190), "shot": (255, 90, 230),
        "description": "Longo alcance",
    },
    "sniper": {
        "name": "Sniper", "cost": 145, "damage": 105, "range": 235,
        "delay": 2.15, "colour": (53, 102, 67), "shot": (235, 255, 190),
        "description": "Dano extremo e lento",
    },
    "fogo": {
        "name": "Fogo", "cost": 105, "damage": 24, "range": 105,
        "delay": 0.38, "colour": (211, 79, 38), "shot": (255, 174, 45),
        "description": "Rajadas muito rápidas",
    },
    "tesla": {
        "name": "Tesla", "cost": 135, "damage": 32, "range": 125,
        "delay": 0.9, "colour": (68, 111, 210), "shot": (105, 220, 255),
        "chain": 2, "description": "Eletricidade em cadeia",
    },
    "morteiro": {
        "name": "Morteiro", "cost": 160, "damage": 72, "range": 190,
        "delay": 1.75, "colour": (91, 82, 70), "shot": (245, 115, 54),
        "splash": 82, "description": "Grande explosão",
    },
    "veneno": {
        "name": "Veneno", "cost": 100, "damage": 19, "range": 130,
        "delay": 0.65, "colour": (86, 174, 63), "shot": (146, 255, 79),
        "poison": True, "description": "Perfura e enfraquece",
    },
    "cristal": {
        "name": "Cristal", "cost": 175, "damage": 48, "range": 165,
        "delay": 0.58, "colour": (61, 195, 187), "shot": (128, 255, 241),
        "description": "Tecnologia avançada",
    },
    "dragao": {
        "name": "Dragão", "cost": 260, "damage": 95, "range": 165,
        "delay": 0.75, "colour": (184, 48, 34), "shot": (255, 126, 30),
        "splash": 68, "special": True, "description": "Chamas explosivas",
    },
    "temporal": {
        "name": "Temporal", "cost": 245, "damage": 42, "range": 180,
        "delay": 0.48, "colour": (58, 114, 205), "shot": (150, 230, 255),
        "slow": 0.48, "special": True, "description": "Controla o tempo",
    },
    "solar": {
        "name": "Solar", "cost": 285, "damage": 120, "range": 190,
        "delay": 1.05, "colour": (225, 161, 37), "shot": (255, 245, 130),
        "chain": 3, "special": True, "description": "Energia celestial",
    },
    "necromante": {
        "name": "Necromante", "cost": 235, "damage": 55, "range": 175,
        "delay": 0.62, "colour": (93, 48, 133), "shot": (195, 106, 255),
        "poison": True, "special": True, "description": "Maldição prolongada",
    },
    "guardiao": {
        "name": "Guardião", "cost": 310, "damage": 145, "range": 145,
        "delay": 1.25, "colour": (178, 183, 194), "shot": (235, 245, 255),
        "splash": 90, "special": True, "description": "Defesa lendária",
    },
    "balista": {
        "name": "Balista", "cost": 115, "damage": 68, "range": 185,
        "delay": 1.35, "colour": (130, 88, 48), "shot": (222, 184, 117),
        "description": "Projéteis pesados",
    },
    "vento": {
        "name": "Vento", "cost": 95, "damage": 14, "range": 145,
        "delay": 0.34, "colour": (142, 202, 196), "shot": (210, 255, 249),
        "slow": 0.72, "description": "Rajadas de controlo",
    },
    "sombra": {
        "name": "Sombra", "cost": 150, "damage": 61, "range": 155,
        "delay": 0.82, "colour": (67, 55, 91), "shot": (151, 116, 210),
        "poison": True, "description": "Maldição silenciosa",
    },
    "bombardeiro": {
        "name": "Bombardeiro", "cost": 185, "damage": 84, "range": 145,
        "delay": 1.55, "colour": (111, 65, 48), "shot": (255, 92, 40),
        "splash": 105, "description": "Área de impacto enorme",
    },
    "runa": {
        "name": "Runa", "cost": 155, "damage": 36, "range": 175,
        "delay": 0.52, "colour": (48, 161, 138), "shot": (102, 255, 214),
        "chain": 1, "description": "Magia versátil",
    },
}

TOWER_DETAILS = {
    "arqueira": "Ataca depressa e custa pouco. Excelente para as primeiras ondas.",
    "canhao": "Cada bala explode e danifica grupos próximos. Ideal em curvas apertadas.",
    "gelo": "Abranda os alvos atingidos, dando mais tempo às outras torres para atacar.",
    "laser": "Combina longo alcance e dano constante. Funciona bem no centro do mapa.",
    "sniper": "Elimina alvos resistentes à distância, mas demora bastante entre disparos.",
    "fogo": "Dispara rajadas muito rápidas. É eficaz contra corredores com pouca vida.",
    "tesla": "A descarga salta entre vários inimigos próximos e enfraquece grupos inteiros.",
    "morteiro": "Atira lentamente a grande distância e provoca uma explosão de área ampla.",
    "veneno": "Aplica dano contínuo durante vários segundos, mesmo depois do primeiro impacto.",
    "cristal": "Torre avançada com excelente dano, alcance e velocidade, mas bastante cara.",
    "dragao": "Especial. Lança chamas devastadoras que explodem e atingem vários inimigos.",
    "temporal": "Especial. Dobra o tempo à volta dos inimigos e abranda grandes grupos.",
    "solar": "Especial. Canaliza energia celestial que salta entre múltiplos adversários.",
    "necromante": "Especial. Aplica uma maldição poderosa que continua a retirar vida.",
    "guardiao": "Especial. Causa o maior dano explosivo, embora tenha disparos mais lentos.",
    "balista": "Perfura inimigos com virotes pesados. Boa contra tanques e regeneradores.",
    "vento": "Ataca muito rapidamente e abranda cada alvo com fortes rajadas de ar.",
    "sombra": "Mistura dano direto com veneno. Útil contra inimigos que regeneram vida.",
    "bombardeiro": "Tem a maior área de explosão das torres normais. Excelente contra multidões.",
    "runa": "Magia equilibrada que salta para um alvo adicional e cobre uma grande área.",
}

ENEMY_TYPES = {
    "normal": {"name": "Soldado", "hp": 1.0, "speed": 1.0, "reward": 1.0,
               "radius": 13, "colour": (221, 74, 59),
               "description": "Equilibrado, sem habilidade especial."},
    "rapido": {"name": "Corredor", "hp": 0.58, "speed": 1.75, "reward": 0.9,
               "radius": 10, "colour": (238, 176, 48),
               "description": "Muito veloz, mas tem pouca vida."},
    "tanque": {"name": "Tanque", "hp": 2.8, "speed": 0.62, "reward": 2.0,
               "radius": 17, "colour": (126, 75, 151),
               "description": "Blindado com muita vida e baixa velocidade."},
    "regenerador": {"name": "Regenerador", "hp": 1.65, "speed": 0.85,
                    "reward": 1.6, "radius": 14, "colour": (55, 177, 117),
                    "regen": 0.018,
                    "description": "Recupera vida enquanto percorre o caminho."},
    "boss": {"name": "Boss", "hp": 8.0, "speed": 0.48, "reward": 6.0,
             "radius": 23, "colour": (104, 31, 31),
             "description": "Gigante; causa 3 de dano ao castelo."},
}


@dataclass
class Enemy:
    kind: str
    x: float
    y: float
    hp: float
    max_hp: float
    speed: float
    reward: int
    radius: int
    colour: tuple
    waypoint: int = 1
    slow_timer: float = 0.0
    poison_timer: float = 0.0
    poison_dps: float = 0.0


@dataclass
class Tower:
    kind: str
    x: float
    y: float
    level: int = 1
    cooldown: float = 0.0
    angle: float = -math.pi / 2
    moved: bool = False

    @property
    def data(self):
        return TOWER_TYPES[self.kind]

    @property
    def attack_range(self):
        special_bonus = 1.18 if self.data.get("special") else 1.0
        return int(self.data["range"] * special_bonus * (1 + (self.level - 1) * 0.09))

    @property
    def damage(self):
        special_bonus = 1.45 if self.data.get("special") else 1.0
        return self.data["damage"] * special_bonus * (1 + (self.level - 1) * 0.42)

    @property
    def fire_delay(self):
        return max(0.18, self.data["delay"] * (1 - (self.level - 1) * 0.07))

    @property
    def upgrade_cost(self):
        return int(self.data["cost"] * (0.65 + self.level * 0.25))


@dataclass
class Projectile:
    x: float
    y: float
    target: Enemy
    tower: Tower
    speed: float = 500


@dataclass
class VisualEffect:
    kind: str
    x: float
    y: float
    x2: float
    y2: float
    colour: tuple
    timer: float
    duration: float


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tower Defense: Quatro Reinos")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 18)
        self.small = pygame.font.SysFont("arial", 14)
        self.tiny = pygame.font.SysFont("arial", 12)
        self.medium = pygame.font.SysFont("arial", 25, bold=True)
        self.big = pygame.font.SysFont("arial", 46, bold=True)
        self.title_font = pygame.font.SysFont("arial", 58, bold=True)
        self.state = "menu"
        self.level_key = None
        self.pending_level = None
        self.loadout = []
        self.loadout_notice = ""
        self.loadout_page = 0
        self.game_speed = 1
        self.level_buttons = {}
        self.loadout_buttons = {}
        self.tower_buttons = {}
        self.wave_button = pygame.Rect(650, 644, 185, 42)
        self.upgrade_button = pygame.Rect(873, 600, 205, 31)
        self.move_button = pygame.Rect(873, 636, 205, 29)
        self.sell_button = pygame.Rect(873, 670, 205, 25)
        self.menu_button = pygame.Rect(18, 645, 105, 40)
        self.speed_buttons = {
            1: pygame.Rect(480, 645, 45, 40),
            2: pygame.Rect(530, 645, 45, 40),
            3: pygame.Rect(580, 645, 45, 40),
        }
        self.confirm_loadout_button = pygame.Rect(430, 620, 240, 50)
        self.back_button = pygame.Rect(30, 625, 130, 42)
        self.enemy_info_button = pygame.Rect(430, 625, 240, 45)
        self.previous_page_button = pygame.Rect(720, 625, 125, 42)
        self.next_page_button = pygame.Rect(860, 625, 125, 42)
        self.make_background()
        self.animation_time = 0.0

    def make_background(self):
        random.seed(12)
        self.grass_blades = [
            (random.randrange(MAP_WIDTH), random.randrange(MAP_HEIGHT),
             random.randrange(3, 8)) for _ in range(180)
        ]
        self.ground_tiles = [
            (random.randrange(MAP_WIDTH), random.randrange(MAP_HEIGHT),
             random.randrange(12, 35), random.randrange(5, 13))
            for _ in range(90)
        ]
        self.stars = [(random.randrange(WIDTH), random.randrange(HEIGHT), random.randrange(1, 4))
                      for _ in range(90)]

    def start_level(self, key):
        self.level_key = key
        self.level = LEVELS[key]
        self.path = self.level["path"]
        self.money = self.level["money"]
        self.lives = self.level["lives"]
        self.max_lives = self.level["lives"]
        self.wave = 0
        self.score = 0
        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.effects = []
        self.spawn_queue = []
        self.spawn_timer = 0
        self.wave_active = False
        self.wave_total = 0
        self.wave_resolved = 0
        self.auto_wave_timer = 4.0
        self.selected_kind = "arqueira"
        if self.loadout:
            self.selected_kind = self.loadout[0]
        self.selected_tower = None
        self.moving_tower = None
        self.game_speed = 1
        self.game_over = False
        self.victory = False
        self.message = "Escolhe uma torre e constroi-a no terreno."
        self.message_timer = 4.0
        self.state = "game"

    def open_loadout(self, key):
        self.pending_level = key
        self.loadout = []
        self.loadout_page = 0
        self.loadout_notice = "Podes escolher apenas uma torre especial."
        self.state = "loadout"

    @staticmethod
    def distance(ax, ay, bx, by):
        return math.hypot(ax - bx, ay - by)

    def point_near_path(self, x, y):
        for (x1, y1), (x2, y2) in zip(self.path, self.path[1:]):
            dx, dy = x2 - x1, y2 - y1
            length_sq = dx * dx + dy * dy
            t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / length_sq))
            px, py = x1 + t * dx, y1 + t * dy
            if self.distance(x, y, px, py) < PATH_WIDTH / 2 + 22:
                return True
        return False

    def can_place(self, x, y, ignore_tower=None):
        if x < 25 or x > MAP_WIDTH - 25 or y < 25 or y > MAP_HEIGHT - 25:
            return False
        if self.point_near_path(x, y):
            return False
        return all(
            t is ignore_tower or self.distance(x, y, t.x, t.y) >= 48
            for t in self.towers
        )

    def start_wave(self):
        if self.wave_active or self.game_over or self.victory:
            return
        maximum = self.level["waves"]
        if maximum and self.wave >= maximum:
            return
        self.wave += 1
        count = 6 + self.wave * 2
        base_hp = (38 + self.wave * 17 + self.wave ** 2 * 1.8) * self.level["difficulty"]
        base_speed = 48 + min(self.wave, 18) * 2.4
        kinds = ["normal"]
        if self.wave >= 2:
            kinds.append("rapido")
        if self.wave >= 4:
            kinds.append("tanque")
        if self.wave >= 6:
            kinds.append("regenerador")
        queue = []
        for _ in range(count):
            kind = random.choice(kinds)
            queue.append((kind, base_hp, base_speed))
        if self.wave % 5 == 0:
            queue.append(("boss", base_hp, base_speed))
        random.shuffle(queue)
        self.spawn_queue = queue
        self.spawn_timer = 0
        self.wave_active = True
        self.wave_total = len(queue)
        self.wave_resolved = 0
        self.auto_wave_timer = 0
        self.message = f"Onda {self.wave}: {len(queue)} inimigos a caminho!"

    def spawn_enemy(self):
        kind, base_hp, base_speed = self.spawn_queue.pop()
        data = ENEMY_TYPES[kind]
        hp = base_hp * data["hp"] * random.uniform(0.92, 1.08)
        self.enemies.append(Enemy(
            kind, self.path[0][0], self.path[0][1], hp, hp,
            base_speed * data["speed"],
            max(2, int((4 + self.wave * 0.45) * data["reward"])),
            data["radius"], data["colour"],
        ))

    def upgrade_selected(self):
        tower = self.selected_tower
        if not tower:
            self.message = "Seleciona uma torre para a evoluir."
        elif tower.level >= 8:
            self.message = "Esta torre atingiu o nivel maximo."
        elif self.money < tower.upgrade_cost:
            self.message = "Moedas insuficientes para esta evolucao."
        else:
            cost = tower.upgrade_cost
            self.money -= cost
            tower.level += 1
            self.message = f"{tower.data['name']} evoluiu para nivel {tower.level}!"

    def sell_selected(self):
        if not self.selected_tower:
            return
        tower = self.selected_tower
        invested = tower.data["cost"]
        for level in range(1, tower.level):
            invested += int(tower.data["cost"] * (0.65 + level * 0.25))
        value = int(invested * 0.65)
        self.money += value
        self.towers.remove(tower)
        if self.moving_tower is tower:
            self.moving_tower = None
        self.selected_tower = None
        self.message = f"Torre vendida por {value} moedas."

    def begin_move(self):
        if not self.selected_tower:
            self.message = "Seleciona primeiro uma torre para mover."
            return
        if self.selected_tower.moved:
            self.message = "Esta torre ja utilizou o seu unico movimento."
            return
        self.moving_tower = self.selected_tower
        self.message = "Escolhe a nova posicao. Cada torre so pode ser movida uma vez."

    def handle_game_click(self, pos):
        x, y = pos
        if self.game_over or self.victory:
            if self.menu_button.collidepoint(pos):
                self.state = "menu"
            return
        if self.menu_button.collidepoint(pos):
            self.state = "menu"
            return
        for speed, rect in self.speed_buttons.items():
            if rect.collidepoint(pos):
                self.game_speed = speed
                self.message = f"Velocidade do jogo: x{speed}"
                return
        if self.wave_button.collidepoint(pos):
            self.start_wave()
            return
        if self.upgrade_button.collidepoint(pos):
            self.upgrade_selected()
            return
        if self.sell_button.collidepoint(pos):
            self.sell_selected()
            return
        if self.move_button.collidepoint(pos):
            self.begin_move()
            return
        for kind, rect in self.tower_buttons.items():
            if rect.collidepoint(pos):
                self.selected_kind = kind
                self.selected_tower = None
                self.message = f"{TOWER_TYPES[kind]['name']} selecionada."
                return
        if x >= MAP_WIDTH or y >= MAP_HEIGHT:
            return
        if self.moving_tower:
            if self.can_place(x, y, self.moving_tower):
                self.moving_tower.x = x
                self.moving_tower.y = y
                self.moving_tower.moved = True
                self.message = "Torre reposicionada. O movimento desta torre foi utilizado."
                self.moving_tower = None
            else:
                self.message = "Essa posicao nao e valida para mover a torre."
            return
        for tower in self.towers:
            if self.distance(x, y, tower.x, tower.y) <= 23:
                self.selected_tower = tower
                self.message = f"{tower.data['name']} nivel {tower.level} selecionada."
                return
        self.selected_tower = None
        data = TOWER_TYPES[self.selected_kind]
        if self.money < data["cost"]:
            self.message = "Nao tens moedas suficientes."
        elif data.get("special") and any(
            tower.data.get("special") for tower in self.towers
        ):
            self.message = "So pode existir uma torre especial no campo."
        elif not self.can_place(x, y):
            self.message = "Nao podes construir nesse local."
        else:
            self.towers.append(Tower(self.selected_kind, x, y))
            self.money -= data["cost"]
            self.message = f"{data['name']} construida!"

    def damage_enemy(self, enemy, tower):
        if enemy not in self.enemies:
            return
        enemy.hp -= tower.damage
        if "slow" in tower.data:
            enemy.slow_timer = max(enemy.slow_timer, 1.8 + tower.level * 0.2)
        if tower.data.get("poison"):
            enemy.poison_timer = 3.0 + tower.level * 0.35
            enemy.poison_dps = max(enemy.poison_dps, tower.damage * 0.28)
        if "splash" in tower.data:
            radius = tower.data["splash"] + tower.level * 4
            for other in self.enemies:
                if other is not enemy and self.distance(enemy.x, enemy.y, other.x, other.y) <= radius:
                    other.hp -= tower.damage * 0.45
        if tower.data.get("chain"):
            nearby = sorted(
                (other for other in self.enemies if other is not enemy),
                key=lambda other: self.distance(enemy.x, enemy.y, other.x, other.y),
            )
            for other in nearby[:tower.data["chain"] + tower.level // 2]:
                if self.distance(enemy.x, enemy.y, other.x, other.y) <= 95:
                    other.hp -= tower.damage * 0.4
        self.remove_dead()

    def remove_dead(self):
        for enemy in self.enemies[:]:
            if enemy.hp <= 0:
                self.enemies.remove(enemy)
                self.effects.append(
                    VisualEffect("death", enemy.x, enemy.y, enemy.x, enemy.y,
                                 enemy.colour, 0.42, 0.42)
                )
                self.wave_resolved += 1
                self.money += enemy.reward
                self.score += enemy.reward * 10

    def update(self, dt):
        if self.state != "game" or self.game_over or self.victory:
            return
        self.animation_time += dt
        for effect in self.effects[:]:
            effect.timer -= dt
            if effect.timer <= 0:
                self.effects.remove(effect)
        if not self.wave_active:
            maximum = self.level["waves"]
            if maximum is None or self.wave < maximum:
                self.auto_wave_timer = max(0, self.auto_wave_timer - dt)
                if self.auto_wave_timer <= 0:
                    self.start_wave()
        if self.wave_active and self.spawn_queue:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.spawn_enemy()
                self.spawn_timer = max(0.22, 0.72 - self.wave * 0.012)

        for enemy in self.enemies[:]:
            enemy.slow_timer = max(0, enemy.slow_timer - dt)
            if enemy.poison_timer > 0:
                enemy.poison_timer = max(0, enemy.poison_timer - dt)
                enemy.hp -= enemy.poison_dps * dt
            data = ENEMY_TYPES[enemy.kind]
            if data.get("regen") and enemy.hp < enemy.max_hp:
                enemy.hp = min(enemy.max_hp, enemy.hp + enemy.max_hp * data["regen"] * dt)
            if enemy.hp <= 0:
                continue
            tx, ty = self.path[enemy.waypoint]
            dx, dy = tx - enemy.x, ty - enemy.y
            distance = math.hypot(dx, dy)
            speed = enemy.speed * (0.58 if enemy.slow_timer > 0 else 1)
            movement = speed * dt
            if distance <= movement:
                enemy.x, enemy.y = tx, ty
                enemy.waypoint += 1
                if enemy.waypoint >= len(self.path):
                    self.enemies.remove(enemy)
                    self.wave_resolved += 1
                    self.lives -= 3 if enemy.kind == "boss" else 1
                    if self.lives <= 0:
                        self.lives = 0
                        self.game_over = True
                    continue
            elif distance:
                enemy.x += dx / distance * movement
                enemy.y += dy / distance * movement

        self.remove_dead()
        for tower in self.towers:
            tower.cooldown = max(0, tower.cooldown - dt)
            targets = [e for e in self.enemies if
                       self.distance(tower.x, tower.y, e.x, e.y) <= tower.attack_range]
            if targets and tower.cooldown <= 0:
                target = max(targets, key=lambda e: (e.waypoint, -self.distance(e.x, e.y, self.path[e.waypoint][0], self.path[e.waypoint][1])))
                tower.angle = math.atan2(target.y - tower.y, target.x - tower.x)
                self.projectiles.append(Projectile(tower.x, tower.y, target, tower))
                self.effects.append(
                    VisualEffect("attack", tower.x, tower.y, target.x, target.y,
                                 tower.data["shot"], 0.13, 0.13)
                )
                tower.cooldown = tower.fire_delay

        for shot in self.projectiles[:]:
            if shot.target not in self.enemies:
                self.projectiles.remove(shot)
                continue
            dx, dy = shot.target.x - shot.x, shot.target.y - shot.y
            distance = math.hypot(dx, dy)
            movement = shot.speed * dt
            if distance <= movement + shot.target.radius:
                self.projectiles.remove(shot)
                self.damage_enemy(shot.target, shot.tower)
            elif distance:
                shot.x += dx / distance * movement
                shot.y += dy / distance * movement

        if self.wave_active and not self.spawn_queue and not self.enemies:
            self.wave_active = False
            bonus = 8 + self.wave
            self.money += bonus
            maximum = self.level["waves"]
            if maximum and self.wave >= maximum:
                self.victory = True
                self.score += self.lives * 100
            else:
                self.auto_wave_timer = 5.0
                self.message = f"Onda concluida! Proxima onda em 5 segundos."

    def text(self, value, font, colour, pos, center=False):
        image = font.render(str(value), True, colour)
        rect = image.get_rect(center=pos) if center else image.get_rect(topleft=pos)
        self.screen.blit(image, rect)

    def button(self, rect, label, enabled=True, selected=False):
        colour = GREEN if selected else (BLUE if enabled else DISABLED)
        pygame.draw.rect(self.screen, colour, rect, border_radius=7)
        pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=7)
        self.text(label, self.small, WHITE, rect.center, center=True)

    def progress_bar(self, rect, progress, label, colour=GREEN):
        progress = max(0.0, min(1.0, progress))
        pygame.draw.rect(self.screen, (18, 28, 35), rect, border_radius=5)
        if progress > 0:
            fill = rect.copy()
            fill.width = max(8, int(rect.width * progress))
            pygame.draw.rect(self.screen, colour, fill, border_radius=5)
        pygame.draw.rect(self.screen, (218, 229, 235), rect, 1, border_radius=5)
        self.text(label, self.tiny, WHITE, rect.center, center=True)

    def draw_menu(self):
        self.screen.fill((13, 25, 39))
        for x, y, size in self.stars:
            pygame.draw.circle(self.screen, (80, 115, 140), (x, y), size)
        self.text("TOWER DEFENSE", self.title_font, GOLD, (WIDTH // 2, 82), True)
        self.text("QUATRO REINOS", self.medium, WHITE, (WIDTH // 2, 132), True)
        self.text("Escolhe o teu desafio", self.font, (184, 202, 214), (WIDTH // 2, 185), True)
        self.level_buttons.clear()
        colours = [
            (71, 145, 72), (153, 129, 63), (143, 65, 56), (53, 123, 122),
            (75, 135, 158), (177, 127, 54), (81, 75, 104),
        ]
        for index, (key, data) in enumerate(LEVELS.items()):
            col, row = index % 4, index // 4
            rect = pygame.Rect(30 + col * 265, 220 + row * 165, 245, 130)
            self.level_buttons[key] = rect
            pygame.draw.rect(self.screen, colours[index], rect, border_radius=12)
            pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=12)
            self.text(data["name"], self.font, WHITE, (rect.centerx, rect.y + 32), True)
            self.text(data["subtitle"], self.font, WHITE, (rect.centerx, rect.y + 72), True)
            self.text(f"Vidas: {data['lives']}  |  Moedas: {data['money']}",
                      self.small, (225, 237, 225), (rect.centerx, rect.y + 100), True)
        self.text("Clique num nível para começar", self.small, (160, 180, 195),
                  (WIDTH // 2, 585), True)
        self.button(self.enemy_info_button, "Enciclopedia de inimigos")

    def draw_enemy_info(self):
        self.screen.fill((13, 25, 39))
        for x, y, size in self.stars:
            pygame.draw.circle(self.screen, (65, 96, 120), (x, y), size)
        self.text("INIMIGOS", self.big, GOLD, (WIDTH // 2, 65), True)
        self.text("Conhece o adversario antes da batalha", self.font,
                  (190, 211, 224), (WIDTH // 2, 112), True)
        for index, (kind, data) in enumerate(ENEMY_TYPES.items()):
            rect = pygame.Rect(25 + index * 215, 175, 195, 330)
            pygame.draw.rect(self.screen, PANEL_LIGHT, rect, border_radius=12)
            pygame.draw.rect(self.screen, data["colour"], rect, 3, border_radius=12)
            cx, cy = rect.centerx, rect.y + 65
            if kind == "rapido":
                pygame.draw.polygon(self.screen, data["colour"],
                                    [(cx + 28, cy), (cx - 24, cy - 24), (cx - 24, cy + 24)])
            elif kind == "tanque":
                pygame.draw.rect(self.screen, data["colour"],
                                 (cx - 28, cy - 25, 56, 50), border_radius=5)
            elif kind == "regenerador":
                pygame.draw.polygon(self.screen, data["colour"],
                                    [(cx, cy - 30), (cx + 30, cy),
                                     (cx, cy + 30), (cx - 30, cy)])
            elif kind == "boss":
                points = [(cx - 18, cy - 28), (cx + 18, cy - 28),
                          (cx + 30, cy - 10), (cx + 26, cy + 24),
                          (cx, cy + 32), (cx - 26, cy + 24), (cx - 30, cy - 10)]
                pygame.draw.polygon(self.screen, data["colour"], points)
                pygame.draw.polygon(self.screen, GOLD, points, 3)
            else:
                pygame.draw.circle(self.screen, data["colour"], (cx, cy), 28)
            self.text(data["name"], self.medium, WHITE, (cx, rect.y + 125), True)
            self.text(f"Vida: x{data['hp']}", self.small, WHITE, (rect.x + 18, rect.y + 165))
            self.text(f"Velocidade: x{data['speed']}", self.small, WHITE,
                      (rect.x + 18, rect.y + 190))
            self.text(f"Recompensa: x{data['reward']}", self.small, GOLD,
                      (rect.x + 18, rect.y + 215))
            words = data["description"].split()
            lines, line = [], ""
            for word in words:
                candidate = f"{line} {word}".strip()
                if self.tiny.size(candidate)[0] > 160:
                    lines.append(line)
                    line = word
                else:
                    line = candidate
            lines.append(line)
            for row, line in enumerate(lines):
                self.text(line, self.tiny, (190, 209, 219),
                          (rect.centerx, rect.y + 255 + row * 17), True)
        self.button(self.back_button, "Voltar")

    def draw_loadout(self):
        self.screen.fill((13, 25, 39))
        for x, y, size in self.stars:
            pygame.draw.circle(self.screen, (65, 96, 120), (x, y), size)
        level_name = LEVELS[self.pending_level]["name"]
        self.text("PREPARAR DEFESAS", self.big, GOLD, (WIDTH // 2, 55), True)
        self.text(level_name, self.font, WHITE, (WIDTH // 2, 97), True)
        self.text(f"Escolhe 4 torres para levar ao combate ({len(self.loadout)}/4)",
                  self.font, (190, 211, 224), (WIDTH // 2, 128), True)
        self.text(self.loadout_notice, self.small, (255, 202, 104),
                  (WIDTH // 2, 151), True)
        self.loadout_buttons.clear()
        all_towers = list(TOWER_TYPES.items())
        page_towers = all_towers[self.loadout_page * 10:self.loadout_page * 10 + 10]
        for index, (kind, data) in enumerate(page_towers):
            col, row = index % 5, index // 5
            rect = pygame.Rect(35 + col * 213, 174 + row * 190, 190, 175)
            self.loadout_buttons[kind] = rect
            selected = kind in self.loadout
            pygame.draw.rect(self.screen, (48, 109, 69) if selected else PANEL_LIGHT,
                             rect, border_radius=10)
            edge = (235, 97, 76) if data.get("special") else (124, 145, 158)
            pygame.draw.rect(self.screen, GOLD if selected else edge,
                             rect, 3 if selected else 1, border_radius=10)
            pygame.draw.rect(self.screen, (15, 24, 30),
                             (rect.centerx - 25, rect.y + 9, 50, 38), border_radius=8)
            pygame.draw.polygon(self.screen, data["colour"],
                                [(rect.centerx, rect.y + 12), (rect.centerx - 20, rect.y + 44),
                                 (rect.centerx + 20, rect.y + 44)])
            self.text(data["name"], self.font, WHITE, (rect.centerx, rect.y + 60), True)
            self.text(f"{data['cost']} moedas", self.small, GOLD,
                      (rect.centerx, rect.y + 82), True)
            attacks = 1 / data["delay"]
            self.text(f"Dano {data['damage']} | {attacks:.1f} at/s | Alc. {data['range']}",
                      self.tiny, (207, 220, 227), (rect.centerx, rect.y + 101), True)
            words = TOWER_DETAILS[kind].split()
            lines, line = [], ""
            for word in words:
                candidate = f"{line} {word}".strip()
                if self.tiny.size(candidate)[0] > 168:
                    lines.append(line)
                    line = word
                else:
                    line = candidate
            lines.append(line)
            for line_index, detail_line in enumerate(lines[:3]):
                self.text(detail_line, self.tiny, (164, 215, 188),
                          (rect.centerx, rect.y + 122 + line_index * 15), True)
            if selected:
                self.text(f"#{self.loadout.index(kind) + 1}", self.tiny,
                          WHITE, (rect.x + 17, rect.y + 14), True)
            if data.get("special"):
                self.text("ESPECIAL", self.tiny, (255, 143, 112),
                          (rect.right - 35, rect.y + 13), True)
        self.button(self.back_button, "Voltar")
        self.button(self.confirm_loadout_button, "Entrar no nivel",
                    len(self.loadout) == 4, len(self.loadout) == 4)
        self.button(self.previous_page_button, "< Anterior", self.loadout_page > 0)
        self.button(self.next_page_button, "Seguinte >", self.loadout_page < 1)
        self.text(f"Pagina {self.loadout_page + 1}/2", self.tiny, WHITE,
                  (922, 608), True)

    def draw_map(self):
        self.screen.fill(self.level["grass"])
        texture_dark = tuple(max(0, c - 9) for c in self.level["grass"])
        texture_light = tuple(min(255, c + 7) for c in self.level["grass"])
        for index, (x, y, width, height) in enumerate(self.ground_tiles):
            colour = texture_dark if index % 2 else texture_light
            pygame.draw.polygon(
                self.screen, colour,
                [(x, y), (x + width, y + 2), (x + width - 4, y + height),
                 (x + 3, y + height - 1)]
            )
        for x, y, length in self.grass_blades:
            colour = tuple(max(0, c - 14) for c in self.level["grass"])
            pygame.draw.line(self.screen, colour, (x, y), (x + 2, y - length), 1)
            pygame.draw.line(self.screen, colour, (x + 2, y), (x + 5, y - length + 2), 1)
        shadow_path = [(x + 4, y + 6) for x, y in self.path]
        pygame.draw.lines(self.screen, (55, 51, 42), False, shadow_path, PATH_WIDTH + 10)
        pygame.draw.lines(self.screen, (105, 76, 48), False, self.path, PATH_WIDTH + 8)
        pygame.draw.lines(self.screen, (193, 151, 96), False, self.path, PATH_WIDTH)
        for (x1, y1), (x2, y2) in zip(self.path, self.path[1:]):
            distance = max(1, int(math.hypot(x2 - x1, y2 - y1)))
            for step in range(18, distance, 38):
                ratio = step / distance
                px, py = x1 + (x2 - x1) * ratio, y1 + (y2 - y1) * ratio
                pygame.draw.line(self.screen, (167, 126, 78),
                                 (px - 7, py - 2), (px + 7, py + 2), 2)
        self.text("INICIO", self.tiny, WHITE, (8, self.path[0][1] - 37))
        # Castelo da base, desenhado por camadas para dar volume.
        castle_y = self.path[-1][1]
        pygame.draw.rect(self.screen, (39, 47, 48), (758, castle_y - 3, 105, 17),
                         border_radius=3)
        pygame.draw.rect(self.screen, (104, 112, 116), (775, castle_y - 76, 70, 78))
        pygame.draw.rect(self.screen, (139, 145, 145), (783, castle_y - 69, 54, 69))
        for tx in (764, 824):
            pygame.draw.rect(self.screen, (117, 125, 128), (tx, castle_y - 92, 28, 92))
            pygame.draw.polygon(self.screen, (55, 75, 94),
                                [(tx - 3, castle_y - 91), (tx + 14, castle_y - 116),
                                 (tx + 31, castle_y - 91)])
        pygame.draw.rect(self.screen, (53, 40, 31), (801, castle_y - 37, 20, 39),
                         border_top_left_radius=9, border_top_right_radius=9)
        pygame.draw.line(self.screen, (55, 55, 55),
                         (810, castle_y - 76), (810, castle_y - 123), 3)
        pygame.draw.polygon(self.screen, RED,
                            [(812, castle_y - 122), (843, castle_y - 112),
                             (812, castle_y - 101)])
        self.text("BASE", self.tiny, WHITE, (786, castle_y + 7))
        health_rect = pygame.Rect(758, castle_y - 139, 96, 11)
        pygame.draw.rect(self.screen, (53, 24, 25), health_rect, border_radius=4)
        health_fill = health_rect.copy()
        health_fill.width = int(health_rect.width * self.lives / self.max_lives)
        if health_fill.width:
            pygame.draw.rect(self.screen, (73, 205, 92), health_fill, border_radius=4)
        pygame.draw.rect(self.screen, WHITE, health_rect, 1, border_radius=4)
        self.text(f"{self.lives}/{self.max_lives}", self.tiny, WHITE,
                  (health_rect.centerx, health_rect.y - 8), True)

    def draw_towers(self):
        for tower in self.towers:
            selected = tower is self.selected_tower
            if selected:
                diameter = tower.attack_range * 2
                area = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
                pygame.draw.circle(
                    area, (80, 195, 255, 38),
                    (tower.attack_range, tower.attack_range), tower.attack_range
                )
                pygame.draw.circle(
                    area, (145, 225, 255, 190),
                    (tower.attack_range, tower.attack_range), tower.attack_range, 2
                )
                self.screen.blit(
                    area, (tower.x - tower.attack_range, tower.y - tower.attack_range)
                )
            pygame.draw.polygon(self.screen, (33, 47, 42),
                                [(tower.x - 22, tower.y + 14),
                                 (tower.x + 22, tower.y + 14),
                                 (tower.x + 16, tower.y + 22),
                                 (tower.x - 16, tower.y + 22)])
            shape = list(TOWER_TYPES).index(tower.kind) % 5
            outline = WHITE if selected else (25, 35, 42)
            if shape == 0:
                outer = [(tower.x - 20, tower.y - 13), (tower.x, tower.y - 24),
                         (tower.x + 20, tower.y - 13), (tower.x + 20, tower.y + 13),
                         (tower.x, tower.y + 24), (tower.x - 20, tower.y + 13)]
                inner = [(tower.x - 16, tower.y - 10), (tower.x, tower.y - 19),
                         (tower.x + 16, tower.y - 10), (tower.x + 16, tower.y + 10),
                         (tower.x, tower.y + 19), (tower.x - 16, tower.y + 10)]
                pygame.draw.polygon(self.screen, outline, outer)
                pygame.draw.polygon(self.screen, tower.data["colour"], inner)
            elif shape == 1:
                outer = pygame.Rect(tower.x - 22, tower.y - 19, 44, 38)
                inner = pygame.Rect(tower.x - 18, tower.y - 15, 36, 30)
                pygame.draw.rect(self.screen, outline, outer, border_radius=4)
                pygame.draw.rect(self.screen, tower.data["colour"], inner, border_radius=3)
            elif shape == 2:
                outer = [(tower.x, tower.y - 25), (tower.x + 24, tower.y),
                         (tower.x, tower.y + 22), (tower.x - 24, tower.y)]
                inner = [(tower.x, tower.y - 20), (tower.x + 19, tower.y),
                         (tower.x, tower.y + 17), (tower.x - 19, tower.y)]
                pygame.draw.polygon(self.screen, outline, outer)
                pygame.draw.polygon(self.screen, tower.data["colour"], inner)
            elif shape == 3:
                outer = [(tower.x - 21, tower.y - 12), (tower.x, tower.y - 24),
                         (tower.x + 21, tower.y - 12), (tower.x + 21, tower.y + 12),
                         (tower.x, tower.y + 24), (tower.x - 21, tower.y + 12)]
                inner = [(tower.x - 17, tower.y - 9), (tower.x, tower.y - 19),
                         (tower.x + 17, tower.y - 9), (tower.x + 17, tower.y + 9),
                         (tower.x, tower.y + 19), (tower.x - 17, tower.y + 9)]
                pygame.draw.polygon(self.screen, outline, outer)
                pygame.draw.polygon(self.screen, tower.data["colour"], inner)
            else:
                outer = [(tower.x, tower.y - 25), (tower.x + 24, tower.y + 19),
                         (tower.x - 24, tower.y + 19)]
                inner = [(tower.x, tower.y - 19), (tower.x + 18, tower.y + 15),
                         (tower.x - 18, tower.y + 15)]
                pygame.draw.polygon(self.screen, outline, outer)
                pygame.draw.polygon(self.screen, tower.data["colour"], inner)
            barrel_end = (
                tower.x + math.cos(tower.angle) * 29,
                tower.y + math.sin(tower.angle) * 29,
            )
            pygame.draw.line(self.screen, (20, 28, 33),
                             (tower.x, tower.y), barrel_end, 8)
            pygame.draw.line(self.screen, tower.data["shot"],
                             (tower.x, tower.y), barrel_end, 4)
            if tower.kind == "canhao":
                pygame.draw.rect(self.screen, (35, 42, 47),
                                 (tower.x - 5, tower.y - 27, 10, 28))
            elif tower.kind == "laser":
                pygame.draw.polygon(self.screen, (235, 120, 245),
                                    [(tower.x, tower.y - 24), (tower.x - 8, tower.y), (tower.x + 8, tower.y)])
            elif tower.kind == "sniper":
                pygame.draw.line(self.screen, (35, 53, 37),
                                 (tower.x - 10, tower.y + 8), (tower.x + 15, tower.y - 22), 6)
                pygame.draw.circle(self.screen, (185, 220, 125),
                                   (int(tower.x + 7), int(tower.y - 13)), 4)
            elif tower.kind == "fogo":
                pygame.draw.polygon(self.screen, (255, 206, 52),
                                    [(tower.x, tower.y - 28), (tower.x - 9, tower.y - 5),
                                     (tower.x, tower.y + 1), (tower.x + 10, tower.y - 7)])
            elif tower.kind == "tesla":
                pygame.draw.line(self.screen, (145, 235, 255),
                                 (tower.x - 8, tower.y - 4), (tower.x, tower.y - 25), 4)
                pygame.draw.line(self.screen, (145, 235, 255),
                                 (tower.x, tower.y - 25), (tower.x + 9, tower.y - 5), 4)
            elif tower.kind == "morteiro":
                pygame.draw.circle(self.screen, (42, 43, 39),
                                   (int(tower.x), int(tower.y - 7)), 12)
                pygame.draw.circle(self.screen, (12, 15, 15),
                                   (int(tower.x), int(tower.y - 7)), 6)
            elif tower.kind == "veneno":
                pygame.draw.circle(self.screen, (174, 255, 85),
                                   (int(tower.x), int(tower.y - 9)), 9)
                pygame.draw.circle(self.screen, (235, 255, 210),
                                   (int(tower.x - 3), int(tower.y - 12)), 3)
            elif tower.kind == "cristal":
                pygame.draw.polygon(self.screen, (140, 255, 244),
                                    [(tower.x, tower.y - 28), (tower.x - 10, tower.y - 5),
                                     (tower.x, tower.y + 2), (tower.x + 10, tower.y - 5)])
            elif tower.kind == "dragao":
                pygame.draw.polygon(self.screen, (255, 105, 38),
                                    [(tower.x, tower.y - 29), (tower.x - 14, tower.y - 5),
                                     (tower.x - 4, tower.y - 9), (tower.x, tower.y + 2),
                                     (tower.x + 12, tower.y - 8)])
            elif tower.kind == "temporal":
                pygame.draw.arc(self.screen, (165, 235, 255),
                                (tower.x - 14, tower.y - 24, 28, 28), 0.3, 5.7, 4)
                pygame.draw.line(self.screen, WHITE, (tower.x, tower.y - 10),
                                 (tower.x + 8, tower.y - 18), 2)
            elif tower.kind == "solar":
                pygame.draw.polygon(self.screen, (255, 229, 83),
                                    [(tower.x, tower.y - 29), (tower.x - 12, tower.y - 4),
                                     (tower.x + 13, tower.y - 4)])
                pygame.draw.circle(self.screen, (255, 248, 184),
                                   (int(tower.x), int(tower.y - 12)), 7)
            elif tower.kind == "necromante":
                pygame.draw.polygon(self.screen, (188, 91, 235),
                                    [(tower.x, tower.y - 28), (tower.x - 13, tower.y),
                                     (tower.x + 13, tower.y)])
                pygame.draw.rect(self.screen, (106, 255, 119),
                                 (tower.x - 2, tower.y - 20, 4, 13))
            elif tower.kind == "guardiao":
                pygame.draw.polygon(self.screen, (225, 232, 238),
                                    [(tower.x, tower.y - 29), (tower.x - 13, tower.y - 7),
                                     (tower.x, tower.y + 2), (tower.x + 13, tower.y - 7)])
            elif tower.kind == "gelo":
                pygame.draw.circle(self.screen, (190, 245, 255), (int(tower.x), int(tower.y)), 7)
            else:
                pygame.draw.line(self.screen, (92, 48, 27),
                                 (tower.x, tower.y), (tower.x, tower.y - 25), 4)
            pygame.draw.circle(self.screen, (255, 255, 255),
                               (int(tower.x - 7), int(tower.y - 8)), 3)
            self.text(tower.level, self.tiny, WHITE, (tower.x, tower.y + 5), True)
            if selected:
                pulse = 3 + int((math.sin(self.animation_time * 5) + 1) * 2)
                colour = (255, 229, 104)
                for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
                    cx, cy = tower.x + sx * (25 + pulse), tower.y + sy * (25 + pulse)
                    pygame.draw.line(self.screen, colour, (cx, cy), (cx - sx * 9, cy), 2)
                    pygame.draw.line(self.screen, colour, (cx, cy), (cx, cy - sy * 9), 2)

        if self.moving_tower:
            mx, my = pygame.mouse.get_pos()
            if mx < MAP_WIDTH and my < MAP_HEIGHT:
                valid = self.can_place(mx, my, self.moving_tower)
                colour = (91, 235, 125, 170) if valid else (255, 83, 76, 170)
                radius = self.moving_tower.attack_range
                preview = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(preview, colour, (radius, radius), radius, 2)
                self.screen.blit(preview, (mx - radius, my - radius))
                pygame.draw.polygon(
                    self.screen, colour[:3],
                    [(mx, my - 24), (mx + 22, my + 18), (mx - 22, my + 18)], 3
                )

    def draw_enemies(self):
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, (45, 48, 40),
                             (enemy.x - enemy.radius, enemy.y + enemy.radius,
                              enemy.radius * 2, 4))
            border = (135, 225, 255) if enemy.slow_timer > 0 else (64, 24, 20)
            if enemy.poison_timer > 0:
                border = (137, 255, 76)
            x, y, r = enemy.x, enemy.y, enemy.radius
            if enemy.kind == "rapido":
                points = [(x + r, y), (x - r, y - r), (x - r, y + r)]
                pygame.draw.polygon(self.screen, enemy.colour, points)
                pygame.draw.polygon(self.screen, border, points, 2)
            elif enemy.kind == "tanque":
                rect = pygame.Rect(x - r, y - r + 2, r * 2, r * 2 - 4)
                pygame.draw.rect(self.screen, enemy.colour, rect, border_radius=3)
                pygame.draw.rect(self.screen, border, rect, 2, border_radius=3)
                pygame.draw.rect(self.screen, (52, 43, 57), (x - 5, y - r - 3, 10, 12))
            elif enemy.kind == "regenerador":
                points = [(x, y - r), (x + r, y), (x, y + r), (x - r, y)]
                pygame.draw.polygon(self.screen, enemy.colour, points)
                pygame.draw.polygon(self.screen, border, points, 2)
                pygame.draw.line(self.screen, WHITE, (x - 5, y), (x + 5, y), 2)
                pygame.draw.line(self.screen, WHITE, (x, y - 5), (x, y + 5), 2)
            elif enemy.kind == "boss":
                points = [
                    (x - r * .45, y - r), (x + r * .45, y - r),
                    (x + r, y - r * .35), (x + r, y + r * .45),
                    (x + r * .4, y + r), (x - r * .4, y + r),
                    (x - r, y + r * .45), (x - r, y - r * .35),
                ]
                pygame.draw.polygon(self.screen, enemy.colour, points)
                pygame.draw.polygon(self.screen, GOLD, points, 3)
                pygame.draw.polygon(self.screen, GOLD,
                                    [(x - 10, y - r + 2), (x - 5, y - r - 9),
                                     (x, y - r + 1), (x + 7, y - r - 10),
                                     (x + 11, y - r + 3)])
            else:
                pygame.draw.circle(self.screen, enemy.colour, (int(x), int(y)), r)
                pygame.draw.circle(self.screen, border, (int(x), int(y)), r, 2)
            width = max(26, enemy.radius * 2)
            pygame.draw.rect(self.screen, (65, 18, 18),
                             (enemy.x - width / 2, enemy.y - enemy.radius - 10, width, 5))
            pygame.draw.rect(self.screen, (91, 222, 105),
                             (enemy.x - width / 2, enemy.y - enemy.radius - 10,
                              width * max(0, enemy.hp / enemy.max_hp), 5))
        for shot in self.projectiles:
            dx, dy = shot.target.x - shot.x, shot.target.y - shot.y
            length = max(1, math.hypot(dx, dy))
            tail = (shot.x - dx / length * 18, shot.y - dy / length * 18)
            pygame.draw.line(self.screen, shot.tower.data["shot"],
                             tail, (shot.x, shot.y), 6)
            pygame.draw.circle(self.screen, WHITE, (int(shot.x), int(shot.y)), 7)
            pygame.draw.circle(self.screen, shot.tower.data["shot"],
                               (int(shot.x), int(shot.y)), 5)
        for effect in self.effects:
            progress = 1 - effect.timer / effect.duration
            if effect.kind == "attack":
                strength = max(1, int(5 * (1 - progress)))
                pygame.draw.line(self.screen, effect.colour,
                                 (effect.x, effect.y), (effect.x2, effect.y2), strength)
                pygame.draw.polygon(
                    self.screen, WHITE,
                    [(effect.x - 5, effect.y), (effect.x, effect.y - 5),
                     (effect.x + 5, effect.y), (effect.x, effect.y + 5)]
                )
            else:
                radius = 7 + int(progress * 25)
                points = []
                for index in range(12):
                    angle = index * math.pi / 6
                    distance = radius if index % 2 == 0 else radius * 0.42
                    points.append((effect.x + math.cos(angle) * distance,
                                   effect.y + math.sin(angle) * distance))
                pygame.draw.polygon(self.screen, effect.colour, points, 3)
                pygame.draw.line(self.screen, WHITE,
                                 (effect.x - radius, effect.y),
                                 (effect.x + radius, effect.y), 2)

    def draw_side_panel(self):
        pygame.draw.rect(self.screen, PANEL, (MAP_WIDTH, 0, WIDTH - MAP_WIDTH, HEIGHT))
        self.text(self.level["name"], self.medium, GOLD, (975, 28), True)
        maximum = self.level["waves"]
        wave_text = f"Onda {self.wave}/{maximum}" if maximum else f"Onda {self.wave} - Infinito"
        self.text(wave_text, self.font, WHITE, (975, 65), True)
        self.text(f"Castelo: {self.lives}/{self.max_lives}    Moedas: {self.money}",
                  self.font, WHITE, (975, 94), True)
        self.text("CONSTRUIR TORRE", self.small, (180, 201, 213), (870, 130))
        self.tower_buttons.clear()
        for index, kind in enumerate(self.loadout):
            data = TOWER_TYPES[kind]
            rect = pygame.Rect(870, 158 + index * 76, 210, 65)
            self.tower_buttons[kind] = rect
            selected = kind == self.selected_kind and not self.selected_tower
            pygame.draw.rect(self.screen, GREEN if selected else PANEL_LIGHT, rect, border_radius=7)
            pygame.draw.rect(self.screen, data["colour"], (rect.x + 8, rect.y + 9, 45, 45),
                             border_radius=5)
            self.text(data["name"], self.font, WHITE, (rect.x + 62, rect.y + 7))
            self.text(f"{data['cost']} moedas", self.small, GOLD, (rect.x + 62, rect.y + 29))
            self.text(data["description"], self.tiny, (190, 207, 216), (rect.x + 62, rect.y + 47))
        if self.selected_tower:
            tower = self.selected_tower
            pygame.draw.rect(self.screen, (30, 45, 56), (865, 463, 220, 135),
                             border_radius=7)
            self.text(f"{tower.data['name']}  -  Nivel {tower.level}/8",
                      self.font, GOLD, (875, 470))
            self.text(f"Dano: {int(tower.damage)}", self.small, WHITE, (875, 498))
            self.text(f"Velocidade: {1 / tower.fire_delay:.2f} ataques/s",
                      self.small, WHITE, (875, 518))
            self.text(f"Alcance: {tower.attack_range} px",
                      self.small, WHITE, (875, 538))
            effect = "Nenhum"
            if tower.kind == "canhao":
                effect = f"Explosao: {tower.data['splash'] + tower.level * 4}px"
            elif tower.kind == "gelo":
                effect = "Lentidao: 42%"
            elif tower.kind == "laser":
                effect = "Disparo de longo alcance"
            elif tower.kind == "sniper":
                effect = "Precisao de elite"
            elif tower.kind == "fogo":
                effect = "Cadencia muito elevada"
            elif tower.kind == "tesla":
                effect = f"Salta entre {tower.data['chain'] + tower.level // 2} alvos"
            elif tower.kind == "morteiro":
                effect = f"Explosao: {tower.data['splash'] + tower.level * 4}px"
            elif tower.kind == "veneno":
                effect = "Veneno durante 3 segundos"
            elif tower.kind == "cristal":
                effect = "Energia de alto impacto"
            elif tower.kind == "balista":
                effect = "Virote de alto dano"
            elif tower.kind == "vento":
                effect = "Rajada de lentidao"
            elif tower.kind == "sombra":
                effect = "Veneno prolongado"
            elif tower.kind == "bombardeiro":
                effect = f"Explosao: {tower.data['splash'] + tower.level * 4}px"
            elif tower.kind == "runa":
                effect = "Salta para outro alvo"
            self.text(f"Efeito: {effect}", self.tiny, (183, 211, 225), (875, 559))
            if tower.level < 8:
                special_damage = 1.45 if tower.data.get("special") else 1.0
                special_range = 1.18 if tower.data.get("special") else 1.0
                next_damage = tower.data["damage"] * special_damage * (1 + tower.level * 0.42)
                next_range = int(
                    tower.data["range"] * special_range * (1 + tower.level * 0.09)
                )
                self.text(f"Proximo: {int(next_damage)} dano / {next_range} alcance",
                          self.tiny, (124, 222, 137), (875, 579))
            cost = tower.upgrade_cost if tower.level < 8 else "--"
            self.button(self.upgrade_button, f"Evoluir ({cost})", tower.level < 8)
            self.button(
                self.move_button,
                ("A escolher posicao..." if self.moving_tower is tower
                 else "Movimento utilizado" if tower.moved
                 else "Mover torre [M]"),
                not tower.moved, self.moving_tower is tower
            )
            self.button(self.sell_button, "Vender torre")
        else:
            pygame.draw.rect(self.screen, (30, 45, 56), (865, 470, 220, 115),
                             border_radius=7)
            self.text("INFORMACAO DA TORRE", self.small, GOLD, (875, 483))
            self.text("Seleciona uma torre no mapa", self.small,
                      (160, 179, 190), (875, 516))
            self.text("para ver atributos, efeito", self.tiny,
                      (160, 179, 190), (875, 541))
            self.text("e valores da evolucao.", self.tiny,
                      (160, 179, 190), (875, 559))

    def draw_game(self):
        self.draw_map()
        self.draw_towers()
        self.draw_enemies()
        wave_progress = (
            self.wave_resolved / self.wave_total if self.wave_total else 0
        )
        maximum = self.level["waves"]
        if maximum:
            completed = max(0, self.wave - (1 if self.wave_active else 0))
            level_progress = (completed + (wave_progress if self.wave_active else 0)) / maximum
            level_label = f"Progresso do nivel: {int(level_progress * 100)}%"
        else:
            cycle_wave = (max(1, self.wave) - 1) % 5
            level_progress = (cycle_wave + wave_progress) / 5
            level_label = f"Proximo boss: {int(level_progress * 100)}%"
        self.progress_bar(
            pygame.Rect(18, 15, 300, 18), wave_progress,
            f"Onda {self.wave}: {self.wave_resolved}/{self.wave_total}", BLUE
        )
        self.progress_bar(
            pygame.Rect(18, 40, 300, 18), level_progress, level_label, GOLD
        )
        alert_rect = pygame.Rect(330, 14, 500, 44)
        pygame.draw.rect(self.screen, (128, 28, 31), alert_rect, border_radius=7)
        pygame.draw.rect(self.screen, (255, 108, 101), alert_rect, 2, border_radius=7)
        self.text(self.message, self.small, WHITE, alert_rect.center, True)
        self.draw_side_panel()
        pygame.draw.rect(self.screen, PANEL, (0, MAP_HEIGHT, MAP_WIDTH, HEIGHT - MAP_HEIGHT))
        self.button(self.menu_button, "Menu")
        self.text(f"Pontos: {self.score}", self.font, WHITE, (145, 651))
        self.text("Velocidade", self.tiny, (180, 199, 210), (487, 629))
        for speed, rect in self.speed_buttons.items():
            self.button(rect, f"x{speed}", True, self.game_speed == speed)
        label = (
            "Onda em curso" if self.wave_active
            else f"Proxima em {self.auto_wave_timer:.1f}s [Espaco]"
        )
        self.button(self.wave_button, label, not self.wave_active)
        if self.game_over or self.victory:
            shade = pygame.Surface((MAP_WIDTH, MAP_HEIGHT), pygame.SRCALPHA)
            shade.fill((0, 0, 0, 155))
            self.screen.blit(shade, (0, 0))
            title = "VITORIA!" if self.victory else "FIM DO JOGO"
            colour = GOLD if self.victory else (255, 100, 90)
            self.text(title, self.big, colour, (MAP_WIDTH // 2, 235), True)
            self.text(f"Onda {self.wave}  |  Pontos {self.score}",
                      self.medium, WHITE, (MAP_WIDTH // 2, 300), True)
            self.text("Usa o botão Menu para escolher outro desafio.",
                      self.font, WHITE, (MAP_WIDTH // 2, 350), True)

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "enemy_info":
            self.draw_enemy_info()
        elif self.state == "loadout":
            self.draw_loadout()
        else:
            self.draw_game()
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "game" and self.moving_tower:
                            self.moving_tower = None
                            self.message = "Movimento cancelado."
                        elif self.state == "game":
                            self.state = "menu"
                        elif self.state == "loadout":
                            self.state = "menu"
                        elif self.state == "enemy_info":
                            self.state = "menu"
                        else:
                            running = False
                    elif self.state == "game":
                        if event.key == pygame.K_SPACE:
                            self.start_wave()
                        elif event.key == pygame.K_u:
                            self.upgrade_selected()
                        elif event.key == pygame.K_s:
                            self.sell_selected()
                        elif event.key == pygame.K_m:
                            self.begin_move()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.state == "menu":
                        if self.enemy_info_button.collidepoint(event.pos):
                            self.state = "enemy_info"
                        else:
                            for key, rect in self.level_buttons.items():
                                if rect.collidepoint(event.pos):
                                    self.open_loadout(key)
                                    break
                    elif self.state == "enemy_info":
                        if self.back_button.collidepoint(event.pos):
                            self.state = "menu"
                    elif self.state == "loadout":
                        if self.back_button.collidepoint(event.pos):
                            self.state = "menu"
                        elif (self.previous_page_button.collidepoint(event.pos)
                              and self.loadout_page > 0):
                            self.loadout_page -= 1
                        elif (self.next_page_button.collidepoint(event.pos)
                              and self.loadout_page < 1):
                            self.loadout_page += 1
                        elif (self.confirm_loadout_button.collidepoint(event.pos)
                              and len(self.loadout) == 4):
                            self.start_level(self.pending_level)
                        else:
                            for kind, rect in self.loadout_buttons.items():
                                if rect.collidepoint(event.pos):
                                    if kind in self.loadout:
                                        self.loadout.remove(kind)
                                    elif len(self.loadout) < 4:
                                        is_special = TOWER_TYPES[kind].get("special", False)
                                        already_special = any(
                                            TOWER_TYPES[chosen].get("special", False)
                                            for chosen in self.loadout
                                        )
                                        if is_special and already_special:
                                            self.loadout_notice = (
                                                "So podes escolher uma torre especial."
                                            )
                                        else:
                                            self.loadout.append(kind)
                                            self.loadout_notice = (
                                                "Escolhe exatamente 4 torres."
                                            )
                                    break
                    else:
                        self.handle_game_click(event.pos)
                elif (event.type == pygame.MOUSEBUTTONDOWN
                      and event.button == 3 and self.state == "game"):
                    self.moving_tower = None
                    self.message = "Movimento cancelado."
            self.update(dt * self.game_speed)
            self.draw()
        pygame.quit()


if __name__ == "__main__":
    Game().run()
