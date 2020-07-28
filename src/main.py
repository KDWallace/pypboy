import pygame, json, os
import config as CON

#obtains path used for files
PATH = (os.path.dirname(os.path.realpath(__file__)))[:-4]

class MissingFileError(Exception):
    """Exception raised when an essential file is missing from the expected directory
    Attributes:
        directory -- directory that caused error
    """

    def __init__(self, directory, message='Essential file missing from directory'):
        self.directory = directory
        super().__init__(message)

    def __str__(self):
        return f'("{self.directory}" could not be found)'




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
            raise AttributeError(f'{self.current} module missing draw(display) function')
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
        self.title        = args[0]
        self.items        = {}
        self.current_item = 0
        self.font         = pygame.font.Font(CON.TEXT_FONT,CON.TEXT_SIZE)
        self.items_DIR    = f'{PATH}\\resources\\data\\{args[0]}.json'

        #allows for override in config and checks if chosen file exists
        try:
            if os.path.isfile(f'{CON.PATH}\\{args[0]}.json'):
                self.items_DIR = f'{CON.PATH}\\{args[0]}.json'
            elif not(os.path.isfile(self.items_DIR)):
                raise MissingAttributeError(self.items_DIR,f'Missing file: {args[0]}.json')

        except:
            if not(os.path.isfile(self.items_DIR)):
                raise MissingFileError(self.items_DIR,f'Missing file: {args[0]}.json')

        self.get_items()

    #obtains item data
    def get_items(self):
        with open(self.items_DIR,'r') as f:
            print(self.items_DIR)
            self.items = json.load(f)

    #saves item data
    def set_items(self):
        with open(self.items_DIR,'w') as f:
            json.dump(self.items,f,indent=4)

    #selects/deselects current item
    def select_current(self):
        if 'selected' in self.items[self.current_item]:
            self.items[self.current_item]['selected'] = not(self.items[self.current_item]['selected'])
        else:
            self.items[self.current_item]['selected'] = True

    #function called in Engine.refresh()
    def draw(display):
        if len(self.items) < 10:
            posY = CON.BOARDER_SPACE
            for item in self.items:
                string = self.font.render(item.name,False,CON.TEXT_COLOUR)
                #display.blit(string,)

#initialisation
pygame.init()

#testing submodules
itemsModule = []
subnames = ['weapons','apparel','aid','misc','ammo']
for i in subnames:
    itemsModule.append(SubModule(i))


pipboy = Engine(Module('ITEMS',itemsModule))
while True:
    pipboy.refresh()
