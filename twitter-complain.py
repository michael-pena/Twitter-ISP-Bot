from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

PROMISED_DOWN = 50  # the internet speed you're paying for in Mbps
DRIVER_PATH = ""  # add the driver path for your Chrome browser here
TWITTER_USERNAME = ""  # your Twitter username
TWITTER_PASSWORD = ""  # your Twitter password
ISP_TWITTER = "@"  # the twitter account of your ISP 


class InternetSpeedTwitterBot:
    def __init__(self):
        driver_path = DRIVER_PATH  # on windows add .exe
        self.down = 0.0
        self.driver = webdriver.Chrome(driver_path)

    def get_internet_speed(self):
        speed_url = "https://www.speedtest.net/"
        self.driver.get(speed_url)
        start_button = self.driver.find_element_by_class_name("start-text")
        start_button.click()
        time.sleep(60)
        self.down = float(self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text)
        print(f"Download Speed: {self.down}")

        # if download speeds are 5 Mbps slower than advertised, then complain
        if self.down < (PROMISED_DOWN - 5):
            print("The internet speeds are slower than promised.\nComplaining on Twitter...")
            self.complain_on_twitter()

    def complain_on_twitter(self):
        self.driver.get("https://twitter.com/login")
        time.sleep(2)
        username = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')
        time.sleep(2)
        username.send_keys(TWITTER_USERNAME)
        password = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')
        time.sleep(2)
        password.send_keys(TWITTER_PASSWORD)
        time.sleep(2)
        password.send_keys(Keys.ENTER)
        time.sleep(5)
        tweet = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div')
        tweet_msg = f"Hey {ISP_TWITTER}, why is my internet speed {self.down} Mbps when I pay for {PROMISED_DOWN} Mbps?"
        tweet.send_keys(tweet_msg)
        time.sleep(2)
        tweet_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]/div[3]')
        tweet_button.click()
        time.sleep(3)
        self.driver.quit()


bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
