# over_dragon_gate

这是一个基于Pygame开发的2D横版跳跃动作游戏，玩家可以选择不同的角色和背景主题，在有限的时间内通过跳跃、下蹲和飞行等操作躲避障碍物，收集各种道具获得更高分数。

## 游戏特性

- 多种角色选择，每个角色都有独特的外观
- 多样化的背景主题
- 丰富的游戏道具系统
- 简单直观的操作方式
- 计时挑战模式

## 环境配置

### 前提条件

确保你的系统已安装Python 3.6或更高版本。

### 安装依赖

1. 克隆或下载本项目到本地（使用git命令）：

```bash
git clone https://github.com/Dot28800/over_dragon_gate.git
```

2. 进入项目目录：

```bash
cd over_dragon_gate
```

3. 安装所需依赖：

```bash
pip install -r requirements.txt
```

依赖列表：
- Pillow==12.0.0
- pygame==2.6.1
- pygame_gui==0.6.13

## 开始游戏

在项目目录下运行以下命令启动游戏：

```bash
python main.py
```

## 选择界面

您需要选择一个我们给定的角色和场景，然后点击“开始游戏”
<img width="1929" height="1318" alt="image" src="https://github.com/user-attachments/assets/8baee07e-9e9b-4b00-b0fa-fba780ab3194" />

之后可以看到进入倒计时环节，倒计时结束后会正式开始游戏：
<img width="2101" height="1242" alt="image" src="https://github.com/user-attachments/assets/bcbf6b5a-9baf-46b3-850a-12958fa6d908" />

## 游戏控制

### 普通状态
- **K键**：跳跃
- **S键**：下蹲
- **A键**：后退
- **D键**：前进

### 飞行状态
- **W键**：上浮
- **S键**：下沉
- **A键**：后退
- **D键**：前进

## 游戏规则

### 障碍物与道具说明

1. **栅栏**：阻碍前进，碰到会扣分且短暂无法移动
2. **倒针**：碰到会扣更多分数
3. **时钟**：收集后增加游戏时间
4. **护盾**：获得短暂的无敌状态，期间碰到障碍物不会受到伤害
5. **翅膀**：获得飞行能力，可以自由在空中移动
6. **流矢**：贯穿伤害，需要小心躲避

### 游戏目标

在60秒的游戏时间内（可通过收集时钟延长），尽可能躲避障碍物，收集道具，获得更高的分数。

## 项目结构

```
over_dragon_gate/
├── resources/             # 游戏资源文件夹
│   ├── background_image/  # 背景图片
│   ├── player_image/      # 角色图片
│   └── prob_image/        # 道具和障碍物图片
├── main.py                # 游戏主入口
├── jumping.py             # 游戏核心逻辑
├── arrow.py               # 流矢类
├── dinasour.py            # 角色类
├── fence.py               # 栅栏类
├── horse.py               # 马类（游戏元素）
├── needle_trap.py         # 倒针陷阱类
├── shield.py              # 护盾类
├── time_clock.py          # 时钟类
├── wing.py                # 翅膀类
├── requirements.txt       # 依赖列表
└── README.md              # 项目说明文件
```

## 开发说明

本游戏使用Python的Pygame库开发，采用面向对象的设计方式，各游戏元素都被封装为独立的类，便于维护和扩展。


## 致谢

感谢所有为这个项目提供支持和建议的朋友！

