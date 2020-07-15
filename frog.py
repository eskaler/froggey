from frogClasses import *

class Main():
    def __init__(self):
        """GAME LOGIC"""
        pg.display.set_caption("froggey")
        pg.mixer.init()
        pg.mixer.music.load('./sounds/theme.mp3')

        soundMove = pg.mixer.Sound('./sounds/move.wav')
        soundLoseLife = pg.mixer.Sound('./sounds/loselife.wav')
        soundGameOver = pg.mixer.Sound('./sounds/gameover.wav')
        soundWin = pg.mixer.Sound('./sounds/win.wav')

        highestLevel = 1
        playing = False

        while True:
            DISPLAY.fill(BLACK)
            if not playing:
                pg.display.set_caption("Space - START High: "+str(highestLevel))
                drawIntro(highestLevel)
                for e in pg.event.get():
                    if e.type == pg.KEYDOWN:
                        if e.key == K_SPACE:
                            playing = True
                        elif e.key == K_ESCAPE:
                            gameQuit()
            else:
                frog = Frog()
                levelNum = 1
                prevLevelNum = 0
                while playing:
                    pg.mixer.music.play()
                    if prevLevelNum != levelNum:
                        level = Level(levelNum)
                    else:
                        level.isNotOver = True
                    frog.spawn()
                    pg.event.set_allowed(pg.KEYUP)
                    while level.isNotOver:
                        pg.display.set_caption("Level: "+str(levelNum)+" Lives: "+str(frog.lives)+" High: " + str(highestLevel))
                        for e in pg.event.get():
                            if e.type == pg.KEYDOWN:
                                soundMove.play()
                                frog.move(e.key)
                                if e.key == pg.K_ESCAPE:
                                    gameQuit()

                        level.draw()
                        frog.draw()
                        level.drawInfo(levelNum, highestLevel)

                        if(frog.checkWin()):
                            level.isNotOver = False
                            prevLevelNum = levelNum
                            levelNum += 1
                            highestLevel = max(highestLevel, levelNum)
                            

                        for enemy in level.enemies:
                            enemy.draw()
                            if enemy.x == frog.x:
                                if frog.checkHit(enemy.x, enemy.y) == True:
                                    level.isNotOver = False
                                    prevLevelNum = levelNum
                                    pg.mixer.music.stop()
                                    soundLoseLife.play()
                                    pg.time.delay(3000)
                                    break
                            enemy.ticked()
                        update()

                    playing = frog.alive
                    if not playing:
                        pg.mixer.music.stop()
                        soundGameOver.play()
                        pg.time.delay(5000)  
                    if prevLevelNum < levelNum:
                        pg.event.set_blocked(pg.KEYUP)
                        pg.mixer.music.stop()
                        soundWin.play()
                        pg.time.delay(6000)                   

            update()

main = Main()