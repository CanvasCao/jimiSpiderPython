# -*- coding:UTF-8 -*-
# 测试selenium 没成功

from selenium import webdriver


driver = webdriver.PhantomJS()
driver.get("http://passport.cnblogs.com/user/signin?ReturnUrl=http%3A%2F%2Fwww.cnblogs.com%2F")
# driver.get('https://www.baidu.com/')

# driver.find_element_by_id('kw').send_keys('aaa')
# driver.find_element_by_id('su').click()

print driver.current_url
driver.quit()