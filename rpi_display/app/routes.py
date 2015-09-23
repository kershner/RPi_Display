from modules import pi_config, pi_display_logic
from flask import render_template, jsonify
from app import app


@app.route('/')
def index():
    return render_template('/pi_display.html')


@app.route('/pi_display_json')
def pi_display_json():
    data = pi_display_logic.pi_display_main()
    return jsonify(data)


##############################################################################
# Pi Display Config ##########################################################
@app.route('/config')
def pi_display_config():
    data = pi_config.pi_config_main()
    return render_template('pi_display_config.html',
                           current_gif=data['current_gif'],
                           main_urls_count=data['main_urls_count'],
                           animals_urls_count=data['animals_urls_count'],
                           gaming_urls_count=data['gaming_urls_count'],
                           strange_urls_count=data['strange_urls_count'],
                           educational_urls_count=data['educational_urls_count'],
                           category=data['category'].title(),
                           delay=data['delay'])


@app.route('/pi-display-config-update')
def pi_display_config_update():
    data = pi_config.pi_config_update()
    return jsonify(data)


@app.route('/pi-display-config-prev')
def pi_display_config_prev():
    data = pi_config.get_prev()
    return jsonify(data)


@app.route('/pi-display-config-auto')
def pi_display_config_auto():
    data = pi_config.set_auto_update()
    return jsonify(data)


@app.route('/pi-display-config-categories')
def pi_display_config_all():
    data = pi_config.set_category()
    return jsonify(data)


@app.route('/pi-display-config-delay')
def pi_display_config_delay():
    data = pi_config.set_delay()
    return jsonify(data)


@app.route('/previous-gifs')
def previous_gifs():
    data = pi_config.get_previous_gifs()
    return jsonify(data)


@app.route('/last-played/<number>')
def last_played(number):
    data = pi_config.get_last_played(number)
    return jsonify(data)


@app.route('/clear-session')
def clear_session():
    data = pi_config.clear()
    return jsonify(data)


@app.route('/email-gifs')
def email_gifs():
    data = pi_config.get_email_link()
    return jsonify(data)
