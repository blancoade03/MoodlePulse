Para correr la aplicacion debe tener activo un servidor de redis local

para correr celery debe abrir 2 consolas y poner:
  1. celery -A moodle_pulse beat
  2. celery -A moodle_pulse worker -P solo
