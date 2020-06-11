from __future__ import print_function
from tensorflow.keras.models import load_model
import random
import numpy as np
import curses
import json

cat_image = '    /\_____/\\\n' + \
            '   /  o   o  \\\n' + \
            '  ( ==  ^  == )\n' + \
            '   )         (\n' + \
            '  (           )\n' + \
            ' ( (  )   (  ) )\n' + \
            '(__(__)___(__)__)\n'

BASE_DIR = '/Users/dmytromindra/Projects/prj-nlp-2020/students/DmytroMindra/00-capstone/'


def get_random_sample(X, y):
    range_start = random.randrange((len(X)))
    return X[range_start:range_start + 4], y[range_start:range_start + 4], range(range_start, range_start + 4)


def get_question_form_data(question, support, answers, correct_answer, predicted_answer):
    form_data = {}

    form_data['question'] = question
    form_data['support'] = support
    form_data['answers'] = answers
    form_data['predicted_label'] = predicted_answer
    form_data['correct_label'] = correct_answer

    return form_data


def draw_static_main_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas

    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Initialization
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Declaration of strings
    title = "Capstone Project"[:width - 1]
    subtitle = "Factual Question Answering"[:width - 1]
    author = "by Dmytro Mindra"[:width - 1]
    keystr = "Press any key to start"[:width - 1]
    statusbarstr = "Press 'q' to exit"

    # Centering calculations
    start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
    start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
    start_x_author = int((width // 2) - (len(author) // 2) - len(author) % 2)

    start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
    start_y = int((height // 2) - 2)

    # Rendering some text
    whstr = "Width: {}, Height: {}".format(width, height)
    stdscr.addstr(0, 0, whstr, curses.color_pair(1))

    # Render status bar
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height - 1, 0, statusbarstr)
    stdscr.addstr(height - 1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
    stdscr.attroff(curses.color_pair(3))

    # Turning on attributes for title
    stdscr.attron(curses.color_pair(2))
    stdscr.attron(curses.A_BOLD)

    # Rendering title

    cat_image_lines = cat_image.splitlines()
    #print (len(cat_image_lines))
    for i in range(len(cat_image_lines)):
        cat_x = int((width // 2) - ((len(cat_image_lines[0])) // 2) - len(title) % 2)-2
        cat_y = start_y+i-len(cat_image_lines)-1
        stdscr.addstr(cat_y, cat_x, cat_image_lines[i].rstrip("\n"))



    stdscr.addstr(start_y, start_x_title, title)

    # Turning off attributes for title
    stdscr.attroff(curses.color_pair(2))
    stdscr.attroff(curses.A_BOLD)


    # Print rest of text
    stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
    stdscr.addstr(start_y + 2, start_x_author, author)
    stdscr.addstr(start_y + 4, (width // 2) - 2, '-' * 4)
    stdscr.addstr(start_y + 6, start_x_keystr, keystr)
    # stdscr.move(cursor_y, cursor_x)

    # Refresh the screen
    stdscr.refresh()


def text_to_lines(text, width):
    lines = []
    tokens = text.split()
    current_line = ''
    for token in tokens:
        current_line = ' '.join([current_line, token]).strip()
        if len(current_line) > width:
            lines.append(current_line)
            current_line = ''

    if len(current_line) > 0:
        lines.append(current_line)
    return lines


def draw_interactive_question_screen(stdscr, form_data):
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Initialization
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Declaration of strings
    question_length = int(width // 3)
    question = text_to_lines(form_data['question'], question_length)

    support_text = form_data['support'][:question_length*8]
    if support_text=='':
        support_text = '404 - no support text provided :((('

    support = text_to_lines(support_text, question_length)

    # Turning on attributes for title
    stdscr.attron(curses.color_pair(2))
    stdscr.attron(curses.A_BOLD)

    start_y = int((height // 4) - 2)

    for i in range(len(question)):
        # Centering calculations
        start_x_question = int((width // 2) - (len(question[i]) // 2) - len(question[i]) % 2)
        stdscr.addstr(start_y + i, start_x_question, question[i])

    start_y += len(question)

    statusbarstr = "Press 'q' to exit"

    # Turning off attributes for title
    stdscr.attroff(curses.color_pair(2))
    stdscr.attroff(curses.A_BOLD)

    answers = form_data['answers']

    for i in range(len(answers)):
        answer = answers[i]

        stdscr.addstr(start_y + 1 + i // 2, width // 3 + (width // 4) * (i % 2), '{}. {}'.format(i, answer))

    predicted = form_data['predicted_label']
    correct = form_data['correct_label']
    stdscr.move(0, 0)

    stdscr.getch()

    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(start_y + 1 + predicted // 2, width // 3 + (width // 4) * (predicted % 2) - 4, '->')
    stdscr.attroff(curses.color_pair(1))

    stdscr.addstr(start_y + 4, width // 3, '-> predicted answer')

    stdscr.move(0, 0)

    stdscr.getch()
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(start_y + 1 + correct // 2, width // 3 + (width // 4) * (correct % 2) - 2, '*')
    stdscr.attroff(curses.color_pair(2))
    stdscr.addstr(start_y + 5, width // 3, '* correct answer')

    stdscr.getch()
    #print support

    stdscr.attron(curses.color_pair(4))
    for i in range(len(support)):
        # Centering calculations
        start_x_support = int((width // 2) - (len(support[i]) // 2) - len(support[i]) % 2)
        stdscr.addstr(start_y + 7 + i, start_x_support, support[i])
    stdscr.attroff(curses.color_pair(4))

    stdscr.move(0, 0)
    stdscr.refresh()


def main():
    with open(BASE_DIR + 'data/test-data-vectorized.txt') as json_file:
        data = json.load(json_file)

    test_vectorized_data = []
    for data_item in data['vectorized_data']:
        test_vectorized_data.append(np.array(data_item))

    test_form_data = data['form_data']
    test_correct = data['correct']

    model = load_model(BASE_DIR + 'qa_model_rev3')

    X = test_vectorized_data
    y = test_correct

    stdscr = curses.initscr()
    draw_static_main_menu(stdscr)

    k = ''
    stdscr.getch()

    while k != 113:
        X_sample, y_sample, ids = get_random_sample(X, y)
        y_prob = model.predict(np.array(X_sample))
        y_classes = y_prob.argmax(axis=-1)

        selected_question = random.randrange(4)
        predicted_label = y_classes[selected_question]
        question_id = ids[selected_question]
        data = test_form_data[question_id]

        correct_answer = y_sample[selected_question]
        predicted_answer = y_classes[selected_question]

        form_data = get_question_form_data(data['question'], data['support'], data['answers'], correct_answer,
                                           predicted_answer)

        draw_interactive_question_screen(stdscr, form_data)

        k = stdscr.getch()
    stdscr.clear()


if __name__ == "__main__":
    main()
