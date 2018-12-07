import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def bilgicek(session, url):
    async with session.get(url) as response:
        return await response.text()

async def basla():
    async with aiohttp.ClientSession() as session:
        html = await bilgicek(session, 'https://www.doviz.com/')
        soup = BeautifulSoup(html, "lxml")
        dovizbolumu = soup.find('div', {'class': 'grid4 doviz-column2 btgreen'})
        for sira, doviz in enumerate(dovizbolumu.find_all("li")):
        	if sira > 0:
        		durum = doviz.find('div', {'class': 'arrow-row'})
        		yukseldi = None
        		if durum == '<div class="arrow-row"><span class="arrow-down"></span></div>':
        			yukseldi = False
        		elif durum == '<div class="arrow-row"><span class="arrow-up"></span></div>':
        			yukseldi = True
        		for bilgi in ((1, "USD"), (2, "EUR"), (3, "GBP"), (4, "CHF"), (5, "CAD")):
        			if sira == bilgi[0]:
        				print(("\n" if sira != 1 else "") + "• " +
        					str(bilgi[1]) + ":" + " " +
        					("(▲)" if yukseldi else "(▼)"))
        				break
        		parabirimleri = doviz.find_all('div', {'class': 'column2-row2'})
        		for sira2, doviz in enumerate(parabirimleri):
        			if sira2 == 0:
        				print("  • Alış: " + str(doviz.text) + " TL.")
        			elif sira2 == 1:
        				print("  • Satış: " + str(doviz.text) + " TL.")
loop = asyncio.get_event_loop()
loop.run_until_complete(basla())