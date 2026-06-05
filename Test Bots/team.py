import random, time
from playwright.sync_api import sync_playwright
import concurrent.futures

n = input("Имена для БотНета: ")
c = int(input("Сколько раз заходить: "))
u = input("Юзернейм канала (без @): ")

def j():
 with sync_playwright() as p:
  b = p.chromium.launch(headless=False)
  ct = b.new_context()
  pg = ct.new_page()

  try:
   pg.goto('https://web.teamgram.net/a/ ', timeout=60000)
   pg.click('button:has-text("Log in by phone Number")')
   ph = '+86' + ''.join(str(random.randint(0,9)) for _ in range(10))
   pg.fill('#sign-in-phone-number', ph)
   pg.click('button:has-text("Next")')

   pg.wait_for_selector('#sign-in-code', state='visible', timeout=45000)
   pg.fill('#sign-in-code', '12345')
   pg.press('#sign-in-code', 'Enter')

   pg.wait_for_selector('#registration-first-name', state='visible', timeout=30000)
   pg.fill('#registration-first-name', n)
   pg.click('div.ripple-container')

   pg.wait_for_selector('#telegram-search-input', state='visible', timeout=30000)
   s = pg.query_selector('#telegram-search-input')
   s.click(); s.focus(); s.fill('')
   for ch in u:
    s.press(ch)
    time.sleep(0.1)

   pg.wait_for_selector('div.ListItem.chat-item-clickable.search-result', timeout=60000)
   cs = f'div.ListItem.chat-item-clickable.search-result:has-text("{u}")'
   pg.wait_for_selector(cs, timeout=30000)
   pg.click(cs)

   js = 'button.Button.tiny.primary.fluid.has-ripple:has-text("Join Channel")'
   pg.wait_for_selector(js, timeout=30000)
   pg.click(js)

   print(f"Вступил в {u}")
   pg.screenshot(path=f's_{time.time()}.png')
   time.sleep(3)
   ct.close()
   b.close()

  except Exception as e:
   print(f"E: {e}")
   pg.screenshot(path=f'e_{time.time()}.png')
   try:ct.close();b.close()
   except:pass

def m():
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
  f = [ex.submit(j) for _ in range(c)]
  concurrent.futures.wait(f)

m()