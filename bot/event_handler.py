import json
import logging
import re

logger = logging.getLogger(__name__)


class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer

    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.write_help_message(event['channel'])
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        else:
            pass

    def _handle_message(self, event):
        # Filter out messages from the bot itself, and from non-users (eg. webhooks)
        if ('user' in event) and (not self.clients.is_message_from_me(event['user'])):
            import pdb; pdb.set_trace()
            msg_txt = event['text']

            if self.clients.is_bot_mention(msg_txt) or self._is_direct_message(event['channel']):
                
                # routes:   
                    # new task :task_name
                    # new event :task_name
                    # :task_name status
                    # help
                if re.search(r'^new task', msg_txt):
                    # add new task
                    pass
                elif re.search(r'^new event', msg_txt):
                    # add new event
                    pass
                elif 'status' in msg_txt:
                    # get status of a task
                    pass
                else:
                    # help!
                    pass

    def _is_direct_message(self, channel):
        """Check if channel is a direct message channel

        Args:
            channel (str): Channel in which a message was received
        """
        return channel.startswith('D')
