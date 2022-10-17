import PySimpleGUI as sg
import time

start_layout = [[sg.Text('Press Button to Start the Quiz', font=("Comic Sans MS", 20))],
                [sg.Button('Start', font=("Comic Sans MS", 20))]]

start_layout1 = [[sg.VPush()],
                 [sg.Push(), sg.Column(start_layout, element_justification='c'), sg.Push()],
                 [sg.VPush()]]

# Start Screen -----------------------------------------------------------------------
window = sg.Window('Start Screen', start_layout1, size=(750, 450), resizable=True)

while True:
    start_event, start_values = window.read()
    if start_event == sg.WINDOW_CLOSED:
        break

    if start_event == 'Start':
        force_continue = False

        file = open("Quiz 1.txt", "r")
        line_count = 0
        questions = []
        options = []
        answers = []

        while True:
            line = file.readline()
            if not line:
                break
            elif line_count % 3 == 0:
                line = line[:len(line) - 1]
                questions.append(line)
            elif line_count % 3 == 1:
                option = line.split(", ")
                option[3] = option[3][:len(option[3]) - 1]
                options.append(option)
            elif line_count % 3 == 2:
                line = int(line[0])
                answers.append(line)
            line_count += 1

        file.close()

        count = 0
        responses = [None for x in range(len(questions))]

        question_layout = [[sg.Text(questions[count], font=("Comic Sans MS", 20), key='text')],
                           [sg.Radio(options[count][0], 'Question_1', default=False, font=("Comic Sans MS", 12),
                                     key='radio1')],
                           [sg.Radio(options[count][1], 'Question_1', default=False, font=("Comic Sans MS", 12),
                                     key='radio2')],
                           [sg.Radio(options[count][2], 'Question_1', default=False, font=("Comic Sans MS", 12),
                                     key='radio3')],
                           [sg.Radio(options[count][3], 'Question_1', default=False, font=("Comic Sans MS", 12),
                                     key='radio4')]]

        layout_1 = [[sg.VPush()],
                    [sg.Push(), sg.Column(question_layout), sg.Push()],
                    [sg.VPush()],
                    [sg.Button('Back', font=("Comic Sans MS", 20), key='Back'), sg.Push(),
                     sg.Button('Next', font=("Comic Sans MS", 20), key='Next')]]

        # Quiz Screen ------------------------------------------------------------------------------
        window_1 = sg.Window('Quiz App', layout_1, size=(750, 450), resizable=True)

        while len(questions) > count >= 0:

            quiz_event, quiz_values = window_1.read()
            if quiz_event == sg.WINDOW_CLOSED:
                window_1.close()
                break

            if quiz_values['radio1'] is True:
                responses[count] = 0
            elif quiz_values['radio2'] is True:
                responses[count] = 1
            elif quiz_values['radio3'] is True:
                responses[count] = 2
            elif quiz_values['radio4'] is True:
                responses[count] = 3

            if quiz_event == 'Next' and count < len(questions) - 1:
                count += 1
                window_1['text'].update(questions[count])
                window_1['radio1'].update(False, text=options[count][0])
                window_1['radio2'].update(False, text=options[count][1])
                window_1['radio3'].update(False, text=options[count][2])
                window_1['radio4'].update(False, text=options[count][3])

            elif quiz_event == 'Back' and count > 0:
                count -= 1
                window_1['text'].update(questions[count])
                window_1['radio1'].update(False, text=options[count][0])
                window_1['radio2'].update(False, text=options[count][1])
                window_1['radio3'].update(False, text=options[count][2])
                window_1['radio4'].update(False, text=options[count][3])

            elif quiz_event == 'Next' and None in responses:

                confirm_layout = [[sg.Text('You have not answered all the questions.', font=("Comic Sans MS", 16))],
                                  [sg.Text('Do you still want to submit the quiz?', font=("Comic Sans MS", 16))],
                                  [sg.Button('Yes', font=("Comic Sans MS", 16)),
                                   sg.Button('No', font=("Comic Sans MS", 16))]]

                confirm_layout1 = [[sg.VPush()],
                                   [sg.Push(), sg.Column(confirm_layout, element_justification='c'), sg.Push()],
                                   [sg.VPush()]]

                # Confirmation Screen ----------------------------------------------------------------------------
                confirm_window = sg.Window('Confirmation', confirm_layout1, size=(750, 450))

                while True:
                    confirm_event, confirm_values = confirm_window.read()

                    if confirm_event == 'Yes':
                        confirm_window.close()
                        force_continue = True
                        break
                    elif confirm_event == 'No' or confirm_event == sg.WINDOW_CLOSED:
                        confirm_window.close()
                        break

            if (quiz_event == 'Next' and None not in responses) or force_continue:
                time.sleep(1.0)

                correct = 0
                num_of_prob = len(answers)

                for answer in range(num_of_prob):
                    if answers[answer] == responses[answer]:
                        correct += 1

                end_layout = [[sg.Text('You got ' + str(correct) + '/' + str(num_of_prob) + ' questions right!',
                                       font=("Comic Sans MS", 20))]]

                end_layout1 = [[sg.VPush()],
                               [sg.Push(), sg.Column(end_layout, element_justification='c'), sg.Push()],
                               [sg.VPush()],
                               [sg.Button('Home', font=("Comic Sans MS", 20))]]

                # End Screen ----------------------------------------------------------------------------
                end_window = sg.Window('End Screen', end_layout1, size=(750, 450), resizable=True)

                end_event, end_values = end_window.read()
                window_1.close()

                if end_event == 'Home' or end_event == sg.WINDOW_CLOSED:
                    end_window.close()

window.close()
