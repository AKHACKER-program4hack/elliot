# Elliot
![Python Version](https://img.shields.io/badge/Python-v3.9-blue)
[![Join Group](https://img.shields.io/badge/Telegram-Join%20Group-informational)](https://t.me/program4hack)
![Pull Requests](https://img.shields.io/github/issues-pr/AKHACKER-program4hack/elliot)

The faster and time saving md5 hash cracker
Save time by saving session.

<img src="elliotgithub.jpg">

## Usage
```
$ python3 elliot.py

usage: elliot.py [-h] [-w WORDLIST] [--min MIN] [--max MAX] [--char CHARS]
                 [-t HASH] [-n NEWSESSION] [-r RESUMESESSION]
                 [--output OUTPUTFILE]

optional arguments:
  -h, --help            show this help message and exit
  -w WORDLIST           Path of wordlist
  --min MIN             minimum lenght of chars
  --max MAX             maximum lenght of chars
  --char CHARS, -c CHARS
                        characters to use in brute force using incremental
                        mode avaliable : [ lower upper num symbol ] use (,) to
                        use together like lower,num
  -t HASH               md5hash to crack
  -n NEWSESSION         Session name with path
  -r RESUMESESSION      Path of session file
  --output OUTPUTFILE, -o OUTPUTFILE
                        Path of output file where password will store after
                        cracking it

```
# Session saving 
If You use sessions,the tools will save the session after every 5 minute.I hope this update make you more happy
Use ```-n``` for saving iterations while cracking md5 hash 
example : 
```
$ python3 elliot.py -t d6a6bc0db10694a2d90e3a69648f3a03 -o cracked.txt -n akhacker.session
```
For Resuming from the last iteration use ```-r``` option and give the path of session file example:

```
$ python3 elliot.py -r <session file path>
```

for more info see the video on youtube

```
For more info see the video on Official YouTube Channel Of AK.HACKER.
```
<a href="https://youtu.be/DSOOCnM8mXk"><img src="https://img.shields.io/badge/How%20To%20Deploy-blue.svg?logo=Youtube"></a>
<a href="https://youtu.be/DSOOCnM8mXk"><img src="https://img.shields.io/youtube/views/DSOOCnM8mXk?style=social"></a>

# Follow me on Social media
> instagram : akhacker_program4hack

