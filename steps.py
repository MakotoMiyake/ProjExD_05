import math
import random
import sys
import time

import pygame as pg


WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ

lr = (-1, +1)  # 右向きか左向きかを表す定数

class Player(pg.sprite.Sprite):
    """
    プレイヤーに関するクラス
    """
    def __init__(self, pos: tuple):
        """
        プレイヤー画像Surfaceを作成し、rectを設定する
        引数：プレイヤーの位置
        """
        super().__init__()
        self.image = pg.image.load("ex05/fig/3.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.dir = 0
        self.jump = 0
        self.jump_power = 20
        self.jump_max = 2

    def update(self, screen: pg.Surface):
        """
        プレイヤーを移動させる
        引数：ゲームウィンドウのSurface
        """
        screen.blit(self.image, self.rect.center)
    
    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)

class Score_my():

    """
    スコアに関するクラス
    """
    def __init__(self):
        """
        スコアを0に初期化する
        """
        self.font = pg.font.SysFont("hgp創英角ポップ体", 50)
        self.color = (0, 0, 255)
        self.score = 0
        self.img = self.font.render(f"SCORE:{self.score}", 0, self.color)
        self.rct = self.img.get_rect()
        self.rct.center = (100, HEIGHT-50)
        
    
    def score_up(self, add):
        self.score = self.score + add

    def update(self, screen: pg.Surface):
        """
        スコアを更新する
        """
        self.img = self.font.render(f"SCORE:{self.score}", 0, self.color)
        screen.blit(self.img, self.rct)

class Limit:
    """
    時間に関するクラス
    """
    def __init__(self):
        """
        制限時間の初期設定を300にする
        """
        self.limit = 300
        self.font = pg.font.SysFont("hgp創英角ポップ体", 50)
        self.color = (255, 0, 0)
        self.img = self.font.render(f"LIMIT:{self.limit}", 0, self.color)
        self.rct = self.img.get_rect()
        self.rct.center = (100, HEIGHT-100)

    def update(self, screen: pg.Surface):
        """
        制限時間を更新する
        0以下になった場合制限時間が0で止まる
        """
        self.img = self.font.render(f"LIMIT:{math.floor(self.limit)}", 0, self.color)
        screen.blit(self.img, self.rct)
        if self.limit<=0:
            self.limit=0
        else:
            self.limit-=1/50
        

class Step(pg.sprite.Sprite):
    """
    階段に関するクラス
    """
    def __init__(self, pos: tuple):
        """
        階段画像Surfaceを作成し、rectを設定する
        引数：階段の位置
        """
        super().__init__()
        self.size = (150, 30)
        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, (255, 0, 0), [0, 0, *self.size])
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self, screen: pg.Surface):
        """
        階段を移動させる
        引数：ゲームウィンドウのSurface
        """
        screen.blit(self.image, self.rect.center)


def main():
    pg.display.set_caption("こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")

    player = Player((800,470))
    steps = pg.sprite.Group()

    tmr = 0
    clock = pg.time.Clock()

    limit=Limit()
    score = Score_my()

    first_flag = True
    sx = 800

    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:

                return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                player.update(screen)
                rand = random.choice(lr)  # 左右どちらに作成するかをランダムに決める
                sx += 200 * rand
                if sx < 0 or sx+150 > WIDTH:  # 画面外に作成しないようにする
                    sx -= 400 * rand
                steps.add(Step((sx, 0)))  # 階段を作成
                for step in steps:
                    step.rect.move_ip(0, 100)  # 100ずつ下に移動する
                    if step.rect.top > HEIGHT:  # 画面外に出たら削除する
                        step.kill()
                score.score_up(1)

        screen.blit(bg_img, [0, 0])
        if first_flag:  # 最初の階段を作成
            first_flag = False  # 2回目以降は作成しない
            for sy in range(400, 0, -100):  # 400, 300, 200, 100の4個を作成
                rand = random.choice(lr)    # 左右どちらに作成するかをランダムに決める
                sx += 200 * rand
                if sx < 0 or sx+150 > WIDTH:  # 画面外に作成しないようにする
                    sx -= 400 * rand
                steps.add(Step((sx, sy)))  # 階段を作成

        player.update(screen)
        score.update(screen)
        limit.update(screen)
        steps.update(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()