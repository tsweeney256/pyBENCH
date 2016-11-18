import unittest
import io
import copy
import bench.commands
import example_x264_defaults


test_loc = 'folder\\test'

bepipe_loc = 'Programs\\BePipe.exe'
nero_loc = 'Programs\\neroAacEnc.exe'
bescript = 'import(^Documents\\script.avs^)'
audio_dest_loc = test_loc + '.m4a'

x264_loc = 'Programs\\x264.exe'
avs4x26x_loc = 'Programs\\avs4x26x.exe'
video_input_loc = 'Documents\\script.avs'
video_dest_loc = test_loc + '.264'
x264_args = example_x264_defaults.make_avs4x26x_defaults()

mkvmerge_loc = 'Programs\\mkvmerge.exe'
mux_output_loc = test_loc + '.mkv'
fontA_loc = 'Arial.ttf'
fontA_mime_type = 'application/x-truetype-font'
fontA_name = 'Arial'
fontA_description = 'you'
fontB_loc = 'Helvetica.ttf'
fontB_mime_type = 'application/x-truetype-font'
fontB_name = 'Helvetica'
fontB_description = 'the font she tells you not to worry about'


# Because assertEqual()'s truncation of strings is dumb
def assertStrEqual(a, b):
    msg = "'" + a + "'\ndoes not equal\n'" + b + "'"
    assert a == b, msg


