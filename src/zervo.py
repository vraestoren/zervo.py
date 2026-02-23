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
		return self.session.post(
			f"{self.api}/pinpon-app-system/v3/app-user/register",
			data=data).json()

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
		return self.session.post(
			f"{self.api}/pinpon-app-system/v2/app-user/register",
			data=data).json()

	def login(
			self,
			email: str,
			password: str) -> dict:
		data = {
			"email": email,
			"password": password
		}
		response = self.session.post(
			f"{self.api}/pinpon-app-auth/v3/auth/login/email",
			data=data).json()
		if "token" in response["data"]["pinponToken"]:
			self.user_id = response["data"]["appUserId"]
			self.token = response["data"]["pinponToken"]["token"]
			self.session.headers["pinpon-auth"] = self.token
		return response


	def login_with_google(self, google_id: str) -> dict:
		data = {
			"source": "google",
			"id": google_id
		}
		response = self.session.post(
			f"{self.api}/pinpon-app-auth/auth/login/source",
			data=data).json()
		if "token" in response["data"]["pinponToken"]:
			self.user_id = response["data"]["appUserId"]
			self.token = response["data"]["pinponToken"]["token"]
			self.session.headers["pinpon-auth"] = self.token
		return response
	
	def request_verification_code(self, email: str) -> dict:
		data = {
			"email": email,
			"type": 2,
			"language": self.language
		}
		return self.session.post(
			f"{self.api}/pinpon-app-system/v2/app-user/mail",
			data=data).json()

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
		return self.session.post(
			f"{self.api}/pinpon-app-system/app-comment/save",
			data=data).json()
	
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
		return self.session.post(
			f"{self.api}/pinpon-app-system/app-like/like/status",
			data=data).json()
	
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
		return self.session.post(
			f"{self.api}/pinpon-app-system/app-friend-req/save",
			data=data).json()
	
	def block_user(
			self,
			user_id: int,
			is_friend: bool = False) -> dict:
		data = {
			"friendUserId": user_id,
			"isFriend": is_friend
		}
		return self.session.post(
			f"{self.api}/pinpon-app-system/app-friend/block",
			data=data).json()
		
	def unblock_user(self, user_id: int) -> dict:
		data = {
			"friendUserId": user_id
		}
		return self.session.post(
			f"{self.api}/pinpon-app-system/app-friend/unblock",
			data=data).json()
		
	def get_album_info(
			self,
			album_id: int,
			limit: int = 10) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/v2/app-meme/page?limit={limit}&albumId={album_id}").json()
		
	def get_post_comments(
			self,
			post_id: int,
			size: int = 10,
			current: int = 1) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/app-comment/list?contentId={post_id}&size={size}&current={current}&commentId").json()
		
	def get_app_roles(self) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-auth/pinpon-app-system/v2/app-role/default").json()
		
	def get_friends_list(self) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/app-friend/list").json()
		
	def get_role_info(self, role_id: int) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/app-role/detail?roleId={role_id}").json()
		
	def get_recent_posts(
			self,
			size: int = 10,
			current: int = 1) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/app-content/query?size={size}&current={current}").json()
		
	def get_user_oc_list(self, user_id: int) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/app-oc/list?appUserId={user_id}").json()
		
	def get_user_info(self, user_id: int) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/v2/app-user/detail?appUserId={user_id}").json()
		
	def get_user_stats(self, user_id: int) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/app-content/stats?appUserId={user_id}").json()
		
	def get_user_posts(self, user_id: int, size: int = 10) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/app-content/list?appUserId={user_id}&contentId&size={size}").json()
		
	def get_user_albums(self, user_id: int) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/v2/app-album/list?appUserId={user_id}").json()
		
	def get_recommended_channels(
			self,
			current: int = 1,
			size: int = 10,
			name: str = None) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/v2/app-channel/recommend/tag?current={current}&size={size}&name={name}").json()
		
	def join_channel(self, channel_id: int) -> dict:
		data = {
			channel_id
		}
		return self.session.post(
			f"{self.api}/pinpon-app-system/v2/app-channel-user/save",
			data=data).json()
		
	def leave_channel(self, channel_id: int) -> dict:
		data = {
			"channelId": channel_id
		}
		return self.session.post(
			f"{self.api}/pinpon-app-system/v2/app-channel-user/remove",
			data=data).json()
		
	def invite_to_channel(
			self,
			channel_id: int,
			user_id: int) -> dict:
		data = {
			"guildId": "1111111111111111111",
			"appUserIds": [
				user_id
			],
			"channelId": channel_id
		}
		return self.session.post(
			f"{self.api}/pinpon-app-system/app-channel-user/invite",
			data=data).json()
		
	def get_channel_info(self, channel_id: int) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/v2/app-channel/detail?channelId={channel_id}").json()
		
	def get_channel_users(
			self,
			channel_id: int,
			current: int = 1,
			size: int = 10) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/app-channel-user/{channel_id}?current={current}&size={size}").json()
		
	def get_channel_moderators(self, channel_id: int) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/app-channel-user/moderator?channelId={channel_id}").json()
		
	def get_current_session(self) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/app-user/current-detail").json()
		
	def get_recommended_users(
			self,
			current: int = 1,
			size: int = 10,
			name: str = None) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/v4/app-recommend?size={size}&current={current}&name={name}").json()
		
	def get_recommended_albums(
			self,
			current: int = 1,
			size: int = 10,
			name: str = None) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/app-album/recommend?current={current}&size={size}&name={name}").json()
		
	def get_recommended_all(
			self,
			current: int = 1,
			size: int = 10,
			name: str = None) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/v4/app-recommend/all?current={current}&size={size}&name={name}").json()
		
	def get_app_tags(self) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/app-tag/list").json()
		
	def get_channel_blacklist(
			self,
			channel_id: int,
			current: int = 1,
			size: int = 10) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/app-group-black/list?current={current}&size={size}&groupId={channel_id}").json()
		
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
		return self.session.post(
			f"{self.api}/pinpon-app-system/v3/app-channel/chat/save",
			data=data).json()
		
	def edit_channel(
			self,
			channel_id: int,
			title: str = None,
			description: str = None,
			language: str = None) -> dict:
		data = {"channelId": channel_id}
		if title:
			data["name"] = title
		if description:
			data["bio"] = description
		if language:
			data["language"] = language
		return self.session.post(
			f"{self.api}/pinpon-app-system/v2/app-channel/update",
			data=data).json()
		
	def delete_channel(self, channel_id: int) -> dict:
		data = {
			"channelId": channel_id
		}
		return self.session.post(
			f"{self.api}/pinpon-app-system/v2/app-channel/remove",
			data=data).json()
		
	def report_user(
			self,
			user_id: int,
			description: str,
			type: int = 0,
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
			"type": type,
			"url": url
		}
		return self.session.post(
			f"{self.api}/pinpon-app-system/app-report/save",
			data=data).json()
		
	def get_friend_requests(self) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/app-friend-req/list").json()
		
	def edit_profile(
			self,
			nickname: str = None,
			description: str = None,
			language: str = None,
			role_id: int = None,
			gender: int = 1) -> dict:
		data = {}
		if nickname:
			data["nickname"] = nickname
		if description:
			data["bio"] = description
		if language:
			data["language"] = language
		if gender:
			data["sex"] = gender
		if role_id:
			data["appRoleId"] = role_id
		return self.session.post(
			f"{self.api}/pinpon-app-system/app-user/update",
			data=data).json()
		
	def edit_profile_id(self, id: str) -> dict:
		return self.session.post(
			f"{self.api}/pinpon-app-system/app-user/update/userId?userId={id}").json()
		
	def get_owned_app_roles(self) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/v2/app-role/owned-list-all").json()
		
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
		return self.session.post(
			f"{self.api}/pinpon-app-system/app-content/save",
			data=data).json()
		
	def delete_post(self, post_id: int) -> dict:
		return self.session.post(
			f"{self.api}/pinpon-app-system/app-content/remove?contentId={post_id}").json()
		
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
		return self.session.post(
			f"{self.api}/pinpon-app-system/app-oc/save",
			data=data).json()
		
	def delete_oc(self, oc_id: int) -> dict:
		data = {
			"ids": oc_id
		}
		return self.session.post(
			f"{self.api}/pinpon-app-system/app-oc/remove",
			data=data).json()
		
	def get_joined_channels(self) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/v3/app-channel/chat/list").json()
		
	def get_game_maps(
			self,
			current: int = 1,
			page: int = 10) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/game-map/list?current={current}&page={page}").json()
		
	def get_points(self) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/app-user/point").json
		
	def spin_gachapon(self) -> dict:
		return self.session.post(
			f"{self.api}/pinpon-app-system/app-library/draw").json()

	def choose_avatar(self, template_id: int) -> dict:
		data = {
			"avatarTemplateId": template_id
		}
		return self.session.post(
			f"{self.api}/pinpon-app-system/app-avatar/choose/template",
			data=data).json()

	def get_recommended_rp(
			self,
			current: int = 1,
			size: int = 20) -> dict:
		data = {
			"current": current,
			"size": size
		}
		return self.session.post(
			f"{self.api}/pinpon-app-system/v5/app-recommend/rp",
			data=data).json()

	def get_oc_current_list(self) -> dict:
		return self.session.get(
			f"{self.api}/pinpon-app-system/app-oc/current/list").json()
