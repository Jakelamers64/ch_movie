import pandas as pd
import re

def parse_srt_to_dataframe(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()

    # Split the data into subtitle blocks
    subtitle_blocks = re.split(r'\n{2,}', data.strip())

    nums = []
    times = []
    chinese_texts = []
    english_texts = []

    for block in subtitle_blocks:
        lines = block.split('\n')

        # Extract the subtitle number
        num = int(re.sub(r'\D', '', lines[0].strip()))
        nums.append(num)

        # Extract the time duration
        time_info = lines[1].strip()
        times.append(time_info)

        # Extract the Chinese and English text
        text = ' '.join(line.strip() for line in lines[2:])

        # Define a pattern to match Chinese characters (including punctuation and symbols)
        chinese_pattern = re.compile(r'[\u3000-\u303F\u4E00-\u9FFF\uFF00-\uFFEF\s]+')  # Unicode range for Chinese characters
        # Define a pattern to match English alphabetic characters (both lowercase and uppercase)
        english_pattern = re.compile(r'[a-zA-Z\s]+')  # Matches one or more English letters


        # Use the pattern to find all Chinese characters in the input string
        chinese_characters = chinese_pattern.findall(text)
        # Use the pattern to find all English letters in the input string
        english_letters = english_pattern.findall(text)

        chinese_texts.append(''.join(chinese_characters).strip())
        english_texts.append(''.join(english_letters).strip())

    # Create a DataFrame
    df = pd.DataFrame({
        "Num": nums,
        "Time": times,
        "Chinese": chinese_texts,
        "English": english_texts
    })

    return df

# Example usage
file_path = r"C:\Users\jakel\Desktop\Study\Language\Chinese\CTHD\[SubtitleTools.com] Crouching.Tiger.Hidden.Dragon.2000.720p.BluRay.x264.VPPV.cht -Chinese.srt"
df = parse_srt_to_dataframe(file_path)
df.to_csv("sent.csv", index=False)
print(df.head())
