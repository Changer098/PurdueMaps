from flask import Flask, render_template, send_file, send_from_directory
from os import walk
import re
import json


class main:
    app = Flask(__name__)
    # PDF_LOCATION = "C:\\Users\\everettr\\Documents\\PDF\\"
    PDF_LOCATION = "/home/ryan/PDF/"
    buildings = dict()  # buildings -> list(tuple(floor, filename)
    jString = None
    matchReg = re.compile("[a-zA-Z]+-[a-zA-Z0-9]+")
    splitReg = re.compile("[-\.]")

    def __init__(self):
        # Get buildings and their floors
        files = self.getFiles()

        for file in files:
            if self.matchReg.match(file) is not None:
                # building - floor - pdf
                tokens = self.splitReg.split(file)
                if tokens[0].lower() not in self.buildings:
                    self.buildings[tokens[0].lower()] = list()
                self.buildings[tokens[0].lower()].append((tokens[1], file))
        main.buildings = self.buildings
        main.jString = json.dumps(self.buildings, default=self.set_default)
        main.jString = main.jString

    def getFiles(self):
        for (dirpath, dirnames, filenames) in walk(self.PDF_LOCATION):
            return filenames

    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError

    @app.route('/')
    def index():
        return render_template('index.html', buildings=main.buildings, data=main.jString, storedFileData=False)

    @app.route('/<string:filename>')
    def indexFilename(filename):
        if main.matchReg.match(filename) is not None:
            tokens = main.splitReg.split(filename)
            buildingName = tokens[0].lower()
            floorName = tokens[1]
            if buildingName in main.buildings:
                return render_template('index.html', buildings=main.buildings, data=main.jString,
                                       buildingName=tokens[0].lower(), floorName=tokens[1], storedFileData=True)
            else:
                print "{0} not in buildings".format(buildingName)
                return render_template('index.html', buildings=main.buildings, data=main.jString,
                                       buildingName=None, floorName=None, storedFileData=False)
        else:
            return render_template('index.html', buildings=main.buildings, data=main.jString,
                                   buildingName=None, floorName=None, storedFileData=False)

    @app.route('/file/<string:filename>')
    def file(filename):
        return send_file(main.PDF_LOCATION + filename)

    @app.route('/static/<path:path>')
    def staticfiles(path):
        mimetype = 'text/html'
        if '.js' in path:
            mimetype = 'text/javascript'
        elif '.css' in path:
            mimetype = 'text/css'
        elif '.html' in path:
            mimetype = 'text/html'
        return send_from_directory('static', path, mimetype=mimetype)

    def run(self):
        self.app.env = "development"
        self.app.templates_auto_reload = True
        self.app.run(host='0.0.0.0', port='8080')


if __name__ == "__main__":
    main().run()
