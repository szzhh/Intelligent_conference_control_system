import pyautogui
pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

class EventAction:
    def __init__(self):
        pass

    def response(self, action, **params):
        '''
        action: 
            'next_page_of_ppt'
            'click'
            'keydown {key: value}'
            'text {content: value}'
            'volume_up'
            'volume_down'
            'video_forward'
            'video_backward'
        '''
        func_map = {
            'next_page_of_ppt': self.next_page_of_ppt,
            'last_page_of_ppt': self.last_page_of_ppt,
            'click': self.click,
            'keydown': self.keydown,
            'text': self.text,
            'exit': self.exit,
            'parse': self.parse,
            'move_mouse': self.move_mouse
        }
        f = func_map[action]
        print(params)
        return f(para=params)
    
    def next_page_of_ppt(self, **params):
        pyautogui.keyDown('down')

    def last_page_of_ppt(self, **params):
        pyautogui.keyDown('up') 

    def click(self, **params):
        pyautogui.click()

    def keydown(self, **params):
        pyautogui.keyDown(params['key'])

    def text(self, **params):
        pyautogui.typewrite(params['text'])

    def exit(self, **params):
        pyautogui.keyDown('esc')

    def parse(self, **params):
        pyautogui.keyDown('f5')

    def move_mouse(self, **params):
        size_x, size_y = pyautogui.size()
        print(size_x, size_y)
        pyautogui.moveTo( float(params['para']['para'][0]) * size_x,float(params['para']['para'][1]) * size_y)