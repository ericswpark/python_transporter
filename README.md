## Archival notice

As of June 13th, 2019, this project is now archived. No new commits will be pushed.

I may reopen this project again in the future.

# Transporter

Small script to send videos to ingest computer. Links sent to the specific Slack channel will be parsed and downloaded.

# Usage

1. Create a Slack App in the Slack App Directory.
2. Create a bot user.
3. Note down the token.
4. Launch this script **on** the ingest computer.
5. When prompted, enter 'y' and paste in your token.
6. Relaunch the script.
7. Invite your bot user to your specific channel (I recommend #transporter)
8. Have people post video links.
9. Transporter will grab and save video files.

# Supported services

Right now, only WeTransfer (wetransfer.com) links are supported. Other link type support is coming in the future.

# FAQ

### Q: How do I transfer across computers?

A: Copy the `config.ini` file to the new computer, making sure that it is located next to the Python script (or executable if you used something like Nukita.) Run. Video files will not be transferred.

### Q: Transporter is slow/not working.

A: Transporter does not support multi-threaded downloading because I created this script primarily to install on our ancient ingest computer. Therefore, to avoid choking disk I/O or bandwidth, I decided to keep it single-threaded. A multi-thread version might be a possibility in the future, with single-threaded operation invoked with arguments.

### Q: Transporter started overwriting files with the same name! What gives?

A: This is a known design flaw. We do this because sometimes you might submit the wrong file and want to resubmit. Therefore, you should only invite trusted members into the same chat as Transporter.

### Q: I have a suggestion/bug fix/feature addition. Where do I go?

Issues or pull request! Also, thank you!
