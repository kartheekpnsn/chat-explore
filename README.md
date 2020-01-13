# Chat Explore

This is a script that generates an infographic that has statistics and plots between any two users whatsapp chat export.

- **Limitation**: Currently only works with **two** users chat, **Group chats** doesn't work.

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

Sample 1:
![Sample 1 Text](https://raw.githubusercontent.com/kartheekpnsn/chat-explore/master/samples/ss1.PNG "Output Sample 1")

Sample 2:
![Sample 2 Text](https://raw.githubusercontent.com/kartheekpnsn/chat-explore/master/samples/ss2.PNG "Output Sample 2")

### 7. Contributors

- [@Kartheek Palepu](https://www.github.com/kartheekpnsn)

### 8. Idea Credits

**Acknowledgement:**

- This entire idea is inspired from a reddit post (links posted below):
    - Link to the [post:](https://www.reddit.com/r/dataisbeautiful/comments/aiahpx/another_1_year_whatsapp_chat_visualization_oc/)
    - [Author Citation:](https://www.reddit.com/r/dataisbeautiful/comments/aiahpx/another_1_year_whatsapp_chat_visualization_oc/eem8gke/)