class TestCommands(unittest.TestCase):

    def setUp(self):
        self.file = io.StringIO()

    def tearDown(self):
        self.file.close()

    def test_bepipe_nero_no_args(self):
        expected = (
            'REM Audio folder\\test.m4a\n'
            '"Programs\\BePipe.exe" --script "import(^Documents\\script.avs^)" | '
            '"Programs\\neroAacEnc.exe" -if - -of "folder\\test.m4a"\n\n'
        )
        bench.commands.write_bePipe_neroAAC_command(
            self.file, bepipe_loc, nero_loc, bescript, test_loc + '.m4a')
        assertStrEqual(self.file.getvalue(), expected)

    def test_bepipe_nero_one_arg(self):
        expected = (
            'REM Audio folder\\test.m4a\n'
            '"Programs\\BePipe.exe" --script "import(^Documents\\script.avs^)" | '
            '"Programs\\neroAacEnc.exe" -q 0.65 -if - -of "folder\\test.m4a"\n\n'
        )
        args = {'q': '0.65'}
        bench.commands.write_bePipe_neroAAC_command(
            self.file, bepipe_loc, nero_loc, bescript, test_loc + '.m4a', args)
        assertStrEqual(self.file.getvalue(), expected)

    def test_bepipe_nero_two_arg(self):
        expected = (
            'REM Audio folder\\test.m4a\n'
            '"Programs\\BePipe.exe" --script "import(^Documents\\script.avs^)" | '
            '"Programs\\neroAacEnc.exe" -he -q 0.65 -if - -of "folder\\test.m4a"\n\n'
        )
        args = {'q': '0.65', 'he': ''}
        bench.commands.write_bePipe_neroAAC_command(
            self.file, bepipe_loc, nero_loc, bescript, test_loc + '.m4a', args)
        assertStrEqual(self.file.getvalue(), expected)

    def test_x264_no_args(self):
        expected = (
            'REM Video folder\\test.264\n'
            '"Programs\\x264.exe" --output "folder\\test.264" "Documents\\script.avs"\n\n'
        )
        bench.commands.write_x264_command(
            self.file, x264_loc, video_input_loc, video_dest_loc)
        assertStrEqual(self.file.getvalue(), expected)

    def test_x264_default_args(self):
        expected = (
            'REM Video folder\\test.264\n'
            '"Programs\\avs4x26x.exe" --output "folder\\test.264" '
            '--aq-mode 2 --aq-strength 0.8 --b-adapt 2 '
            '--b-pyramid normal --bframes 8 --crf 16 --direct auto --fps 24000/1001 '
            '--input-depth 16 --me umh --merange 24 --no-fast-pskip --partitions all '
            '--profile high10 --psy-rd 0.6:0.1 --qcomp 0.70 --rc-lookahead 60 --ref 9 '
            '--subme 10 --trellis 2 --x26x-binary "Programs\\x264.exe" "Documents\\script.avs"\n\n'
        )
        bench.commands.write_x264_command(
            self.file, avs4x26x_loc, video_input_loc, video_dest_loc, x264_args)
        assertStrEqual(self.file.getvalue(), expected)

    def test_x264_one_custom_arg(self):
        expected = (
            'REM Video folder\\test.264\n'
            '"Programs\\avs4x26x.exe" --output "folder\\test.264" '
            '--aq-mode 2 --aq-strength 0.8 --b-adapt 2 '
            '--b-pyramid normal --bframes 8 --crf 15 --direct auto --fps 24000/1001 '
            '--input-depth 16 --me umh --merange 24 --no-fast-pskip --partitions all '
            '--profile high10 --psy-rd 0.6:0.1 --qcomp 0.70 --rc-lookahead 60 --ref 9 '
            '--subme 10 --trellis 2 --x26x-binary "Programs\\x264.exe" "Documents\\script.avs"\n\n'
        )
        modified_args = copy.deepcopy(x264_args)
        modified_args['crf'] = '15'
        bench.commands.write_x264_command(
            self.file, avs4x26x_loc, video_input_loc, video_dest_loc, modified_args)
        assertStrEqual(self.file.getvalue(), expected)

    def test_x264_two_custom_arg(self):
        expected = (
            'REM Video folder\\test.264\n'
            '"Programs\\avs4x26x.exe" --output "folder\\test.264" '
            '--aq-mode 2 --aq-strength 0.8 --b-adapt 2 '
            '--b-pyramid normal --bframes 2 --crf 21 --direct auto --fps 24000/1001 '
            '--input-depth 16 --me umh --merange 24 --no-fast-pskip --partitions all '
            '--profile high10 --psy-rd 0.6:0.1 --qcomp 0.70 --rc-lookahead 60 --ref 9 '
            '--subme 10 --trellis 2 --x26x-binary "Programs\\x264.exe" "Documents\\script.avs"\n\n'
        )
        modified_args = copy.deepcopy(x264_args)
        modified_args['crf'] = '21'
        modified_args['bframes'] = '2'
        bench.commands.write_x264_command(
            self.file, avs4x26x_loc, video_input_loc, video_dest_loc, modified_args)
        assertStrEqual(self.file.getvalue(), expected)

    def test_MkvTrack_invalid_loc_exception(self):
        self.assertRaises(ValueError, bench.commands.MkvTrack, None)

    def test_MkvAttachment_invalid_loc_exception(self):
        self.assertRaises(ValueError, bench.commands.MkvAttachment, None, 'foo')

    def test_MkvAttachment_invalid_mime_type_exception(self):
        self.assertRaises(ValueError, bench.commands.MkvAttachment, 'foo', None)

    def test_MkvAttachment_invalid_loc_and_mime_type_exception(self):
        self.assertRaises(ValueError, bench.commands.MkvAttachment, None, None)

    def test_mkvmerge_vid_no_args(self):
        expected = (
            'REM Mux folder\\test.mkv\n'
            '"Programs\\mkvmerge.exe" --output "folder\\test.mkv" "folder\\test.264"\n\n'
        )
        video_track = bench.commands.MkvTrack(video_dest_loc)
        tracks = video_track,
        bench.commands.write_mkvmerge_command(
            self.file, mkvmerge_loc, mux_output_loc, tracks)
        assertStrEqual(self.file.getvalue(), expected)

    def test_mkvmerge_vid_one_arg(self):
        expected = (
            'REM Mux folder\\test.mkv\n'
            '"Programs\\mkvmerge.exe" --output "folder\\test.mkv" '
            '--language 0:Japanese "folder\\test.264"\n\n'
        )
        args = {'language': '0:Japanese'}
        video_track = bench.commands.MkvTrack(video_dest_loc, args)
        tracks = video_track,
        bench.commands.write_mkvmerge_command(
            self.file, mkvmerge_loc, mux_output_loc, tracks)
        assertStrEqual(self.file.getvalue(), expected)

    def test_mkvmerge_vid_two_arg(self):
        expected = (
            'REM Mux folder\\test.mkv\n'
            '"Programs\\mkvmerge.exe" --output "folder\\test.mkv" '
            '--language 0:Japanese --track-name 0:Hooplah "folder\\test.264"\n\n'
        )
        args = {'language': '0:Japanese', 'track-name': '0:Hooplah'}
        video_track = bench.commands.MkvTrack(video_dest_loc, args)
        tracks = video_track,
        bench.commands.write_mkvmerge_command(
            self.file, mkvmerge_loc, mux_output_loc, tracks)
        assertStrEqual(self.file.getvalue(), expected)

    def test_mkvmerge_vid_no_arg_audio_no_arg(self):
        expected = (
            'REM Mux folder\\test.mkv\n'
            '"Programs\\mkvmerge.exe" --output "folder\\test.mkv" '
            '"folder\\test.264" "folder\\test.m4a"\n\n'
        )
        video_track = bench.commands.MkvTrack(video_dest_loc)
        audio_track = bench.commands.MkvTrack(audio_dest_loc)
        tracks = video_track, audio_track
        bench.commands.write_mkvmerge_command(
            self.file, mkvmerge_loc, mux_output_loc, tracks)
        assertStrEqual(self.file.getvalue(), expected)

    def test_mkvmerge_vid_two_arg_audio_no_arg(self):
        expected = (
            'REM Mux folder\\test.mkv\n'
            '"Programs\\mkvmerge.exe" --output "folder\\test.mkv" '
            '--language 0:Japanese --track-name 0:Hooplah "folder\\test.264" '
            '"folder\\test.m4a"\n\n'
        )
        args = {'language': '0:Japanese', 'track-name': '0:Hooplah'}
        video_track = bench.commands.MkvTrack(video_dest_loc, args)
        audio_track = bench.commands.MkvTrack(audio_dest_loc)
        tracks = video_track, audio_track
        bench.commands.write_mkvmerge_command(
            self.file, mkvmerge_loc, mux_output_loc, tracks)
        assertStrEqual(self.file.getvalue(), expected)

    def test_mkvmerge_vid_no_arg_audio_two_arg(self):
        expected = (
            'REM Mux folder\\test.mkv\n'
            '"Programs\\mkvmerge.exe" --output "folder\\test.mkv" '
            '"folder\\test.264" '
            '--language 0:Japanese --track-name 0:Hooplah "folder\\test.m4a"\n\n'
        )
        args = {'language': '0:Japanese', 'track-name': '0:Hooplah'}
        video_track = bench.commands.MkvTrack(video_dest_loc)
        audio_track = bench.commands.MkvTrack(audio_dest_loc, args)
        tracks = video_track, audio_track
        bench.commands.write_mkvmerge_command(
            self.file, mkvmerge_loc, mux_output_loc, tracks)
        assertStrEqual(self.file.getvalue(), expected)

    def test_mkvmerge_vid_two_arg_audio_two_arg(self):
        expected = (
            'REM Mux folder\\test.mkv\n'
            '"Programs\\mkvmerge.exe" --output "folder\\test.mkv" '
            '--language 0:Japanese --track-name 0:Hooplah "folder\\test.264" '
            '--language 0:Japanese --track-name 0:Hooplah "folder\\test.m4a"\n\n'
        )
        args = {'language': '0:Japanese', 'track-name': '0:Hooplah'}
        video_track = bench.commands.MkvTrack(video_dest_loc, args)
        audio_track = bench.commands.MkvTrack(audio_dest_loc, args)
        tracks = video_track, audio_track
        bench.commands.write_mkvmerge_command(
            self.file, mkvmerge_loc, mux_output_loc, tracks)
        assertStrEqual(self.file.getvalue(), expected)

    def test_mkvmerge_vid_no_arg_one_attachment_sparse(self):
        expected = (
            'REM Mux folder\\test.mkv\n'
            '"Programs\\mkvmerge.exe" --output "folder\\test.mkv" '
            '--attachment-mime-type application/x-truetype-font --attach-file "Arial.ttf" '
            '"folder\\test.264"\n\n'
        )
        video_track = bench.commands.MkvTrack(video_dest_loc)
        tracks = video_track,
        fontA = bench.commands.MkvAttachment(fontA_loc, fontA_mime_type)
        attachments = fontA,
        bench.commands.write_mkvmerge_command(
            self.file, mkvmerge_loc, mux_output_loc, tracks, attachments)
        assertStrEqual(self.file.getvalue(), expected)

    def test_mkvmerge_vid_no_arg_one_attachment_full(self):
        expected = (
            'REM Mux folder\\test.mkv\n'
            '"Programs\\mkvmerge.exe" --output "folder\\test.mkv" '
            '--attachment-mime-type application/x-truetype-font --attachment-name "Arial" '
            '--attachment-description "you" --attach-file "Arial.ttf" '
            '"folder\\test.264"\n\n'
        )
        video_track = bench.commands.MkvTrack(video_dest_loc)
        tracks = video_track,
        fontA = bench.commands.MkvAttachment(fontA_loc, fontA_mime_type, fontA_name,
                                             fontA_description)
        attachments = fontA,
        bench.commands.write_mkvmerge_command(
            self.file, mkvmerge_loc, mux_output_loc, tracks, attachments)
        assertStrEqual(self.file.getvalue(), expected)

    def test_mkvmerge_vid_no_arg_two_attachment_full(self):
        expected = (
            'REM Mux folder\\test.mkv\n'
            '"Programs\\mkvmerge.exe" --output "folder\\test.mkv" '
            '--attachment-mime-type application/x-truetype-font --attachment-name "Arial" '
            '--attachment-description "you" --attach-file "Arial.ttf" '
            '--attachment-mime-type application/x-truetype-font --attachment-name "Helvetica" '
            '--attachment-description "the font she tells you not to worry about" '
            '--attach-file-once "Helvetica.ttf" '
            '"folder\\test.264"\n\n'
        )
        video_track = bench.commands.MkvTrack(video_dest_loc)
        tracks = video_track,
        fontA = bench.commands.MkvAttachment(fontA_loc, fontA_mime_type, fontA_name,
                                             fontA_description)
        fontB = bench.commands.MkvAttachment(fontB_loc, fontB_mime_type, fontB_name,
                                             fontB_description, True)
        attachments = fontA, fontB
        bench.commands.write_mkvmerge_command(
            self.file, mkvmerge_loc, mux_output_loc, tracks, attachments)
        assertStrEqual(self.file.getvalue(), expected)

    def test_mkvmerge_vid_two_arg_audio_two_arg_two_attachment_full(self):
        expected = (
            'REM Mux folder\\test.mkv\n'
            '"Programs\\mkvmerge.exe" --output "folder\\test.mkv" '
            '--attachment-mime-type application/x-truetype-font --attachment-name "Arial" '
            '--attachment-description "you" --attach-file "Arial.ttf" '
            '--attachment-mime-type application/x-truetype-font --attachment-name "Helvetica" '
            '--attachment-description "the font she tells you not to worry about" '
            '--attach-file-once "Helvetica.ttf" '
            '--language 0:Japanese --track-name 0:Hooplah "folder\\test.264" '
            '--language 0:Japanese --track-name 0:Hooplah "folder\\test.m4a"\n\n'
        )
        args = {'language': '0:Japanese', 'track-name': '0:Hooplah'}
        video_track = bench.commands.MkvTrack(video_dest_loc, args)
        audio_track = bench.commands.MkvTrack(audio_dest_loc, args)
        tracks = video_track, audio_track
        fontA = bench.commands.MkvAttachment(fontA_loc, fontA_mime_type, fontA_name,
                                             fontA_description)
        fontB = bench.commands.MkvAttachment(fontB_loc, fontB_mime_type, fontB_name,
                                             fontB_description, True)
        attachments = fontA, fontB
        bench.commands.write_mkvmerge_command(
            self.file, mkvmerge_loc, mux_output_loc, tracks, attachments)
        assertStrEqual(self.file.getvalue(), expected)

    def test_mkvmerge_vid_two_arg_audio_two_arg_two_attachment_full_two_global_args(self):
        expected = (
            'REM Mux folder\\test.mkv\n'
            '"Programs\\mkvmerge.exe" --output "folder\\test.mkv" '
            '--chapter-language eng --chapters chapters.xml '
            '--attachment-mime-type application/x-truetype-font --attachment-name "Arial" '
            '--attachment-description "you" --attach-file "Arial.ttf" '
            '--attachment-mime-type application/x-truetype-font --attachment-name "Helvetica" '
            '--attachment-description "the font she tells you not to worry about" '
            '--attach-file-once "Helvetica.ttf" '
            '--language 0:Japanese --track-name 0:Hooplah "folder\\test.264" '
            '--language 0:Japanese --track-name 0:Hooplah "folder\\test.m4a"\n\n'
        )
        global_args = {'chapters': 'chapters.xml', 'chapter-language': 'eng'}
        track_args = {'language': '0:Japanese', 'track-name': '0:Hooplah'}
        video_track = bench.commands.MkvTrack(video_dest_loc, track_args)
        audio_track = bench.commands.MkvTrack(audio_dest_loc, track_args)
        tracks = video_track, audio_track
        fontA = bench.commands.MkvAttachment(fontA_loc, fontA_mime_type, fontA_name,
                                             fontA_description)
        fontB = bench.commands.MkvAttachment(fontB_loc, fontB_mime_type, fontB_name,
                                             fontB_description, True)
        attachments = fontA, fontB
        bench.commands.write_mkvmerge_command(
            self.file, mkvmerge_loc, mux_output_loc, tracks, attachments, global_args)
        assertStrEqual(self.file.getvalue(), expected)


if __name__ == '__main__':
    unittest.main()
