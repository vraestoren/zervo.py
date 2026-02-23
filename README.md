# zervo.py

> Mobile-API for [Zervo](https://play.google.com/store/apps/details?id=com.planet.pinponapp) tp interact with the anime roleplay social network

---

## Quick Start

```python
from zervo import Zervo

zervo = Zervo()

# Request a verification code first, then register
zervo.request_verification_code(email="example@gmail.com")
zervo.register(
    email="example@gmail.com",
    password="password",
    nickname="Anon",
    verification_code=123456,
)

# Or just login
zervo.login(email="example@gmail.com", password="password")
```

---

## Features

- 🔐 **Auth** — email/Google login, registration with verification
- 👤 **Profile** — view and edit your profile, avatar, and custom ID
- 📝 **Posts** — create, delete, like, and comment on posts
- 🎭 **OC (Original Characters)** — create, list, and delete OCs
- 📺 **Channels** — create, join, leave, invite, edit, and moderate channels
- 👥 **Friends** — send requests, block/unblock users
- 🔍 **Discovery** — recommended users, albums, channels, and roleplay
- 🎲 **Gacha** — spin the gachapon, choose avatars
- 🗺️ **Game maps** — browse in-app game maps
- 💰 **Points** — check your point balance

---

## Usage

### Auth

```python
z = Zervo(language="en_US")

# Step 1: Request email verification code
zervo.request_verification_code(email="example@gmail.com")

# Step 2: Register
zervo.register(
    email="example@gmail.com",
    password="password",
    nickname="MyName",
    verification_code=123456,
    birthday="1999-09-09 09:00:00.000Z",
    sex=1,
)

# Login with email
zervo.login(email="example@gmail.com", password="password")

# Login with Google
zervo.login_with_google(google_id="google_uid_here")

# Get your current session info
zervo.get_current_session()
```

### Profile

```python
# View a user
zervo.get_user_info(user_id=123)
zervo.get_user_stats(user_id=123)

# Edit your profile
zervo.edit_profile(nickname="NewName", description="About me", gender=1)

# Set a custom profile ID
zervo.edit_profile_id(id="my_custom_id")

# Choose an avatar template
zervo.choose_avatar(template_id=5)

# Check your points balance
zervo.get_points()
```

### Posts

```python
# Browse recent posts
zervo.get_recent_posts(size=10, current=1)

# Get a user's posts
zervo.get_user_posts(user_id=123)

# Create a post in a channel/theme
zervo.create_post(theme_id=1, content="Hello world!", images=[])

# Like a post (like_status=1 to like, 2 to unlike)
zervo.like_post(post_id=456)
zervo.like_post(post_id=456, like_status=2)

# Comment on a post
zervo.comment(post_id=456, comment="Great post!")

# Get post comments
zervo.get_post_comments(post_id=456)

# Delete a post
zervo.delete_post(post_id=456)
```

### OCs (Original Characters)

```python
# List your OCs
zervo.get_oc_current_list()

# List a user's OCs
zervo.get_user_oc_list(user_id=123)

# Create an OC
zervo.create_oc(
    name="My Character",
    description="A brave hero.",
    can_copy=0,
    image_url="https://example.com/image.png",
)

# Delete an OC
zervo.delete_oc(oc_id=789)
```

### Channels

```python
# Browse recommended channels
zervo.get_recommended_channels(size=10)

# Create a channel
zervo.create_channel(title="My Channel", min_age=0, max_age=100)

# Join / leave a channel
zervo.join_channel(channel_id=1)
zervo.leave_channel(channel_id=1)

# Get your joined channels
zervo.get_joined_channels()

# Get channel info, users, moderators
zervo.get_channel_info(channel_id=1)
zervo.get_channel_users(channel_id=1)
zervo.get_channel_moderators(channel_id=1)

# Edit or delete a channel
zervo.edit_channel(channel_id=1, title="New Title", description="New desc")
zervo.delete_channel(channel_id=1)

# Invite a user
zervo.invite_to_channel(channel_id=1, user_id=123)

# View the blacklist
zervo.get_channel_blacklist(channel_id=1)
```

### Friends & Users

```python
# Send / manage friend requests
zervo.send_friend_request(nickname="username", user_id=123)
zervo.get_friend_requests()
zervo.get_friends_list()

# Block / unblock
zervo.block_user(user_id=123)
zervo.unblock_user(user_id=123)

# Report a user
zervo.report_user(user_id=123, description="Spam", type=2)
```

### Discovery

```python
zervo.get_recommended_users()
zervo.get_recommended_albums()
zervo.get_recommended_channels()
zervo.get_recommended_all()
zervo.get_recommended_rp()
```

### Gacha & Roles

```python
# Spin the gachapon
zervo.spin_gachapon()

# Browse available app roles
zervo.get_app_roles()
zervo.get_owned_app_roles()
zervo.get_role_info(role_id=1)
```

---

## API Reference

| Method                      | Description                                        |
|-----------------------------|----------------------------------------------------|
| `login`                     | Sign in with email and password                    |
| `login_with_google`         | Sign in with Google UID                            |
| `register`                  | Create a new account (requires verification code)  |
| `register_with_google`      | Create a new account with Google                   |
| `request_verification_code` | Send a verification code to an email               |
| `get_current_session`       | Get your own profile info                          |
| `get_user_info`             | Get a user's profile                               |
| `get_user_stats`            | Get a user's post/activity stats                   |
| `get_user_posts`            | Get a user's posts                                 |
| `get_user_albums`           | Get a user's albums                                |
| `get_user_oc_list`          | Get a user's OC list                               |
| `edit_profile`              | Update profile fields                              |
| `edit_profile_id`           | Set a custom profile ID                            |
| `choose_avatar`             | Set an avatar from a template                      |
| `get_points`                | Get your point balance                             |
| `create_post`               | Create a post                                      |
| `delete_post`               | Delete a post                                      |
| `like_post`                 | Like or unlike a post                              |
| `comment`                   | Comment on a post                                  |
| `get_post_comments`         | Get comments on a post                             |
| `get_recent_posts`          | Browse recent posts                                |
| `create_oc`                 | Create an original character                       |
| `delete_oc`                 | Delete an OC                                       |
| `get_oc_current_list`       | List your own OCs                                  |
| `create_channel`            | Create a channel                                   |
| `edit_channel`              | Edit a channel                                     |
| `delete_channel`            | Delete a channel                                   |
| `join_channel`              | Join a channel                                     |
| `leave_channel`             | Leave a channel                                    |
| `invite_to_channel`         | Invite a user to a channel                         |
| `get_channel_info`          | Get channel details                                |
| `get_channel_users`         | List channel members                               |
| `get_channel_moderators`    | List channel moderators                            |
| `get_channel_blacklist`     | View channel blacklist                             |
| `get_joined_channels`       | List channels you've joined                        |
| `get_recommended_channels`  | Browse recommended channels                        |
| `send_friend_request`       | Send a friend request                              |
| `get_friend_requests`       | View incoming friend requests                      |
| `get_friends_list`          | List your friends                                  |
| `block_user`                | Block a user                                       |
| `unblock_user`              | Unblock a user                                     |
| `report_user`               | Report a user (0=violation, 1=tease, 2=spam, 3=fraud) |
| `get_recommended_users`     | Get recommended users to follow                    |
| `get_recommended_albums`    | Get recommended albums                             |
| `get_recommended_all`       | Get all recommended content                        |
| `get_recommended_rp`        | Get recommended roleplay content                   |
| `get_app_tags`              | List all available tags                            |
| `get_app_roles`             | List all available roles                           |
| `get_owned_app_roles`       | List roles you own                                 |
| `get_role_info`             | Get details for a specific role                    |
| `get_album_info`            | Get album contents                                 |
| `spin_gachapon`             | Spin the gachapon for rewards                      |
| `get_game_maps`             | Browse in-app game maps                            |

---

## License

MIT
