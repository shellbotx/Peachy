import peachy


class TypeWorld(peachy.World):
    def __init__(self):
        super().__init__('test')
        self.typewriter = peachy.utils.TextCapture("Typing ")

    def render(self):
        peachy.graphics.set_color(255, 255, 255)
        peachy.graphics.draw_text(self.typewriter.value, 16, 16,
                                  font=peachy.fs.resources['Proggy'])
        self.typewriter.update()
        super().render()

game = peachy.Engine((320, 240), 'Typewriter Test')
peachy.fs.load_font('Proggy', '../peachy/fonts/ProggyClean.ttf', 16)
game.add_world(TypeWorld())
game.run()
