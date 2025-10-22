import pygame




class Dinasour:
    def __init__(self, img_path,x,y,
                 screen_width=800,screen_height=450,
                 size_x=80,size_y=100,
                 jump_height=300,speed_forward=10,speed_backward=10,speed_up=20,
                 gravity=10,bg_rgb=(255,255,255),rate=1.1):
        self.img_path = img_path
        self.size_x = size_x
        self.size_y = size_y
        self.get_name(img_path)
        self.normal_img=pygame.image.load(self.img_path).convert()
        self.bg_rgb=bg_rgb
        self.normal_img.set_colorkey(bg_rgb)
        self.normal_img=pygame.transform.scale(self.normal_img,(size_x,size_y))
        self.rate = rate
        if "空桑" in self.name:
            self.rate=1.35
        self.set_shield_img()
        self.set_flying_img()
        self.img=self.normal_img
        self.size_x=size_x
        self.size_y=size_y
        self.screen_width=screen_width
        self.screen_height=screen_height
        self.rect=self.img.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.is_jumping=False   #判断是否在跳跃
        self.jump_peak=False    #判断是否在跳跃顶峰
        self.movable=True       #判断是否可以移动（遇到障碍物时，停止移动）
        self.speed_forward=speed_forward
        self.speed_backward=speed_backward
        self.speed_up=speed_up
        self.jump_height=jump_height
        self.gravity=gravity
        self.continuable=True   #是否继续游戏
        self.ground=screen_height-size_y
        self.ceil=self.screen_height-self.jump_height#跳跃顶峰坐标
        self.secondary_jump_height=self.jump_height
        self.jump_count=0
        self.mask = pygame.mask.from_surface(self.img)  # 创建掩码
        self.show_position()
        self.move_forward=False
        self.move_backward=False
        self.score=0
        self.is_crouch=False
        self.font = pygame.font.SysFont('华文新魏', 80)
        self.hit_messages = []
        self.last_hit_time = 0
        self.max_add_time=10
        self.real_add_time=0
        self.time_delta=2000
        self.invincible =False
        self.invincible_clock=None
        self.invincible_duration=3000
        self.invincible_progress=0
        self.invincible_threshold=2
        self.wing_progress=0
        self.fly_threshold=2
        self.is_flying=False
        self.fly_duration=3000
        self.max_fly_time=3
        self.fly_clock=None
        self.protection_after_fly=False


    def set_shield_img(self):
        shield_path=self.img_path.replace(self.name, "护盾"+self.name)
        self.shield_img = pygame.image.load(shield_path).convert()
        self.shield_img.set_colorkey(self.bg_rgb)
        self.shield_img = pygame.transform.scale(self.shield_img, (self.size_x*self.rate, self.size_y*self.rate))

    def set_flying_img(self):
        flying_path=self.img_path.replace(self.name, "飞行"+self.name)
        self.flying_img = pygame.image.load(flying_path).convert()
        self.flying_img.set_colorkey(self.bg_rgb)
        self.flying_img = pygame.transform.scale(self.flying_img, (self.size_x*self.rate, self.size_y*self.rate))



    def get_flying_img(self):
        flying_path=self.img_path.replace(self.name, "飞行"+self.name)
        return flying_path

    def switch_to_fly(self):
        self.wing_progress+=1
        if self.wing_progress>=self.fly_threshold:
            self.wing_progress=0
            self.is_flying=True
            self.fly_clock=pygame.time.get_ticks()
            self.img=self.flying_img

    def lose_fly(self):
        if not self.is_flying and not self.protection_after_fly:
            return
        cur_time=pygame.time.get_ticks()
        if self.is_flying and cur_time-self.fly_clock>self.fly_duration:
            self.is_flying=False
            self.img=self.shield_img
            self.protection_after_fly=True


    def get_name(self,path):
        self.name=path.split("/")[-1].split(".")[0]


    def add_score(self,incresion=1):
        self.score+=incresion

    def minus_score(self,reduce=1):
        self.score=max(0,self.score-reduce)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > 1000:  # 防止频繁扣分信息显示
            self.hit_messages.append((f"-{reduce}分", current_time))
            self.last_hit_time = current_time

    def draw_hit_messages(self, screen):
        current_time = pygame.time.get_ticks()
        messages_to_remove = []
        for message, time in self.hit_messages:
            if current_time - time < 2000:  # 显示2秒
                text = self.font.render(message, True, (255, 0, 0))
                screen.blit(text, (self.rect.x, self.rect.y - 30))
            else:
                messages_to_remove.append((message, time))
        for message in messages_to_remove:
            self.hit_messages.remove(message)

    def show_position(self):
        print(f"当前位置为{self.rect.x},{self.rect.y}")


    def crouch(self):
        self.is_crouch = True
        self.img = pygame.transform.scale(self.img, (self.size_x, self.size_y // 2))
        self.rect.y = self.screen_height - self.size_y // 2

    def rise(self):
        self.is_crouch = False
        self.img = pygame.transform.scale(self.img, (self.size_x, self.size_y))
        self.rect.y = self.screen_height - self.size_y

    def update(self):
        pygame.key.stop_text_input()
        keys = pygame.key.get_pressed()
        if not self.is_flying and not self.protection_after_fly:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.continuable = False
                    pygame.quit()
                    # sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k and (not self.is_jumping or (self.jump_peak and self.jump_count==1)) and not self.is_crouch:  # 按下上箭头键
                        self.jump()
                    elif event.key == pygame.K_s and not self.is_crouch and not self.is_jumping and self.jump_count==0:  # 按下下箭头键
                        self.crouch()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.move_backward = False
                    elif event.key == pygame.K_d:
                        self.move_forward = False
                    elif event.key == pygame.K_s:
                        self.rise()

            # 根据按键状态持续移动
            if keys[pygame.K_a] and self.movable:
                self.move_backward = True
                self.move_forward = False
                self.backward()
            elif keys[pygame.K_d] and self.movable:
                self.move_forward = True
                self.move_backward = False
                self.forward()

            # 检测跳跃和下蹲的逻辑
            if self.is_jumping:
                if keys[pygame.K_s]:  # 如果在跳跃过程中按下了下蹲键
                    self.crouch_after_jump = True  # 设置标志，表示跳跃结束后需要下蹲
                else:
                    self.crouch_after_jump = False  # 如果没有按下下蹲键，则清除标志

                if not self.jump_peak:
                    if self.jump_count==1:
                        self.rect.y = max(self.ceil, self.rect.y - self.speed_up)
                        if self.rect.y <= self.ceil:  # 触顶了
                            self.jump_peak = True
                    elif self.jump_count == 2:
                        self.rect.y = max(self.screen_height-self.secondary_jump_height, self.rect.y - self.speed_up)
                        if self.rect.y <= self.screen_height-self.secondary_jump_height:  # 触顶了
                            self.jump_peak = True
                else:
                    self.rect.y = min(self.ground, self.gravity + self.rect.y)
                    if self.rect.y >= self.ground:
                        self.jump_peak = False
                        self.jump_count = 0
                        self.is_jumping = False
                        if self.crouch_after_jump and keys[pygame.K_s]:  # 如果跳跃结束且需要下蹲
                            self.crouch()

        elif self.is_flying:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.continuable = False
                    pygame.quit()
            if keys[pygame.K_a] and self.movable:
                self.move_backward = True
                self.move_forward = False
                self.backward()
            elif keys[pygame.K_d] and self.movable:
                self.move_forward = True
                self.move_backward = False
                self.forward()
            if keys[pygame.K_w]:
                self.ascend()
            elif keys[pygame.K_s]:
                self.land()
            self.lose_fly()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.continuable = False
                    pygame.quit()
            if keys[pygame.K_a] and self.movable:
                    self.move_backward = True
                    self.move_forward = False
                    self.backward()
            elif keys[pygame.K_d] and self.movable:
                    self.move_forward = True
                    self.move_backward = False
                    self.forward()
            self.rect.y=min(self.screen_height-self.size_y,self.rect.y+self.gravity)
            if self.rect.y>=self.screen_height-self.size_y:
                 self.end_protection()
        self.lose_invincible()
    def ascend(self):
        self.rect.y=max(0,self.rect.y-0.8*self.speed_up)

    def land(self):
        self.rect.y=min(self.screen_height-self.rect.height,self.rect.y+0.8*self.speed_up)

    def end_protection(self):
        self.protection_after_fly=False
        self.invincible=False
        self.img=self.normal_img


    def judge_invincible(self):
        self.invincible_progress+=1
        if self.invincible_progress>=self.invincible_threshold:
            self.img=self.shield_img
            self.invincible_progress=0
            self.invincible = True
            self.invincible_clock = pygame.time.get_ticks()


    def lose_invincible(self):
        current_time = pygame.time.get_ticks()
        if not self.invincible:
            return
        if current_time - self.invincible_clock > self.invincible_duration:
            self.img = self.normal_img
            self.invincible = False
            self.invincible_clock = None

    def forward(self):
        if not self.is_flying:
            self.rect.x=min(self.screen_width-self.rect.width,self.rect.x+self.speed_forward)
        else:
            self.rect.x=min(self.screen_width-self.rect.width,self.rect.x+1.3*self.speed_forward)


    def backward(self):
        if not self.is_flying:
            self.rect.x=max(0,self.rect.x-self.speed_backward)
        else:
            self.rect.x=max(0,self.rect.x-1.3*self.speed_backward)

    def jump(self):
        if self.jump_count==0:
            self.is_jumping=True
            self.jump_peak=False
            self.jump_count += 1

        elif self.jump_count==1 and self.jump_peak:
            self.jump_peak = False
            self.jump_count += 1
            self.secondary_jump_height=0.5*self.jump_height+self.screen_height-self.rect.y


    def get_mask(self):
        return self.mask

    def get_rect(self):
        return self.rect