import re

# Dữ liệu video của ngôn ngữ kí hiệu mỹ
video_data_en = {
    'Màu sắc': [{'id': 1, 'title': 'màu xanh da trời', 'url': 'https://youtu.be/t2T1_LMVTp8', 'type': 'danh từ'},
                {'id': 2, 'title': 'màu xanh lá cây', 'url': 'https://youtu.be/WrkXE5l6udM', 'type': 'danh từ'},
                {'id': 3, 'title': 'màu trắng', 'url': 'https://youtu.be/uLjkLwFvFtw', 'type': 'danh từ'},
                {'id': 4, 'title': 'màu đỏ', 'url': 'https://youtu.be/lDBvf8SoQuc', 'type': 'danh từ'},
                {'id': 5, 'title': 'màu nâu', 'url': 'https://youtu.be/HGBcts4shKw', 'type': 'danh từ'},
                {'id': 6, 'title': 'màu cam', 'url': 'https://youtu.be/Wt4p6qWgR1k', 'type': 'danh từ'},
                {'id': 7, 'title': 'màu đen', 'url': 'https://youtu.be/O5_4x8p5t4U', 'type': 'danh từ'},
                {'id': 8, 'title': 'màu vàng', 'url': 'https://youtu.be/IjOjCvwsuAk', 'type': 'danh từ'},
                {'id': 9, 'title': 'màu bạc', 'url': 'https://youtu.be/Yi52SqYnlJE', 'type': 'danh từ'}],

    'Trái cây': [{'id': 11, 'title': 'quả chuối', 'url': 'https://youtu.be/4yKyCDC-Tdc', 'type': 'danh từ'},
                 {'id': 12, 'title': 'quả chanh', 'url': 'https://youtu.be/TIYO3ae3nQg', 'type': 'danh từ'},
                 {'id': 13, 'title': 'quả nho', 'url': 'https://youtu.be/NZ68mfHiZa8', 'type': 'danh từ'},
                 {'id': 14, 'title': 'quả lê', 'url': 'https://youtu.be/FoRAeYTyrFk', 'type': 'danh từ'},
                 {'id': 15, 'title': 'quả táo', 'url': 'https://youtu.be/3wIiujOP6Ag', 'type': 'danh từ'}],

    'Thức ăn': [{'id': 16, 'title': 'pizza', 'url': 'https://youtu.be/XIZ2DrdEU3k', 'type': 'danh từ'},
                {'id': 17, 'title': 'hộp sữa', 'url': 'https://youtu.be/quk_XoRtZWk', 'type': 'danh từ'},
                {'id': 18, 'title': 'hamburger', 'url': 'https://youtu.be/IIt5fF-D6d0', 'type': 'danh từ'},
                {'id': 19, 'title': 'trứng', 'url': 'https://youtu.be/uEvKmWqFE-4', 'type': 'danh từ'},
                {'id': 20, 'title': 'kẹo', 'url': 'https://youtu.be/EfJ4xLiX5IA', 'type': 'danh từ'}],

    'Công việc': [{'id': 21, 'title': 'nhân viên', 'url': 'https://youtu.be/akaN6CRjpt0', 'type': 'danh từ'},
                  {'id': 22, 'title': 'nghệ sĩ', 'url': 'https://youtu.be/jORXCych9Q4', 'type': 'danh từ'},
                  {'id': 23, 'title': 'kiến trúc sư ( kĩ sư, thiết kế )', 'url': 'https://youtu.be/YJJQUuKfcpQ', 'type': 'danh từ'},
                  {'id': 24, 'title': 'kiến trúc sư ( nhà cửa )', 'url': 'https://youtu.be/JAp9aao8ciU', 'type': 'danh từ'},
                  {'id': 25, 'title': 'đạo diễn', 'url': 'https://youtu.be/f5yud3flnAQ', 'type': 'danh từ'}],

    'Động vật': [{'id': 26, 'title': 'con mèo', 'url': 'https://youtu.be/ekFrFoJ-x78', 'type': 'danh từ'},
                 {'id': 27, 'title': 'con chó', 'url': 'https://youtu.be/IbpJtH_QssM', 'type': 'danh từ'},
                 {'id': 28, 'title': 'con chim', 'url': 'https://youtu.be/Bibgy-yjgYE', 'type': 'danh từ'},
                 {'id': 29, 'title': 'con ngựa', 'url': 'https://youtu.be/xCJGQseQ3Fw', 'type': 'danh từ'},
                 {'id': 30, 'title': 'con bò', 'url': 'https://youtu.be/I2_nB2cXP58', 'type': 'danh từ'},
                 {'id': 31, 'title': 'con cừu', 'url': 'https://youtu.be/0sF9ZKAYAwo', 'type': 'danh từ'},
                 {'id': 32, 'title': 'con lợn', 'url': 'https://youtu.be/WaW7OJUi_nc', 'type': 'danh từ'},
                 {'id': 33, 'title': 'sâu bọ, côn trùng', 'url': 'https://youtu.be/a-COvvqJXe8', 'type': 'danh từ'}],

    'Thời gian': [{'id': 34, 'title': 'ban ngày', 'url': 'https://youtu.be/6Ag2Q2J9DAU', 'type': 'danh từ'},
                 {'id': 35, 'title': 'ban đêm', 'url': 'https://youtu.be/jNiRlzvjd5U', 'type': 'danh từ'},
                 {'id': 36, 'title': 'tuần', 'url': 'https://youtu.be/N6giWOcMj2U', 'type': 'danh từ'},
                 {'id': 37, 'title': 'tháng', 'url': 'https://youtu.be/YLuGuPS6NU8', 'type': 'danh từ'},
                 {'id': 38, 'title': 'tương lai', 'url': 'https://youtu.be/RMUZFdu6VtI', 'type': 'danh từ'},
                 {'id': 39, 'title': 'mùa xuân', 'url': 'https://youtu.be/5h69GQntuhw', 'type': 'danh từ'},
                 {'id': 40, 'title': 'mùa hạ', 'url': 'https://youtu.be/AaXReP9YjVE', 'type': 'danh từ'},
                 {'id': 41, 'title': 'mùa thu', 'url': 'https://youtu.be/g_DZl3jIAbY', 'type': 'danh từ'},
                 {'id': 42, 'title': 'mùa đông', 'url': 'https://youtu.be/9bLENg2AXrY', 'type': 'danh từ'}],

    'Gia đình': [{'id': 43, 'title': 'mẹ', 'url': 'https://youtu.be/DHl2-NT3mIM', 'type': 'danh từ'},
                 {'id': 44, 'title': 'bố', 'url': 'https://youtu.be/1Vllc4F5ic0', 'type': 'danh từ'},
                 {'id': 45, 'title': 'chú', 'url': 'https://youtu.be/PqtMCA2lu9w', 'type': 'danh từ'}]
}

