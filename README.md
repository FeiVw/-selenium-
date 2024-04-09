数据库结构：

----------------------------------------------------
anime_website   （库）
	drf_animebigwuhureal     （表）
		id:bigint, video_episodes_count:int, video_episodes:varchar, video_title:varchar, video_area:varchar, video_year:varchar, poster:varchar, video_info:varchar, video_update:varchar        （列）
-----------------------------------------------------------------------------
	drf_animesmallwuhureal     （表）
		id:bigint, video_episode:varchar, video_title:varchar, video_area:varchar, video_year:varchar, video_url:varchar, anime_key_id:bigint       （列）
--------------------------------------------------------------------------------------------------------------------------------

其中id都是主键自增，drf_animesmallwuhureal中的anime_key_id是关联的drf_animebigwuhureal中的id，以便查找某一部动漫有哪几集。


创建好数据库后注意把pymysql中的pwd和db换成自己的。
