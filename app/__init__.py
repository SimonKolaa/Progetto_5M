#Application Factory Pattern 

import os
from flask import Flask

def create_app():
    #Creo l'istanza di Flask
    app = Flask(__name__, instance_relative_config=True)

    #Configurazione di base
    app.config.from_mapping(
        SECRET_KEY='dev',  #in produzione va cambiata!
        DATABASE=os.path.join(app.instance_path, 'walletwise.sqlite'),
    )

    #in modo che la cartella instance esista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #inizializza database (02_DB_e_Repository.md)
    from . import db
    db.init_app(app)

    #registrazione Blueprints (03_Blueprints_e_Routing.md)
    from . import auth
    from . import main
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)

    return app
