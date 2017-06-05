# pyBENCH
# Copyright (C) 2017 Thomas Sweeney
# This file is part of pyBENCH.
# pyBENCH is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# pyBENCH is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime, timedelta


class Chapter:

    def __init__(self, name, start, duration):
        self.name = name
        self.start = start
        self.duration = duration

    def __str__(self):
        return self.name + ' starts at ' + str(self.start.time()) \
            + ' and lasts ' + str(self.duration.time())

    @property
    def end(self):
        return (self.start - Chapter.min_time) + self.duration

    @staticmethod
    def to_seconds(val):
        return (val - Chapter.min_time).total_seconds()

    @staticmethod
    def to_frames(val, framerate):
        return round(Chapter.to_seconds(val) * framerate)

    time_format = '%H:%M:%S.%f'
    min_time = datetime.strptime('00:00:00.000', time_format)


def remove_chapters_shorter_than(chapters, seconds):
    for i in range(0, len(chapters)):
        if (chapters[i].duration - Chapter.min_time).total_seconds() < seconds:
            del chapters[i]


def split_chapters(chapters, index):
    ret = []
    delta = timedelta()
    for i in range(0, len(chapters)):
        if i % index == 0:
            ret.append([])
            delta = chapters[i].start - Chapter.min_time
        ret[-1].append(chapters[i])
        ret[-1][-1].start = ret[-1][-1].start - delta
    return ret


def rename_chapters(chapters, names, repeat=False):
    if len(names) > len(chapters):
        raise ValueError('More names provided than there are chapters for')
    if repeat and len(chapters) % len(names) != 0:
        raise ValueError('Number of names does not divide evenly into number of chapters while in '
                         'repeat mode')
    for i in range(0, len(chapters)):
        if i >= len(names) and not repeat:
            return
        chapters[i].name = names[i % len(names)]


def create_mkv_chapters(chapters, file):
    for i in range(0, len(chapters)):
        base_chapter_str = "CHAPTER{0:02d}".format(i+1)
        file.write(base_chapter_str + "=" + str(chapters[i].start.time()) + "\n")
        file.write(base_chapter_str + "NAME=" + chapters[i].name + "\n")
