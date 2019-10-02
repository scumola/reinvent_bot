from config import *

import twitter
import pickledb

db = pickledb.load('session.db', True)

class ReinventBot():
    def __init__(self):
        global db

    def check_if_new(self, session_number):
        global db
        if (db.exists("id."+session_number)):
            return False  
        else:
            return True

    def check_if_updated(self, session_number, new_session_info):
        global db
        is_updated = False
        what_changed = ''
        session_number = session_number
        if (session_number == new_session_info['session_number']):
            version = db.get("version."+session_number)
            session_title = db.get("title."+session_number)
            start_time = db.get("starttime."+session_number)
            if start_time != new_session_info['start_time']:
                is_updated = True
                what_changed = what_changed + "Start Time, "
            else:
                is_updated = False
            end_time = db.get("endtime."+session_number)
            if end_time != new_session_info['end_time']:
                is_updated = True
                what_changed = what_changed + "End Time, "
            else:
                is_updated = False
            room_building = db.get("room."+session_number)
            if room_building != new_session_info['room_building']:
                is_updated = True
                what_changed = what_changed + "Room or Building, "
            else:
                is_updated = False

        if (is_updated):
            what_changed = what_changed[:-2]
            return (int(version) + 1), what_changed
        else:
            return False, False

    def _get_stored_session(self, session_number):
        # Find all records in DB with session_number
        # Set ScanIndexForward to False to return results sorted in desc order on version
        response = self.dynamodb.query(
            ExpressionAttributeValues={
                ':v1': {
                    'S': session_number,
                },
            },
            KeyConditionExpression='session_number = :v1',
            ScanIndexForward=False,
            TableName=self.table_name,
        )
        if (response['Count'] > 0):
            return response
        else:
            return 1

    def store_session(self, session_info):
        global db
        db.set("id."+session_info['session_number'],1)
        db.set("version."+session_info['session_number'],session_info['version'])
        db.set("title."+session_info['session_number'],session_info['session_title'])
        db.set("starttime."+session_info['session_number'],session_info['start_time'])
        db.set("endtime."+session_info['session_number'],session_info['end_time'])
        db.set("room."+session_info['session_number'],session_info['room_building'])
        db.set("abstract."+session_info['session_number'],session_info['abstract'])

    def log_execution(self, topic_id, execution_timestamp, status, duration):
        pass

    def _connect_to_twitter(self):
        api = twitter.Api(
            consumer_key=MY_CONSUMER_KEY,
            consumer_secret=MY_CONSUMER_SECRET,
            access_token_key=MY_ACCESS_TOKEN_KEY,
            access_token_secret=MY_ACCESS_TOKEN_SECRET)
        return api

    def send_tweet(self, tweet):
        tweet = self._process_tweet(tweet)
        status = self.api.PostUpdate(tweet)
        return status.text.encode('utf-8')

    def _process_tweet(self, tweet):
        tweet = (tweet[:125] + '...') if len(tweet) > 140 else tweet
        return tweet

