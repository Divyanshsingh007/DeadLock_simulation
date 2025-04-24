import pygame
import sys
import math

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 80, 80)
GREEN = (0, 255, 150)
GRAY = (180, 180, 180)
YELLOW = (255, 230, 0)
BLUE = (100, 200, 255)
DARK = (30, 30, 30)
PANEL = (50, 50, 50)
BUTTON = (70, 130, 180)
HOVER = (100, 160, 210)
CARD = (40, 40, 40)

class Visualizer:
    def __init__(self, processes, resources):
        pygame.init()
        pygame.font.init()

        # Preload fonts to prevent lag later
        self.font = pygame.font.SysFont("consolas", 18)
        self.title_font = pygame.font.SysFont("consolas", 26, bold=True)
        self.font.render("warmup", True, WHITE)
        self.title_font.render("warmup", True, WHITE)

        self.processes = processes
        self.resources = resources
        self.screen = pygame.display.set_mode((1000, 700), pygame.RESIZABLE)
        pygame.display.set_caption("🔄 Deadlock Simulator")
        self.clock = pygame.time.Clock()

        self.button_rect = pygame.Rect(440, 640, 120, 40)
        self.deadlocked = set()
        self.mode = "cards"

    def update(self, tick):
        self.draw(tick)
        waiting = True
        while waiting:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        waiting = False
                    elif self.toggle_rect.collidepoint(event.pos):
                        self.mode = "network" if self.mode == "cards" else "cards"
            self.draw(tick)
            self.clock.tick(60)

    def draw(self, tick):
        self.screen.fill(DARK)
        width, height = self.screen.get_size()

        title = self.title_font.render("🔄 Deadlock Simulator", True, WHITE)
        self.screen.blit(title, (20, 15))

        # Toggle Button
        self.toggle_rect = pygame.Rect(width - 150, 20, 130, 30)
        pygame.draw.rect(self.screen, PANEL, self.toggle_rect, border_radius=6)
        mode_label = self.font.render("Switch View", True, WHITE)
        self.screen.blit(mode_label, mode_label.get_rect(center=self.toggle_rect.center))

        # Draw Tick
        tick_text = self.font.render(f"Tick: {tick}", True, WHITE)
        self.screen.blit(tick_text, (20, 60))

        # Draw main content
        if self.mode == "cards":
            self.draw_cards()
        else:
            self.draw_network()

        # Draw Next Tick button a bit higher than the bottom
        self.button_rect.centerx = width // 2
        self.button_rect.y = height - 100
        pygame.draw.rect(self.screen, BUTTON, self.button_rect, border_radius=6)
        btn_text = self.font.render("Next Tick", True, WHITE)
        self.screen.blit(btn_text, btn_text.get_rect(center=self.button_rect.center))

        pygame.display.flip()

    def draw_cards(self):
        x, y = 30, 100
        for proc in self.processes:
            color = self.get_state_color(proc)
            pygame.draw.rect(self.screen, CARD, (x, y, 450, 80), border_radius=8)
            label = self.font.render(f"PID: {proc.pid}", True, color)
            state = "Terminated" if proc.terminated else ("Waiting" if proc.is_waiting() else "Running")
            state_txt = self.font.render(f"State: {state}", True, color)
            held = ", ".join(proc.held_resources) if proc.held_resources else "None"
            next_res = proc.next_request() if not proc.terminated else "None"
            held_txt = self.font.render(f"Held: {held}", True, WHITE)
            next_txt = self.font.render(f"Next: {next_res}", True, WHITE)
            self.screen.blit(label, (x + 10, y + 5))
            self.screen.blit(state_txt, (x + 150, y + 5))
            self.screen.blit(held_txt, (x + 10, y + 35))
            self.screen.blit(next_txt, (x + 250, y + 35))
            y += 90

        y = 100
        for res in self.resources.values():
            pygame.draw.rect(self.screen, CARD, (520, y, 450, 80), border_radius=8)
            held_by = ", ".join([f"{pid}: {count}" for pid, count in res.held_by.items()]) or "None"
            lines = [
                f"{res.name} - Total: {res.total} Available: {res.available}",
                f"Held by: {held_by}"
            ]
            for i, line in enumerate(lines):
                txt = self.font.render(line, True, BLUE)
                self.screen.blit(txt, (530, y + 5 + i * 30))
            y += 90

    def draw_network(self):
        cx, cy = self.screen.get_width() // 2, self.screen.get_height() // 2
        radius = 220
        nodes = {}

        for i, proc in enumerate(self.processes):
            angle = (2 * math.pi / len(self.processes)) * i
            px = cx + radius * math.cos(angle)
            py = cy + radius * math.sin(angle)
            nodes[proc.pid] = (int(px), int(py))
            color = self.get_state_color(proc)
            pygame.draw.circle(self.screen, color, (int(px), int(py)), 25)
            pid_txt = self.font.render(proc.pid, True, BLACK)
            self.screen.blit(pid_txt, pid_txt.get_rect(center=(int(px), int(py))))

        r_y = 180
        for res in self.resources.values():
            pygame.draw.rect(self.screen, BLUE, (cx - 40, r_y, 80, 30), border_radius=6)
            txt = self.font.render(res.name, True, BLACK)
            self.screen.blit(txt, txt.get_rect(center=(cx, r_y + 15)))

            for pid in res.held_by:
                if pid in nodes:
                    pygame.draw.line(self.screen, GREEN, nodes[pid], (cx, r_y + 15), 2)

            for proc in self.processes:
                if proc.next_request() == res.name:
                    pygame.draw.line(self.screen, YELLOW, (cx, r_y + 15), nodes[proc.pid], 2)

            r_y += 50

    def get_state_color(self, proc):
        if proc.pid in self.deadlocked:
            return RED
        elif proc.terminated:
            return GRAY
        elif proc.is_waiting():
            return YELLOW
        elif proc.is_running():
            return GREEN
        return WHITE

    def mark_deadlock(self, deadlocked_pids):
        self.deadlocked = set(deadlocked_pids)

    def run_until_closed(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.clock.tick(60)
