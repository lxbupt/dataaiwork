import json

from flask import Blueprint, request, render_template

from dao.SongDao import SongDao

nlpController = Blueprint("nlpController", __name__)


@nlpController.route('/gensong', methods=['get'])
def genSong():
    startWords = request.args.get('startwords')
    nums = request.args.get('nums')
    if startWords and nums and nums.isdigit():
        text = "锄禾日当午"
        song_dao = SongDao()
        song_dao.insert_song(startWords, int(nums), text)
        return json.dumps({'success': 1, 'content': text})
    else:
        return json.dumps({'success': 0, 'content': ''})
    pass


@nlpController.route("/gogensong")
def goGenSong():
    return render_template('gensong02.html')
    pass


@nlpController.route('/allsongs', methods=['get'])
def getAllSongs():
    song_dao = SongDao()
    songs = song_dao.get_all_songs()
    return json.dumps({'success': 1, 'content': songs})
