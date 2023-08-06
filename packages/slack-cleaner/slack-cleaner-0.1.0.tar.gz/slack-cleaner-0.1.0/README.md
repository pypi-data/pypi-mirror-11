# slack-cleaner

Automatically delete messages on Slack.

## Usage

```bash
# Delete all messages from a channel
slack-cleaner --messages --channel general

# Delete all messages from certain user
slack-cleaner --messages --channel gossip --user johndoe

# Delete all messages from bots
slack-cleaner --messages --channel auto-build --bot

# Delete all messages older than 2015/09/19
slack-cleaner --messages --channel general --before 20150919
```
