import os
import urllib.request

from instagrapi import Client
import threading
import time

from instagrapi.exceptions import UnknownError

from config import settings
from . import models


class GetPk(threading.Thread):
    def __init__(self, user_pub, target_userid):
        self.user_pub = user_pub
        self.target_userid = target_userid
        threading.Thread.__init__(self)

    def run(self):
        all_pk = models.InstaPkForCopy.objects.values_list('insta_pk')

        cl = Client(settings=self.user_pub.settings)
        cl.login_flow()
        time.sleep(3)
        media_amount = cl.user_info(user_id=self.target_userid).media_count
        print('---- media amount of target:', media_amount)
        time.sleep(3)
        all_media = cl.user_medias(user_id=self.target_userid, amount=media_amount)
        for i in all_media:
            if i.media_type == 2 and not ((i.pk,) in all_pk):
                models.InstaPkForCopy.objects.create(
                    insta_pk=i.pk,
                    status='drf',
                    user_pub=self.user_pub
                )
                print('---- %s saved in data base:)' % i.pk)
        else:
            print('---- finished:)')


class InstaPosting(threading.Thread):
    def __init__(self, pk, my_username, my_settings, is_reels: bool = True):
        self.pk = pk
        self.my_username = my_username
        self.cl = Client(settings=my_settings)
        self.video_url = None
        self.folder_path = os.path.join(str(settings.MEDIA_ROOT), 'insta_videos_downloaded')
        self.is_reels = is_reels
        self.caption = None
        self.cl.login_flow()
        threading.Thread.__init__(self)

    def get_data(self):
        media_info = self.cl.media_info(media_pk=int(self.pk))
        # print(media_info.dict().keys())
        self.video_url = media_info.video_url
        self.caption = media_info.caption_text
        # print('---url:', self.video_url, '\n---caption:', self.caption)

    def download(self):
        print('---video url:', self.video_url)
        return urllib.request.urlretrieve(self.video_url, os.path.join(self.folder_path, '%s.mp4' % str(self.pk)))

    def re_caption(self):
        text = self.caption
        new_user = "@%s" % self.my_username

        y = text.split("@")
        # print (y)
        capt = []
        self.caption = ""
        for i in y:
            if y.index(i) == 0:
                for aray in i.split(" "):
                    # print(aray)
                    capt.append(aray)
            if not (y.index(i) == 0):
                # print("ok")
                z = i.split(" ")
                # print(z)
                z.remove(z[0])
                # print(z)
                z.insert(0, new_user)
                if "" in z:
                    z.remove("")
                # print(z)
                capt += z
        # print(capt)
        for i in capt:
            self.caption += i + " "
        return self.caption

    def upload(self):
        if self.is_reels:
            self.clip = self.cl.clip_upload(
                path=os.path.join(self.folder_path, '%s.mp4' % str(self.pk)),
                caption=str(self.caption)
            )
            print('---- uploaded reels successfully')
        else:
            try:
                self.clip = self.cl.video_upload(
                    path=os.path.join(self.folder_path, '%s.mp4' % str(self.pk)),
                    caption=str(self.caption)
                )
                print('---- uploaded post successfully')
            except UnknownError:
                pass
        return self.clip

    def comment(self):
        if not ("#" in self.caption):
            hashtags = "#lofi #lofihiphop #lofiedits #lofibeats #lofimusic #lofifilter #newmusicalert #synthwave #vapourwave #vaporwaveaesthetic #vaporwaveart #vaporwavedits #vaporwave #mood #chillin #chilledits #chillmusic #chillbeats #chillvibes #animeedits #amvedits #skateboardedits #beatmaker #animeaesthetic #anime #retro #aesthetic #tumblr #lofibeats"
            self.cl.media_comment(media_id=str(self.clip.id), text=hashtags)
            print('---- commented #')
        else:
            print('---- no need for #')

    def run(self) -> None:
        # self.get_data()
        # print('---data got.')
        self.download()
        print('---video downloaded.')
        self.re_caption()
        print('---re caption is successfully.')
        self.upload()
        time.sleep(30)
        self.comment()
        print('---finished process...')
