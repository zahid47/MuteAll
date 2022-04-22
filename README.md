<div align="center">

  <h1>MuteAll</h1>
  
  <p>This bot was made for groups of friends who play among us together and use discord to communicate. Sometimes people can't or forget to mute themselves and accidentally talk during the game. With this bot, you can mute everyone with a simple command at the start of each game!</p>

<br />

[Invite The Bot](https://discord.com/api/oauth2/authorize?client_id=757369495953342593&permissions=12659776&scope=bot%20applications.commands)

[Join Support Server](https://discord.gg/8hrhffR6aX)

</div>

<!-- Screenshots -->

### Demo Video

- [MuteAll Demo](https://youtu.be/-NQuA2iPri4)

<!-- TechStack -->

### Tech Stack

  <ul>
    <li><a href="https://github.com/Rapptz/discord.py">discord.py</a></li>
    <li><a href="https://pymongo.readthedocs.io/en/stable/">PyMongo</a></li>
  </ul>

<!-- Features -->

### How to use

- Type `.help` to view all the available commands
- Type `.m` to mute and `.u` to unmute everyone in your current voice channel

<br>

<!-- Getting Started -->

## Run Locally

<br>

<!-- Prerequisites -->

### Prerequisites

Python 3.8 or higher is required

<!-- Env Variables -->
<br>

### Environment Variables

To run this project yourself, you will need to add the following environment variables to your .env file

`DISCORD_TOKEN`

`MONGO_STRING`

<!-- Run Locally -->
<br>

### Getting Started

Clone the project

```bash
  git clone https://github.com/zahid47/MuteAll.git
```

Go to the project directory

```bash
  cd MuteAll
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the bot

```bash
  python -m MuteAll
```

<!-- Roadmap -->
<br>

## Todo

- [ ] Add slash commands and buttons

<!-- FAQ -->
<br>

## FAQ

- Why is the bot not muting anyone/everyone?

  - Make everyone disconnect and reconnect to the Voice Channel again

- How can I restrict the bot so that only a select few can use the commands?

  - Give those select few the 'Mute Members' permission, and no one else.

- How do I only mute a specific user or role?

  - Just mention the users or roles after your command! Ex: `.m @username @rolename`

<!-- Contact -->
<br>

## Contact

scarecow#2857 on discord

<!-- Acknowledgments -->
<br>

## Acknowledgements and special Thanks

- [discord.py](https://github.com/Rapptz/discord.py)
- [awesome-readme-template](https://github.com/Louis3797/awesome-readme-template)
