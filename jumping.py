import sys

import pygame
import random

import pygame_gui
from arrow import MyArrow
from pygame import font
import horse

from dinasour import Dinasour
from fence import Fence
from needle_trap import Needle_trap
from time_clock import TimeClock
from shield import Shield
from wing import Wing


class Jumping:
    def __init__(self,screen_width=1400, screen_height=800,player_size_x=96,player_size_y=120,
                       player_path="resources/player_image/诺雅.png",fence_path="resources/prob_image/wb_fence.png",
                        needle_path="resources/prob_image/needles.png",clock_path="resources/prob_image/clock.png",
                        shield_path="resources/prob_image/shield.jpg",wing_path="resources/prob_image/wing.png",
                        arrow_path="resources/prob_image/arrow.png",bg_path="resources/background_image/末世集群.jpg",bg_rgb=(255,255,255)):
        # 初始化pygame
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_size_x = player_size_x
        self.player_size_y = player_size_y

        self.obstacle_size_x = 80
        self.obstacle_size_y = 60
        self.player_path = player_path
        self.fence_path = fence_path
        self.needle_path=needle_path
        self.clock_path=clock_path
        self.shield_path=shield_path
        self.wing_path=wing_path
        self.arrow_path=arrow_path
        self.bg_path = bg_path
        self.n = 4
        self.font = pygame.font.Font(None, 74)
        self.bg_rgb=bg_rgb
        self.bg_img = pygame.image.load(self.bg_path)
        self.bg_img = pygame.transform.scale(self.bg_img, (self.screen_width, self.screen_height))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        # 设置窗口标题
        pygame.display.set_caption("跳跳跳")
        self.frame_rate=50
        # 创建恐龙对象
        self.player = Dinasour(self.player_path, x=0, y=self.screen_height - self.player_size_y,
                              screen_width=self.screen_width, screen_height=self.screen_height,
                               size_x=self.player_size_x, size_y=self.player_size_y,bg_rgb=self.bg_rgb)

        # 创建障碍物列表
        self.obstacles = [
            Fence(self.fence_path, self.screen_width, self.screen_height,
                     size_x=self.obstacle_size_x, size_y=self.obstacle_size_y,
                     x=(i + 1) * self.screen_width // self.n, y=self.screen_height - self.obstacle_size_y) for i in range(int(self.n-1))
        ]

        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()  # 记录游戏开始时间
        self.game_duration = 60000  # 游戏持续时间，单位为毫秒（例如：60秒）
        self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height))
        self.start = True
        self.last_clock_hit_time= 0
        self.show_hit_clock_msg=False
        self.show_invincible=False
        self.show_flying=False
        self.show_immunity=False
        self.immunity_clock=None
        pygame.font.init()
        pygame.display.flip()

    def modify_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.horizontal_move()
            if type(obstacle) in [Needle_trap,Fence,Shield,Wing]:
                if obstacle.rect.x + obstacle.size_x < 0:  # 如果障碍物完全移出屏幕
                    self.obstacles.remove(obstacle)  # 移除障碍物
            else:
                if obstacle.real_x < 0:
                    self.obstacles.remove(obstacle)
            obstacle.vertical_move()
        if len(self.obstacles) < self.n:
            cur=random.random()
            if cur < 0.24:  # 5% 的概率添加障碍物
                new_obstacle = Fence(self.fence_path,
                                    self.screen_width,
                                    self.screen_height,
                                    x=self.screen_width, y=self.screen_height - self.obstacle_size_y,
                                    size_x=self.obstacle_size_x, size_y=self.obstacle_size_y)
                self.obstacles.append(new_obstacle)
            elif cur<0.48:
                new_obstacle = Needle_trap(self.needle_path,
                                           self.screen_width,
                                           self.screen_height,
                                           size_x=self.obstacle_size_x, size_y=self.obstacle_size_y,
                                           upper_bound=self.screen_height -3*self.obstacle_size_y,
                                           lower_bound=self.screen_height- 1.75*self.obstacle_size_y)
                self.obstacles.append(new_obstacle)
            elif cur<=0.57:
                new_obstacle=TimeClock(self.clock_path,self.screen_width, self.screen_height,
                                       size_x=100,size_y=100)
                self.obstacles.append(new_obstacle)
            elif cur<=0.66:
                new_obstacle=Shield(self.shield_path,self.screen_width, self.screen_height,
                                       size_x=100,size_y=120,
                                    x=self.screen_width,y=0-self.obstacle_size_y)
                self.obstacles.append(new_obstacle)
            elif cur<=0.75:
                new_obstacle=Wing(self.wing_path,self.screen_width, self.screen_height,
                                       size_x=100,size_y=120,
                                    x=self.screen_width,y=random.randint(self.screen_height - 4*self.obstacle_size_y,self.screen_height- int(2.5*self.obstacle_size_y)))
                self.obstacles.append(new_obstacle)
            elif cur<=1:
                new_obstacle=MyArrow(self.arrow_path,self.screen_width, self.screen_height,
                                       size_x=100,size_y=120,
                                    x=self.screen_width,y=self.screen_height - self.obstacle_size_y)
                self.obstacles.append(new_obstacle)

    def deal_fence(self,obstacle):
        if self.player.rect.x > obstacle.rect.x + obstacle.size_x and not obstacle.visited:
            obstacle.visited = True
            self.player.add_score()
        self.player.movable = True and self.player.movable
        player_mask = self.player.get_mask()
        player_rect = self.player.get_rect()
        obstacle_mask = obstacle.get_mask()
        obstacle_rect = obstacle.get_rect()
        # 计算偏移量
        offset = (obstacle_rect.x - player_rect.x, obstacle_rect.y - player_rect.y)
        # 使用掩码进行碰撞检测
        if player_mask.overlap(obstacle_mask, offset) and not obstacle.collapsed and not self.player.invincible:
            self.player.movable = False
            self.player.minus_score()
            obstacle.collapsed = True
        elif player_mask.overlap(obstacle_mask, offset) and not obstacle.collapsed and self.player.invincible:
            self.show_immunity=True
            self.immunity_clock = pygame.time.get_ticks()


    def deal_needle(self,obstacle):
        if self.player.rect.x > obstacle.rect.x + obstacle.size_x and not obstacle.visited and not obstacle.collapsed:
            obstacle.visited = True
            self.player.add_score()
        player_mask = self.player.get_mask()
        player_rect = self.player.get_rect()
        obstacle_mask = obstacle.get_mask()
        obstacle_rect = obstacle.get_rect()
        # 计算偏移量
        offset = (obstacle_rect.x - player_rect.x, obstacle_rect.y - player_rect.y)
        # 使用掩码进行碰撞检测
        if player_mask.overlap(obstacle_mask, offset) and not obstacle.collapsed and not self.player.invincible:
            self.player.minus_score(2)
            obstacle.collapsed = True
        elif player_mask.overlap(obstacle_mask, offset) and not obstacle.collapsed and self.player.invincible:
            self.show_immunity=True
            self.immunity_clock = pygame.time.get_ticks()

    def deal_clock(self,obstacle):
        player_mask = self.player.get_mask()
        player_rect = self.player.get_rect()
        obstacle_mask = obstacle.get_mask()
        obstacle_rect = obstacle.get_rect()
        # 计算偏移量
        offset = (obstacle_rect.x - player_rect.x, obstacle_rect.y - player_rect.y)
        # 使用掩码进行碰撞检测
        if player_mask.overlap(obstacle_mask, offset) and not obstacle.collapsed and not obstacle.visited:
            if self.player.real_add_time < self.player.max_add_time:
                self.game_duration += self.player.time_delta
                self.player.real_add_time += 1
            obstacle.collapsed = True
            self.show_hit_clock_msg = True
            self.last_clock_hit_time = pygame.time.get_ticks()

    def deal_shield(self,obstacle):
        player_mask = self.player.get_mask()
        player_rect = self.player.get_rect()
        obstacle_mask = obstacle.get_mask()
        obstacle_rect = obstacle.get_rect()
        # 计算偏移量
        offset = (obstacle_rect.x - player_rect.x, obstacle_rect.y - player_rect.y)
        if player_mask.overlap(obstacle_mask, offset) and not obstacle.collapsed:
            obstacle.collapsed = True
            self.player.judge_invincible()
            if self.player.invincible:
                self.show_invincible = True
            #self.obstacles.remove(obstacle)
    def deal_wing(self,obstacle):
        player_mask = self.player.get_mask()
        player_rect = self.player.get_rect()
        obstacle_mask = obstacle.get_mask()
        obstacle_rect = obstacle.get_rect()
        # 计算偏移量
        offset = (obstacle_rect.x - player_rect.x, obstacle_rect.y - player_rect.y)
        if player_mask.overlap(obstacle_mask, offset) and not obstacle.collapsed:
            obstacle.collapsed = True
            self.player.switch_to_fly()
            #self.obstacles.remove(obstacle)
            self.show_flying = True

    def deal_arrow(self,obstacle):
        if self.player.rect.x > obstacle.rect.x + obstacle.size_x and not obstacle.visited:
            obstacle.visited = True
            self.player.add_score()
        player_mask = self.player.get_mask()
        player_rect = self.player.get_rect()
        obstacle_mask = obstacle.get_mask()
        obstacle_rect = obstacle.get_rect()
        # 计算偏移量
        offset = (obstacle_rect.x - player_rect.x, obstacle_rect.y - player_rect.y)
        # 使用掩码进行碰撞检测
        if player_mask.overlap(obstacle_mask, offset) and not obstacle.collapsed and not self.player.invincible:
            self.player.minus_score()
            obstacle.collapsed=True
        elif player_mask.overlap(obstacle_mask, offset) and not obstacle.collapsed and self.player.invincible:
            self.show_immunity=True
            self.immunity_clock = pygame.time.get_ticks()

    def detect_collision(self):
        flag = True
        for obstacle in self.obstacles:
            if type(obstacle)==Fence:
                if (self.screen_height - self.player.rect.y - self.player_size_y <
                        self.screen_height - obstacle.rect.y):
                    flag = False
                self.deal_fence(obstacle)
            elif type(obstacle)==Needle_trap:
                self.deal_needle(obstacle)
            elif type(obstacle)==TimeClock:
                self.deal_clock(obstacle)
            elif type(obstacle)==Shield:
                self.deal_shield(obstacle)
            elif type(obstacle)==Wing:
                self.deal_wing(obstacle)
            elif type(obstacle)==MyArrow:
                self.deal_arrow(obstacle)
        if flag:
            self.player.movable = True


    def run(self):
        while self.player.continuable:
            if self.start:
                self.player.update()
                if self.player.movable:
                    self.modify_obstacles()
            self.detect_collision()
            self.screen.blit(self.bg_img, (0, 0))
            self.screen.blit(self.player.img, self.player.rect)
            for obstacle in self.obstacles:
                if type(obstacle) in (Fence,Needle_trap,MyArrow):
                    self.screen.blit(obstacle.img, obstacle.rect)
                elif not obstacle.collapsed and not obstacle.visited:
                    self.screen.blit(obstacle.img, obstacle.rect)
            if self.start:
                self.show_texts()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)
            if (pygame.time.get_ticks() - self.start_time) >= self.game_duration:
                self.show_end_game_dialog()
                self.handle_end_game_dialog()




    def init_view(self):
        self.screen.blit(self.bg_img, (0, 0))
        self.screen.blit(self.player.img, self.player.rect)
        for obstacle in self.obstacles:
            self.screen.blit(obstacle.img, obstacle.rect)
        pygame.display.flip()

    def show_texts(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        remaining_time = max(0, self.game_duration / 1000 - elapsed_time)
        time_text = self.font.render(f"Time: {int(remaining_time)}/{self.game_duration // 1000} s", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 10))  # 在屏幕左上角绘制时间
        score_text = self.font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 50))
        this_font= pygame.font.SysFont("华文新魏", 50)
        invincible_text=this_font.render(f"无敌进度: {self.player.invincible_progress}/{self.player.invincible_threshold}", True, (255, 255, 255))
        self.screen.blit(invincible_text, (10, 90))
        wing_text=this_font.render(f"飞行充能: {self.player.wing_progress}/{self.player.fly_threshold}", True, (255, 255, 255))
        self.screen.blit(wing_text, (10, 130))
        if self.show_hit_clock_msg:
            cur_time=pygame.time.get_ticks()
            this_font= pygame.font.SysFont("华文新魏", 50)
            if cur_time-self.last_clock_hit_time<=1500:
                if self.player.real_add_time<self.player.max_add_time:
                    clock_hit_text = this_font.render(f"时间+{self.player.time_delta/1000}s", True, (255, 255, 255))
                else:
                    clock_hit_text = this_font.render("超过加时上限", True, (255, 255, 255))
                self.screen.blit(clock_hit_text, (self.screen_width//2-100, self.screen_height//2-30))
        if self.show_invincible:
            cur_time=pygame.time.get_ticks()
            this_font = pygame.font.SysFont("华文新魏", 50)
            if self.player.invincible and cur_time-self.player.invincible_clock<=self.player.invincible_duration:
                invincible_text = this_font.render(f"剩余无敌时间：{(self.player.invincible_duration-cur_time+self.player.invincible_clock)}ms", True, (255, 255, 255))
                self.screen.blit(invincible_text, (self.screen_width//2-100, 10))
        if self.show_flying:
            cur_time=pygame.time.get_ticks()
            this_font = pygame.font.SysFont("华文新魏", 50)
            if self.player.is_flying and cur_time-self.player.fly_clock<=self.player.fly_duration:
                flying_text = this_font.render(f"剩余飞行时间：{(self.player.fly_duration-cur_time+self.player.fly_clock)}ms", True, (255, 255, 255))
                self.screen.blit(flying_text, (self.screen_width//2-100, 50))
        if self.show_immunity:
            cur_time=pygame.time.get_ticks()
            this_font = pygame.font.SysFont("华文新魏", 50)
            if self.show_immunity and cur_time-self.immunity_clock<=500:
                immunity_text = this_font.render(f"免疫伤害", True, (255, 255, 255))
                self.screen.blit(immunity_text, (self.screen_width//2-100, 90))
            else:
                self.show_immunity=False
                self.immunity_clock=None
    def prepare(self):
        self.screen.blit(self.bg_img, (0, 0))
        self.screen.blit(self.player.img, self.player.rect)
        for obstacle in self.obstacles:
            self.screen.blit(obstacle.img, obstacle.rect)
        font1 = pygame.font.Font(None, 500)
        countdown_start_time = pygame.time.get_ticks()
        countdown_duration = 3000  # 倒计时总时间，单位为毫秒（例如：3秒）
        countdown_text = ["3", "2", "1", "Go!"]
        countdown_index = 0
        while countdown_index < len(countdown_text):
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - countdown_start_time
            if elapsed_time >= (countdown_index + 1) * (countdown_duration / len(countdown_text)):
                countdown_index += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    #sys.exit()

            # 绘制背景
            self.screen.blit(self.bg_img, (0, 0))
            self.screen.blit(self.player.img, self.player.rect)
            for obstacle in self.obstacles:
                self.screen.blit(obstacle.img, obstacle.rect)
            remaining_time = self.game_duration / 1000
            time_text = self.font.render(f"Time: {int(remaining_time)}", True, (255, 255, 255))
            self.screen.blit(time_text, (10, 10))  # 在屏幕左上角绘制时间
            score_text = self.font.render(f"Score: {self.player.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 50))
            if countdown_index >= len(countdown_text):
                break
            # 绘制倒计时文本
            text = font1.render(countdown_text[countdown_index], True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(text, text_rect)
            # 更新屏幕显示
            pygame.display.flip()
            # 控制游戏帧率
            self.clock.tick(50)
        self.start_time = pygame.time.get_ticks()  # 重新记录游戏开始时间

    def show_end_game_dialog(self):
        font = pygame.font.SysFont('华文新魏', 100)
        self.restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width // 2 - 150, self.screen_height // 2 +50), (100, 50)),
            text='Again',
            manager=self.manager,
        )
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width // 2 + 50, self.screen_height // 2 +50), (100, 50)),
            text='Exit',
            manager=self.manager
        )
        end_text = font.render("游戏结束！", True, (255, 255, 255))
        self.screen.blit(end_text, (self.screen_width // 2 - 200, self.screen_height // 2 - 200))
        score_text = font.render(f"得分：{self.player.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.screen_width // 2 - 150, self.screen_height // 2 - 75))
        pygame.display.flip()

    def handle_end_game_dialog(self):
        while True:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.player.continuable = False
                    return
                self.manager.process_events(event)
                self.handle_end_game_dialog_events(event)
                if self.player.continuable == False:
                    pygame.quit()
                    return
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

    def handle_end_game_dialog_events(self, event):
        #print("处理结束事件")
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.restart_button:
                #print("重新开始游戏")
                self.restart_game()
            elif event.ui_element == self.quit_button:
                self.player.continuable = False

    def restart_game(self):
        self.player = Dinasour(self.player_path, x=0, y=self.screen_height - self.player_size_y,
                               screen_width=self.screen_width, screen_height=self.screen_height,
                               size_x=self.player_size_x, size_y=self.player_size_y,bg_rgb=self.bg_rgb)
        self.obstacles = [
            Fence(self.fence_path, self.screen_width, self.screen_height,
                     size_x=self.obstacle_size_x, size_y=self.obstacle_size_y,
                     x=(i + 1) * self.screen_width // self.n, y=self.screen_height - self.obstacle_size_y) for i in
            range(int(self.n))
        ]
        self.start_time = pygame.time.get_ticks()  # 重新开始计时
        self.player.score = 0  # 重置得分
        self.showing_dialog = False  # 关闭对话框
        self.game_duration = 60000
        self.prepare()
        self.run()


# 创建游戏实例并运行
if __name__ == "__main__":
    game = Jumping()
    # game.init_view()


