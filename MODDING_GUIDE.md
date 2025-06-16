# MODDING GUIDE
## How To?
Mods müssen in den Ordner *assets/mods* gelegt werden

## Projektstruktur
```
GAME/assets/mods:
    BeispielMod/
        mod.py
        assets/
            BeispielTextur.png
```
    
## Was kann modifiziert werden?
* Neue Keybinds
* Neue Items mit eigenen Effekten
* Eigene Befehle

### Eigene Keybinds?
* Wenn Taste x gedrückt, dann das
* benötigt: hook()
* register_hook(hook)

### Eigene Items?
* Wenn Item x equiped, dann das
* benötigt: equip(), (falls mit Custom Funktion dann auch hook())
* register_item(item)
* register_hook(hook)

### Eigene Befehle?