# Dữ liệu video của ngôn ngữ kí hiệu việt nam ( miền bắc )
video_data_vn = {
    'Màu sắc': [{'id': 1, 'title': 'màu xanh da trời', 'url': 'https://qipedc.moet.gov.vn/videos/W02142B.mp4', 'type': 'danh từ'},
                {'id': 2, 'title': 'màu xanh lá cây', 'url': 'https://qipedc.moet.gov.vn/videos/W02143B.mp4', 'type': 'danh từ'},
                {'id': 3, 'title': 'màu trắng', 'url': 'https://qipedc.moet.gov.vn/videos/W02140B.mp4', 'type': 'danh từ'},
                {'id': 4, 'title': 'màu đỏ', 'url': 'https://qipedc.moet.gov.vn/videos/W02134.mp4', 'type': 'danh từ'},
                {'id': 5, 'title': 'màu nâu', 'url': 'https://qipedc.moet.gov.vn/videos/W02137B.mp4', 'type': 'danh từ'},
                {'id': 6, 'title': 'màu cam', 'url': 'https://qipedc.moet.gov.vn/videos/W02132.mp4', 'type': 'danh từ'},
                {'id': 7, 'title': 'màu đen', 'url': 'https://qipedc.moet.gov.vn/videos/W02133B.mp4', 'type': 'danh từ'}], # thieu mau bac

    'Trái cây': [{'id': 11, 'title': 'quả chuối', 'url': 'https://qipedc.moet.gov.vn/videos/W02730.mp4', 'type': 'danh từ'},
                 {'id': 12, 'title': 'quả chanh', 'url': 'https://qipedc.moet.gov.vn/videos/W02728.mp4', 'type': 'danh từ'},
                 {'id': 13, 'title': 'quả nho', 'url': 'https://qipedc.moet.gov.vn/videos/W02749.mp4', 'type': 'danh từ'},
                 {'id': 14, 'title': 'quả lê', 'url': 'https://qipedc.moet.gov.vn/videos/W02744.mp4', 'type': 'danh từ'},
                 {'id': 15, 'title': 'quả táo', 'url': 'https://qipedc.moet.gov.vn/videos/W02757B.mp4', 'type': 'danh từ'}],

    'Thức ăn': [{'id': 16, 'title': 'pizza', 'url': 'https://qipedc.moet.gov.vn/videos/W00140.mp4', 'type': 'danh từ'},
                {'id': 17, 'title': 'hộp sữa', 'url': 'https://qipedc.moet.gov.vn/videos/W01704.mp4', 'type': 'danh từ'},
                {'id': 18, 'title': 'hamburger', 'url': 'https://qipedc.moet.gov.vn/videos/D0391.mp4', 'type': 'danh từ'},
                {'id': 19, 'title': 'trứng', 'url': 'https://qipedc.moet.gov.vn/videos/W03659B.mp4', 'type': 'danh từ'},
                {'id': 20, 'title': 'kẹo', 'url': 'https://qipedc.moet.gov.vn/videos/W01743B.mp4', 'type': 'danh từ'}],

    'Công việc': [{'id': 21, 'title': 'nhân viên', 'url': 'https://qipedc.moet.gov.vn/videos/D0004.mp4', 'type': 'danh từ'},
                  {'id': 22, 'title': 'nghệ sĩ', 'url': 'https://qipedc.moet.gov.vn/videos/W02356.mp4', 'type': 'danh từ'},
                  {'id': 23, 'title': 'kiến trúc sư', 'url': 'https://qipedc.moet.gov.vn/videos/W01887.mp4', 'type': 'danh từ'},
                  {'id': 25, 'title': 'đạo diễn', 'url': 'https://qipedc.moet.gov.vn/videos/D0093.mp4', 'type': 'danh từ'}],

    'Động vật': [{'id': 26, 'title': 'con mèo', 'url': 'https://qipedc.moet.gov.vn/videos/W00772B.mp4', 'type': 'danh từ'},
                 {'id': 27, 'title': 'con chó', 'url': 'https://qipedc.moet.gov.vn/videos/W00739B.mp4', 'type': 'danh từ'},
                 {'id': 28, 'title': 'con chim', 'url': 'https://qipedc.moet.gov.vn/videos/W00738.mp4', 'type': 'danh từ'},
                 {'id': 29, 'title': 'con ngựa', 'url': 'https://qipedc.moet.gov.vn/videos/W00778B.mp4', 'type': 'danh từ'},
                 {'id': 30, 'title': 'con bò', 'url': 'https://qipedc.moet.gov.vn/videos/W00735B.mp4', 'type': 'danh từ'},
                 {'id': 31, 'title': 'con cừu', 'url': 'https://qipedc.moet.gov.vn/videos/W00751.mp4', 'type': 'danh từ'},
                 {'id': 32, 'title': 'con lợn', 'url': 'https://qipedc.moet.gov.vn/videos/W00770B.mp4', 'type': 'danh từ'},
                 {'id': 33, 'title': 'sâu bọ, côn trùng', 'url': 'https://qipedc.moet.gov.vn/videos/W02944.mp4', 'type': 'danh từ'}],

    'Thời gian': [{'id': 34, 'title': 'ban ngày', 'url': 'https://qipedc.moet.gov.vn/videos/W00089.mp4', 'type': 'danh từ'},
                 {'id': 35, 'title': 'ban đêm', 'url': 'https://qipedc.moet.gov.vn/videos/W00086B.mp4', 'type': 'danh từ'},
                 {'id': 36, 'title': 'tuần', 'url': 'https://qipedc.moet.gov.vn/videos/W03685B.mp4', 'type': 'danh từ'},
                 {'id': 37, 'title': 'tháng', 'url': 'https://qipedc.moet.gov.vn/videos/W03167B.mp4', 'type': 'danh từ'},
                 {'id': 38, 'title': 'tương lai', 'url': 'https://qipedc.moet.gov.vn/videos/D0288.mp4', 'type': 'danh từ'},
                 {'id': 39, 'title': 'mùa xuân', 'url': 'https://qipedc.moet.gov.vn/videos/W02272B.mp4', 'type': 'danh từ'},
                 {'id': 40, 'title': 'mùa hạ', 'url': 'https://qipedc.moet.gov.vn/videos/W02270B.mp4', 'type': 'danh từ'},
                 {'id': 41, 'title': 'mùa thu', 'url': 'https://qipedc.moet.gov.vn/videos/W02271.mp4', 'type': 'danh từ'},
                 {'id': 42, 'title': 'mùa đông', 'url': 'https://qipedc.moet.gov.vn/videos/W02269.mp4', 'type': 'danh từ'}],

    'Gia đình': [{'id': 43, 'title': 'mẹ', 'url': 'https://qipedc.moet.gov.vn/videos/W02110.mp4', 'type': 'danh từ'},
                 {'id': 44, 'title': 'bố', 'url': 'https://qipedc.moet.gov.vn/videos/W00325.mp4', 'type': 'danh từ'},
                 {'id': 45, 'title': 'chú', 'url': 'https://qipedc.moet.gov.vn/videos/W00506.mp4', 'type': 'danh từ'}]
}

# Dữ liệu ngôn ngữ kí hiệu nhật


def get_video_data(language):
    if language == 'en':
        return video_data_en
    elif language == 'vn':
        return video_data_vn
    else:
        return None


def extract_youtube_embed_url(url):
    match = re.match(r'^.*(?:youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=)([^#\&\?]*).*', url)
    if match:
        video_id = match.group(1)
        embed_url = f'https://www.youtube.com/embed/{video_id}'
        return embed_url
    return None


for topic in video_data_en.values():
    for video in topic:
        video['url'] = extract_youtube_embed_url(video['url'])
