# Chat Explore

This is a script that generates an infographic that has statistics and plots between any two users whatsapp chat export.

- **Limitation 1**: Currently only works with **two** users chat, **Group chats** doesn't work.
- **Limitation 2**: Currently only works for Android exports. **iOS** not supported.

## Getting Started

### 1. Install Python 3+

If you don't already have Python 3+ installed, grab it from <https://www.python.org/downloads/>. You'll want to download install the latest version of **Python 3.x**. As of 2019-11-22, that is Version 3.8.

### 2. Get Your Whatsapp Chat Export Data
Here you can find out how to export your whatsapp chat between two users: <https://faq.whatsapp.com/en/android/23756533/></br>

To use this script, you need to export the chat history between yourself and any other user.
That exported chat (.txt) needs to be present in the same system which runs the code mentioned below.

### 3. Clone This Repository

On <https://github.com/kartheekpnsn/chat-explore>, click the green "Clone or Download" button at the top right of the page. If you want to get started with this script more quickly, click the "Download ZIP" button, and extract the ZIP somewhere on your computer.

### 4. Install Dependencies

In a [command prompt or Terminal window](https://tutorial.djangogirls.org/en/intro_to_command_line/#what-is-the-command-line), [navigate to the directory](https://tutorial.djangogirls.org/en/intro_to_command_line/#change-current-directory) containing this repository's files. Then, type the following, and press enter:

```shell
pip install -r requirements.txt
```

#### wordcloud installation problem
**Note**: If you are facing issues installing `wordcloud` on Windows10. The follow the below procedure.

- Go to: https://www.lfd.uci.edu/~gohlke/pythonlibs/#wordcloud
- Click on the matching whl file to download.
    - **Naming**: wordcloud-**[version]**-cp **[python-version]**-cp **[python-version]**-win **[32bit-or-64bit]**.whl
- Then below command in command prompt

```shell
pip install <location_of_wordcloud_whl_file>
```

**Example:**

```shell
pip install "C:\Users\Testuser\Desktop\wordcloud-1.6.0-cp38-cp38-win32.whl"
```


### 5. Run the Script

In the same command prompt or Terminal window, type the following, and press enter:

```shell
python run.py -f <file_path>
```

#### Example:
```shell
python run.py -f "C:\Users\Testuser\Desktop\WhatsApp Chat with Kartheek.txt"
```

### 6. Sample Output

**Sample 1**:

![Sample 1 Text](https://raw.githubusercontent.com/kartheekpnsn/chat-explore/master/samples/ss1.PNG "Output Sample 1")

**Sample 2**:

![Sample 2 Text](https://raw.githubusercontent.com/kartheekpnsn/chat-explore/master/samples/ss2.PNG "Output Sample 2")

### 7. Update Patch

- `16Jan2020` Added First to text feature in the plots
- `17Jan2020`: Sentiment over period of time, Usual Sentiment through out the 24 hours
    - Can help in understanding if people are showing positive emotions in the morning and negative in the evenings.
- TODO: Parser for iOS exports.


### 8. Contributors

- [@Kartheek Palepu](https://www.github.com/kartheekpnsn)
- [@Yashwanth Kuruganti](https://github.com/yashkuru)

### 9. Idea Credits

**Acknowledgement:**

- This entire idea is inspired from a reddit post (links posted below):
    - Link to the [post](https://www.reddit.com/r/dataisbeautiful/comments/aiahpx/another_1_year_whatsapp_chat_visualization_oc/)
    - [Author Citation](https://www.reddit.com/r/dataisbeautiful/comments/aiahpx/another_1_year_whatsapp_chat_visualization_oc/eem8gke/)
