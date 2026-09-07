import FreeSimpleGUI as sg
from game.game import Game


class GUI():
    def __init__(self, game: Game):
        self.game = game
        self.window = self.create_window(game)
        self.valid_directions = ['south', 'north', 'east', 'west']

    def create_window(self, game):
        """Create and return the main application window.

        The left area is a coloured `sg.Graph` element used to represent the current location.
        The right area shows the description and a text input.
        """
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
                100, 4), font='Any 12', key='-OUTPUT-')],
            [command_col],
        ]
        return sg.Window('Adventure Game', layout, size=(400, 200))

    def run(self):
        while True:
            event, values = self.window.read()
            if event == 'Enter':
                command_complete = False
                output_message = self.game.get_current_location().story

                input = values['-IN-'].lower()

                if input in self.valid_directions:
                    output_message = self.game.validate_move(input)

                    command_complete = True

                if command_complete:
                    self.window['-OUTPUT-'].update(
                        value=str(self.game.player) +
                        '\n' + output_message
                    )
                    self.window['-IN-'].update(value='')
                    output_message = ''

                # Update the image to reflect the new location.
                self.window['-IMG-'].update(filename=self.game.get_current_location().image)


            elif event == 'Exit' or event is None or event == sg.WIN_CLOSED:
                break
        self.window.close()
