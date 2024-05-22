from django.db import transaction 

from .logger import info_log, error_log
from builder_video.models import (
    Video,
    VideoActor,
    VideoStaff,
    VideoGenre,
    VideoThumbnail,
    VideoWatch,
    VideoTag,
    Actor,
    Staff,
    Genre,
)


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
    find_actor = Actor.objects.filter(name=new_actor['name']).all()
    if find_actor.exists():
        actor = find_actor.first()
    else:
        actor = create_actor(new_actor)
    video.actor.add(actor)
    
    return True


def create_video_staff(video, new_staff):
    find_staff = Staff.objects.filter(name=new_staff['name']).all()
    if find_staff.exists():
        staff = find_staff.first()
    else:
        staff = create_staff(new_staff)
    video.staff.add(staff)

    return True


def create_video_genre(video, new_genre):
    find_genre = Genre.objects.filter(name=new_genre['name']).all()
    if find_genre.exists():
        genre = find_genre.first()
    else:
        genre = create_genre(new_genre)
    video.genre.add(genre)
    
    return True


def create_video_thumbnail(video, new_thumbnail):
    VideoThumbnail.objects.create(
        video = video,
        type = new_thumbnail['type'],
        url = new_thumbnail['url'],
        extension = new_thumbnail['extension'],
        size = new_thumbnail['size'],
    ).save()

    return True


def create_video_watch(video, new_watch):
    VideoWatch.objects.create(
        video = video,
        type = new_watch['type'],
        url = new_watch['url'],
    ).save()

    return True


def create_content_data(new_content):
    object_name = "create_content_data"
    try:
        with transaction.atomic():
            video = create_video(new_content)
            for new_actor in new_content['actor']:
                create_video_actor(video, new_actor)
            for new_staff in new_content['staff']:
                create_video_staff(video, new_staff)
            for new_genre in new_content['genre']:
                create_video_genre(video, new_genre)
            for new_watch in new_content['watch']:
                create_video_watch(video, new_watch)
            for new_thumbnail in new_content['thumbnail']:
                create_video_thumbnail(video, new_thumbnail)
        info_log(object_name, "Created video data. platform_id: {} / id: {}".format(new_content['platform_id'], video.id))
        return video
    except Exception as e:
        error_log(object_name, "Video data creation failed. platform_id: {} / {}".format(new_content['platform_id'], e))
        return False


def exist_content_video(video_id=None, platform_id=None):
    try:
        video = None
        if video_id:
            video = Video.objects.filter(id=video_id)
        elif platform_id:
            video = Video.objects.filter(platform_id=platform_id)

        if video.exists():
            return True
        else:
            return False
    except Exception as e:
        error_log("exist_video", "Failed to check video existence: {}".format(e))
        return False


def get_video(video_id):
    try:
        video = Video.objects.get(id=video_id),
        info_log("get_video", "Video search successful with ID: {}".format(id))
        return video
    
    except Exception as e:
        error_log("get_video", "Video retrieval failed with ID: {} / {}".format(id, e))
        return None


def get_video_by_platform_id(platform_id):
    try:
        video = Video.objects.get(platform_id=platform_id)
        return video
    except Exception as e:
        error_log(
            "get_video_by_platform_id",
            "Video retrieval failed with platform_id: {} / {}".format(platform_id, e)
        )
        return None


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



