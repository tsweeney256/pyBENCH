# pyBENCH
# Copyright (C) 2016 Thomas Sweeney
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


class MkvTrack:

    def __init__(self, file_loc, args=None):
        """Arguments:
        file_loc: string file location of the track you wish to import.
            It is the responsibility of the functions that use objects of this type to wrap
            parentheses around the file location. This class itself should not be constructed with
            parentheses already present.
        args: Nullable string-string dictionary for extra arguments you want for the track
            e.g. {aspect-ratio: '0:16/9'}. Both abbreviated and full named args are acceptable."""

        if not file_loc:
            raise ValueError("Must give file location for track")

        self.file_loc = file_loc
        self.args = args

    def write_to(self, file):
        if self.args:
            _write_args_from_dict(file, self.args)
        file.write(' "')
        file.write(self.file_loc)
        file.write('"')


class MkvAttachment:

    def __init__(self, file_loc, mime_type, name=None, description=None, attach_once=False):
        """Arguments:
        file_loc: string file location of the attachment you wish to import.
            It is the responsibility of the functions that use objects of this type to wrap
            parentheses around the file location. This class itself should not be constructed with
            parentheses already present.
        mime_type: string mime_type description as explained in the mkvmerge documentation
        name: Nullable string name of the attachment
        description: Nullable string description of the attachment
        attach_once: Boolean value to use --attach-file-once instead of --attach-file"""

        if not file_loc:
            raise ValueError("Must give file location for attachment")
        if not mime_type:
            raise ValueError("Must give mime type for attachment. mkvmerge requires it")

        self.file_loc = file_loc
        self.mime_type = mime_type
        self.name = name
        self.description = description
        self.attach_once = attach_once

    def write_to(self, file):
        file.write(' --attachment-mime-type ')
        file.write(self.mime_type)
        if self.name:
            file.write(' --attachment-name "')
            file.write(self.name)
            file.write('"')
        if self.description:
            file.write(' --attachment-description "')
            file.write(self.description)
            file.write('"')
        if self.attach_once:
            file.write(' --attach-file-once "')
        else:
            file.write(' --attach-file "')
        file.write(self.file_loc)
        file.write('"')


def write_bePipe_neroAAC_command(file, bepipe_loc, nero_loc, script, audio_dest_loc,
                                 nero_args=None):
    """Write BePipe input into NeroAAC command to file

    Arguments:
    Note: All file location strings have Parentheses wrapped around them by this function.

    file: The file
    bepipe_loc: string file location of the BePipe executable
    nero_loc: string file location of the NeroAAC executable
    script: string script argument to BePipe, e.g. 'import(^myfile.avs^)'
    audio_dest_loc: string file location of the audio file output
    nero_args: Nullable string, string dictionary for the arguments to be passed to NeroAAC
        e.g. {'q': '0.65'}"""

    # header
    file.write('REM Audio ')
    file.write(audio_dest_loc)
    file.write('\n')

    # command
    file.write('"')
    file.write(bepipe_loc)
    file.write('" --script "')
    file.write(script)
    file.write('" | "')
    file.write(nero_loc)
    file.write('"')
    if nero_args:
        _write_args_from_dict(file, nero_args, '-')
    file.write(' -if - -of "')
    file.write(audio_dest_loc)
    file.write('"\n\n')


def write_x264_command(file, x264_loc, video_input_loc, video_dest_loc, args=None):
    """Write x264 command to file

    Arguments:
    Note: All file location strings have Parentheses wrapped around them by this function.

    file: The file
    x264_loc: The string file location of the x264 executable.
    video_input_loc: The string file location of the input video.
    video_dest_loc: The string file location of the output video
    args: Nullable string, string dictionary for the arguments to be passed to x264
        e.g. {'crf': '16'}"""

    # header
    file.write('REM Video ')
    file.write(video_dest_loc)
    file.write('\n')

    # command
    file.write('"')
    file.write(x264_loc)
    file.write('" --output "')
    file.write(video_dest_loc)
    file.write('"')

    if args:
        _write_args_from_dict(file, args)

    file.write(' "')
    file.write(video_input_loc)
    file.write('"\n\n')


def write_mkvmerge_command(file, mkvmerge_loc, mux_output_loc, tracks, attachments=None,
                           global_args=None):
    """Write mkvmerge command to file

    Arguments:
    Note: All file location strings have Parentheses wrapped around them by this function.

    file: The file
    mkvmerge_loc: String file location of the mkvmerge executable
    mux_output_loc: String file location of the muxed output
    tracks: list of MkvTrack objects
    attachments: Nullable list of MkvAttachment objects
    global_args: string, string dictionary pairs for the global arguments to be passed to mkvmerge
        e.g. title='Hooplah'"""

    # header
    file.write('REM Mux ')
    file.write(mux_output_loc)
    file.write('\n')

    # command
    file.write('"')
    file.write(mkvmerge_loc)
    file.write('" --output "')
    file.write(mux_output_loc)
    file.write('"')

    if global_args:
        _write_args_from_dict(file, global_args)
    if attachments:
        for attachment in attachments:
            attachment.write_to(file)
    for track in tracks:
        track.write_to(file)
    file.write('\n\n')


def _write_args_from_dict(file, args, argument_specifier_override=None):

    keys = sorted(args.keys())
    for key in keys:
        file.write(' ')
        if argument_specifier_override:
            file.write(argument_specifier_override)
        elif len(key) == 1:
            file.write('-')
        else:
            file.write('--')
        file.write(key)
        if args[key]:
            file.write(' ')
            file.write(args[key])
