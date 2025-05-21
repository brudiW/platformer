import json
import datetime
import os

class GameSave:
    def __init__(self):
        self.saveName = ""
        self.saveData = {}
        self.saveJSON = ""
        self.header = {}
        self.levels = {}
        self.stats = {}
        self.items = {}

    def create(self, saveName, path):
        self.saveName = saveName
        x = datetime.datetime.now()
        self.header = {
            "savename": saveName,
            "saveid": 1,
            "created": x.isoformat()
        }
        self.levels = {
            "1-1": {
                "unlocked": True,
                "completed": False,
                "time": -1
            },
            "1-2": {
                "unlocked": False,
                "completed": False,
                "time": -1
            }
        }
        self.stats = {
            "coins": 0,
            "artefacts": {
                "test": "test"
            },
            "enemysKilled": 0,
            "timesDied": 0
        }
        self.items = {
            "test": {
                "name": "test",
                "description": "Test Item",
                "effect": "none",
                "rarety": "Impossible",
                "durability": -1
            }
        }
        print(f"[DEBUG] Speicherpfad beim Speichern: {path}")

        self.save(path)

    def load(self, path):
        try:
            with open(path, 'r') as f:
                map_data = json.load(f)
            self.header = map_data['header']
            self.levels = map_data['levels']
            self.stats = map_data['stats']
            self.items = map_data['items']
        except FileNotFoundError:
            print(f"[WARNING] Speicherdatei nicht gefunden: {path}")
        except json.JSONDecodeError:
            print(f"[ERROR] Fehler beim Laden der JSON-Datei: {path}")


    def save(self, path):
        assert isinstance(path, str) and path.strip() != "", f"[SAVE ERROR] Ungültiger Pfad: {path}"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump({
                'header': self.header,
                'levels': self.levels,
                'stats': self.stats,
                'items': self.items
            }, f, indent=4)


    def updateLevel(self, level, info, path):
        self.load(path)
        self.levels[level] = info
        self.save(path)

    def updateLevelCompletion(self, level, state, path):
        self.load(path)
        self.levels[level]['completed'] = state
        self.save(path)

    def updateLevelUnlock(self, level, state, path):
        self.load(path)
        self.levels[level]['unlocked'] = state
        self.save(path)

    def updateLevelTime(self, level, time, path):
        self.load(path)
        self.levels[level]['time'] = time
        self.save(path)

    def getCoins(self, path):
        self.load(path)
        return self.stats['coins']

    def updateCoins(self, path, coins):
        self.load(path)
        self.stats['coins'] = coins
        self.save(path)

    def checkCompletion(self, level, path):
        self.load(path)
        return self.levels[level]['completed']

    def checkUnlock(self, level, path):
        with open('hidden/unlock_requirements.json', 'r') as f:
            map_data = json.load(f)

        checkLevel = map_data.get(level)
        if checkLevel["requires"] != "none":
            if self.checkCompletion(checkLevel["requires"], path):
                self.updateLevelUnlock(level, True, path)
            else:
                self.updateLevelUnlock(level, False, path)
