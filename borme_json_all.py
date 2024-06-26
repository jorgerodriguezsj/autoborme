#!/usr/bin/env python3
#
# borme_json_all.py - Convert all BORME PDF files to JSON
# Copyright (C) 2015-2022 Pablo Castellano <pablo@anche.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import bormeparser
import bormeparser.borme
from common import get_git_revision_short_hash

from bormeparser.backends.defaults import OPTIONS
OPTIONS['SANITIZE_COMPANY_NAME'] = True

import argparse
import os
import sys
import time

from threading import Thread
from queue import Queue

# # BORME_ROOT = bormeparser.CONFIG["borme_root"]
# THREADS = 6
# BORME_ROOT = r'C:/Users/jorge/OneDrive/Escritorio/autoborme/dowloads/'

# class ThreadConvertJSON(Thread):
#     def __init__(self, queue):
#         super(ThreadConvertJSON, self).__init__()
#         self.queue = queue

#     def run(self):
#         while True:
#             pdf_path, json_path = self.queue.get()
#             print('Creating %s ...' % json_path)
#             try:
#                 borme = bormeparser.parse(pdf_path, bormeparser.SECCION.A)
#                 borme.to_json(json_path)
#                 print('{cve}: OK'.format(cve=borme.cve))
#             except Exception as e:
#                 print('ERROR: {} ({})'.format(os.path.basename(pdf_path), e))
#             self.queue.task_done()


# def walk_borme_root(bormes_root, json_root=None):
#     pdf_root = os.path.join(bormes_root, 'pdf')
#     if json_root is None:
#         json_root = os.path.join(bormes_root, 'json')

#     _, year_dirs, _ = next(os.walk(pdf_root))
#     for year in year_dirs:
#         year_dir = os.path.join(pdf_root, year)
#         json_year_dir = os.path.join(json_root, year)
#         _, month_dirs, _ = next(os.walk(year_dir))
#         for month in month_dirs:
#             month_dir = os.path.join(year_dir, month)
#             json_month_dir = os.path.join(json_year_dir, month)
#             _, day_dirs, _ = next(os.walk(month_dir))
#             for day in day_dirs:
#                 day_dir = os.path.join(month_dir, day)
#                 json_day_dir = os.path.join(json_month_dir, day)

#                 os.makedirs(json_day_dir, exist_ok=True)

#                 _, _, files = next(os.walk(day_dir))
#                 for filename in files:
#                     yield day_dir, json_day_dir, filename


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Convert all BORME PDF files to JSON.')
#     parser.add_argument('-d', '--directory', default=BORME_ROOT, help='Directory to download files (default is {})'.format(BORME_ROOT))
#     args = parser.parse_args()

#     start_time = time.time()

#     q = Queue()
#     for i in range(THREADS):
#         t = ThreadConvertJSON(q)
#         t.daemon = True
#         # t.setDaemon(True)
#         t.start()

#     json_folder = 'json_' + get_git_revision_short_hash()
#     json_root = os.path.join(args.directory, json_folder)
#     if os.path.exists(json_root):
#         print('{} already exists'.format(json_root))
#         sys.exit(1)

#     for day_dir, json_day_dir, filename in walk_borme_root(args.directory, json_root):
#         if not filename.endswith('.pdf') or filename.endswith('-99.pdf'):
#             continue
#         pdf_path = os.path.join(day_dir, filename)
#         json_filename = filename.replace('.pdf', '.json')
#         json_path = os.path.join(json_day_dir, json_filename)
#         q.put((pdf_path, json_path))
#     q.join()

#     elapsed_time = time.time() - start_time
#     print('Elapsed time: %.2f seconds' % elapsed_time)

import bormeparser
import bormeparser.borme
from common import get_git_revision_short_hash

from bormeparser.backends.defaults import OPTIONS
OPTIONS['SANITIZE_COMPANY_NAME'] = True

import argparse
import os
import sys
import time

from threading import Thread
from queue import Queue

# BORME_ROOT = bormeparser.CONFIG["borme_root"]
THREADS = 6
# BORME_ROOT = r'C:/Users/jorge/OneDrive/Escritorio/autoborme/dowloads/'

class ThreadConvertJSON(Thread):
    def __init__(self, queue):
        super(ThreadConvertJSON, self).__init__()
        self.queue = queue
        self.daemon = True  # Configuración correcta del hilo como daemon

    def run(self):
        while True:
            pdf_path, json_path = self.queue.get()
            print('Creating %s ...' % json_path)
            try:
                borme = bormeparser.parse(pdf_path, bormeparser.SECCION.A)
                borme.to_json(json_path)
                print('{cve}: OK'.format(cve=borme.cve))
            except Exception as e:
                print('ERROR: {} ({})'.format(os.path.basename(pdf_path), e))
            self.queue.task_done()

def walk_borme_root(bormes_root, json_root=None):
    pdf_root = os.path.join(bormes_root, 'pdf')
    if json_root is None:
        json_root = os.path.join(bormes_root, 'json')

    _, year_dirs, _ = next(os.walk(pdf_root))
    for year in year_dirs:
        year_dir = os.path.join(pdf_root, year)
        json_year_dir = os.path.join(json_root, year)
        _, month_dirs, _ = next(os.walk(year_dir))
        for month in month_dirs:
            month_dir = os.path.join(year_dir, month)
            json_month_dir = os.path.join(json_year_dir, month)
            _, day_dirs, _ = next(os.walk(month_dir))
            for day in day_dirs:
                day_dir = os.path.join(month_dir, day)
                json_day_dir = os.path.join(json_month_dir, day)

                os.makedirs(json_day_dir, exist_ok=True)

                _, _, files = next(os.walk(day_dir))
                for filename in files:
                    yield day_dir, json_day_dir, filename

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert all BORME PDF files to JSON.')
    # parser.add_argument('-d', '--directory', default=BORME_ROOT, help='Directory to download files (default is {})'.format(BORME_ROOT))
    args = parser.parse_args()

    start_time = time.time()

    q = Queue()
    for i in range(THREADS):
        t = ThreadConvertJSON(q)
        t.daemon = True  # Configuración correcta del hilo como daemon
        t.start()

    # json_folder = 'json_' + get_git_revision_short_hash()
    json_folder = 'json_folder'   
    json_root = os.path.join(os.getenv('DIRECTORY'), json_folder)
    if os.path.exists(json_root):
        print('{} already exists'.format(json_root))
        sys.exit(1)  # Termina el programa si el directorio ya existe

    for day_dir, json_day_dir, filename in walk_borme_root(os.getenv('DIRECTORY'), json_root):
        if not filename.endswith('.pdf') or filename.endswith('-99.pdf'):
            continue
        pdf_path = os.path.join(day_dir, filename)
        json_filename = filename.replace('.pdf', '.json')
        json_path = os.path.join(json_day_dir, json_filename)
        q.put((pdf_path, json_path))
    q.join()

    elapsed_time = time.time() - start_time
    print('Elapsed time: %.2f seconds' % elapsed_time)
