import aiohttp
import os

from .utils import read_file_txt, read_file_json


class HideMyEmail:
    base_url = 'https://p68-maildomainws.icloud.com/v1/hme'

    def __init__(self, label: str = "rtuna's gen", cookie_path: str = os.path.join('data', 'cookies.txt'), params_path: str = os.path.join('data', 'params.json')):
        self.label = label
        self._cookie_file_path = cookie_path
        self._params_file_path = params_path

    async def __aenter__(self):
        self.params, cookies = self._load_files()

        self.s = aiohttp.ClientSession(
            headers={
                'Connection': "keep-alive",
                'Pragma': "no-cache",
                'Cache-Control': "no-cache",
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36",
                'Content-Type': "text/plain",
                'Accept': "*/*",
                'Sec-GPC': "1",
                'Origin': "https://www.icloud.com",
                'Sec-Fetch-Site': "same-site",
                'Sec-Fetch-Mode': "cors",
                'Sec-Fetch-Dest': "empty",
                'Referer': "https://www.icloud.com/",
                'Accept-Language': "en-US,en-GB;q=0.9,en;q=0.8,cs;q=0.7",
                'Cookie': cookies.strip()
            },
            timeout=aiohttp.ClientTimeout(total=10),
        )

        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        await self.s.close()

    def _load_files(self):
        if not os.path.exists(self._cookie_file_path):
            raise FileNotFoundError(
                f"File '{self._cookie_file_path}' does not exists.")

        if not os.path.exists(self._params_file_path):
            raise FileNotFoundError(
                f"File '{self._params_file_path}' does not exists.")

        cookies = read_file_txt(self._cookie_file_path)
        params = read_file_json(self._params_file_path)

        return params, cookies

    async def generate_email(self):
        async with self.s.post(f'{self.base_url}/generate', params=self.params) as resp:
            res = await resp.json()
            return res

    async def reserve_email(self, email: str):
        payload = {"hme": email, "label": self.label,
                   "note": "Generated by rtuna's iCloud email generator"}
        async with self.s.post(f'{self.base_url}/reserve', params=self.params, json=payload) as resp:
            res = await resp.json()
            return res
