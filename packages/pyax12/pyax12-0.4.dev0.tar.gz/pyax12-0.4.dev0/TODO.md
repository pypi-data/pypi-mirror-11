# TODO

## Version 0.3

- [x] change the package name (from `pydynamixel` to `pyax12`), as the project
      now focus on Dynamixel AX-12 actuators

## Version 0.4

- [ ] écrire les fonctions Connection.dump(), Connection.scan(),
      Connection.reset(), ...
- [ ] ajouter la fonction "Packet.print_info()" et "Connection.print_info()" qui
      affichent des informations facilement intelligibles par un
      humain plutôt que des codes hexa (ex: "position=...°\nspeed=..." ;
      "baudrate=...\nport=...\n...") + self.__str__() appelle self.print()
- [ ] améliorer les docstrings
- [ ] générer la documentation Sphinx (mise dispo sur readthedocs.org ?)
- [ ] nettoyer tous les modules avec pylint
- [ ] vérifier systématiquement la validité des arguments (type, bornes, ...)
- [ ] remplacer les warning par des exceptions ?
- [ ] créer des tests unitaires
- [ ] missing datas and tests
    - [ ] error table (p.11)
    - [ ] access RD/WD (p.12)
    - [ ] addr/labels (p.12)
    - [ ] baudrates (p.13)
    - [ ] status return level (p.14)
    - [ ] alarm led (p.15)
    - [ ] alarm shutdown (p.15)
    - [ ] complience margin and slope (p.16)
    - [ ] present load (p.17)
    - [ ] goal spped setting (p.18)
    - [ ] range (p.18)
    - [ ] instruction set labels (p.19)
    - [ ] UART p.30 and 31
- [ ] écrire un "context manager" (with) pour la classe Connection (pour fermer
      automatiquement la connexion)
- [ ] certains tests unitaires "requires to be connected to the Dynamixel
      number 1 using port "/dev/ttyUSB0" (thus it works on Unix systems only)
      at 57600 baud." -> corriger ça... (essentiellement dans test_status_packet)
- [ ] implements `__str__` in Packet
- [ ] implements `__iter__` and `next` in Packet to make it iterable
- [ ] implements `with` context in Connection


## Version 0.5

- [ ] ajouter des exemples
- [x] ajouter une vidéo de démonstration dans le README.rst
- [ ] amélorer la description dans le README.rst

## Version 0.6

- [ ] corriger les "TODO" restant
- [ ] rendre le code de lecture plus robuste dans connection.send()

## Version 1.0

- [ ] revoir la gestion des modules/paquets/imports (cf. pyai) ?
- [ ] tester si la génération de paquets Debian fonctionne toujours
- [ ] tester si la setup.py fonctionne toujours
- [ ] distribuer pyax12 sur PyPi
- [ ] tester sous Windows
- [ ] amélorer la description dans le README.rst: instructions d'installation
      avec pip, etc.

## Misc

- [ ] créer le référentiel pyax12gui (PyAX-12-gui) : des outils graphiques (GTK+3) pour manipuler les servos Dynamixel avec PyAX-12
- [ ] tester depuis un RaspberryPi sans usbdynamixel (utiliser les GPIO) et sans CM-5 (utiliser des piles ou des LiPo)

