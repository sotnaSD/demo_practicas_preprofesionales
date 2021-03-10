from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pandas import DataFrame
from random import randint
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
from django.conf import settings

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from pandas import DataFrame
from random import randint, normalvariate
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep


# Create your views here.
class CrawlerWeb:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    elem = None

    # driver = webdriver.Chrome()

    def newDriver(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def setElement(self, by='q', findby=0):

        if (findby == 0):
            self.elem = self.driver.find_element_by_name(by)
        elif findby == 1:
            self.elem = self.driver.find_element_by_xpath(by)

        self.elem.clear()

    def searchByCSS(self, keys=[], elementsPath='', urlPath='', namePath='', next_element='', n_result=10):
        df = DataFrame(columns=['titulo', 'url'])
        next = None
        for key in keys:
            self.elem.send_keys(key)
            self.elem.send_keys(Keys.RETURN)
            while len(df) < int(n_result):
                lista = self.driver.find_elements_by_css_selector(elementsPath)
                for elem in lista:
                    try:
                        title = elem.find_element_by_css_selector(namePath)
                        url = elem.find_element_by_css_selector(urlPath).get_attribute("href")

                        df = df.append({'titulo': title.text, 'url': url}, ignore_index=True)
                    except (NoSuchElementException, StaleElementReferenceException) as exp:
                        pass
                sleep(randint(5, 8))
                try:
                    next = self.driver.find_element_by_xpath(next_element)
                    next.click()
                except NoSuchElementException:
                    break
        self.driver.close()
        return df

    def searchByXPATH(self, keys=[], elementsPath='', urlPath='', namePath='', next_element='', n_result=10):
        # self.driver = webdriver.Chrome()
        df = DataFrame(columns=['titulo', 'url'])
        next = None
        for key in keys:
            self.elem.send_keys(key)
            self.elem.send_keys(Keys.RETURN)
            print('///////////')
            print(len(df))
            print(n_result)
            while len(df) < int(n_result):
                lista = self.driver.find_elements_by_xpath(elementsPath)
                for elem in lista:
                    title = elem.find_element_by_xpath(namePath)
                    url = elem.find_element_by_xpath(urlPath).get_attribute("href")

                    df = df.append({'titulo': title.text, 'url': url}, ignore_index=True)
                sleep(randint(5, 8))
                try:
                    next = self.driver.find_element_by_xpath(next_element)
                    next.click()
                except NoSuchElementException:
                    break
        self.driver.close()
        return df

    def setUrl(self, url):
        self.driver.get(url)

    def e_commerceML(self, keys=[], elementsPath='li.ui-search-layout__item',
                     urlPath='a.ui-search-link',
                     namePath='h2.ui-search-item__title',
                     next_element='//a[@title="Siguiente"', n_result=10):
        return self.searchByCSS(keys, elementsPath, urlPath, namePath, next_element, n_result)

    def e_commerceOLX(self, key='', elementsPath='//li[@data-aut-id="itemBox"]',
                      buttonPath='//button[@data-aut-id="btnLoadMore"]', titlePath='.//span[@data-aut-id="itemTitle"]',
                      urlPath='.//a', n_result=1):
        # self.driver = webdriver.Chrome()
        df = DataFrame(columns=['titulo', 'url'])
        self.driver.get('https://www.olx.com.ec/items/q-' + key)
        for i in range(int(n_result)):
            try:
                # //button[@data-aut-id="btnLoadMore"]
                boton = self.driver.find_element_by_xpath(buttonPath)
                boton.click()
                sleep(randint(5, 6))
                boton = self.driver.find_element_by_xpath(buttonPath)
            except:
                break

        lista = self.driver.find_elements_by_xpath(elementsPath)
        print(len(lista))
        for elem in lista:
            # Por cada anuncio hallo el preico

            try:
                title = elem.find_element_by_xpath(titlePath).text
                url = elem.find_element_by_xpath(urlPath).get_attribute("href")
                df = df.append({'titulo': title, 'url': url}, ignore_index=True)
            except StaleElementReferenceException:
                print('error')
        self.driver.close()
        return df

    def e_commerceAmz(self, keys=[], elementsPath='//div[@data-component-type="s-search-result"]',
                      urlPath='.//a[@class="a-link-normal a-text-normal"]',
                      namePath='.//span[@class="a-size-base-plus a-color-base a-text-normal"]',
                      next_element='//li[@class="a-last"]', n_result=10):
        return self.searchByXPATH(keys, elementsPath, urlPath, namePath, next_element, n_result)

    def pinterest(self, keys=[], elementsPath='div.Yl-.MIw.Hb7', urlPath='.//a', namePath='.//figcaption/h3',
                  imgPath='.//img', n_result=4):
        df = DataFrame(columns=['elemento', 'url', 'img', 'titulo', 'descripcion'])
        self.pinterestLogin(settings.PINTEREST_USERNAME, settings.PINTEREST_PASSWORD)
        sleep(randint(1, 3))
        i = 0

        for key in keys:

            self.driver.get('https://www.pinterest.com/search/pins/?q=' + key)
            body = self.driver.find_element_by_css_selector('body')
            for k in range(int(n_result) + 1):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            lista = self.driver.find_elements_by_css_selector(elementsPath)
            print(len(lista))
            for elem in lista:
                try:
                    title = 'Elemento ' + str(i)
                    url = elem.find_element_by_xpath(urlPath).get_attribute("href")
                    img = elem.find_element_by_xpath(imgPath).get_attribute("src")
                    print('------', url, '----')
                    i += 1
                    df = df.append({'elemento': title, 'url': url, 'img': img}, ignore_index=True)
                except NoSuchElementException:
                    break
                except StaleElementReferenceException:
                    pass
        self.driver.close()
        return df

    def pinterestLogin(self, user, password):
        self.driver.get("https://www.pinterest.com")
        self.driver.implicitly_wait(30)
        try:
            login_elem = self.driver.find_element_by_class_name('Il7')
            login_elem.send_keys(Keys.ENTER)
            self.pause()
            email_elem = self.driver.find_element_by_name('id')
            email_elem.send_keys(user)
            self.pause()
            pw_elem = self.driver.find_element_by_name('password')
            pw_elem.send_keys(password)
            self.pause()
            login_elem = self.driver.find_element_by_class_name('SignupButton')
            login_elem.send_keys(Keys.RETURN)
        except NoSuchElementException:
            self.pause()
            email_elem = self.driver.find_element_by_name('id')
            email_elem.send_keys(user)
            self.pause()
            pw_elem = self.driver.find_element_by_name('password')
            pw_elem.send_keys(password)
            self.pause()
            login_elem = self.driver.find_element_by_class_name('SignupButton')
            login_elem.send_keys(Keys.ENTER)

    def getPinterestUrl(self, data):
        df_comentarios = DataFrame(columns=['url', 'comentario'])
        # dftitle = DataFrame(columns=['url', 'titulo', 'descripcion'])
        self.pinterestLogin(settings.PINTEREST_USERNAME, settings.PINTEREST_PASSWORD)
        sleep(randint(1, 3))
        commentTab = './/div[@data-test-id="canonicalCommentsTab"]'
        commentButton = '//button[@aria-label="Mostrar más"]'
        moreComment = './/div[@class="tBJ dyH iFc _yT B9u DrD IZT mWe"]'
        title = './/h1[@class="lH1 dyH iFc ky3 pBj DrD IZT"]'
        description = './/span[@class="tBJ dyH iFc MF7 pBj DrD IZT swG"]'
        # for i in data['url']:

        for index, fila in data.iterrows():
            self.driver.get(fila.url)
            # print(self.driver.get_attribute('innerHTML'))
            sleep(randint(1, 2))
            # seccion de comentarios
            try:
                titulo = self.driver.find_element_by_xpath(title).text
            except Exception as e:
                titulo = ''
            try:
                descripcion = self.driver.find_element_by_xpath(description).text
            except:
                descripcion = ''
            print(titulo, descripcion)
            fila.titulo = titulo
            fila.descripcion = descripcion
            # dftitle = dftitle.append({'url': fila.url, 'titulo': titulo,    'descripcion': descripcion}, ignore_index=True)
            try:
                # //button[@data-aut-id="btnLoadMore"]
                comentario = self.driver.find_element_by_xpath(commentButton)
                comentario.click()
            except:
                try:
                    comentario = self.driver.find_element_by_xpath(commentTab)
                    comentario.click()
                except Exception as e:
                    print('error en tab')
                    comentario = ""
                    pass
            while 1:
                print("aquiiiiiii")
                try:
                    comentarios = self.driver.find_element_by_xpath(moreComment)
                    comentarios.click()
                except Exception as e:
                    break
                sleep(randint(1, 2))
            textos = self.driver.find_elements_by_xpath('.//span[@class="tBJ dyH iFc _yT pBj DrD swG"]')
            print(len(textos))
            for text in textos:
                df_comentarios = df_comentarios.append({'url': fila.url, 'comentario': text.text}, ignore_index=True)
        self.driver.close()
        return data, df_comentarios

    def pause(self):
        sleep(abs(normalvariate(3, 0.2)))
