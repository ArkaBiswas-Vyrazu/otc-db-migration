create view
    otc_test_pg_3.public.feed_data as
select
    otc_test_pg_3.public.user_posts.id AS id,
    cast(
        otc_test_pg_3.public.user_posts.user_id as varchar(255)
    ) AS user_id,
    0 AS entity_id,
    cast(1 as text) AS existing_post,
    1 AS existing_post_id,
    otc_test_pg_3.public.user.username AS username,
    otc_test_pg_3.public.user.user_photo AS user_photo,
    concat (
        otc_test_pg_3.public.user.first_name,
        ' ',
        otc_test_pg_3.public.user.last_name
    ) AS user_full_name,
    otc_test_pg_3.public.user_posts.post_message AS post_message,
    otc_test_pg_3.public.user_posts.image AS image,
    3 AS entity_type,
    otc_test_pg_3.public.user_posts.status AS status,
    otc_test_pg_3.public.user_posts.video AS video,
    (
        select
            count(0)
        from
            otc_test_pg_3.public.user_posts_likes
        where
            (
                (
                    otc_test_pg_3.public.user_posts_likes.user_post_id = otc_test_pg_3.public.user_posts.id
                )
                and (otc_test_pg_3.public.user_posts_likes.like = 1)
            )
    ) AS total_likes,
    (
        select
            count(0)
        from
            otc_test_pg_3.public.user_post_comments
        where
            (
                (
                    otc_test_pg_3.public.user_post_comments.user_post_id = otc_test_pg_3.public.user_posts.id
                )
                and (
                    otc_test_pg_3.public.user_post_comments.status = 1
                )
            )
    ) AS total_comments,
    (
        select
            count(0)
        from
            otc_test_pg_3.public.user_post_share
        where
            (
                (
                    otc_test_pg_3.public.user_post_share.original_post_id = otc_test_pg_3.public.user_posts.id
                )
                and (otc_test_pg_3.public.user_post_share.status = 1)
            )
    ) AS shared_count,
    0 AS is_shared_post,
    otc_test_pg_3.public.user_posts.created_at AS created_at,
    otc_test_pg_3.public.user_posts.updated_at AS updated_at
from
    (
        otc_test_pg_3.public.user_posts
        join otc_test_pg_3.public.user on (
            (
                otc_test_pg_3.public.user_posts.user_id = otc_test_pg_3.public.user.id
            )
        )
    )
where
    (otc_test_pg_3.public.user_posts.status = 1)
union
select
    otc_test_pg_3.public.notification.id AS id,
    'Admin' AS user_id,
    otc_test_pg_3.public.notification.entity_id AS entity_id,
    cast(1 as text) AS existing_post,
    1 AS existing_post_id,
    'Campus Team' AS username,
    '5c334d0bcdbb5.png' AS user_photo,
    'Campus Team' AS user_full_name,
    otc_test_pg_3.public.notification.message AS post_message,
    cast(1 as varchar(250)) AS image,
    2 AS entity_type,
    otc_test_pg_3.public.notification.status AS status,
    cast(1 as varchar(255)) AS video,
    (
        select
            count(0)
        from
            otc_test_pg_3.public.user_posts_likes
        where
            (
                (
                    otc_test_pg_3.public.user_posts_likes.user_post_id = otc_test_pg_3.public.notification.id
                )
                and (otc_test_pg_3.public.user_posts_likes.like = 1)
                and (
                    otc_test_pg_3.public.user_posts_likes.entity_type = 2
                )
            )
    ) AS total_likes,
    (
        select
            count(0)
        from
            otc_test_pg_3.public.user_post_comments
        where
            (
                (
                    otc_test_pg_3.public.user_post_comments.user_post_id = otc_test_pg_3.public.notification.id
                )
                and (
                    otc_test_pg_3.public.user_post_comments.status = 1
                )
                and (
                    otc_test_pg_3.public.user_post_comments.entity_type = 2
                )
            )
    ) AS total_comments,
    0 AS shared_count,
    0 AS is_shared_post,
    otc_test_pg_3.public.notification.created_at AS created_at,
    otc_test_pg_3.public.notification.updated_at AS updated_at
from
    otc_test_pg_3.public.notification
union
select
    otc_test_pg_3.public.user_post_share.current_post_id AS id,
    cast(
        otc_test_pg_3.public.user_post_share.user_id as varchar(255)
    ) AS user_id,
    0 AS entity_id,
    otc_test_pg_3.public.user_post_share.original_post_message AS existing_post,
    otc_test_pg_3.public.user_post_share.original_post_id AS existing_post_id,
    otc_test_pg_3.public.user.username AS username,
    otc_test_pg_3.public.user.user_photo AS user_photo,
    concat (
        otc_test_pg_3.public.user.first_name,
        ' ',
        otc_test_pg_3.public.user.last_name
    ) AS user_full_name,
    otc_test_pg_3.public.user_post_share.post AS post_message,
    cast(1 as varchar(250)) AS image,
    4 AS entity_type,
    otc_test_pg_3.public.user_post_share.status AS status,
    cast(1 as varchar(255)) AS video,
    (
        select
            count(0)
        from
            otc_test_pg_3.public.user_posts_likes
        where
            (
                (
                    otc_test_pg_3.public.user_posts_likes.user_post_id = otc_test_pg_3.public.user_post_share.current_post_id
                )
                and (otc_test_pg_3.public.user_posts_likes.like = 1)
            )
    ) AS total_likes,
    (
        select
            count(0)
        from
            otc_test_pg_3.public.user_post_comments
        where
            (
                (
                    otc_test_pg_3.public.user_post_comments.user_post_id = otc_test_pg_3.public.user_post_share.current_post_id
                )
                and (
                    otc_test_pg_3.public.user_post_comments.status = 1
                )
            )
    ) AS total_comments,
    (
        select
            count(0)
        from
            otc_test_pg_3.public.user_post_share
        where
            (
                (
                    otc_test_pg_3.public.user_post_share.original_post_id = otc_test_pg_3.public.user_post_share.current_post_id
                )
                and (otc_test_pg_3.public.user_post_share.status = 1)
            )
    ) AS shared_count,
    1 AS is_shared_post,
    otc_test_pg_3.public.user_posts.created_at AS created_at,
    otc_test_pg_3.public.user_posts.updated_at AS updated_at
from
    (
        (
            otc_test_pg_3.public.user_post_share
            join otc_test_pg_3.public.user on (
                (
                    otc_test_pg_3.public.user_post_share.user_id = otc_test_pg_3.public.user.id
                )
            )
        )
        join otc_test_pg_3.public.user_posts on (
            (
                (
                    otc_test_pg_3.public.user_post_share.current_post_id = otc_test_pg_3.public.user_posts.id
                )
                and (otc_test_pg_3.public.user_posts.status = 0)
            )
        )
    )
