import pygame, json
import config as CON


class Engine():
    def __init__(self,*args,**kwargs):
        #initialisation
        self.display = pygame.display.set_mode(CON.SIZE)
        pygame.display.set_caption(CON.TITLE)
        self.clock   = pygame.time.Clock()

        #modules loaded and position of loading list
        self.modules = args
        self.current = 0

    #refresh function
    def refresh(self):
        #checks if draw function exists for module
        if hasattr(self.modules[self.current],'draw'):
            self.modules[self.current].draw(self.display)
        #raises error if function is missing
        else:
            raise MissingAttributeError(f'{self.current} module missing draw(display) function')
        #refreshes the display
        pygame.display.flip()
        self.clock.tick(24)

class Module():
    def __init__(self,*args,**kwargs):
        #takes two arguments, first is the name and second is the list of submodules
        self.title      = args[0]
        self.subModules = args[1]
        self.font       = pygame.font.Font(CON.TEXT_FONT,CON.TEXT_SIZE)
        #current submodule selected
        self.current    = 0

    #function called in Engine.refresh()
    def draw(self,display):
        length = 0
        for item in self.subModules:
            string = self.font.render(item.title,False,(0,0,0))
            length += string.get_width()
        seps = int((CON.SIZE[0]-(len(self.subModules)*2*CON.BOX_SPACE) + CON.BOARDER_SPACE*2)/(len(self.subModules)+1))

        i = 0
        x = seps + CON.BOARDER_SPACE
        for item in self.subModules:
            string = self.font.render(item.title,False,CON.TEXT_COLOUR)
            display.blit(string,(x,CON.SIZE[1]-CON.BOARDER_SPACE*2-string.get_height()))
            i += 1
            x += seps + CON.BOX_SPACE
        
class SubModule():
    def __init__(self,*args,**kwargs):
        self.title = args[0]
        #self.items_DIR = args[1]
        self.items = {}
        self.current_item = 0
        self.font = pygame.font.Font(CON.TEXT_FONT,CON.TEXT_SIZE)

    def get_items(self):
        with open(self.items_DIR,'r') as f:
            self.items = json.load(f)

    def set_items(self):
        with open(self.items_DIR,'w') as f:
            json.dump(self.items,f,indent=4)

    def select_current(self):
        if 'selected' in self.items[self.current_item]:
            self.items[self.current_item]['selected'] = not(self.items[self.current_item]['selected'])
        else:
            self.items[self.current_item]['selected'] = True

    def draw(display):
        if len(self.items) < 10:
            posY = CON.BOARDER_SPACE
            for item in self.items:
                string = self.font.render(item.name,False,CON.TEXT_COLOUR)
                #display.blit(string,)

pygame.init()
itemsModule = []
subnames = ['Weapons','Apparel','Aid','Misc','Ammo']
for i in subnames:
    itemsModule.append(SubModule(i))


pipboy = Engine(Module('ITEMS',itemsModule))
while True:
    pipboy.refresh()
