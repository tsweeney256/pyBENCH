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

from bluread import Bluray
from datetime import datetime
import chapters


class BlurayTitleInfo:

    """
    Useful information for encoding the given bluray title
    Public methods:
        __init__(bd_loc, title_num=-1, bd_key_loc=None, bd=None):
            Arguments:
                bd_loc: [string] The root directory of the bluray, i.e. the one that contains the
                    directories BDMV and CERTIFICATE. You must always supply this
                title_num: [int] The title you want information about.
                    -1 means to use the main title
                bd_key_loc: [nullable string] The file location of KEYDB.cfg.
                    Requires libaacs and libbdplus
                bd: [nullable bluread.Bluray] Opened Bluray object to be reused

    Public data members:
        title_num: [int] The value of the selected title
        playlist: [string] The file name of the playlist containing the selected title
        run_length: [string] The run length of the title
        resolution: [string] The resolution of the video
        frame_rate: [string] The frame rate of the video
        num_audio_tracks: [int] The number of audio tracks in the title
        clip_files: [list<string>] The m2ts files that the playlist points to
        chapters: [list<Chapter>] list of chapters of the title. See the Chapter class for details
    """

    def __init__(self, bd_loc, title_num=-1, bd_key_loc=None, bd=None):
        if bd_loc.endswith('/') or bd_loc.endswith('\\'):
            bd_loc = bd_loc[:-1]

        if bd:
            self._create(bd_loc, title_num, bd)
        else:
            with Bluray(bd_loc, bd_key_loc) as bd:
                bd.Open()
                self._create(bd_loc, title_num, bd)

    def __str__(self):
        ret = 'title_num: ' + str(self.title_num) + '\n'
        ret += 'playlist: ' + self.playlist + '\n'
        ret += 'run_length: ' + str(self.run_length.time()) + '\n'
        ret += 'resolution: ' + self.resolution + '\n'
        ret += 'frame_rate: ' + self.frame_rate + '\n'
        ret += 'num_audio_tracks: ' + str(self.num_audio_tracks) + '\n'
        i = 1
        for clip in self.clip_files:
            ret += 'clip ' + str(i) + ': ' + clip + '\n'
            i += 1
        i = 1
        for chapter in self.chapters:
            ret += str(chapter) + '\n'
            i += 1
        return ret

    def _create(self, bd_loc, title_num, bd):
        time_format = chapters.Chapter.time_format
        if title_num < 0:
            self.title_num = bd.MainTitleNumber
        title = bd.GetTitle(self.title_num)
        self.playlist = title.Playlist
        self.run_length = datetime.strptime(title.LengthFancy, time_format)
        video = title.GetClip(0).GetVideo(0)
        # Because of an error in bluread where they forgot to account for 1080i
        self.resolution = '1080i' if video.Format == '4' else video.Format
        self.frame_rate = video.Rate
        self.num_audio_tracks = title.GetClip(0).NumberOfAudiosPrimary
        first_chapter = title.GetChapter(1)
        self.chapters = [chapters.Chapter(
            name='Chapter 1',
            start=chapters.Chapter.min_time,
            duration=datetime.strptime(first_chapter.StartFancy, time_format))]
        for chapter_num in range(1, title.NumberOfChapters):
            chapter = title.GetChapter(chapter_num)
            self.chapters.append(chapters.Chapter(
                name='Chapter ' + str(chapter_num+1),
                start=datetime.strptime(chapter.StartFancy, time_format),
                duration=datetime.strptime(chapter.LengthFancy, time_format)))
        self.clip_files = []
        for i in range(title.NumberOfClips):
            clip = title.GetClip(i)
            self.clip_files.append(clip.ClipId + '.m2ts')
