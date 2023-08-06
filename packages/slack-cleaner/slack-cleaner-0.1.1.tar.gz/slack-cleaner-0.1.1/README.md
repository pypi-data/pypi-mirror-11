# slack-cleaner

Automatically delete messages on Slack.

## Install

```bash
pip install slack-cleaner
```

## Usage

```bash
# Delete all messages from a channel
slack-cleaner --token=<TOKEN> --messages --channel general

# Delete all messages from certain user
slack-cleaner --token=<TOKEN> --messages --channel gossip --user johndoe

# Delete all messages from bots
slack-cleaner --token=<TOKEN> --messages --channel auto-build --bot

# Delete all messages older than 2015/09/19
slack-cleaner --token=<TOKEN> --messages --channel general --before 20150919
```
