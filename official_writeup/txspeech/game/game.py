from flask import *
from flag import checktoken
from pathlib import Path
import time
import os

import recog
import logger

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = int(2.1*1024*1024)

MAX_SUBMISSION = 400
SUBMISSION_COOLDOWN = 10
HIST_PATH = Path('history')

def get_tot_submission(uid) -> int:
    (HIST_PATH / uid).mkdir(exist_ok=True)
    if not (HIST_PATH / uid / 'submission.txt').exists():
        return 0
    with (HIST_PATH / uid / 'submission.txt').open() as f:
        cnt = int(f.read().strip())
    return cnt

def get_last_submission(uid) -> float:
    if not (HIST_PATH / uid / 'last.txt').exists():
        return 0
    with (HIST_PATH / uid / 'last.txt').open() as f:
        return float(f.read().strip())

def do_recog(uid, suffix, data):
    logs = []
    def do_log(s):
        logs.append(s)
        logger.write(uid, ['output', s])
    recog.log = do_log

    is_tx_succ = recog.main(suffix, data)
    return is_tx_succ, '\n'.join(logs)

@app.get('/')
def index():
    token = os.environ.get('hackergame_token', '')
    uid = checktoken(token)
    if not uid:
        return 'Invalid token! Please contact staff.'

    submission_left = MAX_SUBMISSION - get_tot_submission(uid)
    return render_template('index.html', submission_left=submission_left)

@app.post('/submit')
def submit():
    token = os.environ.get('hackergame_token', '')
    uid = checktoken(token)
    if not uid:
        return 'Invalid token! Please contact staff.'

    submission_idx = get_tot_submission(uid)
    if MAX_SUBMISSION - submission_idx <= 0:
        return 'No submission quota left, please contact staff!'

    last_ts = get_last_submission(uid)
    if time.time() - last_ts < SUBMISSION_COOLDOWN:
        return 'Wait for submission cool down!'

    file = request.files['file']
    suffix = file.filename.split('.')[-1]

    data = file.stream.read()
    if len(data)>2.1*1024*1024:
        return 'File too large!'

    if suffix=='ogg_':
        suffix = 'ogg'
    if suffix not in ['wav', 'pcm', 'ogg', 'mp3', 'm4a', 'aac']:
        return 'Invalid file type!'

    logger.write(uid, ['submit', submission_idx, suffix, len(data)])

    with (HIST_PATH / uid / 'last.txt').open('w') as f:
        f.write(str(time.time()))

    is_tx_succ, res = do_recog(uid, suffix, data)

    logger.write(uid, ['done', submission_idx, is_tx_succ])

    if is_tx_succ:
        with (HIST_PATH / uid / f'{submission_idx}.{suffix}').open('wb') as f:
            f.write(data)
        with (HIST_PATH / uid / 'submission.txt').open('w') as f:
            f.write(str(submission_idx+1))

    return render_template('success.html', res=res)