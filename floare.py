import pygame
import random
import math
import os


from pygame.constants import MOUSEBUTTONDOWN

#initializarea ferestrei
pygame.init()
screen = pygame.display.set_mode((800,600)) #ecranul
pygame.display.set_caption('Floare') #titlul ferestrei
gameIcon = pygame.image.load('gameicon.png') #iconita jocului
pygame.display.set_icon(gameIcon) 


# generarea fisierului highscore daca este nevoie
if os.path.isfile('highscore.txt') == False:
    f = open('highscore.txt','w')
    f.write('0')
    f.close()

backgroundImg = pygame.image.load('imgs\\bg\\background.png') #se incarca imaginea intr-o variabila pentru a fi afisata la nevoie



#variabilele necesare soarelui, imagine si coordonate
sun = pygame.image.load('imgs\\bg\\sun.png')
sunX = 0
sunSpeed = 1

# in functie de stagiu, variabila floareImg va primi valoarea corespunzatoare, default fiind valoarea 1
flowerStages = ['imgs\\flower\\stageOne.png', 'imgs\\flower\\stageTwo.png', 'imgs\\flower\\stageThree.png']
flowerXY = ((350,380), (350, 252), (350, 0))
flowerAge = 0

# cate zile au trecut; o zi inseamna parcurgerea ecranului de catre soare
# progresul este mecanica prin care floarea creste, totodata ofilindu-se daca ajunge sub 0
# se castiga progres prin simpla trecere a zilei si prin a colecta stropitori atunci cand apar. ratarea stropitorilor va scade din progres
daysPassed = 0
lifespan = 0
score = 0 # in score se va memora lifespan-ul maxim la care s-a ajuns
#sistemul de stropire
stropitoareImg = pygame.image.load('imgs\\pWatering\\stropitoare.png')
# in fiecare zi, este o sansa de numar% ca o stropitoare sa apara random in joc intr-o anumita portiune a ecranului
# functia de mai jos este apelata dupa fiecare zi si stabileste daca ziua curenta va spawna o stropitoare, daca da
# va pune in stropitoareX si stropitoareY coordonate aleatorii si va face variabila folosita in if-ul de afisare in true
stropitoareX = 0
stropitoareY = 0
spawnStropitoare = False
def plasare_stropitoare():
    if random.randrange(1,100) <= 100:
        global spawnStropitoare
        global stropitoareX
        global stropitoareY
        spawnStropitoare = True
        stropitoareX = random.randrange(100,700)
        stropitoareY = random.randrange(100,500)

    

# desemnarea unui font
textFont = pygame.font.Font('freesansbold.ttf',16)
def gameStages(x, y):
    daysPassedDisplay = textFont.render("Day: " + str(daysPassed), True, (255, 255, 255))
    lifespanDisplay = textFont.render("Life: " + str(lifespan), True, (255, 255, 255))
    stagesDisplay = textFont.render("Flower Age: " + str(flowerAge + 1) + " / 3", True, (255, 255, 255))
    screen.blit(daysPassedDisplay, (x,y))
    screen.blit(lifespanDisplay,(x, y + 20))
    screen.blit(stagesDisplay,(x, y + 40))

# functia de game over, opreste soarele, prin urmare tot jocul. un text va aparea pe ecran pentru a reseta jocul
# odata ce lifespan == 0, tot jocul se reseteaza
textFontGameover = pygame.font.Font('freesansbold.ttf',40)
def game_over_screen():
    global sunSpeed
    global score
    sunSpeed = 0
    highscoreFILE = open('highscore.txt','r')
    hscore = highscoreFILE.readline()
    highscoreFILE.close()
    if int(hscore) < score:
        highscoreFILE = open('highscore.txt','w')
        hscore = str(score)
        highscoreFILE.write(str(score))
        highscoreFILE.close()
    
    screen.blit(textFontGameover.render("          PLANTA S-A OFILIT!", True, (255,0,0)), (100,220))
    screen.blit(textFontGameover.render("Apasa tasta R pentru a reseta jocul", True, (255,0,0)), (80,280))
    screen.blit(textFont.render("Scorul actual: " + str(score), True, (255,0,0)), (10,460))
    screen.blit(textFont.render("Highscore actual: " + str(hscore), True, (255,0,0)), (10,480))

gameRunning = True
gameOver = False

def reset_game():
    global sunSpeed
    global spawnStropitoare
    global gameOver
    global flowerAge
    global sunX
    global daysPassed
    global score
    score = 0
    daysPassed = 0
    sunX = -200
    gameOver = False
    sunSpeed = 1
    flowerAge = 0



while gameRunning:
    for event in pygame.event.get(): #events
        if event.type == pygame.QUIT: 
            gameRunning = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and gameOver:
            reset_game()
    
    screen.fill((0,0,0))
    screen.blit(backgroundImg,(0,0))
    screen.blit(sun,(sunX,0))
    sunX += sunSpeed
    if sunX > 800: #daca soarele iese din ecran, va iesi din stanga dinou
        sunX = -200
        daysPassed += 1
        lifespan += 1
        score = max(lifespan,score)
        stropitoareReroll = True
        if flowerAge == 2:
            sunSpeed += 0.05
        plasare_stropitoare()





    if lifespan <= 30: #cum lifespan poate sa scada, dar flowerage nu, trebuie sa ma asigur ca nu apar probleme
        flowerAge = max(int(lifespan / 15), flowerAge)
    else:
        flowerAge = 2

    

    screen.blit(pygame.image.load(flowerStages[flowerAge]),flowerXY[flowerAge])
    

    
    if spawnStropitoare:
        screen.blit(stropitoareImg, (stropitoareX,stropitoareY))
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseDistance = math.isqrt(pow(mouseX - (stropitoareX + 42),2) + pow(mouseY - (stropitoareY + 37),2))
        stropitoareColectata = False
        if event.type == MOUSEBUTTONDOWN and mouseDistance <= 70:
            stropitoareColectata = True
            spawnStropitoare = False
            if flowerAge == 2:
                lifespan += int(lifespan * 0.05)
            lifespan += 3
        score = max(score,lifespan)

        if stropitoareColectata == False and sunX >= 200:
            spawnStropitoare = False
            if lifespan - 30 <= 0:
                lifespan = 0
                gameOver = True
            else:
                lifespan -= 30

            
        
        
    if gameOver:
        game_over_screen()
    gameStages(10,400)

    pygame.display.update()

