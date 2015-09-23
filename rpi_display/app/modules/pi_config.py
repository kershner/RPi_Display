from flask import request, json, session
from urllib2 import quote
import os

file_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.dirname(os.path.dirname(os.path.abspath(file_path)))
urls_path = os.path.join(config_path, 'urls')


# Initalizes session variables, returns variables for display in template
def pi_config_main():
    session['prev'] = -1
    session['prev_stop'] = -2
    session['prev_start'] = 3

    with open('%s/all_urls.txt' % urls_path, 'r') as urls_file:
        main_urls_list = list(urls_file)

    with open('%s/animals_urls.txt' % urls_path, 'r') as urls_file:
        animals_urls_list = list(urls_file)

    with open('%s/gaming_urls.txt' % urls_path, 'r') as urls_file:
        gaming_urls_list = list(urls_file)

    with open('%s/strange_urls.txt' % urls_path, 'r') as urls_file:
        strange_urls_list = list(urls_file)

    with open('%s/educational_urls.txt' % urls_path, 'r') as urls_file:
        educational_urls_list = list(urls_file)

    with open('%s/pi_display_config.txt' % config_path, 'r') as config_file:
        config = list(config_file)

    data = {
        'main_urls_count': len(main_urls_list),
        'animals_urls_count': len(animals_urls_list),
        'gaming_urls_count': len(gaming_urls_list),
        'strange_urls_count': len(strange_urls_list),
        'educational_urls_count': len(educational_urls_list),
        'category': config[0][:config[0].find('\n')],
        'current_gif': config[1][:config[1].find('\n')],
        'delay': config[2][:config[2].find('\n')]
    }

    return data


# AJAX call to update config site to currently playing GIF
def pi_config_update():
    session['prev'] = -1

    with open('%s/pi_display_config.txt' % config_path, 'r') as config_file:
        config = list(config_file)
        current_gif = config[1][:config[1].find('\n')]
        message = 'Currently Playing GIF'
        data = {
            'current_gif': current_gif,
            'message': message
        }

        return data


# AJAX call when 'previous GIF' is clicked
def get_prev():
    session['prev'] -= 1

    with open('%s/last_played.txt' % urls_path, 'a+') as f:
        last_played_list = list(f)
        gifs = last_played_list[int('%d' % session['prev'])][:last_played_list[int('%d' % session['prev'])].find('\n')]
        message = 'Previous GIF'
        data = {
            'last_played': gifs,
            'message': message
        }

        return data


# Sets auto-update
def set_auto_update():
    with open('%s/pi_display_config.txt' % config_path, 'r') as config_file:
        config = list(config_file)
        delay = config[2][:config[2].find('\n')]
        data = {
            'delay': delay + '000'
        }

        return data


# Set category
def set_category():
    category = request.args.get('category', 0, type=str)

    with open('%s/pi_display_config.txt' % config_path, 'r') as config_file:
        config = list(config_file)
        delay = config[2][:config[2].find('\n')]

    with open('%s/pi_display_config.txt' % config_path, 'w+') as config_file:
        config_file.write('%s' % category + '\n')
        config_file.write(config[1])
        config_file.write(config[2])
        message = 'Category changed to %s' % category.title()
        data = {
            'message': message,
            'category': category.title(),
            'delay': delay
        }

        return data


# Set refresh delay
def set_delay():
    delay = request.args.get('delay', 0, type=str)

    with open('%s/pi_display_config.txt' % config_path, 'r') as config_file:
        config = list(config_file)
        category = config[0][:config[0].find('\n')]

    with open('%s/pi_display_config.txt' % config_path, 'w+') as config_file:
        config_file.write(config[0])
        config_file.write(config[1])
        config_file.write('%s' % delay + '\n')
        message = 'Delay changed to %s seconds' % delay
        data = {
            'message': message,
            'category': category.title(),
            'delay': delay
        }

        return data


# Get 5 previous GIFs
def get_previous_gifs():
    session['prev_stop'] -= 5
    session['prev_start'] -= 5

    with open('%s/last_played.txt' % urls_path, 'a+') as f:
        last_played_list = list(f)
        prev_5 = ''.join(last_played_list[session['prev_start']:session['prev_stop']:-1]).split()
        data = {
            'prev_5': prev_5,
            'id': session['prev_start']
        }

        return data


# Get any number of previous GIFs
def get_last_played(number):
    number = 0 - int(number)

    with open('%s/last_played.txt' % urls_path, 'r') as f:
        last_played_list = list(f)
        gifs = ''.join(last_played_list[-2:number - 2:-1]).split()
        data = {
            'gifs': gifs
        }

        return data


# Clear session (mostly for removing auto-update)
def clear():
    session['prev_stop'] = -2
    session['prev_start'] = 3
    message = 'Session cleared'
    data = {
        'message': message
    }

    return data


# Return mailto link containing saved GIFs
def get_email_link():
    email = request.args.get('email', 0, type=str)
    gifs = json.loads(request.args.get('images', 0, type=str))
    subject = 'Your Saved GIFs'
    gifs = '\n'.join(gifs)
    body = '%s' % gifs
    link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
    data = {
        'link': link
    }

    return data