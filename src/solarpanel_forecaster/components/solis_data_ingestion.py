from datetime import datetime
import hashlib
import hmac
import base64
from datetime import timezone
import requests
from solarpanel_forecaster import logger
import json
import pandas as pd
import time


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
        logger.info(
            'requests.post(req, data=Body, headers=header, timeout=500)')
        x = requests.post(req, data=Body, headers=header, timeout=500)

        return x

    def get_todays_data(self):

        todays_date = datetime.now()
        todays_formatted_date = todays_date.strftime("%Y-%m-%d")
        todays_extract = self.extract_day_data(
            extract_date=todays_formatted_date
            )
        return todays_extract.json()

    def convert_to_data_frame(self, raw_data) -> pd.DataFrame:
        df = pd.DataFrame(raw_data.json()['data'])

        df['timeStr'] = pd.to_datetime(df['timeStr'])
        dfCP = df.copy().drop(columns=["dataTimestamp", "time", "pacStr"])
        dfCP = dfCP.select_dtypes(exclude=['object'])

        dfCP = dfCP.set_index("timeStr")

        return dfCP

    def extract_full_daily_range(self, start_date, end_date):

        def simplified_sleep(duration):
            """For testing pause functionality independently."""
            logger.info(f'Start {duration} s pause')
            time.sleep(duration)
            logger.info('End pause')

        day_list = pd.date_range(start=start_date, end=end_date)

        df_all = pd.DataFrame()
        for day in day_list:
            # pause_duration = 10  # seconds
            # Test pause functionality independently
            # simplified_sleep(pause_duration)
            logger.info(f'running extract_day_data() on {day}')
            daily_extract = self.extract_day_data(extract_date=day)
            df_temp = self.convert_to_data_frame(raw_data=daily_extract)

            df_all = pd.concat([df_all, df_temp])

        return df_all
