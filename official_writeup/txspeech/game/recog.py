import tempfile
import subprocess
import shlex
import json
import base64

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.asr.v20190614 import asr_client, models

try:
    from flag import getflag
except:
    def getflag(index):
        return [
            'fake{congrats, now get flag1 on the server}',
            'fake{congrats, now get flag2 on the server}',
        ][index-1]

# get an api key (5000 req / month for free) at https://cloud.tencent.com/product/asr if you need
API_KEY = "AKID2vSq5FF5nYNAoQq6B96sTrJn7HF8qQrK"
API_SECRET = "SKTEoVBzhGi5icEmDUhow54vmXTNA4ui"

ANSWER = "科技并带着趣味###不觉得这很酷吗###作为一名理工男###我觉得这太酷了###很符合我对未来生活的想象"

log = print

# below are audio formats as supported by tencent cloud api, except silk and speex (which cannot be decoded by ffmpeg)
# https://cloud.tencent.com/document/product/1093/35646

SUFFIX_TO_TENCENT_FORMAT = {
    'wav': 'wav',
    'pcm': 'pcm',
    'ogg': 'ogg-opus',
    'mp3': 'mp3',
    'm4a': 'm4a',
    'aac': 'aac',
}

SUFFIX_TO_FFMPEG_FORMAT = {
    'wav': 'wav',
    'pcm': 's16le',
    'ogg': 'ogg',
    'mp3': 'mp3',
    'm4a': 'm4a',
    'aac': 'aac',
}

def delay_correct(t):
    ret = 9500<=t<=10500
    if not ret:
        log(f'停顿时间错误：{t}ms')
    return ret

def recognize(format, data):
    b64_data = base64.b64encode(data).decode()
    try:
        cred = credential.Credential(API_KEY, API_SECRET)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "asr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = asr_client.AsrClient(cred, "", clientProfile)

        req = models.SentenceRecognitionRequest()
        params = {
            "ProjectId": 0,
            "SubServiceType": 2,
            "EngSerViceType": "8k_zh",
            "SourceType": 1,
            "VoiceFormat": format,
            "UsrAudioKey": "x",
            "Data": b64_data,
            "DataLen": len(data),
            "WordInfo": 1,
        }
        req.from_json_string(json.dumps(params))

        resp = client.SentenceRecognition(req)
        res = json.loads(resp.to_json_string())
        #print(res)
        
        if res["WordList"] is None:
            return []
        
        return [(w["Word"], w["StartTime"]) for w in res["WordList"]]

    except TencentCloudSDKException as err:
        log(f'腾讯云识别失败：{err}')
        return None
       
def ffmpeg_duration(format, data):
    with tempfile.NamedTemporaryFile() as tmpf:
        tmpf.write(data)
        tmpf.flush()
        try:
            out = subprocess.check_output(
                f'ffprobe -f {format} -ac 1 -ar 8000 {shlex.quote(tmpf.name)} -print_format json -show_format',
                shell=True,
            ).decode()
        except Exception as e:
            log('获取时长失败')
            return None
        else:
            log(f'ffprobe 输出：{out}')
        return float(json.loads(out)['format']['duration'])
       
def is_sentence_correct(words):
    left = ANSWER
    
    for idx, (word, time_ms) in enumerate(words):
        try:
            assert left.startswith(word)
            left = left[len(word):]
            if left.startswith('###'):
                assert delay_correct(words[idx+1][1] - time_ms)
                left = left[3:]
        except Exception:
            log(f'单词 #{idx} 验证失败')
            return False
    
    if left!='':
        log('句子不完整')
        return False
    
    return True
       
def main(suffix, data) -> bool:
    try:
        if suffix not in SUFFIX_TO_TENCENT_FORMAT:
            log('不支持这种格式')
            return False

        dur = ffmpeg_duration(SUFFIX_TO_FFMPEG_FORMAT[suffix], data)
        log(f'文件大小是 {len(data)} 字节')
        log(f'录音时长是 {dur} 秒')
        flag_condition_1 = 0<len(data)<=12288
        flag_condition_2 = .001<dur<=30
    except Exception as e:
        log(f'错误：{type(e)}')
        return False

    try:
        words = recognize(SUFFIX_TO_TENCENT_FORMAT[suffix], data)
        if words is None:
            return False
        if words==[]:
            log('没有识别到内容')
            return True

        log('识别结果如下：')
        for ind, (word, time_ms) in enumerate(words):
            log(f'#{ind:03d} {time_ms: 8d}ms {word}')

        if not is_sentence_correct(words):
            return True

        log('识别正确！')

        if flag_condition_1 or flag_condition_2:
            log(getflag(1))
        if flag_condition_1 and flag_condition_2:
            log(getflag(2))
        return True
    except Exception as e:
        log(f'错误：{type(e)}')
        return True
