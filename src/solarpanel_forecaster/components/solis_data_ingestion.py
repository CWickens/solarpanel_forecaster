from datetime import datetime
import hashlib
import hmac
import base64
from datetime import timezone
import requests
from solarpanel_forecaster import logger
import json


class SolisDataIngestion:
    def __init__(
            self,
            config,
            config_secret):
        self.config = config
        self.config_secret = config_secret

    def save(self, data: json):
        output_file = self.config.output_file

        with open(output_file, 'w') as f:
            logger.info(f'Saving to {output_file}')
            json.dump(data, f)
            logger.info('Saving complete!')

    def _encode_data_request_string(self, request_day) -> str:
        return base64.b64encode(
            hashlib.md5(
                request_day.encode(self.config.encoder)
                ).digest()
                ).decode(self.config.encoder)

    def _prepare_data_request(self, date) -> str:

        str_date = date
        single_day_request = {"sn": f"{self.config_secret.sn}",
                              "time": f"{str_date}",
                              "timeZone": "0"}
        single_day_request = f'{single_day_request}'
        single_day_request = single_day_request.replace("'", "\"")
        encoded_single_day_request = self._encode_data_request_string(
            request_day=single_day_request)

        return encoded_single_day_request, single_day_request

    def extract_day_data(self, extract_date):
        Content_MD5, Body = self._prepare_data_request(date=extract_date)
        now = datetime.now(timezone.utc)
        Date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

        encryptStr = (self.config.VERB + "\n"
                      + Content_MD5 + "\n"
                      + self.config.Content_Type + "\n"
                      + Date + "\n"
                      + self.config.CanonicalizedResource)

        secretKey = self.config_secret.secretKey.encode('utf-8')
        h = hmac.new(secretKey,
                     msg=encryptStr.encode(self.config.encoder),
                     digestmod=hashlib.sha1)
        Sign = base64.b64encode(h.digest())
        Authorization = "API " + self.config_secret.KeyId + ":" \
                        + Sign.decode(self.config.encoder)

        header = {"Content-MD5": Content_MD5,
                  "Content-Type": self.config.Content_Type,
                  "Date": Date,
                  "Authorization": Authorization
                  }

        req = self.config.url + self.config.CanonicalizedResource
        x = requests.post(req, data=Body, headers=header)

        return x

    def get_todays_data(self):

        todays_date = datetime.now()
        todays_formatted_date = todays_date.strftime("%Y-%m-%d")
        todays_extract = self.extract_day_data(
            extract_date=todays_formatted_date
            )
        return todays_extract.json()
