#in case of some weird bug happening, make sure csv, pkmn.txt, and pkmn.jpg files are deleted before retrying

##** make sure current directory is the outer pokedex folder before running! **##

import pygame
import os       #for running spider in terminal and deleting files
import csv      #for reading csv file
import re       #for replacing text
import urllib.request   #for getting img from url

######################################## FUNCTIONS ########################################

#create txt file (solution to not being able to import pkmn variable to pokedex_spider :,))
def create_txt(pkmn):
    pkmn_txt = open("pkmn.txt","w+")
    pkmn_txt.write(pkmn)    #write inputted pkmn name to file
    pkmn_txt.close()
    
#delete files
def delete_files(pkmn):
    #from GitHub https://stackoverflow.com/questions/10840533/most-pythonic-way-to-delete-a-file-which-may-not-exist
    try:
        os.remove(pkmn + ".csv")    #contains data
        os.remove("pkmn.txt")       #contains inputted pokemon name
        os.remove("pkmn.jpg")       #image of pokemon
    except OSError:     #occurs in the case of invalid input
        pass

#run the spider
def run_spider(pkmn):
    create_txt(pkmn)    #so that the spider can get input name
    os.system(f"scrapy crawl pokedex -o {pkmn}.csv") #run terminal command to crawl

#clean up the output
def clean(row, key):
    #if pokemon is genderless, there's no span tag (pokedex_spider)
    if "gender" in key and row[key]=="":
        row["h_gender"] = "Genderless"
    #original output is like "80 ,\n" so fix that
    elif "cycles" in key:
        row[key] = re.sub("[\s,]", "", row[key])    
    #adjust some weird chars
    row[key] = row[key].replace(",", ", ")      #add a space after commas
    row[key] = row[key].replace("Â", "")        #don't know what the Â represents so remove that
    row[key] = row[key].replace("â€²", "'")     # -> '
    row[key] = row[key].replace("â€³", '"')     # -> ""
    row[key] = row[key].replace("Ã©", "é")      #in the word "Pokémon"

#get picture of inputted pokemon
def get_img(nat):
    #from https://www.delftstack.com/howto/python/download-image-in-python/
    urllib.request.urlretrieve(f"https://www.serebii.net/pokemon/art/{nat}.png","pkmn.jpg")
    #different source because pokemondb gives 403 error 

#get data from csv file and return as list
def get_data(pkmn):
    with open(pkmn+".csv", newline="") as csvfile:        
        reader = csv.DictReader(csvfile)
        output = []
        for row in reader:      #row = dict
            for key in row:
                clean(row,key)              #remove some weird corrupted text
                output.append(row[key])     #append data
                if "national" in key:
                    get_img(row[key])       #create img file
        return output       #return list containing data

### FRONT-END RELATED FUNCTIONS ###
#mouse is clicking on which tab
def collide_which():
    if mx<270:          #left-most tab
        return ENTRY1
    elif mx<510:        #middle tab
        return ENTRY2
    elif mx>510:        #right-most tab
        return ENTRY3

#draw everything
def draw(status, screen):
    screen.blit(bgs[status],(0,0))  #blit bg according to status

    if status == SEARCH:
        input_box.draw(screen)      #draw search box

    elif status > ERROR:            #if one of the entries:
        name = MAIN_DATA_FONT.render(f"{pkmn.capitalize()}    {data[0]}", True, COLOUR)
        species = MAIN_DATA_FONT.render(data[2], True, COLOUR)
        screen.blit(name,(100,108))         #draw name + national number text
        screen.blit(species,(100,152))      #draw species text

        icon = pygame.image.load("pkmn.jpg")
        icon = pygame.transform.scale(icon, (235,235))
        screen.blit(icon, (92, 235))        #draw image of pokemon
        
        #draw each entry's respective text
        if status==ENTRY1:
            #draw types, height, weight, and abilities
            ty = DATA_FONT.render(data[1], True, COLOUR)
            ht = DATA_FONT.render(data[3], True, COLOUR)
            wt = DATA_FONT.render(data[4], True, COLOUR)
            ab = DATA_FONT.render(data[5], True, COLOUR)
            screen.blit(ty,(484,164))
            screen.blit(ht,(554,252))
            screen.blit(wt,(554,302))
            screen.blit(ab,(484,400))
        if status==ENTRY2:
            #draw egg groups, gender ratio, and egg cycles
            gr = DATA_FONT.render(data[6], True, COLOUR)
            ge = DATA_FONT.render(data[7], True, COLOUR)
            cy = DATA_FONT.render(data[8], True, COLOUR)
            screen.blit(gr,(484,182))
            screen.blit(ge,(484,278))
            screen.blit(cy,(484,374))
        if status==ENTRY3:
            #draw type weaknesses, resistances, and immunity
            we = DATA_FONT.render(data[9], True, COLOUR)
            re = DATA_FONT.render(data[10], True, COLOUR)
            im = DATA_FONT.render(data[11], True, COLOUR)
            screen.blit(we,(442,182))
            screen.blit(re,(442,278))
            screen.blit(im,(442,374))
            
