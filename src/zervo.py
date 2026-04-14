from requests import Session

class Zervo:
    def __init__(self, language: str = "en_US") -> None:
        self.api = "https://wg6.pinpon.cool"
        self.token = None
        self.user_id = None
        self.language = language
        self.session = Session()
        self.session.headers = {
            "User-Agent": "Dart/2.18 (dart:io)",
            "language": self.language
        }

    def _post(self, endpoint: str, data: dict = None) -> dict:
        return self.session.post(
            f"{self.api}{endpoint}", data=data).json()

    def _get(self, endpoint: str) -> dict:
        return self.session.get(
            f"{self.api}{endpoint}").json()

    def _filter(self, data: dict) -> dict:
        return {key: value for key, value in data.items() if value is not None}

    def _set_auth(self, response: dict) -> None:
        self.user_id = response["data"]["appUserId"]
        self.token = response["data"]["pinponToken"]["token"]
        self.session.headers["pinpon-auth"] = self.token

    def register(
            self,
            email: str,
            password: str,
            nickname: str,
            verification_code: int,
            birthday: str = "1999-09-09 09:00:00.000Z",
            sex: int = 1) -> dict:
        data = {
            "email": email,
            "password": password,
            "source": "email",
            "code": verification_code,
            "nickname": nickname,
            "birthday": birthday,
            "sex": sex
        }
        return self._post(
            "/pinpon-app-system/v3/app-user/register", data)

    def register_with_google(
            self,
            google_id: str,
            role_id: int,
            nickname: str,
            birthday: str = "2003-04-07 20:00:00.000Z") -> dict:
        data = {
            "appRoleId": f"{role_id}",
            "nickname": nickname,
            "birthday": birthday,
            "source": "google",
            "uid": google_id
        }
        return self._post(
            "/pinpon-app-system/v2/app-user/register", data)

    def login(self, email: str, password: str) -> dict:
        data = {
            "email": email,
            "password": password
        }
        response = self._post(
            "/pinpon-app-auth/v3/auth/login/email", data)
        if "token" in response["data"]["pinponToken"]:
            self._set_auth(response)
        return response

    def login_with_google(self, google_id: str) -> dict:
        data = {
            "source": "google",
            "id": google_id
        }
        response = self._post(
            "/pinpon-app-auth/auth/login/source", data)
        if "token" in response["data"]["pinponToken"]:
            self._set_auth(response)
        return response

    def request_verification_code(self, email: str) -> dict:
        data = {
            "email": email,
            "type": 2,
            "language": self.language
        }
        return self._post(
            "/pinpon-app-system/v2/app-user/mail", data)

    def comment(
            self,
            post_id: int,
            comment: str,
            images: list = []) -> dict:
        data = {
            "contentId": post_id,
            "comment": comment,
            "images": images
        }
        return self._post(
            "/pinpon-app-system/app-comment/save", data)

    def like_post(self, post_id: int, like_status: int = 1) -> dict:
        """
        LIKE-STATUS TYPES:
            1 - TO LIKE,
            2 - TO UNLIKE
        """
        data = {
            "typeId": post_id,
            "type": 1,
            "likeStatus": like_status
        }
        return self._post(
            "/pinpon-app-system/app-like/like/status", data)

    def send_friend_request(
            self,
            nickname: str,
            user_id: int) -> dict:
        data = {
            "isNickname": True,
            "nickname": nickname,
            "receiveUserId": user_id,
            "source": 1
        }
        return self._post(
            "/pinpon-app-system/app-friend-req/save", data)

    def block_user(
            self,
            user_id: int,
            is_friend: bool = False) -> dict:
        data = {
            "friendUserId": user_id,
            "isFriend": is_friend
        }
        return self._post(
            "/pinpon-app-system/app-friend/block", data)

    def unblock_user(self, user_id: int) -> dict:
        data = {
            "friendUserId": user_id
        }
        return self._post(
            "/pinpon-app-system/app-friend/unblock", data)

    def get_album_info(self, album_id: int, limit: int = 10) -> dict:
        return self._get(
            f"/pinpon-app-system/v2/app-meme/page?limit={limit}&albumId={album_id}")

    def get_post_comments(
            self,
            post_id: int,
            size: int = 10,
            current: int = 1) -> dict:
        return self._get(
            f"/pinpon-app-system/app-comment/list?contentId={post_id}&size={size}&current={current}&commentId")

    def get_app_roles(self) -> dict:
        return self._get(
            "/pinpon-app-auth/pinpon-app-system/v2/app-role/default")

    def get_friends_list(self) -> dict:
        return self._get("/pinpon-app-system/app-friend/list")

    def get_role_info(self, role_id: int) -> dict:
        return self._get(
            f"/pinpon-app-system/app-role/detail?roleId={role_id}")

    def get_recent_posts(
            self,
            size: int = 10,
            current: int = 1) -> dict:
        return self._get(
            f"/pinpon-app-system/app-content/query?size={size}&current={current}")

    def get_user_oc_list(self, user_id: int) -> dict:
        return self._get(
            f"/pinpon-app-system/app-oc/list?appUserId={user_id}")

    def get_user_info(self, user_id: int) -> dict:
        return self._get(
            f"/pinpon-app-system/v2/app-user/detail?appUserId={user_id}")

    def get_user_stats(self, user_id: int) -> dict:
        return self._get(
            f"/pinpon-app-system/app-content/stats?appUserId={user_id}")

    def get_user_posts(self, user_id: int, size: int = 10) -> dict:
        return self._get(
            f"/pinpon-app-system/app-content/list?appUserId={user_id}&contentId&size={size}")

    def get_user_albums(self, user_id: int) -> dict:
        return self._get(
            f"/pinpon-app-system/v2/app-album/list?appUserId={user_id}")

    def get_recommended_channels(
            self,
            current: int = 1,
            size: int = 10,
            name: str = None) -> dict:
        return self._get(
            f"/pinpon-app-system/v2/app-channel/recommend/tag?current={current}&size={size}&name={name}")

    def join_channel(self, channel_id: int) -> dict:
        data = {
            "channelId": channel_id
        }
        return self._post(
            "/pinpon-app-system/v2/app-channel-user/save", data)

    def leave_channel(self, channel_id: int) -> dict:
        data = {
            "channelId": channel_id
        }
        return self._post(
            "/pinpon-app-system/v2/app-channel-user/remove", data)

    def invite_to_channel(
            self,
            channel_id: int,
            user_id: int) -> dict:
        data = {
            "guildId": "1111111111111111111",
            "appUserIds": [user_id],
            "channelId": channel_id
        }
        return self._post(
            "/pinpon-app-system/app-channel-user/invite", data)

    def get_channel_info(self, channel_id: int) -> dict:
        return self._get(
            f"/pinpon-app-system/v2/app-channel/detail?channelId={channel_id}")

    def get_channel_users(
            self,
            channel_id: int,
            current: int = 1,
            size: int = 10) -> dict:
        return self._get(
            f"/pinpon-app-system/app-channel-user/{channel_id}?current={current}&size={size}")

    def get_channel_moderators(self, channel_id: int) -> dict:
        return self._get(
            f"/pinpon-app-system/app-channel-user/moderator?channelId={channel_id}")

    def get_current_session(self) -> dict:
        return self._get(
            "/pinpon-app-system/app-user/current-detail")

    def get_recommended_users(
            self,
            current: int = 1,
            size: int = 10,
            name: str = None) -> dict:
        return self._get(
            f"/pinpon-app-system/v4/app-recommend?size={size}&current={current}&name={name}")

    def get_recommended_albums(
            self,
            current: int = 1,
            size: int = 10,
            name: str = None) -> dict:
        return self._get(
            f"/pinpon-app-system/app-album/recommend?current={current}&size={size}&name={name}")

    def get_recommended_all(
            self,
            current: int = 1,
            size: int = 10,
            name: str = None) -> dict:
        return self._get(
            f"/pinpon-app-system/v4/app-recommend/all?current={current}&size={size}&name={name}")

    def get_app_tags(self) -> dict:
        return self._get("/pinpon-app-system/app-tag/list")

    def get_channel_blacklist(
            self,
            channel_id: int,
            current: int = 1,
            size: int = 10) -> dict:
        return self._get(
            f"/pinpon-app-system/app-group-black/list?current={current}&size={size}&groupId={channel_id}")

    def create_channel(
            self,
            title: str,
            avatar: str = "",
            max_age: int = 1000,
            min_age: int = 0,
            tag_list: list = []) -> dict:
        data = {
            "avatar": avatar,
            "maxAge": max_age,
            "minAge": min_age,
            "name": title,
            "tagList": tag_list
        }
        return self._post(
            "/pinpon-app-system/v3/app-channel/chat/save", data)

    def edit_channel(
            self,
            channel_id: int,
            title: str = None,
            bio: str = None,
            language: str = None) -> dict:
        data = self._filter({
            "channelId": channel_id,
            "name": title,
            "bio": bio,
            "language": language
        })
        return self._post(
            "/pinpon-app-system/v2/app-channel/update", data)

    def delete_channel(self, channel_id: int) -> dict:
        data = {
            "channelId": channel_id
        }
        return self._post(
            "/pinpon-app-system/v2/app-channel/remove", data)

    def report_user(
            self,
            user_id: int,
            description: str,
            report_type: int = 0,
            url: str = None) -> dict:
        """
        REPORT-TYPES:
            0 - VIOLATION,
            1 - TEASE,
            2 - SPAM,
            3 - FRAUD
        """
        data = {
            "reportedUserId": user_id,
            "description": description,
            "type": report_type,
            "url": url
        }
        return self._post(
            "/pinpon-app-system/app-report/save", data)

    def get_friend_requests(self) -> dict:
        return self._get(
            "/pinpon-app-system/app-friend-req/list")

    def edit_profile(
            self,
            nickname: str = None,
            bio: str = None,
            language: str = None,
            role_id: int = None,
            gender: int = 1) -> dict:
        data = self._filter({
            "nickname": nickname,
            "bio": bio,
            "language": language,
            "sex": gender,
            "appRoleId": role_id
        })
        return self._post(
            "/pinpon-app-system/app-user/update", data)

    def edit_profile_id(self, user_id: str) -> dict:
        return self._post(
            f"/pinpon-app-system/app-user/update/userId?userId={user_id}")

    def get_owned_app_roles(self) -> dict:
        return self._get(
            "/pinpon-app-system/v2/app-role/owned-list-all")

    def create_post(
            self,
            theme_id: int,
            content: str,
            images: list = []) -> dict:
        data = {
            "channelId": theme_id,
            "content": content,
            "images": images
        }
        return self._post(
            "/pinpon-app-system/app-content/save", data)

    def delete_post(self, post_id: int) -> dict:
        return self._post(
            f"/pinpon-app-system/app-content/remove?contentId={post_id}")

    def create_oc(
            self,
            name: str,
            description: str,
            can_copy: int = 0,
            image_url: str = None,
            audio_url: str = None,
            emotion: str = "",
            sort: int = 0) -> dict:
        data = {
            "appOC": {
                "name": name,
                "bio": description,
                "isCopy": can_copy
            },
            "addAppOcStatues": [
                {
                    "audioUrl": audio_url,
                    "emotion": emotion,
                    "sort": sort,
                    "url": image_url
                }
            ]
        }
        return self._post(
            "/pinpon-app-system/app-oc/save", data)

    def delete_oc(self, oc_id: int) -> dict:
        data = {
            "ids": oc_id
        }
        return self._post(
            "/pinpon-app-system/app-oc/remove", data)

    def get_joined_channels(self) -> dict:
        return self._get(
            "/pinpon-app-system/v3/app-channel/chat/list")

    def get_game_maps(
            self,
            current: int = 1,
            page: int = 10) -> dict:
        return self._get(
            f"/pinpon-app-system/game-map/list?current={current}&page={page}")

    def get_points(self) -> dict:
        return self._get("/pinpon-app-system/app-user/point")

    def spin_gachapon(self) -> dict:
        return self._post("/pinpon-app-system/app-library/draw")

    def choose_avatar(self, template_id: int) -> dict:
        data = {
            "avatarTemplateId": template_id
        }
        return self._post(
            "/pinpon-app-system/app-avatar/choose/template", data)

    def get_recommended_rp(
            self,
            current: int = 1,
            size: int = 20) -> dict:
        data = {
            "current": current,
            "size": size
        }
        return self._post(
            "/pinpon-app-system/v5/app-recommend/rp", data)

    def get_oc_current_list(self) -> dict:
        return self._get(
            "/pinpon-app-system/app-oc/current/list")
