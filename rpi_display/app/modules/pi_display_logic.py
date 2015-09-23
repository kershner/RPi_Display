import random
import os


def pi_display_main():
    file_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.dirname(os.path.dirname(os.path.abspath(file_path)))
    urls_path = os.path.join(config_path, 'urls')

    # Open config file, grab variables from it
    with open('%s/pi_display_config.txt' % config_path, 'r') as config_file:
        config = list(config_file)

    category = config[0][:config[0].find('\n')]
    delay = config[2][:config[2].find('\n')]
    filename = category + '_urls.txt'
    toplay_filename = category + '_urls_to_play.txt'

    with open('%s/%s' % (urls_path, filename), 'r') as urls_file:
        urls_list = list(urls_file)

    with open('%s/%s' % (urls_path, toplay_filename), 'r') as urls_toplay_file:
        urls_toplay_list = list(urls_toplay_file)

    # If there are no more URLs in the to_play file, create a new one
    if len(urls_toplay_list) > 1:
        pass
    else:
        urls_toplay_file = open('%s/%s' % (urls_path, toplay_filename), 'a+')
        for entry in urls_list:
            urls_toplay_file.write(entry)
        urls_toplay_file.close()

    # Choose random URL from to_play list, writing to config file
    gif_url = random.choice(urls_toplay_list)
    with open('%s/pi_display_config.txt' % config_path, 'w+') as config_file:
        config_file.write(config[0])
        config_file.write('%s' % gif_url)
        config_file.write(config[2])

    # Open/close to_play_urls.txt (taking advantage of side effect to erase contents)
    open('%s/%s' % (urls_path, toplay_filename), 'w').close()

    # Rewrite to_play.txt without current gif URL (won't play twice)
    with open('%s/%s' % (urls_path, toplay_filename), 'a+') as urls_to_play:
        for entry in urls_toplay_list:
            if entry == gif_url:
                continue
            else:
                urls_to_play.write(entry)

    # Add currently playing GIF to last_played file
    with open('%s/last_played.txt' % urls_path, 'a+') as f:
        f.write(gif_url)

    delay = str(delay) + '000'

    data = {
        "URL": gif_url,
        "delay": delay
    }

    return data