######################################## CLASS (for search box) ########################################
class Box:
    def __init__(self):
        self.rect = pygame.Rect(105,250,400,65)     #box size
        self.text = ""                              #text that user is typing
        self.text_surface = SEARCH_FONT.render(self.text, True, COLOUR)     #text rendering

    def get_input(self):  #return inputted text
        output = self.text.replace(" ","-")     #replace spaces with hyphens
        self.text = ''                          #reset input text
        return output

    def write(self, evt):  #write text
        if evt.key == pygame.K_BACKSPACE:        #remove last letter
            self.text = self.text[:-1]    

        elif evt.key != pygame.K_RETURN and len(self.text)<20:  #add inputted letter (and make sure it's within character limit)
            self.text += evt.unicode       

        self.text_surface = SEARCH_FONT.render(self.text, True, COLOUR) #re-render text  

    def draw(self, screen):
        screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+18))  #draw text

#####################################################################################################
#####################################################################################################
pygame.init()
pygame.display.set_caption("POKEDEX") 
WIDTH, HEIGHT = 800, 600 
screen = pygame.display.set_mode((WIDTH,HEIGHT))

#set imgs
bgs   = [pygame.image.load("bgs/search.jpg").convert_alpha(), pygame.image.load("bgs/loading.jpg").convert_alpha(), pygame.image.load("bgs/error.jpg").convert_alpha(), pygame.image.load("bgs/entry1.jpg").convert_alpha(), pygame.image.load("bgs/entry2.jpg").convert_alpha(), pygame.image.load("bgs/entry3.jpg").convert_alpha()]
mask_imgs = [pygame.image.load("masks/mask_search.png").convert_alpha(),pygame.image.load("masks/mask_tab.png").convert_alpha(),pygame.image.load("masks/mask_back.png").convert_alpha()]
masks = []
for img in mask_imgs:
    masks.append(pygame.mask.from_surface(img))     #convert images to actual masks

#set fonts and colours
SEARCH_FONT = pygame.font.Font(None, 50)
MAIN_DATA_FONT = pygame.font.Font(None, 35)
DATA_FONT= pygame.font.Font(None, 25)
COLOUR = pygame.Color(19,19,19)

#status
SEARCH = 0
LOADING = 1
ERROR = 2
ENTRY1 = 3
ENTRY2 = 4
ENTRY3 = 5

#initialize variables
status = SEARCH     #set initial status 
input_box = Box()   #set input box
pkmn = ""           #set inpuuted pokemon name
data = []           #set list containing scraped data

clock = pygame.time.Clock()
running = True
################## Game Loop ##################
while running:
    mx, my = pygame.mouse.get_pos()     #mouse x and y pos
    mb = pygame.mouse.get_pressed()     #mouse click

    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:        #quit
            running = False
        
        if evt.type == pygame.KEYDOWN:

            if status == SEARCH:         #input text
                input_box.write(evt)       
                if evt.key == pygame.K_RETURN:     #return text on enter
                    pkmn = input_box.get_input()
                
            elif status > ERROR:      #for navigating between entries using arrow keys
                if evt.key == pygame.K_LEFT and status != ENTRY1:
                    status -= 1
                elif evt.key == pygame.K_RIGHT and status != ENTRY3:
                    status += 1 

        if status == SEARCH and mb[0]==1 and masks[0].get_at((mx,my))==1:  #return text on click
            pkmn = input_box.get_input()  
           
    if status == SEARCH:
        if len(pkmn) != 0:      #if input has been entered, go to loading screen
            status = LOADING
    
    elif status == LOADING:
        run_spider(pkmn)        #run the spider to fetch info
        data = get_data(pkmn)   #get the information as a list
        if len(data)==0:        #if info list is empty (ie spider couldn't get anything because the pokemon doesn't exist)
            status = ERROR      #go to error screen
        else: 
            data[3] = data[3].replace("\xa0", " ")      #fix the output (not sure why this happens)
            data[4] = data[4].replace("\xa0", " ")           
            status = ENTRY1                           

    elif status == ERROR:
        if mb[0] and masks[2].get_at((mx,my))==1:       #if user clicks the back-to-search button:
            delete_files(pkmn)                          #delete all the created files
            pkmn = ""                                   #reset the inputted pkmn name
            input_box = Box()                           #new input box
            status = SEARCH                             #back to search screen

    elif status > ERROR:                                #one of the entries
        if mb[0] and masks[2].get_at((mx,my))==1:       #if user clicks the back-to-search button, reset everything
            delete_files(pkmn)                          
            pkmn = ""           
            input_box = Box()   
            status = SEARCH

        if mb[0]==1 and masks[1].get_at((mx,my))==1:    #if clicking on tab mask
            status = collide_which()                    #check which tab user is clicking on & switch entries

    draw(status, screen)                                #draw everything

    pygame.display.flip()
    clock.tick(30)
    
delete_files(pkmn)                                      #delete created files
pygame.quit()