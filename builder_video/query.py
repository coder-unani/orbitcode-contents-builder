from django.db import transaction 

from builder_video.models import (
    Video,
    VideoActor,
    VideoStaff,
    VideoGenre,
    VideoThumbnail,
    VideoWatch,
    VideoKeyword,
    Actor,
    Staff,
    Genre,
)

'''
create video
'''
def create_video(new_video):
    video = Video.objects.create(
        type = new_video['type'],
        title = new_video['title'],
        synopsis = new_video['synopsis'],
        release = new_video['release'],
        runtime = new_video['runtime'],
        notice_age = new_video['notice_age'],
        platform_code = new_video['platform_code'],
        platform_id = new_video['platform_id'],
    )
    video.save()

    return video

def create_actor(new_cast):
    actor = Actor.objects.create(
        name = new_cast['name'],
        picture = new_cast['picture'] if new_cast['picture'] else "",
        profile = new_cast['profile'] if new_cast['profile'] else "",
    )
    actor.save()

    return actor

def create_staff(new_staff):
    staff = Staff.objects.create(
        name = new_staff['name'],
        picture = new_staff['picture'] if new_staff['picture'] else "",
        profile = new_staff['profile'] if new_staff['profile'] else "",
    )
    staff.save()

    return staff

def create_genre(new_genre):
    genre = Genre.objects.create(
        name = new_genre['name'],
    )
    genre.save()

    return genre

def create_video_actor(video, new_actor):
    actor = Actor.objects.filter(name=new_actor['name'])
    if actor.exists():
        actor = actor.first()
    else:
        actor = create_actor(new_actor)

    video_actor = VideoActor.objects.create(
        video = video,
        actor = actor,
        type = new_actor['type'],
        role = new_actor['role'],
    ).save()

    return video_actor

def create_video_staff(video, new_staff):
    staff = Staff.objects.filter(name=new_staff['name'])
    if staff.exists():
        staff = staff.first()
    else:
        staff = create_staff(new_staff)

    video_staff = VideoStaff.objects.create(
        video = video,
        staff = staff,
        type = new_staff['type'],
    ).save()

    return video_staff

def create_video_genre(video, new_genre):
    genre = Genre.objects.filter(name=new_genre['name'])
    if genre.exists():
        genre = genre.first()
    else:
        genre = create_genre(new_genre)

    video_genre = VideoGenre.objects.create(
        video = video,
        genre = genre,
    ).save()

    return video_genre

def create_video_thumbnail(video, new_thumbnail):
    video_thumbnail = VideoThumbnail.objects.create(
        video = video,
        type = new_thumbnail['type'],
        thumbnail = new_thumbnail['thumbnail'],
        extension = new_thumbnail['extension'],
        size = new_thumbnail['size'],
    ).save()

    return video_thumbnail

def create_video_watch(video, new_watch):
    video_watch = VideoWatch.objects.create(
        video = video,
        type = new_watch['type'],
        url = new_watch['url'],
    ).save()

    return video_watch

def create_content_data(new_content):
    print(new_content)
    try:
        with transaction.atomic():
            video = create_video(new_content)
            for new_actor in new_content['actors']:
                create_video_actor(video, new_actor)
            for new_staff in new_content['staffs']:
                create_video_staff(video, new_staff)
            for new_genre in new_content['genres']:
                create_video_genre(video, new_genre)
            for new_thumbnail in new_content['thumbnails']:
                create_video_thumbnail(video, new_thumbnail)
            for new_watch in new_content['watchs']:
                create_video_watch(video, new_watch)
        return True
    except Exception as e:
        print(e)
        return False


'''
get video
'''
def get_video(id):
    video = Video.objects.get(id=id)
    return video
    
def get_video_by_platform_id(platform_id):
    video = Video.objects.get(platform_id=platform_id)
    return video


'''
videos
'''
def get_videos():
    pass

def get_video_by_title(title):
    videos = Video.objects.filter(title=title).all()
    return videos

def get_videos_by_genre(genre):
    # videos = Video.objects.filter(genres__genre=genre).all()
    # return videos
    pass

def get_videos_by_cast(cast):
    pass

def get_videos_by_staff(staff):
    pass



