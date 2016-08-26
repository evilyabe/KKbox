import unittest, time
from selenium import webdriver
from selenium import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class test_search(unittest.TestCase):

	def setUp(self):
		# Launch Chrome browser and go to Https://www.kkbox.com/play/
		self.driver = webdriver.Chrome()
		self.driver.implicitly_wait(30)
		self.base_url = "https://www.kkbox.com/play/"

	def test_kkbox_webplayer(self):
		# Go to Https://www.kkbox.com/play/ and login to an account
		driver = self.driver
		driver.get(self.base_url)
		driver.find_element_by_id("uid").clear()
		driver.find_element_by_id("uid").send_keys("0988284686")
		driver.find_element_by_id("pwd").clear()
		driver.find_element_by_id("pwd").send_keys("evilyabe258")
		driver.find_element_by_id("login-btn").click()
		# Print out four button 「我的音樂庫」、「線上精選」、「電台」、「一起聽」
		login = driver.find_elements_by_xpath("//div[@id='container']//div[@class='sidebar-nav']//span")
		btn_number = len(login)
		for i in range(btn_number):
			if i > 3:
				break
			else:
				print(login[i].text + " " + "has been found!")
			
		wait = WebDriverWait(driver, 3)
		try:
			wait.until(EC.element_to_be_clickable((By.ID, "search_btn_cnt")))
			print("Your page is ready")
		except TimeoutException:
			print("It takes too long")
			
		# Test search function by entering "清平調"
		driver.find_element_by_xpath("//input[@type='text']").clear()
		driver.find_element_by_xpath("//input[@type='text']").send_keys("清平調")
		driver.find_element_by_id("search_btn_cnt").click()	
		time.sleep(3)
		# Search specific signer can be found after search
		singer = driver.find_elements_by_xpath("//div[@class='wrapper']//div[@class='songs-table']//div[@class='normal']//tr//td//following-sibling::td//a")
		for name in singer:
			keyword = "王菲&鄧麗君 (Faye Wong & Teresa Teng)"
			if	keyword in name.text:
				print("Signer: 王菲&鄧麗君 (Faye Wong & Teresa Teng) has been found!!")
				break
				
		# Click 「電台」and entering to Radio tab
		driver.find_element_by_xpath("//div[@id='container']//span[@translate='電台']").click()
		try:
			wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='main-content']//div[@class='cover']")))
			print("Your page is ready")
		except TimeoutException:
			print("It takes too long")
			
		# Click the first radio station
		station = driver.find_element_by_xpath("//div[@class='main-content']//div[@class='cover']")
		hidden_btn = driver.find_element_by_xpath("//div[@class='main-content']//div[@class='cover']//a[@class='btn-radio']")
		ActionChains(driver).move_to_element(station).click(hidden_btn).perform()
		try:
			WebDriverWait(driver, 3).until(EC.alert_is_present())
			alert = driver.switch_to_alert()
			alert.accept()
			print("alert accepted")
		except TimeoutException:
			print("There is no alert")
			
		time.sleep(3)
		#Check the song has been change to another one after click Dislike button
		current_song = driver.find_element_by_xpath("//div[@id='container']//div[@class='right-column']//div[@id='player']//h3//a").text
		dislike_btn = driver.find_element_by_xpath("//div[@class='main-content']//div[@class='controller-container']//a[@analytics-event='Dislike']")
		ActionChains(driver).move_to_element(dislike_btn).click().perform()
		time.sleep(3)
		next_song = driver.find_element_by_xpath("//div[@id='container']//div[@class='right-column']//div[@id='player']//h3//a").text
		if next_song != current_song:
			print("You have press Dislike button and change to next song")
		else:
			print("Song didn't change")

	def tearDown(self):
		self.driver.close()
		
if __name__ == '__main__':
	unittest.main()
