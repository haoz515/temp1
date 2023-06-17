
import random
import time

import requests
import pandas as pd

def crawl_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    data_list = []
    next_cursor = ''

    while url:
        response = requests.get(url, headers=headers)
        data = response.json()

        items = data.get('items', [])
        for item in items:
            model_data = item.get('ai_model', {})
            cfg_data = item.get('configs')
            prompt_data = item.get('prompt', {})
            image_data = item.get('image_url', '')

            cfg_scale = cfg_data.get('cfg_scale') if cfg_data else None
            height = cfg_data.get('height') if cfg_data else None
            negative_prompt = cfg_data.get('negative_prompt') if cfg_data else None
            sampler = cfg_data.get('sampler') if cfg_data else None
            seed = cfg_data.get('seed') if cfg_data else None
            steps = cfg_data.get('steps') if cfg_data else None
            width = cfg_data.get('width') if cfg_data else None

            data_list.append({
                
                'id': item.get('id', ''),
                'ai_model': model_data,
                'ava_score': item.get('ava_score', ''),
                'cfg_scale': cfg_scale,
                'height': height,
                'negative_prompt': negative_prompt,
                'sampler': sampler,
                'seed': seed,
                'steps': steps,
                'width': width,
                'image_height': item.get('image_height', ''),
                'image_seed': item.get('image_seed', ''),
                'image_url': image_data,
                'image_width': item.get('image_width', ''),
                'prompt': prompt_data,
            })

        next_cursor = data.get('nextCursor', '')
        url = f'https://openart.ai/api/feed/community?cursor={next_cursor}' if next_cursor else None
        time.sleep(random.uniform(3, 5))


        # Write data to Excel after each page
        df = pd.DataFrame(data_list)

        print(df)
        print(url)
        df.to_excel('openard_data.xlsx', index=False)

    return data_list

if __name__ == '__main__':
    start_url = 'https://openart.ai/api/feed/community?cursor='
    data = crawl_data(start_url)
