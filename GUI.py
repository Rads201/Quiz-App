import FreeSimpleGUI as sg
import time
import zmq
import random
import json

start_layout = [[sg.Text('Press a Button to Start a Quiz', font=("Comic Sans MS", 20))],
                [sg.Button('Standard Quiz', font=("Comic Sans MS", 20)),
                 sg.Button('Custom Quiz', font=("Comic Sans MS", 20)),
                 sg.Button('Math Quiz', font=("Comic Sans MS", 20))],
                [sg.Text('Press a Button to Create or Delete a Custom Quiz', font=("Comic Sans MS", 20))],
                [sg.Button('Create Quiz', font=("Comic Sans MS", 20)), sg.Button('Delete Quiz',
                                                                                 font=("Comic Sans MS", 20))]]

start_layout1 = [[sg.VPush()],
                 [sg.Push(), sg.Column(start_layout, element_justification='c'), sg.Push()],
                 [sg.VPush()]]

# Start Screen -----------------------------------------------------------------------
window = sg.Window('Start Screen', start_layout1, size=(750, 500), resizable=True)

while True:
    start_event, start_values = window.read()
    if start_event == sg.WINDOW_CLOSED:
        break

    print(start_event)

    # Create Quiz Option
    if start_event == 'Create Quiz':

        count = 0
        questions = []
        options = []
        answers = []

        create_layout = [[sg.Text('Enter your question, multiple choice options, and correct answer.',
                                  font=("Comic Sans MS", 12))],
                         [sg.Text('Question: ', font=("Comic Sans MS", 12)), sg.InputText(key='question')],
                         [sg.Text('Option 1: ', font=("Comic Sans MS", 12)), sg.InputText(key='option1')],
                         [sg.Text('Option 2: ', font=("Comic Sans MS", 12)), sg.InputText(key='option2')],
                         [sg.Text('Option 3: ', font=("Comic Sans MS", 12)), sg.InputText(key='option3')],
                         [sg.Text('Option 4: ', font=("Comic Sans MS", 12)), sg.InputText(key='option4')],
                         [sg.Text('Which is the correct answer?', font=("Comic Sans MS", 12))],
                         [sg.Radio('Option 1', 'Question_1', default=False, font=("Comic Sans MS", 12),
                                   key='radio1')],
                         [sg.Radio('Option 2', 'Question_1', default=False, font=("Comic Sans MS", 12),
                                   key='radio2')],
                         [sg.Radio('Option 3', 'Question_1', default=False, font=("Comic Sans MS", 12),
                                   key='radio3')],
                         [sg.Radio('Option 4', 'Question_1', default=False, font=("Comic Sans MS", 12),
                                   key='radio4')]]

        create_layout1 = [[sg.VPush()],
                          [sg.Push(), sg.Column(create_layout, element_justification='c'), sg.Push()],
                          [sg.VPush()], [sg.Push(), sg.Button('Next', font=("Comic Sans MS", 20), key='Next')]]

        # Create Screen ------------------------------------------------------------------------------
        create_window = sg.Window('Create Quiz', create_layout1, size=(750, 500), resizable=True)

        while count < 5:

            create_event, create_values = create_window.read()
            if create_event == sg.WINDOW_CLOSED:
                create_window.close()
                break

            questions.append(create_values['question'])
            options.append([create_values['option1'], create_values['option2'], create_values['option3'],
                            create_values['option4']])

            if create_values['radio1'] is True:
                answers.append(0)
            elif create_values['radio2'] is True:
                answers.append(1)
            elif create_values['radio3'] is True:
                answers.append(2)
            elif create_values['radio4'] is True:
                answers.append(3)

            if create_event == 'Next':
                count += 1
                create_window['question'].update('')
                create_window['option1'].update('')
                create_window['option2'].update('')
                create_window['option3'].update('')
                create_window['option4'].update('')
                create_window['radio1'].update(False)
                create_window['radio2'].update(False)
                create_window['radio3'].update(False)
                create_window['radio4'].update(False)

        file = open("Custom Quiz.txt", "w")

        for line in range(5):
            file.write(questions[line] + '\n')
            file.write(options[line][0] + ', ' + options[line][1] + ', ' + options[line][2] + ', ' + options[line][3]
                       + '\n')
            if line != 4:
                file.write(str(answers[line]) + '\n')
            else:
                file.write(str(answers[line]))

        file.close()

        # Close the Create Window
        create_window.close()

    # Delete Quiz Option
    if start_event == 'Delete Quiz':

        open('Custom Quiz.txt', 'w').close()

        delete_layout = [[sg.Text('The Custom Quiz has been Deleted!', font=("Comic Sans MS", 20))],
                         [sg.Button('Home', font=("Comic Sans MS", 20))]]

        delete_layout1 = [[sg.VPush()],
                          [sg.Push(), sg.Column(delete_layout, element_justification='c'), sg.Push()],
                          [sg.VPush()]]

        # Create Screen ------------------------------------------------------------------------------
        delete_window = sg.Window('Create Quiz', delete_layout1, size=(750, 500), resizable=True)

        delete_event, delete_values = delete_window.read()
        if delete_event == 'Home' or delete_event == sg.WINDOW_CLOSED:
            delete_window.close()

    # Math Quiz Option
    if start_event == 'Math Quiz':
        force_continue = False
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:3000")

        random_num = random.randint(0, 2)
        categories = ["addition", "subtraction", "multiplication"]
        socket.send_string(categories[random_num])
        received = json.loads(socket.recv_json())

        problems = []
        correct_answers = []

        for problem in received:
            problems.append(problem)
            correct_answers.append(str(received[problem]))

        count = 0
        responses = [None for x in range(len(problems))]

        math_layout = [[sg.Push(), sg.Text(problems[count], font=("Comic Sans MS", 20), key='text'), sg.Push()],
                       [sg.Text('Answer:', font=("Comic Sans MS", 20)), sg.InputText(do_not_clear=False)]]

        layout_math = [[sg.VPush()],
                       [sg.Push(), sg.Column(math_layout), sg.Push()],
                       [sg.VPush()],
                       [sg.Button('Back', font=("Comic Sans MS", 20), key='Back'), sg.Push(),
                        sg.Button('Next', font=("Comic Sans MS", 20), key='Next')]]

        # Quiz Screen ------------------------------------------------------------------------------
        window_math = sg.Window('Quiz App', layout_math, size=(750, 500), resizable=True)

        while len(problems) > count >= 0:

            quiz_event, quiz_values = window_math.read()
            if quiz_event == sg.WINDOW_CLOSED:
                window_math.close()
                break

            responses[count] = quiz_values[0]

            if quiz_event == 'Next' and count < len(problems) - 1:
                count += 1
                window_math['text'].update(problems[count])

            elif quiz_event == 'Back' and count > 0:
                count -= 1
                window_math['text'].update(problems[count])

            elif quiz_event == 'Next' and (None in responses or "" in responses):

                confirm_layout = [[sg.Text('You have not answered all the questions.', font=("Comic Sans MS", 16))],
                                  [sg.Text('Do you still want to submit the quiz?', font=("Comic Sans MS", 16))],
                                  [sg.Button('Yes', font=("Comic Sans MS", 16)),
                                   sg.Button('No', font=("Comic Sans MS", 16))]]

                confirm_layout1 = [[sg.VPush()],
                                   [sg.Push(), sg.Column(confirm_layout, element_justification='c'), sg.Push()],
                                   [sg.VPush()]]

                # Confirmation Screen ----------------------------------------------------------------------------
                confirm_window = sg.Window('Confirmation', confirm_layout1, size=(750, 500))

                while True:
                    confirm_event, confirm_values = confirm_window.read()

                    if confirm_event == 'Yes':
                        confirm_window.close()
                        force_continue = True
                        break
                    elif confirm_event == 'No' or confirm_event == sg.WINDOW_CLOSED:
                        confirm_window.close()
                        break

            if (quiz_event == 'Next' and None not in responses and "" not in responses) or force_continue:
                time.sleep(1.0)

                correct = 0
                num_of_prob = len(correct_answers)

                for answer in range(num_of_prob):
                    if correct_answers[answer] == responses[answer]:
                        correct += 1

                end_layout = [[sg.Text('You got ' + str(correct) + '/' + str(num_of_prob) + ' questions right!',
                                       font=("Comic Sans MS", 20))]]

                end_layout1 = [[sg.VPush()],
                               [sg.Push(), sg.Column(end_layout, element_justification='c'), sg.Push()],
                               [sg.VPush()],
                               [sg.Button('Home', font=("Comic Sans MS", 20))]]

                # End Screen ----------------------------------------------------------------------------
                end_window = sg.Window('End Screen', end_layout1, size=(750, 500), resizable=True)

                end_event, end_values = end_window.read()
                window_math.close()

                if end_event == 'Home' or end_event == sg.WINDOW_CLOSED:
                    end_window.close()

    # Default Quiz Option
    if start_event == 'Standard Quiz' or start_event == 'Custom Quiz':
        force_continue = False

        if start_event == 'Standard Quiz':
            file = open("Standard Quiz.txt", "r")
        else:
            file = open("Custom Quiz.txt", "r")

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
        window_1 = sg.Window('Quiz App', layout_1, size=(750, 500), resizable=True)

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
                confirm_window = sg.Window('Confirmation', confirm_layout1, size=(750, 500))

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
                end_window = sg.Window('End Screen', end_layout1, size=(750, 500), resizable=True)

                end_event, end_values = end_window.read()
                window_1.close()

                if end_event == 'Home' or end_event == sg.WINDOW_CLOSED:
                    end_window.close()

window.close()
