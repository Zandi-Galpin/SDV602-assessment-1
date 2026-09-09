import FreeSimpleGUI as sg
from game.game import Game
from game.command_parser import CommandParser


class GUI():
    def __init__(self, game: Game):
        self.game = game
        self.parser = CommandParser(game)
        self.window = self.create_window(game)

    def create_window(self, game):
        """Create and return the main application window."""
        sg.theme('Dark Blue 3')

        prompt_input = [
            sg.Text('Enter your command', font='Any 14'),
            sg.Input(key='-IN-', size=(20, 1), font='Any 14'),
        ]
        buttons = [sg.Button('Enter', bind_return_key=True), sg.Button('Exit')]
        command_col = sg.Column([prompt_input, buttons],
                                element_justification='r')

        img = sg.Image(filename=game.get_current_location().image, key='-IMG-')

        layout = [
            [img, sg.Text('HP: ' + str(game.player.health_current) + '/' + str(game.player.health_max) +
                            ' DMG: ' + str(game.player.damage) + ' BLOCK: ' + str(game.player.block) +
                            '\n' +
                            str(game.get_current_location().story), size=(
                100, 10), font='Any 12', key='-OUTPUT-')],
            [command_col],
        ]
        return sg.Window('Adventure Game', layout, resizable=True)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == 'Enter':
                raw_input = values['-IN-']
                output_message = self.parser.execute(raw_input)

                self.window['-OUTPUT-'].update(
                    value=str(self.game.status.summary_line()) + '\n' + output_message
                )
                self.window['-IN-'].update(value='')
                self.window['-IMG-'].update(filename=self.game.get_current_location().image)

            elif event == 'Exit' or event is None or event == sg.WIN_CLOSED:
                break
        self.window.close()
