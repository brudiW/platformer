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

    def create(self, saveName: str, path: str):
        """Erstellt einen neuen Speicherstand mit dem Namen saveName unter dem Dateipfad path

        Args:
            saveName (str): Name des Speicherstandes
            path (str): Speicherpfad des Speicherstandes
        """
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

    def load(self, path: str):
        """Lädt einen Speicherstand aus dem angegebenen Dateipfad

        Args:
            path (str): Dateipfad des Speicherstandes
        """
        try:
            with open(path, 'r') as f:
                map_data = json.load(f)
            self.header = map_data['header']
            self.levels = map_data['levels']
            self.stats = map_data['stats']
            self.items = map_data['items']
        except FileNotFoundError:
            print(f"[WARNING] Speicherdatei nicht gefunden: {path}")
            self.create("New Save", path)
        except json.JSONDecodeError:
            print(f"[ERROR] Fehler beim Laden der JSON-Datei: {path}")


    def save(self, path: str):
        """Speichert den aktuellen Speicherstand unter dem angegebenen Dateipfad

        Args:
            path (str): Der Dateipfad zum Abspeichern des Speicherstandes
        """
        assert isinstance(path, str) and path.strip() != "", f"[SAVE ERROR] Ungültiger Pfad: {path}"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump({
                'header': self.header,
                'levels': self.levels,
                'stats': self.stats,
                'items': self.items
            }, f, indent=4)


    def updateLevel(self, level: str, info: dict, path: str):
        """Aktualisiert die Speicherstand-Informationen über das ausgewählte Level

        Args:
            level (str): Das Level, dessen Informationen aktualisiert werden soll
            info (dict): Die aktualisierten Informationen
            path (str): Der Dateipfad des Speicherstandes
        """
        self.load(path)
        self.levels[level] = info
        self.save(path)

    def updateLevelCompletion(self, level: str, state: bool, path: str):
        """Aktualiert den Status der Level-Completion

        Args:
            level (str): Das Level
            state (bool): Status der Level-Completion
            path (str): Der Speicherpfad des Speicherstandes
        """
        self.load(path)
        self.levels[level]['completed'] = state
        self.save(path)

    def updateLevelUnlock(self, level: str, state: bool, path: str):
        """Aktualisiert den Status der Level Freischaltung

        Args:
            level (str): Das Level
            state (bool): Status der Freischaltung
            path (str): Der Speicherpfad des Speicherstandes
        """
        self.load(path)
        self.levels[level]['unlocked'] = state
        self.save(path)

    def updateLevelTime(self, level: str, time: float, path: str):
        """Aktualisiert die Zeit zum Beendes des Levels

        Args:
            level (str): Das Level
            time (float): Die benötigte Zeit
            path (str): Der Speicherpfad des Speicherstandes
        """
        self.load(path)
        self.levels[level]['time'] = time
        self.save(path)

    def getCoins(self, path: str) -> int:
        """Gibt die Anzahl an Coins zurück
        
        Args:
            path (str): Der Speicherpfad des Speicherstandes

        Returns:
            int: Anzahl Coins
        """
        self.load(path)
        return self.stats['coins']

    def updateCoins(self, path: str, coins: int):
        """Aktualisert die Anzahl an Coins

        Args:
            path (str): Der Speicherpfad des Speicherstandes
            coins (int): Anzahl der Coins
        """
        self.load(path)
        self.stats['coins'] = coins
        self.save(path)

    def checkCompletion(self, level: str, path: str)-> bool:
        """Überprüft die Level-Completion

        Args:
            level (str): Das Level
            path (str): Der Speicherpfad des Speicherstandes

        Returns:
            bool: Der Zustand der Level-Completion
        """
        self.load(path)
        return self.levels[level]['completed']

    def checkUnlock(self, level: str, path: str):
        """Überprüft den aktuellen Freischaltungszustand des Levels

        Args:
            level (str): Das Level
            path (str): Der Speicherpfad des Speicherstandes
        """
        with open('hidden/unlock_requirements.json', 'r') as f:
            map_data = json.load(f)

        checkLevel = map_data.get(level)
        if checkLevel["requires"] != "none":
            if self.checkCompletion(checkLevel["requires"], path):
                self.updateLevelUnlock(level, True, path)
            else:
                self.updateLevelUnlock(level, False, path)

    def getItems(self, path: str) -> dict:
        """
        Gibt die Items aus dem Speicherstand zurück
        
        Args:
            path (str): Der Speicherpfad des Speicherstandes
            
        Returns:
            dict: Die Liste der Items"""
        self.load(path)
        return self.items
    
    def addItem(self, id: str, item: dict, path: str):
        """Fügt ein Item dem Speicherstand hinzu7

        Args:
            id (str): ID des Items
            item (dict): Die Werte des Items
            path (str): Der Speicherpfad des Speicherstandes
        """
        self.load(path)
        if id not in self.items:
            self.items[id] = item.getItem()
            self.save(path)
        else:
            print(f"[WARNING] Item '{id}' already exists in save data.")
