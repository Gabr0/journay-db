#!/usr/bin/env python3

"""diario para probar bases de datos Gabr0."""
from colorama import init, Fore
from collections import OrderedDict
from peewee import *
import datetime
import sys
import os

db = SqliteDatabase('journay.db')
init(autoreset=True)


class Entry(Model):
    """Main class."""

    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        """Import db."""

        database = db


def clear():
    """Borrar la pantalla."""
    os.system('cls' if os.name == 'nt' else 'clear')


def initializate():
    """Crear db y la tabla."""
    db.connect()
    db.create_tables([Entry], safe=True)


def menu_loop():
    """Mostrar el menu."""
    choice = None
    while choice != 's':
        clear()
        print("Introduzca s para salir")

        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))

        choice = input("Action: ").lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


def view_entries(search_query=None):
    """Ver entradas de la base de datos."""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))
    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        clear()
        print(timestamp)
        print('\n\n' + '='*len(timestamp))
        print(entry.content)
        print('N) siguiente entrada')
        print('b) borrar una entrada')
        print('q) volver al menu')
        siguiente_accion = input('Accion:     ').lower().strip()
        if siguiente_accion == 'q':
            break
        elif siguiente_accion == 'b':
            delete_entry(entry)


def delete_entry(entry):
    """Delete entry."""
    if input(Fore.RED + "Estas seguro de que desea borrar"
             "la entrada? [S/N] ").lower() == 's':
        entry.delete_instance()
        print(Fore.GREEN + 'Borrado completado')


def add_entry():
    """Agregar una entrada a la base de datos."""
    print("Introduzca la entrada. Presione ctrl+d cuando haya acabado")
    data = sys.stdin.read().strip()
    if data:
        if input('Save entry?').lower() != 'n':
            Entry.create(content=data)
            print(Style.RESET_ALL)
            print("Guardado completado")
    print(Style.RESET_ALL)


def search_entries():
    """Buscar en las entradas de la base de datos por una palabra."""
    view_entries(input('Buscar: '))


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries)
])
if __name__ == '__main__':
    initializate()
    menu_loop()
